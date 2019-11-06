from compas.datastructures import Mesh
import meshcat
import meshcat.geometry as mcg
import uuid
import numpy as np
from meshcat import Visualizer
from meshcat.animation import Animation
import pymesh
import os

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
    return ["%s_%d" % (id, i) for i, line in enumerate(lines)]

def viewer_draw_sphere(viewer, sphere, color=None, id=None):
    import meshcat.transformations as tf
    if color == None:
        color = 0x777777
    if id == None:
        id = str(uuid.uuid1())
    s = mcg.Sphere(sphere.radius)
    viewer[id].set_object(s), mcg.MeshLambertMaterial(color=color)
    viewer[id].set_transform(tf.translation_matrix(list(sphere.point)))
    return id

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
    return ['%s_xaxis' % id, '%s_yaxis' % id, '%s_zaxis' % id]


class MeshCatViewer(Visualizer):

    def draw_mesh(self, mesh, color=None, id=None):
        return viewer_draw_mesh(self, mesh, color, id)

    def draw_mesh_edges(self, mesh, color=None, id=None):
        return viewer_draw_mesh_edges(self, mesh, color, id)
    
    def draw_box(self, box, color=None, id=None):
        return viewer_draw_box(self, box, color, id)
    
    def draw_frame(self, frame, id=None):
        return viewer_draw_frame(self, frame, id)
    
    def draw_sphere(self, sphere, color=None, id=None):
        return viewer_draw_sphere(self, sphere, id)

