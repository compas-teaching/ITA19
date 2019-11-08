import os
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist
from compas.datastructures import Mesh
from compas.datastructures import mesh_flip_cycles
from compas.geometry import add_vectors
from compas.geometry import scale_vector

# ==============================================================================
# Set the path to the input file.
# The input file was generated with `FOFIN_to`, which serialises the cablenet
# data structure to JSON.
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'cablenet.json')

# ==============================================================================
# Make a cablenet.
# ==============================================================================

cablenet = Cablenet.from_json(FILE_I)

# ==============================================================================
# Flip the cycles of the mesh because the cycles are currently such that the
# normals point to the interior of the structure.
# Note that you could also just flip the cycles once and update the JSON file.
# ==============================================================================

mesh_flip_cycles(cablenet)

# ==============================================================================
# Set the value of the thickness of the foam blocks in [m].
# ==============================================================================

THICKNESS = 0.200

# ==============================================================================
# Randomly select a face to create one block.
# ==============================================================================

fkey = cablenet.get_any_face()

# ==============================================================================
# Get the vertices of the selected face.
# The vertices are always in cycling order.
# ==============================================================================

vertices = cablenet.face_vertices(fkey)

# ==============================================================================
# Look up the coordinates of the face vertices and the normals at those vertices.
# Note that the normals are not stored as attributes, but rather have to be
# computed based on the current geometry.
# Therefore, there is no variant of the `get_vertices_attributes` that can be
# used to look up the vertex normals.
# ==============================================================================

points = cablenet.get_vertices_attributes('xyz', keys=vertices)
normals = [cablenet.vertex_normal(key) for key in vertices]

# ==============================================================================
# The bottom face of the block is formed by the vertices of the face of the
# cablenet. The top vertices of the block are offset along the normal at each
# vertex by the intended thickness of the block.
# Note that this will not result in a block with constant thickness, because the
# normals are generally not parallel. To create a block with constant thickness
# you have to use the face normal to find a parallel offset plane and then
# intersect each of the normal directions at the vertices with this plane.
# ==============================================================================

bottom = points[:]
top = []
for point, normal in zip(points, normals):
    xyz = add_vectors(point, scale_vector(normal, THICKNESS))
    top.append(xyz)

# ==============================================================================
# The vertices of the block mesh are simply the vertices of the bottom and top
# faces. The faces themselves are defined such that once the block is formed
# all face normals point towards the exterior of the block.
# Note that this means that the order of the vertices of the bottom block has
# to be reversed.
# ==============================================================================

vertices = bottom + top
faces = [[0, 3, 2, 1], [4, 5, 6, 7], [3, 0, 4, 7], [2, 3, 7, 6], [1, 2, 6, 5], [0, 1, 5, 4]]

block = Mesh.from_vertices_and_faces(vertices, faces)

# ==============================================================================
# Visualize the block with a mesh artist in the specified layer. Use
# `draw_faces` (with `join_faces=True`) instead of `draw_mesh` to get a flat
# shaded result. Also draw the vertex labels tovisualize the cycle directions.
# ==============================================================================

artist = MeshArtist(block, layer="Boxes::Test")
artist.clear_layer()
artist.draw_faces(join_faces=True, color=(0, 255, 255))
artist.draw_vertexlabels()
