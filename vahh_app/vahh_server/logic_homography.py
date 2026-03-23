import cv2 as cv
import cvzone
from ultralytics import YOLO
from picamera2 import Picamera2
import numpy as np
import threading
import time
import math

# -----------------------------
# Load Homography Matrix
# -----------------------------
H = np.load("homography.npy")  # saved from your calibration script

# -----------------------------
# Initialize Top Camera
# -----------------------------
picam = Picamera2(1)
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
# Shared State
# -----------------------------
detection_state = "idle"  # idle | searching | detected | done
current_object = None

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
    global detection_state

    while detection_state == "searching":
        frame = picam.capture_array()
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
                x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
                w = x2 - x1
                h = y2 - y1
                cx = x1 + w // 2
                cy = y1 + h // 2

                # Homography to world coordinates
                pixel_point = np.array([[[cx, cy]]], dtype=np.float32)
                world_point = cv.perspectiveTransform(pixel_point, H)
                Xw = world_point[0][0][0]
                Yw = world_point[0][0][1]

                print(f"{label} | Pixel=({cx},{cy}) World=({Xw:.2f}cm, {Yw:.2f}cm)")

                if label == current_object:
                    detected = True
                    detection_state = "detected"
                    time.sleep(1.5)  # simulate robotic arm
                    detection_state = "done"
                    return

# -----------------------------
# START DETECTION
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