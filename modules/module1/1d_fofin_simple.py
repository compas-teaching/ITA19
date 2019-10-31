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
numerical = Proxy('compas.numerical')
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

xyz = mesh.get_vertices_attributes('xyz')
fixed = list(mesh.vertices_where({'is_fixed': True}))
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))

edges = list(mesh.edges())
q = mesh.get_edges_attribute('q')

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
    attr['rx'] = r[key][0]
    attr['ry'] = r[key][1]
    attr['rz'] = r[key][2]

for index, (u, v, attr) in enumerate(mesh.edges(True)):
    attr['f'] = f[index][0]

# ==============================================================================
# Visualize result
# ==============================================================================

artist = MeshArtist(mesh, layer="Mesh")
artist.clear_layer()
artist.draw_vertices(
    color={key: (255, 0, 0) for key in mesh.vertices_where({'is_fixed': True})})
artist.draw_edges()
artist.draw_faces()

forces = []
for ..., ..., ... in mesh.edges(True):
    force = attr['...']
    ... = mesh.vertex_coordinates(u)
    ... = mesh.vertex_coordinates(v)
    radius = 0.01 * force
    forces.append({
        'start': start,
        'end': end,
        'radius': radius,
        'color': (..., ..., ...)})

compas_rhino.draw_cylinders(
    forces, layer="Mesh::Forces", clear=True)

reactions = []
for key, attr in mesh.vertices_where({'...': True}, True):
    reaction = [attr['...'], attr['...'], attr['...']]
    vector = scale_vector(reaction, ...)
    start = mesh.vertex_coordinates(key)
    end = add_vectors(start, vector)
    reactions.append({
        'start': start,
        'end': end,
        'arrow': 'end',
        'color': (..., ..., ...)})

compas_rhino.draw_lines(
    reactions, layer="Mesh::Reactions", clear=True)
