import cv2 as cv
import numpy as np
from picamera2 import Picamera2
import time

# Workspace real dimensions (cm)
WORKSPACE_WIDTH = 14.5
WORKSPACE_HEIGHT = 21

# Initialize camera (Top Camera = Cam1)
picam = Picamera2(1)
config = picam.create_preview_configuration(main={"size": (640, 480)})
picam.configure(config)
picam.start()
time.sleep(2)

clicked_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append([x, y])
        print(f"Point {len(clicked_points)}: ({x}, {y})")

cv.namedWindow("Calibration")
cv.setMouseCallback("Calibration", mouse_callback)

while True:
    frame = picam.capture_array()
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    for point in clicked_points:
        cv.circle(frame, tuple(point), 6, (0, 0, 255), -1)

    cv.imshow("Calibration", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    if len(clicked_points) == 4:
        break

cv.destroyAllWindows()

# Convert to numpy
image_points = np.array(clicked_points, dtype=np.float32)

# Define real-world rectangle points
world_points = np.array([
    [0, 0],
    [WORKSPACE_WIDTH, 0],
    [WORKSPACE_WIDTH, WORKSPACE_HEIGHT],
    [0, WORKSPACE_HEIGHT]
], dtype=np.float32)

# Compute homography
H, _ = cv.findHomography(image_points, world_points)

# Save matrix
np.save("homography.npy", H)

print("Homography saved successfully.")
picam.stop()