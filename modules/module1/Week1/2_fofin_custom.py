from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

from fofin.shell import Shell
from fofin.shellartist import ShellArtist

# ==============================================================================
# Input file
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, 'data')
FILE = os.path.join(DATA, 'faces.obj')

# ==============================================================================
# Shell
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
