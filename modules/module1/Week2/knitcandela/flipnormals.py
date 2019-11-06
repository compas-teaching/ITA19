import os
from compas_fofin.datastructures import Cablenet
from compas.datastructures import mesh_flip_cycles

HERE = os.path.dirname(__file__)

FILE_I = os.path.join(HERE, 'data', 'cablenet.json')
FILE_O = os.path.join(HERE, 'data', 'cablenet.json')

cablenet = Cablenet.from_json(FILE_I)

# ==============================================================================
# flip mesh normals
# ==============================================================================

# ==============================================================================
# Export
# ==============================================================================
