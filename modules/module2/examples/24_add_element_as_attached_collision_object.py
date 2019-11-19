import os
import sys
import time
from compas.geometry import Frame
from compas.geometry import Box
from compas.geometry import Transformation
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import CollisionMesh
from compas_fab.robots import AttachedCollisionMesh
from compas_fab.robots import Tool

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
ASSEMBLY_PATH = os.path.abspath(os.path.join(HERE, ".."))
sys.path.append(ASSEMBLY_PATH)

from assembly import Element

# create tool from json
filepath = os.path.join(DATA, "vacuum_gripper.json")
tool = Tool.from_json(filepath)

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

# now we need to bring the element's mesh into the robot's tool0 frame
element_tool0 = element.copy()
T = Transformation.from_frame_to_frame(element_tool0.gripping_frame, tool.frame)
element_tool0.transform(T)

with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)

    # attach tool
    robot.attach_tool(tool)
    # add tool to scene
    scene.add_attached_tool()

    # create an attached collision mesh to the robot's end effector.
    ee_link_name = robot.get_end_effector_link_name()
    brick_acm = AttachedCollisionMesh(CollisionMesh(element_tool0.mesh, 'brick'), ee_link_name)
    # add the collision mesh to the scene
    scene.add_attached_collision_mesh(brick_acm)

    time.sleep(1)
