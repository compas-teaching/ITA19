import os
import sys
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector

HERE = os.path.dirname(__file__)

FILE_I = os.path.join(HERE, 'data', 'cablenet.json')

cablenet = Cablenet.from_json(FILE_I)

# ==============================================================================
# Parameters
# ==============================================================================

OFFSET = 0.200

# ==============================================================================
# Make block
# ==============================================================================

# ==============================================================================
# Visualize
# ==============================================================================
