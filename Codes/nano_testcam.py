from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

# Configure for preview (video mode)
picam2.configure(picam2.create_preview_configuration())

# Start preview window
picam2.start_preview(Preview.QTGL)

picam2.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping camera...")

picam2.stop()
picam2.stop_preview()
print("Done")