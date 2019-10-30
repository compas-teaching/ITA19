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

# ==============================================================================
# Shell
# ==============================================================================

shell = Shell.from_lines(lines, delete_boundary_face=True)

# ==============================================================================
# Geometric key map
# ==============================================================================

gkey_key = {}
for key in shell.vertices():
    xyz = shell.vertex_coordinates(key)
    gkey = geometric_key(xyz)
    gkey_key[gkey] = key
    print(gkey, xyz)

# gkey_key = shell.gkey_key()

# ==============================================================================
# Vertex attributes
# ==============================================================================

for point in points:
    gkey = geometric_key(point)
    print(gkey, point)
    if gkey in gkey_key:
        key = gkey_key[gkey]
        shell.set_vertex_attribute(key, 'is_fixed', True)

high = 16
higher = 1

shell.set_vertex_attribute(high, 'z', 5.0)
shell.set_vertex_attribute(higher, 'z', 7.0)

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
