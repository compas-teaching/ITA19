import os
import random

import compas

from compas.files import OBJReader
from compas.utilities import flatten
from compas.utilities import i_to_red
from compas.utilities import i_to_blue

from compas_fofin.datastructures import Cablenet

from compas_plotters import MeshPlotter

# ==============================================================================
# Make a cablenet
# ==============================================================================

HERE = os.path.dirname(__file__)

FILE = os.path.join(HERE, 'data', 'quadmesh.obj')
cablenet = Cablenet.from_obj(FILE)

# ==============================================================================
# Select a starting edge
# ==============================================================================

start = random.choice(list(set(cablenet.edges()) - set(cablenet.edges_on_boundary())))

# ==============================================================================
# Continuous edges and parallel edges
# ==============================================================================

continuous = cablenet.get_continuous_edges(start)
parallel = cablenet.get_parallel_edges(start, aligned=True)
faces = cablenet.get_face_strip(start)

cables = []
for edge in parallel:
    edges = cablenet.get_continuous_edges(edge)
    cables.append(edges)

chained = cablenet.get_continuous_edges(start, aligned=True)
chain = list(flatten(chained[::2] + chained[-1:]))

# ==============================================================================
# Visualize
# ==============================================================================

vertexcolor = {key: i_to_red(index / len(chain)) for index, key in enumerate(chain)}

arrows = [{
    'start': cablenet.vertex_coordinates(start[0]),
    'end': cablenet.vertex_coordinates(start[1]),
    'color': (1.0, 0.0, 0.0)
}]
for u, v in parallel:
    if u not in start and v not in start:
        arrows.append({
            'start': cablenet.vertex_coordinates(u),
            'end': cablenet.vertex_coordinates(v),
            'color': (0.0, 0.0, 0.0)
        })

facecolor = {key: i_to_blue(index / len(faces)) for index, key in enumerate(faces)}

plotter = MeshPlotter(cablenet, figsize=(10, 7))
plotter.defaults['vertex.radius'] = 0.04
plotter.defaults['edge.width'] = 0.5
plotter.draw_edges(width={key: 3.0 for edges in cables for key in edges})
plotter.draw_vertices(radius={key: 0.06 for key in chain}, facecolor=vertexcolor)
plotter.draw_arrows2(arrows)
plotter.draw_faces(facecolor=facecolor, keys=faces, text={key: str(index) for index, key in enumerate(faces)})
plotter.show()
