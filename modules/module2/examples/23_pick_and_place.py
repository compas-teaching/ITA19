import os
import sys
import math
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Box
from compas.geometry import Transformation
from compas.datastructures import Mesh
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import Configuration
from compas_fab.robots import Tool
from compas.datastructures import mesh_transformed
from compas_fab.robots import AttachedCollisionMesh
from compas_fab.robots import CollisionMesh

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
ASSEMBLY_PATH = os.path.abspath(os.path.join(HERE, ".."))
sys.path.append(ASSEMBLY_PATH)

from assembly import Element

# define end-effector mesh and frame
tool = Tool.from_json(os.path.join(DATA, "vacuum_gripper.json"))

# create Element
w, l, h = 0.06, 0.03, 0.014
box_frame = Frame([-w/2., -l/2, 0], [1, 0, 0], [0, 1, 0])
box = Box(box_frame, w, l, h)
gripping_frame = Frame([0, 0, h], [1, 0, 0], [0, 1, 0])
element_frame = Frame([0, 0, h/2], [1, 0, 0], [0, 1, 0])
element = Element(element_frame, 
                  mesh=Mesh.from_shape(box),
                  gripping_frame=gripping_frame)

def acm_from_element(element, tool):
    """Transform the element into the end-effector's frame.
    """
    T = Transformation.from_frame_to_frame(element.gripping_frame, tool.frame)
    mesh = mesh_transformed(element.mesh, T)
    return AttachedCollisionMesh(CollisionMesh(mesh, 'brick'), 'ee_link')

brick_acm = acm_from_element(element, tool)

start_configuration = Configuration.from_revolute_values([-5.961, 4.407, -2.265, 5.712, 1.571, -2.820])

# define picking frame and configuration
picking_frame = Frame([-0.43, 0, h], [1, 0, 0], [0, 1, 0])
picking_configuration = None

# define target frame
target_frame = Frame([-0.26, -0.28, h], [1, 0, 0], [0, 1, 0])

# define savelevel frames 'above' the picking- and target frames
savelevel_vector = Vector(0, 0, 0.05)
savelevel_picking_frame = picking_frame.copy()
savelevel_picking_frame.point += savelevel_vector
savelevel_target_frame = target_frame.copy()
savelevel_target_frame.point += savelevel_vector

# settings for plan_motion
tolerance_position = 0.001
tolerance_axes = [math.radians(1)] * 3

with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)
    robot.attach_tool(tool)
    scene.add_attached_tool()

    picking_configuration = robot.inverse_kinematics(robot.to_tool0_frame(picking_frame), start_configuration)

    # 1. 'Pick' the object at the picking picking frame with a cartesian path 
    # start_frame and start_configuration are picking_frame and picking_configuration
    frames = [picking_frame, savelevel_picking_frame]
    frames_tool0 = robot.to_tool0_frames(frames)

    trajectory1 = robot.plan_cartesian_motion(frames_tool0,
                                              picking_configuration,
                                              max_step=0.01,
                                              attached_collision_meshes=[brick_acm])
    assert(trajectory1.fraction == 1.)

    # 2. Now calulate a free-space motion to the savelevel_target_frame
    

    # create goal constraints from frame
    goal_constraints = robot.constraints_from_frame(robot.to_tool0_frame(savelevel_target_frame),
                                                    tolerance_position,
                                                    tolerance_axes,
                                                    group)

    trajectory = robot.plan_motion(goal_constraints,
                                   start_configuration,
                                   group,
                                   planner_id='RRT')

    # scene.add_attached_collision_mesh(brick_acm)




    """
    """