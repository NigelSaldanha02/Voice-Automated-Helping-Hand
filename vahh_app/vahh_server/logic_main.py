import cv2 as cv
import cvzone
from ultralytics import YOLO
from picamera2 import Picamera2
import numpy as np
import threading
import time
import math
import ikpy.chain
from adafruit_servokit import ServoKit

# -----------------------------
# Load Homography Matrix
# -----------------------------
H = np.load("homography.npy")

# -----------------------------
# Initialize Top Camera
# -----------------------------
picam = Picamera2(0)
config = picam.create_preview_configuration(main={"size": (640, 480)})
picam.configure(config)
picam.start()
time.sleep(2)

# -----------------------------
# Load YOLO Model
# -----------------------------
model = YOLO("/home/gec123/Downloads/Voice-Automated-Helping-Hand/YOLO_models_dataset/best_9c.pt")
classes = [c.lower() for c in model.names.values()]

# -----------------------------
# ARM SETUP
# -----------------------------
URDF_PATH = "/home/gec123/Downloads/Voice-Automated-Helping-Hand/Dexter_Sim/Models/Dexter_ER2.urdf"
arm = ikpy.chain.Chain.from_urdf_file(
    URDF_PATH,
    active_links_mask=[False, True, True, True, True, True, False]
)

kit = ServoKit(channels=16, frequency=50)

JOINTS = {
    "J1": [0],
    "J2": [1, 2],
    "J3": [4, 5],
    "J4": [6, 7],
    "J5": [9],
    "EE": [8],
}

IK_INDEX = {"J1": 1, "J2": 2, "J3": 3, "J4": 4, "J5": 5}

HOME_SERVO_ANGLES  = {"J1": 90, "J2": 75, "J3": 75, "J4": 75, "J5": 90, "EE": 180}
HANDOFF_SERVO_ANGLES = {"J1": 180, "J2": 45, "J3": 0, "J4": 90, "J5": 90, "EE": 0}
HOME_IK_SEED       = [0.0] * 7
JOINT_OFFSET       = {"J1": 90, "J2": 75, "J3": 75, "J4": 75, "J5": 90}
JOINT_FLIP         = {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False}
GRIP_OPEN          = 180
GRIP_CLOSE         = 0
FIXED_Z            = 0.01
STEP_DELAY         = 0.005

CLASS_CY_OFFSET = {
    "water bottle": 0.9,
    "remote":       0.75,
    # add more objects as you test them
    # anything not listed falls back to DEFAULT
}
DEFAULT_CY_OFFSET = 0.5   # fallback for unlisted objects

_last_angle = {}
current_ik  = None

# -----------------------------
# Shared State
# -----------------------------
detection_state = "idle"   # idle | searching | detected | moving | done
current_object  = None
latest_frame    = None     # JPEG bytes of latest annotated frame
frame_lock      = threading.Lock()

# -----------------------------
# ARM HELPERS
# -----------------------------
def clamp(val, lo, hi):
    return max(lo, min(hi, val))

def set_joint(jname, angle):
    angle = clamp(angle, 0, 180)
    for ch in JOINTS[jname]:
        current = _last_angle.get(ch, None)
        if current is None:
            kit.servo[ch].angle = angle
            _last_angle[ch] = angle
        else:
            current = int(round(current))
            target  = int(round(angle))
            step    = 1 if target > current else -1
            for pos in range(current, target, step):
                kit.servo[ch].angle = pos
                _last_angle[ch] = pos
                time.sleep(STEP_DELAY)
            kit.servo[ch].angle = target
            _last_angle[ch] = target

def move_j1_then_rest(angle_map, gripper_angle=None, j1_delay=0.5):
    if "J1" in angle_map:
        set_joint("J1", angle_map["J1"])
        time.sleep(j1_delay)
    for jname, angle in angle_map.items():
        if jname == "J1":
            continue
        set_joint(jname, angle)
    if gripper_angle is not None:
        set_joint("EE", gripper_angle)

def move_rest_then_j1(angle_map, gripper_angle=None, j1_delay=0.5):
    for jname, angle in angle_map.items():
        if jname == "J1":
            continue
        set_joint(jname, angle)
    time.sleep(j1_delay)
    if "J1" in angle_map:
        set_joint("J1", angle_map["J1"])
    if gripper_angle is not None:
        set_joint("EE", gripper_angle)

def ikpy_to_servo(joint_name, ik_array):
    rad = ik_array[IK_INDEX[joint_name]]
    deg = math.degrees(rad)
    if JOINT_FLIP[joint_name]:
        deg = -deg
    return clamp(deg + JOINT_OFFSET[joint_name], 0, 180)

def move_home(gripper_angle=None):
    move_rest_then_j1(
        {j: HOME_SERVO_ANGLES[j] for j in ["J1","J2","J3","J4","J5"]},
        gripper_angle=gripper_angle if gripper_angle is not None else HOME_SERVO_ANGLES["EE"]
    )
    global current_ik
    current_ik = list(HOME_IK_SEED)

