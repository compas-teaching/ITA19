import random

from compas.utilities import i_to_green
from compas.utilities import i_to_red
from compas.geometry import pointcloud_xy
from compas_plotters import Plotter

cloud = pointcloud_xy(20, (0, 10), (0, 5))

points = []
for xyz in cloud:
    number = random.random()
    points.append({'pos': xyz,
                   'radius': number,
                   'edgecolor': i_to_green(number),
                   'facecolor': i_to_red(1 - number)})

plotter = Plotter(figsize=(8, 5))
plotter.draw_points(points)
plotter.show()
