import os
import time

from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import Tool

from compas.datastructures import Mesh
from compas.geometry import Frame

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))

# create tool from mesh and frame
mesh = Mesh.from_stl(os.path.join(DATA, "vacuum_gripper.stl"))
frame = Frame([0.07, 0, 0], [0, 0, 1], [0, 1, 0])
tool = Tool(mesh, frame)
tool.to_json(os.path.join(DATA, "vacuum_gripper.json"))


with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)
    robot.attach_tool(tool)

    # add attached tool to planning scene
    scene.add_attached_tool()

    # now we can convert frames at robot's tool tip and flange
    frames_tcf = [Frame((-0.309, -0.046, -0.266), (0.276, 0.926, -0.256), (0.879, -0.136, 0.456))]
    frames_tcf0 = robot.from_attached_tool_to_tool0(frames_tcf)

    time.sleep(2)

    # Now remove it again
    scene.remove_attached_tool()
    scene.remove_collision_mesh(tool.name)
    robot.detach_tool()
    time.sleep(1)
