import os
import sys
import time
from compas.geometry import Frame
from compas.geometry import Box
from compas.geometry import Transformation
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import CollisionMesh

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
ASSEMBLY_PATH = os.path.abspath(os.path.join(HERE, ".."))
sys.path.append(ASSEMBLY_PATH)

from assembly import Element

# define brick dimensions
width, length, height = 0.06, 0.03, 0.014

# define target frame
target_frame = Frame([-0.26, -0.28, height], [1, 0, 0], [0, 1, 0])

# create Element and move it to target frame
box_frame = Frame([-width/2., -length/2, 0], [1, 0, 0], [0, 1, 0])
box = Box(box_frame, width, length, height)
gripping_frame = Frame([0, 0, height], [1, 0, 0], [0, 1, 0])
element = Element.from_shape(box, gripping_frame)
element.transform(Transformation.from_frame_to_frame(element.frame, target_frame))

with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)

    # create a CollisionMesh from the element and add it to the scene
    brick = CollisionMesh(element.mesh, 'brick_wall')
    scene.append_collision_mesh(brick)

    time.sleep(2)

    # Remove elements from scene
    scene.remove_collision_mesh(brick.id)
    time.sleep(1)
