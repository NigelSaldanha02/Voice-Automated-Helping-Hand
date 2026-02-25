import cv2 as cv
import cvzone
from ultralytics import YOLO
from picamera2 import Picamera2
import numpy as np
import math
import time

# -----------------------------
# Load Homography Matrix
# -----------------------------
H = np.load("homography.npy")

# -----------------------------
# Initialize Top Camera (Cam1)
# -----------------------------
picam = Picamera2(1)
config = picam.create_preview_configuration(
    main={"size": (640, 480)}
)
picam.configure(config)
picam.start()

time.sleep(2)

# -----------------------------
# Load YOLO Model
# -----------------------------
model = YOLO("/home/gec123/Downloads/Voice-Automated-Helping-Hand-main/YOLO_models_dataset/best_9c.pt")
classes = model.names

# -----------------------------
# Main Loop
# -----------------------------
while True:

    # Capture frame
    frame = picam.capture_array()
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    # Run YOLO
    results = model(frame, stream=True)

    for result in results:
        for box in result.boxes:

            conf = float(box.conf[0])
            if conf < 0.7:
                continue

            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            w = x2 - x1
            h = y2 - y1

            # Center pixel
            cx = x1 + w // 2
            cy = y1 + h // 2

            # -----------------------------
            # Apply Homography Transform
            # -----------------------------
            pixel_point = np.array([[[cx, cy]]], dtype=np.float32)
            world_point = cv.perspectiveTransform(pixel_point, H)

            Xw = world_point[0][0][0]
            Yw = world_point[0][0][1]

            cls = int(box.cls[0])
            conf = math.ceil(conf * 100) / 100

            # -----------------------------
            # Draw Results
            # -----------------------------
            cvzone.cornerRect(frame, (x1, y1, w, h))

            cvzone.putTextRect(
                frame,
                f'{classes[cls]} {conf}',
                (max(0, x1), max(40, y1)),
                scale=1.2
            )

            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Show world coordinates on frame
            cv.putText(
                frame,
                f"({Xw:.1f} cm, {Yw:.1f} cm)",
                (cx + 10, cy - 10),
                cv.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            print(f"{classes[cls]} | Pixel=({cx},{cy})  World=({Xw:.2f}cm, {Yw:.2f}cm)")

    cv.imshow("YOLO + Homography (Top Cam)", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# Cleanup
# -----------------------------
picam.stop()
cv.destroyAllWindows()