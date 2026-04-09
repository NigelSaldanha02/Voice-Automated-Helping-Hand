#!/usr/bin/env python3

import time
from adafruit_servokit import ServoKit

# -----------------------------
# Servo setup
# -----------------------------
kit = ServoKit(channels=16, frequency=50)

# Joint → channels (dual servos if any)
JOINTS = {
    "J1": [0],
    "J2": [1, 2],
    "J3": [4, 5],
    "J4": [6, 7],
    "J5": [8]
}

# -----------------------------
# HOME and TEST angles (degrees)
# -----------------------------
HOME_ANGLES = {
    "J1": 90,
    "J2": 75,
    "J3": 75,
    "J4": 75,
    "J5": 75
}

TEST_ANGLES = {
    "J1": 0,
    "J2": 45,
    "J3": 90,
    "J4": 0,
    "J5": -90
}

# -----------------------------
# Helper: Move joints to specific angles
# -----------------------------
def move_pose(pose):
    for joint, channels in JOINTS.items():
        angle = pose[joint]
        for ch in channels:
            kit.servo[ch].angle = angle  # or 180-angle if mirrored
    print("Moved to pose:", pose)

# -----------------------------
# Main sequence
# -----------------------------
try:
    print("Moving to HOME")
    move_pose(HOME_ANGLES)
    time.sleep(5)

    print("Moving to TEST POSE")
    move_pose(TEST_ANGLES)
    time.sleep(5)

    print("Returning to HOME")
    move_pose(HOME_ANGLES)
    time.sleep(1)

finally:
    print("Releasing servos")
    for joint, channels in JOINTS.items():
        for ch in channels:
            kit.servo[ch].angle = None
    print("Done.")