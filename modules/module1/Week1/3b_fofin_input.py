from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import geometric_key

from fofin.shell import Shell
from fofin.shellartist import ShellArtist

# ==============================================================================
# Input
# ==============================================================================

guids = compas_rhino.select_lines()
lines = compas_rhino.get_line_coordinates(guids)

# ==============================================================================
# Shell
# ==============================================================================

shell = Shell.from_lines(lines, delete_boundary_face=True)

# ==============================================================================
# Vertex attributes
# ==============================================================================

corners = list(shell.vertices_where({'vertex_degree': 3}))
high = 16
higher = 1

shell.set_vertices_attribute('is_fixed', True, keys=corners)
shell.set_vertex_attribute(higher, 'z', 7.0)
shell.set_vertex_attribute(high, 'z', 5.0)

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
artist.draw_faces()
artist.draw_forces(scale=0.01)
artist.draw_reactions(scale=0.1)
