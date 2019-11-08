import math
from compas.geometry import Translation, Cylinder, Circle, Plane
from compas.robots import RobotModel, Joint
from compas_fab.robots import Configuration
from compas.datastructures import Mesh
from compas.geometry import Frame

import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path)
from viewer import RobotArtist

# create cylinder
axis = (0, 0, 1)
radius, length = 0.3, 5
cylinder = Cylinder(Circle(Plane([0, 0, 0], [1, 0, 0]), radius), length)
cylinder.transform(Translation([length / 2., 0, 0]))

# create robot
robot = RobotModel("robot")
parent_link = robot.add_link("world")

for i in range(6):
    origin = Frame.worldXY()
    if i > 0:
        origin.point = (length, 0, 0)
    mesh = Mesh.from_shape(cylinder)
    child_link = robot.add_link("link%d" % i, visual_mesh=mesh)
    robot.add_joint("joint%d" % i, Joint.CONTINUOUS, parent_link, child_link, origin, axis)
    parent_link = child_link

# create artist
artist = RobotArtist(robot)
names = robot.get_configurable_joint_names()
types = [Joint.CONTINUOUS] * len(names)
values = [90, 0, -125, 70, -125, 0]
values = [math.radians(v) for v in values]
configuration = Configuration(values, types)
artist.update(configuration, names, visual=True, collision=False)