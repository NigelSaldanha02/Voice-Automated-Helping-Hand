import cv2 as cv
import cvzone
from ultralytics import YOLO
import math

# Use laptop camera source 0 (to be changed to pi cam)
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load trained model
model = YOLO("D:/College/VScode/Projects/VoiceAutomatedHelpingHand/YOLO_models_dataset/best_9c.pt")

# Workspace configuration
Table_Width_cm = 60
Table_Height_cm = 40

# Access class names from trained models 
classes = model.names

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame, stream = True)

    # Draw bounding boxes with class names
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

            # Get resolution of camera (here 640x480, _->RGB color argument)
            img_h, img_w, _ = frame.shape 

            # Convert into real world coordinates
            x_real = (cx / img_w) * Table_Width_cm
            y_real = (cy /img_h) * Table_Height_cm

            # Class name
            cls = int(box.cls[0])

            # Confidence score greater than 0.7
            conf = math.ceil((box.conf[0] * 100)) / 100
            if conf < 0.7:
                continue

            # Display class name and confidence score
            cvzone.putTextRect(frame, f'{classes[cls], conf}', (max(0,x1),max(40,y1)) , scale = 1.5)

            # Display bounding box and object center dot
            cvzone.cornerRect(frame, (x1,y1,w,h))
            cv.circle(frame, (cx, cy), 5, (0,0,255), -1)

            print(f"{classes[cls]}: pixel=({cx},{cy})  world=({x_real:.1f}cm, {y_real:.1f}cm)")

    # Display camera feed frame by frame
    cv.imshow('camera feed', frame)
    
    # Press 'q' to exit display
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
