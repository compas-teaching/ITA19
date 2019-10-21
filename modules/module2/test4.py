from math import radians

import matplotlib.pyplot as plt
from compas_plotters import Plotter2

from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Rotation
from compas.geometry import Vector

origin = Point(0, 0, 0)

xaxis = Line(origin, origin + Vector(1.0, 0.0, 0.0))
yaxis = Line(origin, origin + Vector(0.0, 1.0, 0.0))

u = Vector(1.0, 0.0, 0.0)
v = Vector(1.0, 0.0, 0.0)

plotter = Plotter2(figsize=(8, 5), viewbox=[[-2.0, 2.0], [-1.25, +1.25]])

plotter.add(origin)
plotter.add(xaxis)
plotter.add(yaxis)

plotter.add(u)
plotter.add(v)

R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(-10))

plotter.draw()
plt.waitforbuttonpress()

for i in range(18):
    v.transform(R)
    uxv = u.cross(v)
    print(f"-{(i+1)*10:<4}: {uxv}")

    plotter.redraw(0.1)

plotter.show()
