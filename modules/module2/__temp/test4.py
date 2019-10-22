from math import radians

import matplotlib.pyplot as plt
from matplotlib.text import Text
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

uxv = u.cross(v)

plotter = Plotter2(figsize=(8, 5), viewbox=[[-1.0, 3.0], [-1, +1.50]])

plotter.add(origin)
plotter.add(xaxis)
plotter.add(yaxis)
plotter.add(u)
plotter.add(v)

text = plotter.axes.add_artist(Text(x=1.0, y=0.75, text=f"Angle: 0\n{uxv}"))

plotter.draw()
plt.waitforbuttonpress()

R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(-10))

for i in range(18):
    v.transform(R)
    uxv = u.cross(v)
    text.set_text(f"Angle: -{(i+1)*10:<4}\n{uxv}")
    plotter.redraw(0.1)

plotter.show()
