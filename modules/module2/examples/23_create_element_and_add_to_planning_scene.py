import os
import sys
import time
import json
from compas.geometry import Frame
from compas.geometry import Transformation
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import CollisionMesh

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
ASSEMBLY_PATH = os.path.abspath(os.path.join(HERE, ".."))
sys.path.append(ASSEMBLY_PATH)

from assembly import Element

# load settings (shared by GH)
settings_file = os.path.join(DATA, "settings.json")
with open(settings_file, 'r') as f:
    data = json.load(f)

# define brick dimensions
width, length, height = data['brick_dimensions']

# define target frame
target_frame = Frame([-0.26, -0.28, height], [1, 0, 0], [0, 1, 0])

# Move brick to target frame
element = Element.from_data(data['brick'])
element.transform(Transformation.from_frame_to_frame(element.frame, target_frame))

with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)

    # create a CollisionMesh from the element and add it to the scene
    brick = CollisionMesh(element.mesh, 'brick_wall')
    scene.append_collision_mesh(brick)

    time.sleep(2)

    # Remove elements from scene
    # scene.remove_collision_mesh(brick.id)
    # time.sleep(1)
