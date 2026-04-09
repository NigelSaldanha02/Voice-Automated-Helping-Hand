import numpy as np
import math
import ikpy.chain
import ikpy.utils.plot as plot_utils
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

# -----------------------------
# LOAD YOUR URDF
# -----------------------------
arm = ikpy.chain.Chain.from_urdf_file(
    "/home/gec123/Downloads/Voice-Automated-Helping-Hand/Dexter_Sim/Models/Dexter_ER2.urdf",
    active_links_mask=[False, True, True, True, True, False, True]
)

# -----------------------------
# TARGET POSITION
# -----------------------------
target_position = [0.2, 0.2, 0]   # change this freely

# -----------------------------
# COMPUTE IK
# -----------------------------
ik = arm.inverse_kinematics(target_position)

# ignore base dummy
angles_deg = [math.degrees(a) for a in ik]

print("Joint angles (rad):", ik)
print("Joint angles (deg):", angles_deg)

# -----------------------------
# FORWARD KINEMATICS CHECK
# -----------------------------
fk = arm.forward_kinematics(ik)

print("Target:", target_position)
print("Reached:", fk[:3, 3])

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plot_utils.init_3d_figure()

arm.plot(ik, ax, target=target_position)

plt.show()