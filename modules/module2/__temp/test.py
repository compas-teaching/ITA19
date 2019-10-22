import numpy
from numpy import cross
from numpy import array
from numpy import multiply
from numpy import empty
from numpy import allclose


def crossproduct(a, b):
    # a = [[x, y, z], [x, y, z], [x, y, z], ...]
    # b = [[x, y, z], [x, y, z], [x, y, z], ...]
    ax = a[:, 0]
    ay = a[:, 1]
    az = a[:, 2]
    bx = b[:, 0]
    by = b[:, 1]
    bz = b[:, 2]
    # output
    c  = empty(a.shape, a.dtype) 
    cx = c[:, 0]
    cy = c[:, 1]
    cz = c[:, 2]
    # (xyz)xy
    multiply(ax, by, out=cz)
    cz -= multiply(ay, bx)
    # x(yzx)y
    multiply(ay, bz, out=cx)
    cx -= multiply(az, by)
    # xy(zxy)
    multiply(az, bx, out=cy)
    cy -= multiply(ax, bz)
    return c


a = array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
b = array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)

c1 = cross(a, b)
c2 = crossproduct(a, b)

print(c1)
print(c2)

print(allclose(c1, c2))
