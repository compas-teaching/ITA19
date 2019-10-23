from math import radians

import compas_rhino

from compas.geometry import pointcloud
from compas.geometry import bounding_box

from compas.utilities import pairwise

cloud1 = pointcloud(20, (0, 10), (0, 5), (0, 3))
bbox1 = bounding_box(cloud1)

Rz = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(30))
Ry = Rotation.from_axis_and_angle([0.0, 1.0, 0.0], radians(20))
Rx = Rotation.from_axis_and_angle([1.0, 0.0, 0.0], radians(40))

R = Rz * Ry * Rz

cloud2 = transform_points(cloud1, R)
bbox2 = transform_points(bbox1, R)

average, vectors, values = numerical.pca_numpy(cloud2)

origin = average[0]
xaxis = vectors[0]
yaxis = vectors[1]
zaxis = vectors[2]

frame = Frame(origin, xaxis, yaxis)
world = Frame.worldXY()

T = Transformation.from_frame_to_frame(frame, world)

cloud3 = transform_points(cloud2, T)

bbox3 = bounding_box(cloud3)
bbox4 = transform_points(bbox3, T.inverse())

# ==============================================================================
# Visualisation
# ==============================================================================

points = []

for xyz in cloud:
    points.append({'pos': xyz, 'color': color})

compas_rhino.draw_points(points, layer=layer, clear=True)

lines = []

for a, b in pairwise(bbox[:4] + bbox[:1]):
    lines.append({'start': a, 'end': b, 'color': color})
for a, b in pairwise(bbox[4:] + bbox[4:5]):
    lines.append({'start': a, 'end': b, 'color': color})
for a, b in zip(bbox[:4], bbox[4:]):
    lines.append({'start': a, 'end': b, 'color': color})

compas_rhino.draw_lines(lines, layer=layer, clear=True)
