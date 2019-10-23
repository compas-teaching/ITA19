from ... import ...
from compas.geometry import pointcloud_xy
from compas_plotters import Plotter

cloud = pointcloud_xy(20, (0, 10), (0, 5))

points = []
for xyz in cloud:
    points.append({'pos': xyz, 'radius': ...})

plotter = Plotter(figsize=(8, 5))
plotter.draw_points(points)
plotter.show()
