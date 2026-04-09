#!/usr/bin/env python3

import math
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
    "J3": [3, 4],
    "J4": [5, 6],
    "J5": [7],  # wrist rotation
    "EE": [8]   # gripper
}

# -----------------------------
# Link lengths (meters)
# -----------------------------
L1 = 0.082
L2 = 0.022
L3 = 0.086
L4 = 0.077
L5 = 0.085
L6 = 0.110

L34 = L3 + L4
L56 = L5 + L6

# -----------------------------
# Home pose (upright)
# -----------------------------
HOME_ANGLES = {
    "J1": 90,
    "J2": 75,
    "J3": 75,  # keep joint3 fixed
    "J4": 75,
    "J5": 75,
    "EE": 0
}

# Gripper positions
GRIP_OPEN = 180
GRIP_CLOSE = 45

# -----------------------------
# IK function (ignoring joint3)
# -----------------------------
def compute_ik(x, y, z):
    theta1 = math.atan2(y, x)
    r = math.sqrt(x*x + y*y)
    q1 = z - (L1 + L2)
    R = math.sqrt(r*r + q1*q1)

    phi2 = math.atan2(q1, r)
    c_phi1 = (L56**2 - L34**2 - R**2) / (-2 * L34 * R)
    c_phi1 = max(-1, min(1, c_phi1))
    phi1 = math.acos(c_phi1)
    theta2 = phi2 - phi1

    c_phi3 = (R**2 - L34**2 - L56**2) / (-2 * L34 * L56)
    c_phi3 = max(-1, min(1, c_phi3))
    phi3 = math.acos(c_phi3)
    theta4 = -(math.pi/3 - phi3)

    # Convert to degrees
    theta1_deg = math.degrees(theta1)
    theta2_deg = math.degrees(theta2)
    theta3_deg = HOME_ANGLES["J3"]  # fixed
    theta4_deg = math.degrees(theta4)
    theta5_deg = 0  # keep as 0 unless needed

    return [theta1_deg, theta2_deg, theta3_deg, theta4_deg, theta5_deg]

# -----------------------------
# Move joints helper
# -----------------------------
def move_joints(thetas_deg, gripper_angle=None):
    joint_names = ["J1","J2","J3","J4","J5"]
    for name, angle in zip(joint_names, thetas_deg):
        for ch in JOINTS[name]:
            kit.servo[ch].angle = max(0, min(180, angle))  # clamp
    if gripper_angle is not None:
        for ch in JOINTS["EE"]:
            kit.servo[ch].angle = gripper_angle
    print("Moved to pose:", thetas_deg, "Gripper:", gripper_angle)

# -----------------------------
# Main sequence
# -----------------------------
if __name__ == "__main__":
    try:
        # 1. Move to Home
        print("Moving to HOME...")
        move_joints([HOME_ANGLES["J1"], HOME_ANGLES["J2"], HOME_ANGLES["J3"],
                     HOME_ANGLES["J4"], HOME_ANGLES["J5"]],
                     gripper_angle=HOME_ANGLES["EE"])
        time.sleep(3)

        # 2. Target coordinates
        x = float(input("Enter target x (m): "))
        y = float(input("Enter target y (m): "))
        z = float(input("Enter target z (m): "))

        # 3. Compute IK (ignoring joint3)
        target_thetas = compute_ik(x, y, z)
        print("IK angles (deg):", target_thetas)

        # 4. Move to target with gripper OPEN
        print("Moving to TARGET (gripper open)...")
        move_joints(target_thetas, gripper_angle=GRIP_OPEN)
        time.sleep(5)

        # 5. Close gripper to pick
        print("Closing gripper to pick...")
        move_joints(target_thetas, gripper_angle=GRIP_CLOSE)
        time.sleep(2)

        # 6. Return to Home (holding object)
        print("Returning to HOME...")
        move_joints([HOME_ANGLES["J1"], HOME_ANGLES["J2"], HOME_ANGLES["J3"],
                     HOME_ANGLES["J4"], HOME_ANGLES["J5"]],
                     gripper_angle=GRIP_CLOSE)
        time.sleep(3)

        # 7. Open gripper to release object
        print("Opening gripper to release...")
        move_joints([HOME_ANGLES["J1"], HOME_ANGLES["J2"], HOME_ANGLES["J3"],
                     HOME_ANGLES["J4"], HOME_ANGLES["J5"]],
                     gripper_angle=GRIP_OPEN)
        time.sleep(2)

    finally:
        # Release all servos
        print("Releasing servos...")
        for channels in JOINTS.values():
            for ch in channels:
                kit.servo[ch].angle = None
        print("Done.")