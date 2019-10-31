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
# Proxy
# ==============================================================================

# from compas.numerical import fd_numpy
from compas.rpc import Proxy
numerical = Proxy('...')
fd_numpy = numerical.fd_numpy

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

corners = list(mesh.vertices_where({'vertex_degree': 2}))
high = [0, 35]

mesh.set_vertices_attribute('is_fixed', True, keys=corners)
mesh.set_vertices_attribute('z', 7.0, keys=high)

# ==============================================================================
# Edge attributes
# ==============================================================================

boundary = list(mesh.edges_on_boundary())

mesh.set_edges_attribute('q', 5.0, keys=boundary)

# ==============================================================================
# FoFin input
# ==============================================================================

xyz = mesh.get_vertices_...('xyz')
fixed = ...(mesh.vertices_where({'is_fixed': True}))
... = mesh.get_vertices_attributes(('...', '...', '...'))

edges = ...(mesh.edges())
... = mesh.get_..._attribute('q')

# ==============================================================================
# Fofin run
# ==============================================================================

xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)

# ==============================================================================
# Fofin update
# ==============================================================================

for key, attr in mesh.vertices(True):
    attr['x'] = xyz[key][0]
    attr['y'] = xyz[key][1]
    attr['z'] = xyz[key][2]
    attr['...'] = r[key][...]
    attr['...'] = r[key][...]
    attr['...'] = r[key][...]

for ..., (u, v, attr) in enumerate(mesh.edges(True)):
    attr['f'] = ...[index][0]

# ==============================================================================
# Visualize result
# ==============================================================================

artist = MeshArtist(mesh, layer="Mesh")
artist.clear_layer()
artist.draw_vertices(
    color={key: (255, 0, 0) for key in mesh.vertices_where({'is_fixed': True})})
artist.draw_edges()
artist.draw_faces()
