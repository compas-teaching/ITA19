from compas.datastructures import Mesh
import meshcat
import meshcat.geometry as mcg
import uuid
import numpy as np
from meshcat import Visualizer

def compas_mesh_to_obj_str(mesh):
    lines = ["g object_1"]
    v, f = mesh.to_vertices_and_faces()
    for p in v:
        lines.append("v {} {} {}".format(*p))
    for p in f:
        if len(p) == 3:
            lines.append("f {} {} {}".format(*p))
        elif len(p) == 4:
            a, b, c, d = p
            lines.append("f {} {} {} {}".format(a+1, b+1, c+1, d+1))
    return "\n".join(lines)

def mesh2mcg(mesh):
    contents = compas_mesh_to_obj_str(mesh)
    return mcg.MeshGeometry(contents, 'obj')

def viewer_draw_box(viewer, box, color=None, id=None):
    mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)
    viewer_draw_mesh(viewer, mesh, color, id)

def viewer_draw_mesh(viewer, mesh, color=None, id=None):
    if color == None:
        color = 0x777777
    if id == None:
        id = str(uuid.uuid1())
    geo = mesh2mcg(mesh)
    mat = mcg.MeshLambertMaterial(color=color)
    viewer[id].set_object(mcg.Mesh(geo, mat))

def viewer_draw_lines(viewer, lines, color=None, id=None):
    if color == None:
        color = 0x777777
    if id == None:
        id = str(uuid.uuid1())
    for i, line in enumerate(lines):
        vertices = np.array([list(line['start']), list(line['end'])]).T
        viewer["%s_%d" % (id, i)].set_object(mcg.Line(mcg.PointsGeometry(vertices), mcg.MeshBasicMaterial(color=color)))


def viewer_draw_mesh_edges(viewer, mesh, color=None, id=None):
    keys = list(mesh.edges())
    lines = []
    for u, v in keys:
        lines.append({
            'start': mesh.vertex_coordinates(u),
            'end'  : mesh.vertex_coordinates(v),
        })
    viewer_draw_lines(viewer, lines, color, id)


def viewer_draw_frame(viewer, frame, id=None):
    if id == None:
        id = str(uuid.uuid1())
    vertices = np.array([list(frame.point), list(frame.point + frame.xaxis)]).T
    viewer['%s_xaxis' % id].set_object(mcg.Line(mcg.PointsGeometry(vertices), mcg.MeshBasicMaterial(color=0xff0000)))
    vertices = np.array([list(frame.point), list(frame.point + frame.yaxis)]).T
    viewer['%s_yaxis' % id].set_object(mcg.Line(mcg.PointsGeometry(vertices), mcg.MeshBasicMaterial(color=0x00ff00)))
    vertices = np.array([list(frame.point), list(frame.point + frame.zaxis)]).T
    viewer['%s_zaxis' % id].set_object(mcg.Line(mcg.PointsGeometry(vertices), mcg.MeshBasicMaterial(color=0x0000ff)))


class MeshCatViewer(Visualizer):

    def draw_mesh(self, mesh, color=None, id=None):
        viewer_draw_mesh(self, mesh, color, id)

    def draw_mesh_edges(self, mesh, color=None, id=None):
        viewer_draw_mesh_edges(self, mesh, color, id)
    
    def draw_box(self, box, color=None, id=None):
        viewer_draw_box(self, box, color, id)
    
    def draw_frame(self, frame, id=None):
        viewer_draw_frame(self, frame, id)
    


"""
import compas
from compas.geometry import Frame
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
import pythreejs as p3js
from IPython.display import display

frame = Frame([1, 0, 0], [-0.45, 0.1, 0.3], [1, 0, 0])
width, length, height = 10, 10, 10

box = Box(frame, width, length, height)

#mesh = Mesh.from_obj(compas.get('hypar.obj'))
mesh = mesh.from_vertices_and_faces(box.vertices, box.faces)
mesh_quads_to_triangles(mesh)

v, f = mesh.to_vertices_and_faces()
# transform vertices
v_t = [frame.represent_point_in_global_coordinates(p) for p in v]

mesh_t = Mesh.from_vertices_and_faces(v_t, f)

vertices = v
faces = f

print(v)
print(f)

vertexcolors = ['#777777'] * len(vertices)
#vertexcolors = ['#000000', '#0000ff', '#00ff00', '#ff0000', '#00ffff', '#ff00ff', '#ffff00', '#ffffff']


# Map the vertex colors into the 'color' slot of the faces
faces = [f + [None, [vertexcolors[i] for i in f], None] for f in faces]

geom = p3js.Geometry(vertices=vertices, faces=faces, colors=vertexcolors)
geom.exec_three_obj_method('computeFaceNormals')

# Create a mesh. Note that the material need to be told to use the vertex colors.
m3 = p3js.Mesh(geometry=geom,
          material=p3js.MeshLambertMaterial(vertexColors='VertexColors'),
          position=[-0.5, -0.5, -0.5])

#size = 10;
#divisions = 10;
#gridHelper = p3js.GridHelper(size, divisions);
# Set up a scene and render it:
cCube = p3js.PerspectiveCamera(position=[10, 10, 10], fov=20,
                      children=[p3js.DirectionalLight(color='#ffffff', position=[-3, 5, 1], intensity=0.5)])
scene = p3js.Scene(children=[m3, cCube, p3js.AmbientLight(color='#dddddd')])


rendererCube = p3js.Renderer(camera=cCube, background='black', background_opacity=1,
                        scene=sceneCube, controls=[p3js.OrbitControls(controlling=cCube)])

display(rendererCube)
"""