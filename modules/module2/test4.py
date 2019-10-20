from math import pi

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Rotation

from compas_plotters import Plotter2

a = Point(0, 0, 0)
b = Point(1, 0, 0)
c = Point(0, 1, 0)

ab = Line(a, b)
ac = Line(a, c)

u = Vector(*b)
v = Vector(*c)

plotter = Plotter2(figsize=(8, 5), viewbox=[[0, 8.0], [0, 5.0]], bgcolor='#cccccc')

plotter.add(a)
plotter.add(b)
plotter.add(c)

plotter.add(ab)
plotter.add(ac)

# plotter.add(u, point=a)
# plotter.add(v, point=a)

R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], 10 * pi / 180.0)

plotter.draw(pause=1.0)

for i in range(9):
    b.transform(R)
    ab.end.transform(R)
    plotter.redraw(pause=0.1)

plotter.show()
