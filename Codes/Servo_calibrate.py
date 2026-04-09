#!/usr/bin/env python3

import time
from adafruit_servokit import ServoKit

# -----------------------------
# SETUP
# -----------------------------
kit = ServoKit(channels=16, frequency=50)

JOINTS = {
    "J1": [0],
    "J2": [1, 2],
    "J3": [3, 4],
    "J4": [5, 6],
    "J5": [7],
    "EE": [8]
}

# Store calibration values
calibration = {
    "J1": {"offset": 90, "invert": 1},
    "J2": {"offset": 90, "invert": 1},
    "J3": {"offset": 90, "invert": 1},
    "J4": {"offset": 90, "invert": 1},
    "J5": {"offset": 90, "invert": 1},
}

# -----------------------------
# HELPER: move joint
# -----------------------------
def move_joint(joint, angle):
    for ch in JOINTS[joint]:
        safe = max(0, min(180, angle))
        kit.servo[ch].angle = safe

# -----------------------------
# CALIBRATION MODE
# -----------------------------
def calibrate_joint(joint):
    angle = 90
    print(f"\n--- Calibrating {joint} ---")
    print("Controls:")
    print("  a: -5 deg | d: +5 deg")
    print("  s: -1 deg | w: +1 deg")
    print("  i: invert direction")
    print("  c: set as center (offset)")
    print("  q: quit joint")

    invert = 1

    while True:
        move_joint(joint, angle)
        print(f"{joint} Angle: {angle}", end="\r")

        cmd = input().lower()

        if cmd == 'a':
            angle -= 5
        elif cmd == 'd':
            angle += 5
        elif cmd == 's':
            angle -= 1
        elif cmd == 'w':
            angle += 1
        elif cmd == 'i':
            invert *= -1
            print("Direction inverted!")
        elif cmd == 'c':
            calibration[joint]["offset"] = angle
            calibration[joint]["invert"] = invert
            print(f"\nSaved center for {joint}: {angle}, invert: {invert}")
        elif cmd == 'q':
            break

        angle = max(0, min(180, angle))

# -----------------------------
# MAIN MENU
# -----------------------------
def main():
    try:
        while True:
            print("\n====== SERVO CALIBRATION ======")
            print("Select Joint:")
            for j in JOINTS.keys():
                print(f"  - {j}")
            print("  - p (print calibration)")
            print("  - x (exit)")

            choice = input("Enter: ").upper()

            if choice in JOINTS:
                calibrate_joint(choice)

            elif choice == 'P':
                print("\n--- Calibration Values ---")
                for j, val in calibration.items():
                    print(f"{j}: offset={val['offset']}, invert={val['invert']}")

            elif choice == 'X':
                break

    finally:
        print("\nReleasing servos...")
        for channels in JOINTS.values():
            for ch in channels:
                kit.servo[ch].angle = None
        print("Done.")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()