from math import pi

from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import matrix_from_axis_and_angle
from compas.geometry import transform_points

a = [1.0, 0.0, 0.0]
b = [1.0, 0.0, 0.0]
c = cross_vectors(a, b)

axis = [0.0, 0.0, 1.0]
angle = pi * 10.0 / 180.0

R = matrix_from_axis_and_angle(axis, angle)

print("0: {:.3f}".format(length_vector(c)))
print("[{0[0]:.3f}, {0[1]:.3f}, {0[2]:.3f}]".format(c))

for i in range(18):
    b = transform_points([b], R)[0]
    c = cross_vectors(a, b)
    print("{}: {:.3f}".format((i + 1) * 10, length_vector(c)))
    print("[{0[0]:.3f}, {0[1]:.3f}, {0[2]:.3f}]".format(c))
