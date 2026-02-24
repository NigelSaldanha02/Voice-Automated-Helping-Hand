import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Robot geometry (YOUR lengths)
# -----------------------------
L3 = 43/500
L4 = 77/1000
L56 = 39/200
L1 = 41/500   # base height


# -----------------------------
# FABRIK solver (planar chain)
# -----------------------------
def fabrik(target, lengths, tol=1e-4, max_iter=100):

    n = len(lengths)

    # initial straight configuration
    points = [np.array([0.0, 0.0])]
    for l in lengths:
        points.append(points[-1] + np.array([l, 0]))

    base = points[0].copy()

    # check reachability
    if np.linalg.norm(target - base) > sum(lengths):
        print("Target unreachable → stretching arm")
        direction = (target - base) / np.linalg.norm(target - base)
        for i in range(1, n+1):
            points[i] = points[i-1] + direction * lengths[i-1]
        return points

    for _ in range(max_iter):

        # --- forward pass ---
        points[-1] = target
        for i in reversed(range(n)):
            r = np.linalg.norm(points[i+1] - points[i])
            lam = lengths[i] / r
            points[i] = (1 - lam) * points[i+1] + lam * points[i]

        # --- backward pass ---
        points[0] = base
        for i in range(n):
            r = np.linalg.norm(points[i+1] - points[i])
            lam = lengths[i] / r
            points[i+1] = (1 - lam) * points[i] + lam * points[i+1]

        if np.linalg.norm(points[-1] - target) < tol:
            break

    return points


# -----------------------------
# Convert positions → angles
# -----------------------------
def get_joint_angles(points):

    x0,y0 = points[0]
    x1,y1 = points[1]
    x2,y2 = points[2]
    x3,y3 = points[3]

    theta2 = np.arctan2(y1-y0, x1-x0)
    theta3 = np.arctan2(y2-y1, x2-x1) - theta2
    theta4 = np.arctan2(y3-y2, x3-x2) - (theta2 + theta3)

    return theta2, theta3, theta4


# -----------------------------
# Target (from YOLO)
# -----------------------------
px, py, pz = 0.12, 0.05, 0.10


# -----------------------------
# Hybrid IK
# -----------------------------

# Step 1 — base rotation
theta1 = np.arctan2(py, px)

# Step 2 — convert to planar coordinates
r = np.sqrt(px**2 + py**2)
z = pz - L1

target = np.array([r, z])

# Step 3 — FABRIK for joints 2 3 4
lengths = [L3, L4, L56]
points = fabrik(target, lengths)

theta2, theta3, theta4 = get_joint_angles(points)

print("\nJoint angles (degrees)")
print("theta1:", np.degrees(theta1))
print("theta2:", np.degrees(theta2))
print("theta3:", np.degrees(theta3))
print("theta4:", np.degrees(theta4))


# -----------------------------
# Visualization
# -----------------------------
fig = plt.figure()
ax = fig.add_subplot(111)

xs = [p[0] for p in points]
ys = [p[1] for p in points]

ax.plot(xs, ys, 'o-', linewidth=3)
ax.scatter(target[0], target[1], s=100, label="Target")

ax.set_aspect('equal')
ax.set_xlim(-0.3, 0.3)
ax.set_ylim(-0.3, 0.3)
ax.set_title("Hybrid IK (θ1 analytic + FABRIK)")
ax.legend()

plt.show()
