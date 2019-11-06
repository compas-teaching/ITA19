from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector

import compas_rhino
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Proxy
# ==============================================================================

from compas.rpc import Proxy
numerical = Proxy('compas.numerical')
fd_numpy = numerical.fd_numpy

# ==============================================================================
# Customizations
# ==============================================================================


class Shell(Mesh):

    def __init__(self):
        super(Shell, self).__init__()
        self.default_vertex_attributes.update({'is_fixed': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
        self.default_edge_attributes.update({'q': 1.0, 'f': 0.0, 'rx': 0.0, 'ry': 0.0, 'rz': 0.0})

    def fofin(self):
        # fofin input
        xyz = mesh.get_vertices_attributes('xyz')
        fixed = list(mesh.vertices_where({'is_fixed': True}))
        loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
        edges = list(mesh.edges())
        q = mesh.get_edges_attribute('q')
        # fofin run
        ...
        # fofin update
        ...


class ShellArtist(...):
    
    def draw_forces(self, scale=1.0, layer="Mesh::Forces"):
        forces = []
        for u, v, attr in self.datastructure.edges(True):
            force = attr['f']
            start = self.datastructure.vertex_coordinates(u)
            end = self.datastructure.vertex_coordinates(v)
            radius = scale * force
            forces.append({
                'start': start,
                'end': end,
                'radius': radius,
                'color': (255, 0, 0)})
        compas_rhino.draw_cylinders(forces, layer=..., clear=True)

    def draw_reactions(self, scale=1.0, layer="Mesh::Reactions"):
        ...


# ==============================================================================
# Input file
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, 'data')
FILE = os.path.join(DATA, 'faces.obj')

# ==============================================================================
# Mesh
# ==============================================================================

shell = Shell.from_obj(FILE)

# ==============================================================================
# Vertex attributes
# ==============================================================================

corners = list(shell.vertices_where({'vertex_degree': 2}))
high = [0, 35]

shell.set_vertices_attribute('is_fixed', True, keys=corners)
shell.set_vertices_attribute('z', 7.0, keys=high)

# ==============================================================================
# Edge attributes
# ==============================================================================

boundary = list(shell.edges_on_boundary())

shell.set_edges_attribute('q', 5.0, keys=boundary)

# ==============================================================================
# Fofin run
# ==============================================================================

shell.fofin()

# ==============================================================================
# Visualize result
# ==============================================================================

artist = ShellArtist(shell, layer="Mesh")
artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
artist.draw_forces(scale=0.01)
artist.draw_reactions(scale=0.1)
