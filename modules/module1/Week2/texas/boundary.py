import os
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import FrameArtist
from compas_rhino.artists import PointArtist
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Box
from compas.geometry import Transformation
from compas.geometry import transform_points
from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors
from compas.geometry import bounding_box_xy
from compas.geometry import offset_polygon
from compas.geometry import intersection_line_plane

# ==============================================================================
# Create a proxy for PCA
# ==============================================================================

from compas.rpc import Proxy

# ==============================================================================
# Construct a cablenet
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'cablenet.json')

cablenet = Cablenet.from_json(FILE_I)

# ==============================================================================
# Parameters
# ==============================================================================

OFFSET = 0.200
PADDING = 0.020

# ==============================================================================
# Vertices on SOUTH
# ==============================================================================

# ==============================================================================
# Boundary plane
# ==============================================================================

# ==============================================================================
# Intersections
# ==============================================================================

# ==============================================================================
# Bounding boxes
# ==============================================================================

# ==============================================================================
# Visualization
# ==============================================================================
