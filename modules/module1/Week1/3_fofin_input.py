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

guids = compas_rhino.select_points()
points = compas_rhino.get_point_coordinates(guids)
names = compas_rhino.get_object_names(guids)

# ==============================================================================
# Shell
# ==============================================================================

shell = Shell.from_lines(lines, delete_boundary_face=True)

# ==============================================================================
# Geometric key map
# ==============================================================================

gkey_key = shell.gkey_key()

# ==============================================================================
# Vertex attributes
# ==============================================================================

for name, point in zip(names, points):
    gkey = geometric_key(point)
    if gkey in gkey_key:
        key = gkey_key[gkey]
        shell.set_vertex_attribute(key, 'is_fixed', True)
        if name:
            parts = name.split('=')
            if len(parts) == 2:
                z = float(parts[1])
                shell.set_vertex_attribute(key, 'z', z)

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
