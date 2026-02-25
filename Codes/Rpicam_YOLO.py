import cv2 as cv
import cvzone
from ultralytics import YOLO
from picamera2 import Picamera2
import math
import time

# -----------------------------
# Initialize Raspberry Pi Camera
# -----------------------------
picam2 = Picamera2()

# Configure camera resolution (matches your previous 640x480)
config = picam2.create_preview_configuration(
    main={"size": (640, 480)}
)
picam2.configure(config)
picam2.start()

time.sleep(2)  # Allow camera to warm up

# -----------------------------
# Load YOLO model
# -----------------------------
model = YOLO("/home/gec123/Downloads/Voice-Automated-Helping-Hand-main/YOLO_models_dataset/best_9c.pt")

# Workspace configuration
Table_Width_cm = 60
Table_Height_cm = 40

# Access class names
classes = model.names

# -----------------------------
# Main Loop
# -----------------------------
while True:
    # Capture frame from Pi camera
    frame = picam2.capture_array()

    # Convert from RGB (Picamera2) to BGR (OpenCV)
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    # Run YOLO inference
    results = model(frame, stream=True)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w = x2 - x1
            h = y2 - y1

            # Center of object
            cx = x1 + w // 2
            cy = y1 + h // 2

            img_h, img_w, _ = frame.shape

            # Convert to real-world coordinates
            x_real = (cx / img_w) * Table_Width_cm
            y_real = (cy / img_h) * Table_Height_cm

            cls = int(box.cls[0])
            conf = math.ceil((box.conf[0] * 100)) / 100

            if conf < 0.7:
                continue

            # Draw results
            cvzone.putTextRect(
                frame,
                f'{classes[cls]} {conf}',
                (max(0, x1), max(40, y1)),
                scale=1.5
            )
            cvzone.cornerRect(frame, (x1, y1, w, h))
            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            print(f"{classes[cls]}: pixel=({cx},{cy})  world=({x_real:.1f}cm, {y_real:.1f}cm)")

    # Show live camera feed
    cv.imshow("YOLO PiCam Feed", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# Cleanup
# -----------------------------
picam2.stop()
cv.destroyAllWindows()