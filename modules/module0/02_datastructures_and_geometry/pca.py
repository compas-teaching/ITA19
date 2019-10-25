from math import radians

import compas_rhino

from compas.geometry import pointcloud
from compas.geometry import bounding_box
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import transform_points
from compas.utilities import pairwise

# from compas.numerical import pca_numpy
from compas.rpc import Proxy
numerical = Proxy('compas.numerical')

# ==============================================================================
# Helpers
# ==============================================================================

def draw_cloud(cloud, bbox, color, layer):
    points = [{'pos': xyz, 'color': color} for xyz in cloud]
    lines = []
    for a, b in pairwise(bbox[:4] + bbox[:1]):
        lines.append({'start': a, 'end': b, 'color': color})
    for a, b in pairwise(bbox[4:] + bbox[4:5]):
        lines.append({'start': a, 'end': b, 'color': color})
    for a, b in zip(bbox[:4], bbox[4:]):
        lines.append({'start': a, 'end': b, 'color': color})
    compas_rhino.draw_points(points, layer=layer, clear=True)
    compas_rhino.draw_lines(lines, layer=layer, clear=False)


def draw_frame(frame, layer):
    origin = list(frame.point)
    xaxis = list(frame.point + frame.xaxis)
    yaxis = list(frame.point + frame.yaxis)
    zaxis = list(frame.point + frame.zaxis)
    points = [{'pos': origin, 'color': (255, 255, 0)}]
    lines = [
        {'start': origin, 'end': xaxis, 'color': (255, 0, 0), 'arrow': 'end'},
        {'start': origin, 'end': yaxis, 'color': (0, 255, 0), 'arrow': 'end'},
        {'start': origin, 'end': zaxis, 'color': (0, 0, 255), 'arrow': 'end'}]
    compas_rhino.draw_points(points, layer=layer, clear=True)
    compas_rhino.draw_lines(lines, layer=layer, clear=False)

# ==============================================================================
# Algorithm
# ==============================================================================

cloud1 = pointcloud(30, (0, 10), (0, 3), (0, 5))
bbox1 = bounding_box(cloud1)

Rz = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(60))
Ry = Rotation.from_axis_and_angle([0.0, 1.0, 0.0], radians(20))
Rx = Rotation.from_axis_and_angle([1.0, 0.0, 0.0], radians(10))

T = Translation([2.0, 5.0, 8.0])

R = T * Rz * Ry * Rx

cloud2 = transform_points(cloud1, R)
bbox2 = transform_points(bbox1, R)

mean, vectors, values = numerical.pca_numpy(cloud2)

origin = mean[0]
xaxis = vectors[0]
yaxis = vectors[1]

frame = Frame(origin, xaxis, yaxis)
world = Frame.worldXY()

X = Transformation.from_frame_to_frame(frame, world)

cloud3 = transform_points(cloud2, X)
bbox3 = bounding_box(cloud3)

bbox4 = transform_points(bbox3, X.inverse())

# ==============================================================================
# Visualisation
# ==============================================================================

draw_cloud(cloud1, bbox1, (0, 0, 0), "Cloud1")
draw_cloud(cloud2, bbox2, (255, 255, 255), "Cloud2")
draw_cloud(cloud3, bbox3, (0, 255, 255), "Cloud3")
draw_cloud(cloud2, bbox4, (255, 0, 0), "Cloud4")

draw_frame(frame, "Frame")
