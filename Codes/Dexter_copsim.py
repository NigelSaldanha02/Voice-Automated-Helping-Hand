import sys
import time

sys.path.append(r"C:\Program Files\CoppeliaSim\programming\remoteApiBindings\python")

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')

target = sim.getObject('/target_dummy')

print("Connected. Moving target...")

sim.setObjectPosition(target, -1, [0.18, 0.0, 0])
time.sleep(2)

sim.setObjectPosition(target, -1, [0.18, 0.05, 0])
time.sleep(2)

sim.setObjectPosition(target, -1, [0.18, -0.05, 0])
time.sleep(2)

print("Done.")
