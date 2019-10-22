from compas.geometry import pointcloud_xy
from compas_plotters import Plotter

cloud = pointcloud_xy(20, xbounds=(0, 10), ybounds=(0, 5))

points = []
for xyz in cloud:
    points.append({'pos': xyz, 'radius': 0.1})

plotter = Plotter(figsize=(8, 5))
plotter.draw_points(points)
plotter.show()
