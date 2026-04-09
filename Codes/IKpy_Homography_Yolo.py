#!/usr/bin/env python3
"""
Dexter ER2 — YOLO + Homography + ikpy combined
User types which object to pick, robot finds and picks it autonomously.
Servos released after drop.
"""

import cv2 as cv
import cvzone
import math
import time
import numpy as np
import ikpy.chain
from ultralytics import YOLO
from picamera2 import Picamera2
from adafruit_servokit import ServoKit

# -------------------------------------------------------
# YOLO + CAMERA
# -------------------------------------------------------
H = np.load("homography.npy")

picam = Picamera2(0)
picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
picam.start()
time.sleep(2)

model   = YOLO("/home/gec123/Downloads/Voice-Automated-Helping-Hand/YOLO_models_dataset/best_9c.pt")
classes = model.names

# -------------------------------------------------------
# CHAIN
# -------------------------------------------------------
URDF_PATH = "/home/gec123/Downloads/Voice-Automated-Helping-Hand/Dexter_Sim/Models/Dexter_ER2.urdf"

arm = ikpy.chain.Chain.from_urdf_file(
    URDF_PATH,
    active_links_mask=[False, True, True, True, True, True, False]
)

# -------------------------------------------------------
# SERVO SETUP
# -------------------------------------------------------
kit = ServoKit(channels=16, frequency=50)

JOINTS = {
    "J1": [0],
    "J2": [1, 2],
    "J3": [4, 5],
    "J4": [6, 7],
    "J5": [9],
    "EE": [8],
}

IK_INDEX = {
    "J1": 1,
    "J2": 2,
    "J3": 3,
    "J4": 4,
    "J5": 5,
}

HOME_SERVO_ANGLES = {
    "J1": 90,
    "J2": 75,
    "J3": 75,
    "J4": 75,
    "J5": 90,
    "EE": 180,
}

HANDOFF_SERVO_ANGLES = {
    "J1": 180,
    "J2": 45,
    "J3": 0,
    "J4": 90,
    "J5": 90,
    "EE": 0,
}

HOME_IK_SEED   = [0.0] * 7
JOINT_OFFSET   = {"J1": 90, "J2": 75, "J3": 75, "J4": 75, "J5": 90}
JOINT_FLIP     = {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False}
GRIP_OPEN      = 180
GRIP_CLOSE     = 0
FIXED_Z        = 0.03
CONF_THRESHOLD = 0.7

current_ik  = None
STEP_DELAY  = 0.005
_last_angle = {}

# -------------------------------------------------------
# HELPERS
# -------------------------------------------------------
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

def release_all_servos():
    print("  Releasing all servos.")
    for channels in JOINTS.values():
        for ch in channels:
            kit.servo[ch].angle = None
    _last_angle.clear()   # clear position memory since servos are now free

def move_j1_then_rest(angle_map, gripper_angle=None, j1_delay=0.5):
    if "J1" in angle_map:
        print(f"  J1 → {angle_map['J1']}°  (rotating base first)")
        set_joint("J1", angle_map["J1"])
        time.sleep(j1_delay)
    for jname, angle in angle_map.items():
        if jname == "J1":
            continue
        print(f"  {jname} → {angle}°")
        set_joint(jname, angle)
    if gripper_angle is not None:
        set_joint("EE", gripper_angle)

def move_rest_then_j1(angle_map, gripper_angle=None, j1_delay=0.5):
    for jname, angle in angle_map.items():
        if jname == "J1":
            continue
        print(f"  {jname} → {angle}°")
        set_joint(jname, angle)
    time.sleep(j1_delay)
    if "J1" in angle_map:
        print(f"  J1 → {angle_map['J1']}°  (rotating base last)")
        set_joint("J1", angle_map["J1"])
    if gripper_angle is not None:
        set_joint("EE", gripper_angle)

def ikpy_to_servo(joint_name, ik_array):
    rad = ik_array[IK_INDEX[joint_name]]
    deg = math.degrees(rad)
    if JOINT_FLIP[joint_name]:
        deg = -deg
    return clamp(deg + JOINT_OFFSET[joint_name], 0, 180)

