# logic.py
import cv2 as cv
from ultralytics import YOLO
import speech_recognition as sr
import threading
import time

model = YOLO("models/best_9c.pt")
CLASS_NAMES = [c.lower() for c in model.names.values()]

cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Shared state
detection_state = "idle"   # idle | searching | detected | done
current_object = None

# --------------------
# SPEECH TO TEXT
# --------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        return r.recognize_google(audio).lower()
    except:
        return ""
    
# --------------------
# CHECK OBJECT
# --------------------
def check_object(text):
    for obj in CLASS_NAMES:
        if obj in text:
            return obj
    return None

# --------------------
# YOLO THREAD
# --------------------
def yolo_worker():
    global detection_state

    while detection_state == "searching":
        ret, frame = cap.read()
        if not ret:
            continue

        results = model(frame)

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id].lower()
            conf = float(box.conf[0])

            if label == current_object and conf > 0.7:
                detection_state = "detected"
                time.sleep(1.5)  # simulate arm motion
                detection_state = "done"
                return

# --------------------
# START DETECTION
# --------------------
def start_detection(obj):
    global current_object, detection_state

    current_object = obj
    detection_state = "searching"

    thread = threading.Thread(target=yolo_worker, daemon=True)
    thread.start()

# --------------------
# GET STATUS
# --------------------
def get_status():
    return detection_state
