from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas.rpc import Proxy

numerical = Proxy('compas.numerical')
fd_numpy = numerical.fd_numpy


class Shell(Mesh):

    def __init__(self):
        super(Shell, self).__init__()
        self.default_vertex_attributes.update({'is_fixed': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
        self.default_edge_attributes.update({'q': 1.0, 'f': 0.0, 'rx': 0.0, 'ry': 0.0, 'rz': 0.0})

    def fofin(self):
        xyz = self.get_vertices_attributes('xyz')
        fixed = list(self.vertices_where({'is_fixed': True}))
        loads = self.get_vertices_attributes(('px', 'py', 'pz'))
        edges = list(self.edges())
        q = self.get_edges_attribute('q')
        xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)
        for key, attr in self.vertices(True):
            attr['x'] = xyz[key][0]
            attr['y'] = xyz[key][1]
            attr['z'] = xyz[key][2]
            attr['rx'] = r[key][0]
            attr['ry'] = r[key][1]
            attr['rz'] = r[key][2]
        for index, (u, v, attr) in enumerate(self.edges(True)):
            attr['f'] = f[index][0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
