from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import add_vectors
from compas.geometry import scale_vector

import compas_rhino
from compas_rhino.artists import MeshArtist


class ShellArtist(MeshArtist):
    
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
        compas_rhino.draw_cylinders(forces, layer=layer, clear=True)

    def draw_reactions(self, scale=1.0, layer="Mesh::Reactions"):
        reactions = []
        for key, attr in self.datastructure.vertices_where({'is_fixed': True}, True):
            reaction = [attr['rx'], attr['ry'], attr['rz']]
            vector = scale_vector(reaction, -scale)
            start = self.datastructure.vertex_coordinates(key)
            end = add_vectors(start, vector)
            reactions.append({
                'start': start,
                'end': end,
                'arrow': 'end',
                'color': (0, 255, 0)})
        compas_rhino.draw_lines(reactions, layer=layer, clear=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
