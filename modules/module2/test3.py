from math import pi

from compas.geometry import Rotation
from compas.geometry import Vector

a = Vector(1.0, 0.0, 0.0)
b = Vector(1.0, 0.0, 0.0)
c = a.cross(b)

axis = Vector(0.0, 0.0, 1.0)
angle = pi * 10.0 / 180.0

R = Rotation.from_axis_and_angle(axis, angle)

print("0  : {0[2]:.3f}".format(c))

for i in range(36):
    b.transform(R)
    c = a.cross(b)

    print("{0:<3}: {1[2]:.3f}".format((i + 1) * 10, c))
