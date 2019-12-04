import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

from compas_vol.primitives import VolSphere, VolBox
from compas_vol.combinations import Union,Subtraction
from compas.geometry import Sphere, Box, Frame
from compas.rpc import Proxy

s = VolSphere(Sphere((0, 0, 0), 6))
b = VolBox(Box(Frame.worldXY(), 10, 10, 10), 1.5)
u = Union(s, b)
t = Subtraction(b, s)

p = Proxy('compas_vol.utilities')
#p.stop_server()
#p = Proxy('compas_vol.utilities')

bounds = ((-25,25,100), (-25,25,100), (-25,25,100))
vs,fs = p.get_vfs_from_tree(str(t), bounds, 1.0)

mesh = rg.Mesh()
for v1, v2, v3 in vs:
    mesh.Vertices.Add(v1, v2, v3)
for f in fs:
    if len(set(f))>2:
        mesh.Faces.AddFace(f[0], f[1], f[2])
mesh.Compact()
mesh.Normals.ComputeNormals()

a = mesh
b = [rs.CreatePoint(v1,v2,v3) for v1, v2, v3 in vs]