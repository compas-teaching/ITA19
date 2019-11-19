import os
from compas.geometry import Frame
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import Tool

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))

filepath = os.path.join(DATA, "vacuum_gripper.json")
tool = Tool.from_json(filepath)

with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)
    robot.attach_tool(tool)

    # add attached tool to planning scene
    scene.add_attached_tool()

    # now we can convert frames at robot's tool tip and flange
    frame_tcf = Frame((-0.309, -0.046, -0.266), (0.276, 0.926, -0.256), (0.879, -0.136, 0.456))
    frame_tcf0 = robot.to_tool0_frame(frame_tcf)
