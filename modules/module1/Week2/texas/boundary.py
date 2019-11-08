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
# Create a proxy for PCA. This will reconnect to an existing proxy server if one
# exists, or start a new one otherwise. Point the proxy to `commpas.numerical`
# to provide access to `pca_numpy`.
# Note that if you are unable to connect to the server, the following things
# might help:
# 1. Kill all instances of running servers. Look for instances of `python.exe`
#    or `pythonw.exe` in the *Activity Monitor* (Mac) or the *Details* tab of the
#    *Task Manager* (Windows).
# 2. Start the proxy server externally from the command line before running this
#    script in Rhino.
# 3. Call a help line.
# ==============================================================================

from compas.rpc import Proxy
numerical = Proxy('compas.numerical')
pca_numpy = numerical.pca_numpy

# ==============================================================================
# Make a cablenet.
# The JSON input file is produced with the command `FOFIN_to`, which serializes
# the cablenet data structure to a JSON file.
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'cablenet.json')

cablenet = Cablenet.from_json(FILE_I)

# ==============================================================================
# Set an offset parameter to define the distance between the edge of the
# structure and the location of the boundary frame.
# Set a padding parameter to add some extra material around the bounding box of
# the intersection points.
# ==============================================================================

OFFSET = 0.200
PADDING = 0.020

# ==============================================================================
# Find the vertices on the *SOUTH* boundary, which are all vertices where the
# attribute `'constraint'` is set to `'SOUTH'`. Remember that the function returns
# a generator object that can be used to iterate over the vertices once. To store
# the vertices such that they can be iterated over multiple times, the generator
# has to be converted to a list.
# ==============================================================================

SOUTH = list(cablenet.vertices_where({'constraint': 'SOUTH'}))

# ==============================================================================
# The vertices returned by `vertices_where` have no particular order. To make
# sure that the vertices are in consecutive order, recreate the list of vertices
# such that the vertices are in the same order as they are on the ordered boundary.
# ==============================================================================

boundary = list(cablenet.vertices_on_boundary(ordered=True))
SOUTH[:] = [key for key in boundary if key in SOUTH]

# ==============================================================================
# Construct the local axes of the *SOUTH* boundary. Align the xaxis with the
# main span of the boundary and the y axis with the world z axis. Use local x
# and y to compute local z.
# ==============================================================================

a = cablenet.vertex_coordinates(SOUTH[0])
b = cablenet.vertex_coordinates(SOUTH[-1])

xaxis = subtract_vectors(b, a)
yaxis = [0, 0, 1.0]
zaxis = cross_vectors(xaxis, yaxis)

# ==============================================================================
# Note that in the general case x and y are not perpendicular because the x axis
# defined by the span of the boundary, which is not necessarily horizontal. Since
# we want to keep the local y axis aligned with the global z axis, use the local
# y and z to redefine the local x.
# ==============================================================================

xaxis = cross_vectors(yaxis, zaxis)

# ==============================================================================
# Construct the frame of the *SOUTH* boundary using first point on the *SOUTH*
# Note that the frame will take care of normalizing the provided axes.
# ==============================================================================

frame = Frame(a, xaxis, yaxis)

# ==============================================================================
# Construct an intersection plane from the frame of the boundary. Use the origin
# of the frame as the plane point and the z axis of the frame as the plane normal.
# Move the plane along the normal by the defined offset.
# ==============================================================================

point = add_vectors(frame.point, scale_vector(frame.zaxis, OFFSET))
normal = frame.zaxis
plane = point, normal

# ==============================================================================
# Compute the intersections of the residual force vectors at the boundary
# vertices with the previously defined intersection plane.
# ==============================================================================

intersections = []

for key in SOUTH:
    a = cablenet.vertex_coordinates(key)
    r = cablenet.residual(key)
    b = add_vectors(a, r)
    x = intersection_line_plane((a, b), plane)

    intersections.append(x)

# ==============================================================================
# Select the first 6 vertices of the boundary for the first segment of the
# supporting structure. Compute a local frame for the selected vertices using a
# PCA of the vertex locations.
# ==============================================================================

points = intersections[:6]

origin, axes, values = pca_numpy(points)
frame1 = Frame(origin, axes[0], axes[1])

# ==============================================================================
# Transform the local coordinates to world coordinates to make it an axis-aligned
# problem.
# ==============================================================================

X = Transformation.from_frame_to_frame(frame1, Frame.worldXY())
points = transform_points(points, X)

# ==============================================================================
# Compute the axis aligned bounding box in world coordinates, ignoring the Z
# components of the points. Add some padding to the bounding box to avoid having
# vertices on the boundaries of the box. Convert the box back to the local
# coordinate system.
# ==============================================================================

bbox = bounding_box_xy(points)
bbox = offset_polygon(bbox, -PADDING)
bbox = transform_points(bbox, X.inverse())

# ==============================================================================
# Convert the box to a mesh for visualisation.
# ==============================================================================

bbox = Mesh.from_vertices_and_faces(bbox, [[0, 1, 2, 3]])

# ==============================================================================
# Use a frame artist to visualize the boundary frame.
# ==============================================================================

artist = FrameArtist(frame, layer="SOUTH::Frame", scale=0.3)
artist.clear_layer()
artist.draw()

# ==============================================================================
# Use a point artist to visualize the intersection points.
# ==============================================================================

PointArtist.draw_collection(intersections, layer="SOUTH::Intersections", clear=True)

# ==============================================================================
# Use a frame artist to visualize the frame of the intersection points.
# ==============================================================================

artist = FrameArtist(frame1, layer="SOUTH::Frame1", scale=0.3)
artist.clear_layer()
artist.draw()

# ==============================================================================
# Use a mesh artist to visualize the bounding box.
# ==============================================================================

artist = MeshArtist(bbox, layer="SOUTH::Bbox1")
artist.clear_layer()
artist.draw_mesh()