def move_home():
    print("  Moving to HOME:")
    move_rest_then_j1(
        {j: HOME_SERVO_ANGLES[j] for j in ["J1","J2","J3","J4","J5"]},
        gripper_angle=HOME_SERVO_ANGLES["EE"]
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

        joints_deg = [round(math.degrees(ik[IK_INDEX[j]]), 1) for j in IK_INDEX]
        print(f"  Attempt {attempt+1}: error={err*1000:.1f}mm  joints={joints_deg}")

        if err < best_err:
            best_err, best_ik = err, ik

        if err < threshold_m:
            break

    fk = arm.forward_kinematics(best_ik)
    print(f"  Target : {[round(v,4) for v in target]}")
    print(f"  Reached: {[round(fk[i,3],4) for i in range(3)]}")
    print(f"  Best error: {best_err*1000:.1f}mm {'✓' if best_err < threshold_m else '⚠ HIGH — target may be unreachable'}")

    current_ik = best_ik
    return best_ik

def move_to_ik(ik_array, gripper_angle=None):
    angle_map = {}
    for jname in IK_INDEX:
        servo_deg = ikpy_to_servo(jname, ik_array)
        raw_deg   = math.degrees(ik_array[IK_INDEX[jname]])
        print(f"  {jname}: ikpy={raw_deg:+.1f}°  →  servo={servo_deg:.1f}°")
        angle_map[jname] = servo_deg
    move_j1_then_rest(angle_map, gripper_angle=gripper_angle)

def retract_from_ik(ik_array, gripper_angle=None):
    angle_map = {}
    for jname in IK_INDEX:
        servo_deg = ikpy_to_servo(jname, ik_array)
        raw_deg   = math.degrees(ik_array[IK_INDEX[jname]])
        print(f"  {jname}: ikpy={raw_deg:+.1f}°  →  servo={servo_deg:.1f}°")
        angle_map[jname] = servo_deg
    move_rest_then_j1(angle_map, gripper_angle=gripper_angle)

def pick_and_handoff(x_m, y_m):
    print(f"\n>>> Picking at x={x_m:.4f}m  y={y_m:.4f}m  z={FIXED_Z}m")

    print("\n=== IK for target ===")
    target_ik = compute_ik(x_m, y_m, FIXED_Z)

    print("\n=== Approaching target (gripper open) ===")
    move_to_ik(target_ik, gripper_angle=GRIP_OPEN)
    time.sleep(3)

    print("\n=== Closing gripper ===")
    set_joint("EE", GRIP_CLOSE)
    time.sleep(2)

    print("\n=== Retracting arm ===")
    retract_from_ik(target_ik, gripper_angle=GRIP_CLOSE)
    time.sleep(1)

    print("\n=== Returning home (holding object) ===")
    move_home()
    time.sleep(2)

    print("\n=== Reaching toward person for handoff ===")
    move_j1_then_rest(
        {j: HANDOFF_SERVO_ANGLES[j] for j in ["J1","J2","J3","J4","J5"]},
        gripper_angle=HANDOFF_SERVO_ANGLES["EE"]
    )
    time.sleep(2)

    print("\n=== Releasing object ===")
    set_joint("EE", GRIP_OPEN)
    time.sleep(2)

    print("\n=== Returning home ===")
    move_home()
    time.sleep(2)

    print("\n=== Releasing all servos ===")
    release_all_servos()

# -------------------------------------------------------
# DETECTION
# -------------------------------------------------------
def find_object_in_frame(target_label, scan_frames=30):
    """
    Scan scan_frames frames for target_label.
    Returns (x_m, y_m) of highest-confidence match, or None.
    Shows live feed while scanning.
    """
    print(f"\n  Scanning for '{target_label}'...")
    best = None   # (conf, x_m, y_m)

    for _ in range(scan_frames):
        frame = picam.capture_array()
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        results = model(frame, stream=True)

        for result in results:
            for box in result.boxes:
                conf     = float(box.conf[0])
                cls_name = classes[int(box.cls[0])].lower().strip()

                if conf < CONF_THRESHOLD or cls_name != target_label.lower().strip():
                    continue

                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
                w, h = x2 - x1, y2 - y1
                cx, cy = x1 + w // 2, y1 + h // 2

                world_pt = cv.perspectiveTransform(
                    np.array([[[cx, cy]]], dtype=np.float32), H
                )
                Xw_cm = world_pt[0][0][0]
                Yw_cm = world_pt[0][0][1]
                x_m   = Xw_cm / 100.0
                y_m   = Yw_cm / 100.0

                # Draw
                cvzone.cornerRect(frame, (x1, y1, w, h))
                cvzone.putTextRect(frame, f'{cls_name} {conf:.2f}',
                                   (max(0, x1), max(40, y1)), scale=1.2)
                cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv.putText(frame, f"({Xw_cm:.1f}cm, {Yw_cm:.1f}cm)",
                           (cx+10, cy-10), cv.FONT_HERSHEY_SIMPLEX,
                           0.6, (0, 255, 0), 2)

                print(f"    Found '{cls_name}' conf={conf:.2f} "
                      f"world=({Xw_cm:.2f}cm, {Yw_cm:.2f}cm)")

                if best is None or conf > best[0]:
                    best = (conf, x_m, y_m)

        cv.imshow("Scanning...", frame)
        cv.waitKey(1)

    cv.destroyAllWindows()
    return (best[1], best[2]) if best is not None else None

# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
if __name__ == "__main__":
    try:
        print("=== HOME ===")
        move_home()
        time.sleep(2)

        print("\nAvailable object classes:")
        for cls in sorted(set(classes.values())):
            print(f"  - {cls}")

        while True:
            print("\n" + "="*40)
            target_label = input("Enter object to pick (or 'q' to quit): ").strip()

            if target_label.lower() == 'q':
                print("Exiting.")
                break

            if not target_label:
                continue

            # Re-engage servos and go home before each pick
            print("\n=== HOME ===")
            move_home()
            time.sleep(2)

            result = find_object_in_frame(target_label, scan_frames=30)

            if result is None:
                print(f"\n  ✗ '{target_label}' not found. Make sure it's in view and try again.")
                continue

            x_m, y_m = result
            print(f"\n  ✓ Found '{target_label}' at ({x_m:.4f}m, {y_m:.4f}m)")

            pick_and_handoff(x_m, y_m)

            print("\n  ✓ Done. Servos released. Ready for next command.")

    finally:
        release_all_servos()
        picam.stop()
        cv.destroyAllWindows()
        print("Done.")