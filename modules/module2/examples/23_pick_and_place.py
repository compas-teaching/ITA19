import os
import sys
import math
import time
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

# brick dimensions
w, l, h = 0.06, 0.03, 0.014

# define start_configuration (close to picking_frame)
start_configuration = Configuration.from_revolute_values([-5.961, 4.407, -2.265, 5.712, 1.571, -2.820])

# define picking frame
picking_frame = Frame([-0.43, 0, h], [1, 0, 0], [0, 1, 0])

# define target frame
target_frame = Frame([-0.26, -0.28, h], [1, 0, 0], [0, 1, 0])

# create Element and move it at target frame
box_frame = Frame([-w/2., -l/2, 0], [1, 0, 0], [0, 1, 0])
box = Box(box_frame, w, l, h)
gripping_frame = Frame([0, 0, h], [1, 0, 0], [0, 1, 0])
element_frame = Frame([0, 0, h/2], [1, 0, 0], [0, 1, 0])
element = Element.from_mesh(Mesh.from_shape(box), element_frame)
element.gripping_frame = gripping_frame
element.transform(Transformation.from_frame_to_frame(element.gripping_frame, target_frame))

def acm_from_element(element, tool):
    """Transform the element into the end-effector's frame.
    """
    T = Transformation.from_frame_to_frame(element.gripping_frame, tool.frame)
    mesh = mesh_transformed(element.mesh, T)
    return AttachedCollisionMesh(CollisionMesh(mesh, 'brick'), 'ee_link')


brick_acm = acm_from_element(element, tool)

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

    # 1. Calculate a cartesian motion from the picking frame to the savelevel_picking_frame
    frames = [picking_frame, savelevel_picking_frame]

    start_configuration = picking_configuration
    trajectory1 = robot.plan_cartesian_motion(robot.to_tool0_frames(frames),
                                              start_configuration,
                                              max_step=0.01,
                                              attached_collision_meshes=[brick_acm])
    assert(trajectory1.fraction == 1.)

    # 2. Calulate a free-space motion to the savelevel_target_frame
    goal_constraints = robot.constraints_from_frame(robot.to_tool0_frame(savelevel_target_frame),
                                                    tolerance_position,
                                                    tolerance_axes)

    start_configuration = trajectory1.points[-1]  # as start configuration take last trajectory's end configuration
    trajectory2 = robot.plan_motion(goal_constraints,
                                    start_configuration,
                                    planner_id='RRT',
                                    attached_collision_meshes=[brick_acm])

    # 3. Calculate a cartesian motion to the target_frame
    frames = [savelevel_target_frame, target_frame]

    start_configuration = trajectory2.points[-1]  # as start configuration take last trajectory's end configuration
    trajectory3 = robot.plan_cartesian_motion(robot.to_tool0_frames(frames),
                                              start_configuration,
                                              max_step=0.01,
                                              attached_collision_meshes=[brick_acm])
    assert(trajectory3.fraction == 1.)

    # 4. Add the brick to the planning scene
    brick = CollisionMesh(element.mesh, 'brick_wall')
    scene.append_collision_mesh(brick)

    time.sleep(1)
