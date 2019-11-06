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
# Visualize result
# ==============================================================================

artist = ShellArtist(shell, layer="Mesh")
artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
