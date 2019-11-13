import math
from compas.geometry import Frame
from compas_fab.backends import RosClient
from compas_fab.robots import Configuration
from compas_fab.robots import AttachedCollisionMesh
import time

from compas.datastructures import Mesh

import compas_fab
from compas_fab.backends import RosClient
from compas_fab.robots import CollisionMesh
from compas_fab.robots import PlanningScene
from compas_fab.robots.ur5 import Robot



frame = Frame([0.4, 0.3, 0.4], [0, 1, 0], [0, 0, 1])
tolerance_position = 0.001
tolerance_axes = [math.radians(1)] * 3

with RosClient('localhost') as client:
    robot = Robot(client) 
    
    start_configuration = Configuration.from_revolute_values([-0.042, 4.295, 0, -3.327, 4.755, 0.])
    group = robot.main_group_name

    # create attached collision object
    mesh = Mesh.from_stl(compas_fab.get('planning_scene/cone.stl'))
    cm = CollisionMesh(mesh, 'tip')
    ee_link_name = 'ee_link'
    touch_links = ['wrist_3_link', 'ee_link']
    acm = AttachedCollisionMesh(cm, ee_link_name, touch_links)

    # create goal constraints from frame
    goal_constraints = robot.constraints_from_frame(frame,
                                                    tolerance_position,
                                                    tolerance_axes,
                                                    group)

     
    trajectory = robot.plan_motion(goal_constraints,
                                   start_configuration,
                                   group,
                                   planner_id='RRT',
                                   attached_collision_meshes=[acm])

print("Computed kinematic path with %d configurations." % len(trajectory.points))
print("Executing this path at full speed would take approx. %.3f seconds." % trajectory.time_from_start)