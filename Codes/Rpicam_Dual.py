import cv2 as cv
import cvzone
from ultralytics import YOLO
from picamera2 import Picamera2
import math
import time

# -----------------------------
# Initialize Cameras
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
# Load YOLO Model
# -----------------------------
model = YOLO("/home/gec123/Downloads/Voice-Automated-Helping-Hand-main/YOLO_models_dataset/best_9c.pt")
classes = model.names

# Workspace dimensions
Table_Width_cm = 60
Table_Height_cm = 40

# -----------------------------
# Switching Settings
# -----------------------------
active_cam = 0
switch_timeout = 5   # seconds without detection before switching
last_detection_time = time.time()

print("Starting on Camera 0")

# -----------------------------
# Main Loop
# -----------------------------
while True:

    # Select active camera
    if active_cam == 0:
        frame = picam0.capture_array()
        cam_label = "Camera 0"
    else:
        frame = picam1.capture_array()
        cam_label = "Camera 1"

    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    detected = False

    # Run YOLO
    results = model(frame, stream=True)

    for result in results:
        for box in result.boxes:

            conf = float(box.conf[0])
            if conf < 0.7:
                continue

            detected = True

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            w = x2 - x1
            h = y2 - y1

            cx = x1 + w // 2
            cy = y1 + h // 2

            img_h, img_w, _ = frame.shape

            x_real = (cx / img_w) * Table_Width_cm
            y_real = (cy / img_h) * Table_Height_cm

            cls = int(box.cls[0])
            conf = math.ceil(conf * 100) / 100

            cvzone.putTextRect(
                frame,
                f'{classes[cls]} {conf}',
                (max(0, x1), max(40, y1)),
                scale=1.2
            )

            cvzone.cornerRect(frame, (x1, y1, w, h))
            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            print(f"[{cam_label}] {classes[cls]}: pixel=({cx},{cy})  world=({x_real:.1f}cm, {y_real:.1f}cm)")

    # Update detection timer
    if detected:
        last_detection_time = time.time()

    # Switch camera if no detection for timeout period
    if time.time() - last_detection_time > switch_timeout:
        active_cam = 1 - active_cam
        last_detection_time = time.time()
        print(f"Switching to Camera {active_cam}")

    # Display active camera label
    cv.putText(frame, f"Active: {cam_label}", (20, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv.imshow("Smart Dual Camera YOLO", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# Cleanup
# -----------------------------
picam0.stop()
picam1.stop()
cv.destroyAllWindows()