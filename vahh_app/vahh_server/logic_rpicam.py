# logic_rpicam.py
import cv2 as cv
import cvzone
from ultralytics import YOLO
from picamera2 import Picamera2
import threading
import time
import speech_recognition as sr

# -----------------------------
# YOLO Model
# -----------------------------
model = YOLO("/home/gec123/Downloads/Voice-Automated-Helping-Hand/YOLO_models_dataset/best_11m.pt")
classes = [c.lower() for c in model.names.values()]

# Workspace dimensions
TABLE_WIDTH_CM = 60
TABLE_HEIGHT_CM = 40

# -----------------------------
# Dual Cameras
# -----------------------------
picam0 = Picamera2(0)
picam1 = Picamera2(1)

config0 = picam0.create_preview_configuration(main={"size": (640, 480)})
config1 = picam1.create_preview_configuration(main={"size": (640, 480)})

picam0.configure(config0)
picam1.configure(config1)

picam0.start()
picam1.start()

time.sleep(2)

# -----------------------------
# Shared State
# -----------------------------
detection_state = "idle"  # idle | searching | detected | done
current_object = None
active_cam = 0
switch_timeout = 5
last_detection_time = time.time()

# -----------------------------
# SPEECH (optional, can call from Flask)
# -----------------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening for object command...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio).lower()
    except:
        return ""

# -----------------------------
# CHECK OBJECT
# -----------------------------
def check_object(text: str):
    for obj in classes:
        if obj in text:
            return obj
    return None

# -----------------------------
# YOLO DETECTION WORKER
# -----------------------------
def yolo_worker():
    global detection_state, last_detection_time, active_cam

    while detection_state == "searching":
        # Pick active camera
        if active_cam == 0:
            frame = picam0.capture_array()
            cam_label = "Camera 0"
        else:
            frame = picam1.capture_array()
            cam_label = "Camera 1"

        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        detected = False

        results = model(frame, stream=True)

        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf < 0.7:
                    continue

                cls_id = int(box.cls[0])
                label = classes[cls_id]

                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w = x2 - x1
                h = y2 - y1
                cx = x1 + w // 2
                cy = y1 + h // 2

                # Real-world estimation
                img_h, img_w, _ = frame.shape
                x_real = (cx / img_w) * TABLE_WIDTH_CM
                y_real = (cy / img_h) * TABLE_HEIGHT_CM

                print(f"[{cam_label}] {label}: pixel=({cx},{cy}) world=({x_real:.1f},{y_real:.1f}cm)")

                if label == current_object:
                    detected = True
                    detection_state = "detected"
                    print(f"{label} detected!")
                    time.sleep(1.5)  # simulate arm motion
                    detection_state = "done"
                    return

        # Switch camera if no detection for timeout
        if time.time() - last_detection_time > switch_timeout:
            active_cam = 1 - active_cam
            last_detection_time = time.time()
            print(f"Switching to Camera {active_cam}")

        # Update last detection time
        if detected:
            last_detection_time = time.time()

# -----------------------------
# START DETECTION (called from Flask)
# -----------------------------
def start_detection(obj: str):
    global current_object, detection_state
    if detection_state == "searching":
        return  # already running

    current_object = obj
    detection_state = "searching"
    print(f"Started searching for: {obj}")

    thread = threading.Thread(target=yolo_worker, daemon=True)
    thread.start()

# -----------------------------
# GET STATUS
# -----------------------------
def get_status():
    return detection_state