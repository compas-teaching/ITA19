from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas_rhino
from compas.utilities import geometric_key

from fofin.shell import Shell
from fofin.shellartist import ShellArtist

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier

# ==============================================================================
# I/O
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, 'data')
FILE = os.path.join(DATA, 'fofin.json')

# ==============================================================================
# Shell
# ==============================================================================

shell = Shell.from_json(FILE)

# ==============================================================================
# Visualization helpers
# ==============================================================================

artist = ShellArtist(shell, layer="Mesh")
artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
artist.redraw()

def redraw():
    artist.clear_layer()
    artist.draw_vertices()
    artist.draw_edges()
    artist.redraw()

# ==============================================================================
# Vertex attributes
# ==============================================================================

while True:
    keys = VertexSelector.select_vertices(shell)
    if not keys:
        break
    if VertexModifier.update_vertex_attributes(shell, keys):
        shell.fofin()
        redraw()

# ==============================================================================
# Export result
# ==============================================================================

shell.to_json(FILE)

# ==============================================================================
# Visualize result
# ==============================================================================

artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
artist.draw_faces()
artist.draw_forces(scale=0.01)
artist.draw_reactions(scale=0.1)
