import pythreejs as p3js
from IPython.display import display
import numpy as np
from compas.utilities import rgb_to_hex
from compas.utilities import hex_to_rgb
from compas_fab.artists import BaseRobotArtist
from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import quaternion_from_matrix
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import Transformation
from compas.utilities import flatten
from compas.datastructures import mesh_quads_to_triangles
import compas

def material_from_color(color=None):
    if color:
        return p3js.MeshLambertMaterial(color=color)
    else:
        return p3js.MeshLambertMaterial(color='#cccccc')

def draw_mesh(mesh, hexcolor):
    mesh_quads_to_triangles(mesh)
    vertices, faces = mesh.to_vertices_and_faces()
    vertexcolors = [hexcolor] * len(vertices)
    faces = [f + [None, [vertexcolors[i] for i in f], None] for f in faces]
    geo = p3js.Geometry(vertices=vertices, faces=faces)
    geo.exec_three_obj_method('computeFaceNormals')
    return p3js.Mesh(geometry=geo, material=p3js.MeshLambertMaterial(vertexColors='VertexColors'), position=[0, 0, 0])

def draw_sphere(sphere, color=None, segments=32):
    geo = p3js.SphereBufferGeometry(sphere.radius, segments, segments)
    mat = material_from_color(color)
    mesh = p3js.Mesh(geometry=geo, material=mat)
    mesh.position = list(sphere.point)
    return mesh

def draw_cylinder(cylinder, color=None, radius_segments=8):
    geo = p3js.CylinderBufferGeometry(radiusTop=cylinder.circle.radius, 
                                      radiusBottom=cylinder.circle.radius, 
                                      height=cylinder.height, 
                                      radiusSegments=radius_segments)
    mat = material_from_color(color)
    mesh = p3js.Mesh(geometry=geo, material=mat)
    mesh.position = list(cylinder.circle.plane.point)
    mesh.quaternion = list(Frame.from_plane(cylinder.circle.plane).quaternion.xyzw)
    return mesh


class RobotArtist(BaseRobotArtist):
    
    def transform(self, geometry, transformation):
        R = transformation.matrix
        m = [R[0][0], R[1][0], R[2][0], R[0][1], R[1][1], R[2][1], R[0][2], R[1][2], R[2][2]]
        qw, qx, qy, qz = quaternion_from_matrix(R)
        geometry.quaternion = [qx, qy, qz, qw]
        geometry.position = [R[0][3], R[1][3], R[2][3]]

    def draw_geometry(self, geometry, name=None, color=None):
        if not color:
            color = '#cccccc'
        else:
            color = rgb_to_hex(255 * color[0], 255 * color[1], 255 * color[2])
        if type(geometry) == compas.datastructures.Mesh:
            return draw_mesh(geometry, color)
        elif type(geometry) ==  compas.geometry.Sphere:
            return draw_sphere(geometry, color)
        elif type(geometry) ==  compas.geometry.Cylinder:
            return draw_cylinder(geometry, color)
        else:
            raise NotImplementedError

    def _apply_transformation_on_transformed_link(self, item, transformation):
        # We transform absolute, so we need to calculate transformation + init 
        absolute_transformation = transformation * item.init_transformation
        for geo in item.native_geometry:
            self.transform(geo, absolute_transformation)
        item.current_transformation = transformation

class ThreeJsViewer(object):
    
    def __init__(self, width=600, height=400):
        light = p3js.DirectionalLight(color='#ffffff', position=[0, 0, 1], intensity=0.5)
        self.camera = p3js.PerspectiveCamera(position=[2.0, 5.0, 2.0], fov=50, children=[light], aspect=width/float(height))
        self.camera.up = (0.0, 0.0, 1.0)

        self.width = 600
        self.height = 400
        self.geometry = []
        self.draw_axes(size=1)
    
       
    def show(self, camera_position=[2.0, 5.0, 2.0], action=None, geometry=None):

        self.camera.position = camera_position

        children = [p3js.AmbientLight(color='#dddddd'), self.camera]
        children += list(self.geometry)
        if geometry:
            children += geometry

        scene = p3js.Scene(children=children, background="#aaaaaa")

        #gridHelper = p3js.GridHelper(10, 10)
        #scene.add(gridHelper)
        #axesHelper = p3js.AxesHelper(1)
        #axesHelper.exec_three_obj_method('geometry.rotateX', -3.14159 / 2.0)
        #scene.add(axesHelper)

        controls = p3js.OrbitControls(controlling=self.camera)
        controls.target = (2.0, 1.0, -2.0)

        renderer = p3js.Renderer(scene=scene, camera=self.camera, 
                                 controls=[controls],
                                 width=self.width, height=self.height)
        if not action:
            display(renderer)
        else:
            display(renderer, action)
    
    def create_action(self, obj, transformations, times):
        if len(transformations) != len(times):
            raise ValueError("Pass equal amount of transformations and times")
        x, y, z, w = obj.quaternion
        Tinit = Rotation.from_quaternion([w, x, y, z]) * Translation(obj.position)
        positions = []
        quaternions = []
        for M in transformations:
            Sc, Sh, R, T, P = (M * Tinit).decomposed()
            positions.append(list(T.translation))
            quaternions.append(R.quaternion.xyzw)
        position_track = p3js.VectorKeyframeTrack(name='.position', times=times, values=list(flatten(positions)))
        rotation_track = p3js.QuaternionKeyframeTrack(name='.quaternion', times=times, values=list(flatten(quaternions)))
        obj_clip = p3js.AnimationClip(tracks=[position_track, rotation_track])
        obj_action = p3js.AnimationAction(p3js.AnimationMixer(obj), obj_clip, obj)
        return obj_action
    
    def create_group_action(self, objs, transformations, times):
        # TODO: how to start multiple animations at once
        if len(transformations) != len(times):
            raise ValueError("Pass equal amount of transformations and times")
        x, y, z, w = objs[0].quaternion
        Tinit = Rotation.from_quaternion([w, x, y, z]) * Translation(objs[0].position)
        positions = []
        quaternions = []
        for M in transformations:
            Sc, Sh, R, T, P = (M * Tinit).decomposed()
            positions.append(list(T.translation))
            quaternions.append(R.quaternion.xyzw)
        position_track = p3js.VectorKeyframeTrack(name='.position', times=times, values=list(flatten(positions)))
        rotation_track = p3js.QuaternionKeyframeTrack(name='.quaternion', times=times, values=list(flatten(quaternions)))

        animation_group = p3js.AnimationObjectGroup()
        animation_group.exec_three_obj_method('add', objs[0]) # this is not working

        obj_clip = p3js.AnimationClip(tracks=[position_track, rotation_track])
        mixer = p3js.AnimationMixer(animation_group)
        obj_action = p3js.AnimationAction(mixer, obj_clip, animation_group)
        return obj_action

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
        Sc, Sh, R, T, P = (Transformation.from_frame(box.frame) * Tinit).decomposed()
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