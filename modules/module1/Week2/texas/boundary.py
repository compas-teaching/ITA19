import os
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import FrameArtist
from compas_rhino.artists import PointArtist
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import transform_points
from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors
from compas.geometry import bounding_box_xy
from compas.geometry import offset_polygon
from compas.geometry import intersection_line_plane

# ==============================================================================
# Create a proxy for PCA
# ==============================================================================

from compas.rpc import Proxy
numerical = Proxy('compas.numerical')
pca_numpy = numerical.pca_numpy

# ==============================================================================
# Construct a cablenet
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'cablenet.json')

cablenet = Cablenet.from_json(FILE_I)

# ==============================================================================
# Parameters
# ==============================================================================

OFFSET = 0.200
PADDING = 0.020

# ==============================================================================
# Vertices on SOUTH
# ==============================================================================

SOUTH = list(cablenet.vertices_where({'constraint': 'SOUTH'}))
boundary = list(cablenet.vertices_on_boundary(ordered=True))
SOUTH[:] = [key for key in boundary if key in SOUTH]

# ==============================================================================
# Boundary plane
# ==============================================================================

a = cablenet.vertex_coordinates(SOUTH[0])
b = cablenet.vertex_coordinates(SOUTH[-1])

xaxis = subtract_vectors(b, a)
yaxis = [0, 0, 1.0]
zaxis = cross_vectors(xaxis, yaxis)
xaxis = cross_vectors(yaxis, zaxis)

frame = Frame(a, xaxis, yaxis)

point = add_vectors(frame.point, scale_vector(frame.zaxis, OFFSET))
normal = frame.zaxis
plane = point, normal

# ==============================================================================
# Intersections
# ==============================================================================

intersections = []

for key in SOUTH:
    a = cablenet.vertex_coordinates(key)
    r = cablenet.residual(key)
    b = add_vectors(a, r)
    x = intersection_line_plane((a, b), plane)

    intersections.append(x)

# ==============================================================================
# Bounding boxes
# ==============================================================================

points = intersections[:6]

origin, axes, values = pca_numpy(points)
frame1 = Frame(origin, axes[0], axes[1])

X = Transformation.from_frame_to_frame(frame1, Frame.worldXY())
points = transform_points(points, X)

bbox = bounding_box_xy(points)
bbox = offset_polygon(bbox, -PADDING)
bbox = transform_points(bbox, X.inverse())

bbox = Mesh.from_vertices_and_faces(bbox, [[0, 1, 2, 3]])

# ==============================================================================
# Visualization
# ==============================================================================

artist = FrameArtist(frame, layer="SOUTH::Frame", scale=0.3)
artist.clear_layer()
artist.draw()

artist = FrameArtist(frame1, layer="SOUTH::Frame1", scale=0.3)
artist.clear_layer()
artist.draw()

artist = MeshArtist(bbox, layer="SOUTH::Bbox1")
artist.clear_layer()
artist.draw_mesh()

PointArtist.draw_collection(intersections, layer="SOUTH::Intersections", clear=True)
