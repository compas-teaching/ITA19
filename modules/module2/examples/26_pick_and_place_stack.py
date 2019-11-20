import os
import sys
import math
import time
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Box
from compas.geometry import Transformation, Translation
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import Configuration
from compas_fab.robots import Tool
from compas_fab.robots import AttachedCollisionMesh
from compas_fab.robots import CollisionMesh

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
ASSEMBLY_PATH = os.path.abspath(os.path.join(HERE, ".."))
sys.path.append(ASSEMBLY_PATH)

from assembly import Element, Assembly

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
brick = Element.from_shape(box, gripping_frame)

num = 7
assembly = Assembly()

for i in range(num):
    dy = i * height
    elem = brick.copy()
    elem.transform(Translation([0, 0, dy]))
    assembly.add_element(elem)

assembly.transform(Translation([-0.26, -0.28, 0]))

# Bring the element's mesh into the robot's tool0 frame
element_tool0 = assembly.elements[0].copy()
T = Transformation.from_frame_to_frame(element_tool0.gripping_frame, tool.frame)
element_tool0.transform(T)

# define start_configuration (close to picking_frame)
start_configuration = Configuration.from_revolute_values([-5.961, 4.407, -2.265, 5.712, 1.571, -2.820])

# little tolerance to not 'crash' into collision objects
tolerance_vector = Vector(0, 0, 0.001)

# define picking frame
picking_frame = Frame([-0.43, 0, height], [1, 0, 0], [0, 1, 0])

# define savelevel frames 'above' the picking- and target frames
savelevel_vector = Vector(0, 0, 0.05)


def calculate_picking_motion(start_configuration, picking_frame, tolerance_vector, savelevel_vector):
    """Returns a trajectory to pick an element.
    """
    picking_frame.point += tolerance_vector

    savelevel_picking_frame = picking_frame.copy()
    savelevel_picking_frame.point += savelevel_vector

    picking_frame_tool0 = robot.from_attached_tool_to_tool0([picking_frame])[0]
    picking_configuration = robot.inverse_kinematics(picking_frame_tool0, start_configuration)

    # calculate a cartesian motion from the picking frame to the savelevel_picking_frame
    frames = [picking_frame, savelevel_picking_frame]

    start_configuration = picking_configuration
    trajectory1 = robot.plan_cartesian_motion(robot.from_attached_tool_to_tool0(frames),
                                              start_configuration,
                                              max_step=0.01,
                                              attached_collision_meshes=[brick_acm])
    return trajectory1


def move_and_placing_motion(element, start_configuration, tolerance_vector, savelevel_vector, brick_acm):
    """Returns two trajectories to move and place an element.
    """

    # settings for plan_motion
    tolerance_position = 0.001
    tolerance_axes = [math.radians(1)] * 3

    target_frame = element.gripping_frame.copy()
    target_frame.point += tolerance_vector

    savelevel_target_frame = target_frame.copy()
    savelevel_target_frame.point += savelevel_vector

    # calulate a free-space motion to the savelevel_target_frame
    savelevel_target_frame_tool0 = robot.from_attached_tool_to_tool0([savelevel_target_frame])[0]
    goal_constraints = robot.constraints_from_frame(savelevel_target_frame_tool0,
                                                    tolerance_position,
                                                    tolerance_axes)

    trajectory2 = robot.plan_motion(goal_constraints,
                                    start_configuration,
                                    planner_id='RRT',
                                    attached_collision_meshes=[brick_acm])

    # calculate a cartesian motion to the target_frame
    frames = [savelevel_target_frame, target_frame]

    start_configuration = trajectory2.points[-1]  # as start configuration take last trajectory's end configuration
    trajectory3 = robot.plan_cartesian_motion(robot.from_attached_tool_to_tool0(frames),
                                              start_configuration,
                                              max_step=0.01,
                                              attached_collision_meshes=[brick_acm])
    assert(trajectory3.fraction == 1.)

    # add the brick to the planning scene
    brick = CollisionMesh(element.mesh, 'brick_wall')
    scene.append_collision_mesh(brick)
    time.sleep(0.5)
    return trajectory2, trajectory3


with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)

    scene.remove_collision_mesh('brick_wall')

    # attach tool
    robot.attach_tool(tool)
    # add tool to scene
    scene.add_attached_tool()

    # create an attached collision mesh to the robot's end effector.
    ee_link_name = robot.get_end_effector_link_name()
    brick_acm = AttachedCollisionMesh(CollisionMesh(element_tool0.mesh, 'brick'), ee_link_name)
    # add the collision mesh to the scene
    scene.add_attached_collision_mesh(brick_acm)

    #
    trajectory1 = calculate_picking_motion(start_configuration, picking_frame, tolerance_vector, savelevel_vector)
    assert(trajectory1.fraction == 1.)
    start_configuration = trajectory1.points[-1]

    for key in assembly.network.vertices():
        elem = assembly.network.vertex[key]['element']
        trajectory2, trajectory3 = move_and_placing_motion(elem, start_configuration, tolerance_vector, savelevel_vector, brick_acm)
        assert(trajectory3.fraction == 1.)
