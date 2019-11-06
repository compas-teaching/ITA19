
class Viewer(object):
    
    def __init__(self, width=600, height=400):
        self.width = 600
        self.height = 400
        self.artists = [] # arists that know how to draw the  
    
    def show(self, **kwargs):
        raise NotImplementedError
    
    def run_animation(self, animation):
        raise NotImplementedError
    

"""
    def draw_box(self, box, color=None):
        geo = p3js.BoxBufferGeometry(width=box.xsize, 
                                     height=box.zsize, 
                                     depth=box.ysize,
                                     widthSegments=box.xsize, 
                                     heightSegments=box.zsize,
                                     depthSegments=box.ysize)
        mat = material_from_color(color)
        mesh = p3js.Mesh(geometry=geo, material=mat)
        Tinit = Translation([box.xsize/2, box.ysize/2, box.zsize/2])
        Sc, Sh, R, T, P = (Transformation.from_frame(box.frame) * Tinit).decompose()
        mesh.quaternion = R.quaternion.xyzw
        mesh.position = list(T.translation)
        self.geometry.append(mesh)
        return mesh
    
    def draw_sphere(self, sphere, color=None, segments=32):
        mesh = draw_sphere(sphere, color, segments)
        self.geometry.append(mesh)
        return mesh

    def draw_mesh(self, mesh, color=None):
        pass

    def draw_line(self, line, color, line_width=1):
        positions = [[list(line[0]), list(line[1])]]
        colors = [[color, color]]
        g = p3js.LineSegmentsGeometry(positions=positions, colors=colors)
        m = p3js.LineMaterial(linewidth=line_width, vertexColors='VertexColors')
        line = p3js.LineSegments2(g, m)
        self.geometry.append(line)
        return line


    def draw_axes(self, size=1):
        amount = 5
        lines = []
        colors = []
        for a in range(-amount*size, (amount+1)*size, size):
            lines.append([[a, amount*size, 0], [a, -amount*size, 0]])
            lines.append([[amount*size, a, 0], [-amount*size, a, 0]])
            if a == 0:
                colors += [[0.4, 0.4, 0.4], [0.4, 0.4, 0.4]]
            else:
                colors += [[0.6, 0.6, 0.6], [0.6, 0.6, 0.6]]
        self.draw_lines(lines, colors)

    
    def draw_lines(self, lines, colors, line_width=1):
        positions = np.array(lines)
        colors = [[colors[i], colors[i]] for i, line in enumerate(lines)]
        g = p3js.LineSegmentsGeometry(positions=positions, colors=colors)
        m = p3js.LineMaterial(linewidth=line_width, vertexColors='VertexColors')
        lines = p3js.LineSegments2(g, m)
        self.geometry.append(lines)
        return lines
    
    def draw_frame(self, frame, size=1, line_width=2):
        lines = [[frame.point, frame.point + frame.xaxis * size],
                 [frame.point, frame.point + frame.yaxis * size],
                 [frame.point, frame.point + frame.zaxis * size]]
        colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        return self.draw_lines(lines, colors, line_width=line_width)

    def draw_mesh_edges(self, mesh, color=None):
        keys = list(mesh.edges())
        lines = []
        for u, v in keys:
            lines.append([mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)])
        colors = [color] * len(lines)
        return self.draw_lines(lines, colors)
"""