def compute_ik(x, y, z, max_attempts=5, threshold_m=0.015):
    global current_ik
    target   = [x, y, z]
    best_ik  = None
    best_err = float('inf')
    for attempt in range(max_attempts):
        if attempt == 0 and current_ik is not None:
            initial = list(current_ik)
        else:
            initial = list(HOME_IK_SEED)
            for idx in IK_INDEX.values():
                initial[idx] += np.random.uniform(-0.3, 0.3)
        ik  = arm.inverse_kinematics(
            target_position=target,
            target_orientation=None,
            orientation_mode=None,
            initial_position=initial,
        )
        fk  = arm.forward_kinematics(ik)
        err = math.sqrt(sum((fk[i,3] - target[i])**2 for i in range(3)))
        if err < best_err:
            best_err, best_ik = err, ik
        if err < threshold_m:
            break
    current_ik = best_ik
    return best_ik

def move_to_ik(ik_array, gripper_angle=None):
    angle_map = {jname: ikpy_to_servo(jname, ik_array) for jname in IK_INDEX}
    move_j1_then_rest(angle_map, gripper_angle=gripper_angle)

def retract_from_ik(ik_array, gripper_angle=None):
    angle_map = {jname: ikpy_to_servo(jname, ik_array) for jname in IK_INDEX}
    move_rest_then_j1(angle_map, gripper_angle=gripper_angle)

def pick_and_handoff(x_m, y_m):
    global detection_state

    detection_state = "moving"
    print(f"Picking at ({x_m:.4f}m, {y_m:.4f}m, {FIXED_Z}m)")

    target_ik = compute_ik(x_m, y_m, FIXED_Z)

    move_to_ik(target_ik, gripper_angle=GRIP_OPEN)
    time.sleep(3)

    set_joint("EE", GRIP_CLOSE)
    time.sleep(2)

    retract_from_ik(target_ik, gripper_angle=GRIP_CLOSE)
    time.sleep(1)

    move_home(gripper_angle=GRIP_CLOSE)
    time.sleep(2)

    move_j1_then_rest(
        {j: HANDOFF_SERVO_ANGLES[j] for j in ["J1","J2","J3","J4","J5"]},
        gripper_angle=HANDOFF_SERVO_ANGLES["EE"]
    )
    time.sleep(2)

    set_joint("EE", GRIP_OPEN)
    time.sleep(2)

    move_home()
    time.sleep(2)

    # Release all servos
    for channels in JOINTS.values():
        for ch in channels:
            kit.servo[ch].angle = None
    _last_angle.clear()

    detection_state = "done"
    print("Done.")

# -----------------------------
# CHECK OBJECT
# -----------------------------
def check_object(text: str):
    for obj in classes:
        if obj in text:
            return obj
    return None

# -----------------------------
# YOLO WORKER
# -----------------------------
def yolo_worker():
    global detection_state, latest_frame

    print("Moving to HOME before search...")
    move_home()

    while detection_state == "searching":
        frame = picam.capture_array()
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        best = None  # (conf, x_m, y_m)

        results = model(frame, stream=True)
        for result in results:
            for box in result.boxes:
                conf     = float(box.conf[0])
                cls_id   = int(box.cls[0])
                label    = classes[cls_id]

                if conf < 0.7:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1
                cx = x1 + w // 2
                # Per-class vertical offset
                cy_ratio = CLASS_CY_OFFSET.get(label, DEFAULT_CY_OFFSET)
                cy = y1 + int(h * cy_ratio)

                pixel_point = np.array([[[cx, cy]]], dtype=np.float32)
                world_point = cv.perspectiveTransform(pixel_point, H)
                Xw = world_point[0][0][0] 
                Yw = world_point[0][0][1] 

                # Draw all detections
                cvzone.cornerRect(frame, (x1, y1, w, h))
                cvzone.putTextRect(frame, f'{label} {conf:.2f}',
                                   (max(0, x1), max(40, y1)), scale=1.2)
                cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv.putText(frame, f"({Xw:.1f}cm, {Yw:.1f}cm)",
                           (cx+10, cy-10), cv.FONT_HERSHEY_SIMPLEX,
                           0.6, (0, 255, 0), 2)

                # Track best match for target object
                if label == current_object:
                    if best is None or conf > best[0]:
                        best = (conf, Xw / 100.0, Yw / 100.0)

        # Encode frame as JPEG and store for streaming
        _, jpeg = cv.imencode('.jpg', frame)
        with frame_lock:
            latest_frame = jpeg.tobytes()

        # If target found, pick it
        if best is not None:
            _, x_m, y_m = best
            print(f"Found {current_object} at ({x_m:.4f}m, {y_m:.4f}m)")
            detection_state = "detected"
            pick_and_handoff(x_m, y_m)
            return

        time.sleep(0.05)

# -----------------------------
# START DETECTION
# -----------------------------
def start_detection(obj: str):
    global current_object, detection_state
    if detection_state in ("searching", "detected", "moving"):
        return

    current_object  = obj
    detection_state = "searching"
    print(f"Searching for: {obj}")

    thread = threading.Thread(target=yolo_worker, daemon=True)
    thread.start()

# -----------------------------
# GET STATUS
# -----------------------------
def get_status():
    return detection_state

# -----------------------------
# GET LATEST FRAME
# -----------------------------
def get_latest_frame():
    with frame_lock:
        return latest_frame