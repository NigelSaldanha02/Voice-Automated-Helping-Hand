import numpy as np
import matplotlib.pyplot as plt
from ikpy.utils import plot
from ikpy.chain import Chain

# Load URDF file
arm = Chain.from_urdf_file(
    "D:\College\VScode\Projects\VoiceAutomatedHelpingHand\Dexter_Sim/Dexter_ER2.urdf",
    active_links_mask=[False, True, True, True, True, True, False]
)

# Target (meters)
target_position = [0.02, 0.01, 0]

# Initialize zero position
initial_angles = np.zeros(len(arm.links))
print(initial_angles)

# Solve IK
ik_solution = arm.inverse_kinematics(target_position, initial_angles, max_iter = 200)

print("\nIK solution:")
for link, angle in zip(arm.links, ik_solution):
    print(f"{link.name:15s}: {angle:.3f}")

# FK check
fk = arm.forward_kinematics(ik_solution)

print("\nEnd-effector position from FK:")
print(fk[:3, 3])

# Visuale in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plot.plot_chain(arm, ik_solution, ax)

ax.set_xlim([-0.3, 0.3])
ax.set_ylim([-0.3, 0.3])
ax.set_zlim([0, 0.5])

plt.show()