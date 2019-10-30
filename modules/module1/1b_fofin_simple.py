from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector

import compas_rhino
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Input file
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, 'data')
FILE = os.path.join(DATA, 'faces.obj')

# ==============================================================================
# Mesh
# ==============================================================================

mesh = Mesh.from_obj(FILE)

mesh.update_default_vertex_attributes({'is_fixed': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
mesh.update_default_edge_attributes({'q': 1.0, 'f': 0.0, 'rx': 0.0, 'ry': 0.0, 'rz': 0.0})

# ==============================================================================
# Vertex attributes
# ==============================================================================

corners = ...(mesh.vertices_where({'...': 2}))
high = [0, 35]

mesh.set_vertices_attribute('is_fixed', True, keys=corners)
mesh.set_vertices_attribute('z', ..., keys=high)

# ==============================================================================
# Edge attributes
# ==============================================================================

boundary = list(mesh.edges_on_boundary())

mesh.set_edges_attribute('q', 5.0, keys=boundary)

# ==============================================================================
# Visualize result
# ==============================================================================

artist = MeshArtist(mesh, layer="Mesh")
artist.clear_layer()
artist.draw_vertices(
    color={key: (..., 0, 0) for key in mesh.vertices_where({'...': True})})
artist.draw_edges()
artist.draw_faces()
