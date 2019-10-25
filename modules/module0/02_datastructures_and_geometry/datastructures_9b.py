import os
import compas

from compas.datastructures import Mesh
from compas.topology import breadth_first_ordering
from compas.utilities import i_to_red
from compas_plotters import MeshPlotter

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, 'data')
FILE = os.path.join(DATA, 'faces.obj')

mesh = Mesh.from_obj(FILE)

mesh.set_vertices_attributes('xyz', [0, 0, 0])

bfo = breadth_first_ordering(mesh.adjacency, 0)

print(bfo)
