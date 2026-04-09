#!/usr/bin/env python3
"""
Calibration script for Dexter ER2
Moves one joint at a time so you can find the correct offset and flip for each.
"""
from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16, frequency=50)

JOINTS = {
    "J1": [0],
    "J2": [1, 2],
    "J3": [4, 5],
    "J4": [6, 7],
    "J5": [9],
    "EE": [8],
}

def set_joint(joint_name, angle):
    angle = max(0, min(180, angle))
    for ch in JOINTS[joint_name]:
        kit.servo[ch].angle = angle
    print(f"  {joint_name} → {angle}°")

def release_all():
    for channels in JOINTS.values():
        for ch in channels:
            kit.servo[ch].angle = None

# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
if __name__ == "__main__":
    print("=== Dexter ER2 Servo Calibration ===")
    print("This script lets you manually command each joint.")
    print("For each joint, note down:")
    print("  1. What servo angle makes it sit at physical 0° (straight/neutral)")
    print("  2. Does increasing servo angle rotate the joint + or - physically")
    print()

    try:
        while True:
            print("\nJoints:", list(JOINTS.keys()))
            joint = input("Enter joint name (or 'q' to quit): ").strip().upper()
            if joint == 'Q':
                break
            if joint not in JOINTS:
                print("Unknown joint.")
                continue

            angle = input(f"Enter servo angle for {joint} (0-180): ").strip()
            try:
                set_joint(joint, float(angle))
            except ValueError:
                print("Invalid angle.")

    finally:
        release_all()
        print("Done.")
