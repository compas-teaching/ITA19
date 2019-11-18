import os
from compas.geometry import Frame
from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Transformation
from compas.datastructures import Mesh
from compas_fab.backends import RosClient
from compas_fab.robots import Configuration
from compas_fab.robots import CollisionMesh
from compas_fab.robots import AttachedCollisionMesh
from compas_fab.robots import PlanningScene

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))

ee_mesh = Mesh.from_stl(os.path.join(DATA, "vacuum_gripper.stl"))
ee_frame = Frame([0.07, 0, 0], [0, 0, 1], [0, 1, 0])

# create attached collision object

w, l, h = 0.06, 0.029, 0.013
box = Box(Frame.worldXY(), w, l, h)
T = Translation([-w/2., -l/2, -h])
box.transform(T)
T = Transformation.from_frame_to_frame(Frame.worldXY(), ee_frame)
box.transform(T)
mesh = Mesh.from_shape(box) # the brick in relation to the end-effector frame
brick_acm = AttachedCollisionMesh(CollisionMesh(mesh, 'brick'), 'ee_link')

with RosClient('localhost') as client:
    robot = client.load_robot()
    group = robot.main_group_name
    tool_acm = robot.set_end_effector(ee_mesh, ee_frame)
    scene = PlanningScene(robot)

    scene.add_attached_collision_mesh(tool_acm)
    scene.add_attached_collision_mesh(brick_acm)

    # attention must be specified for the robots ee-link
    frames = []
    frames.append(Frame([0.3, 0.1, 0.5], [1, 0, 0], [0, 1, 0]))
    frames.append(Frame([0.5, 0.1, 0.6], [1, 0, 0], [0, 1, 0]))

    start_configuration = Configuration.from_revolute_values([-0.042, 0.033, -2.174, 5.282, -1.528, 0.000])

    trajectory = robot.plan_cartesian_motion(frames,
                                             start_configuration,
                                             max_step=0.01,
                                             avoid_collisions=True,
                                             group=group,
                                             attached_collision_meshes=[brick_acm])

    print("Computed cartesian path with %d configurations, " % len(trajectory.points))
    print("following %d%% of requested trajectory." % (trajectory.fraction * 100))
    print("Executing this path at full speed would take approx. %.3f seconds." % trajectory.time_from_start)
