import os
from compas.geometry import Frame
from compas.datastructures import Mesh
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))

# load local mesh
ee_mesh = Mesh.from_stl(os.path.join(DATA, "vacuum_gripper.stl"))

# define end-effector frame
ee_frame = Frame([0.07, 0, 0], [0, 0, 1], [0, 1, 0])

with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)
    tool_acm = robot.set_end_effector(ee_mesh, ee_frame)

    # add end-effector to planning scene
    scene.add_attached_collision_mesh(tool_acm)

    # now we can convert frames at robot's tool tip and flange
    frame_tcf = Frame((-0.309, -0.046, -0.266), (0.276, 0.926, -0.256), (0.879, -0.136, 0.456))
    frame_tcf0 = robot.to_t0cf(frame_tcf)
