import pythreejs as p3js
from IPython.display import display
import numpy as np
from compas.utilities import rgb_to_hex
from compas.utilities import hex_to_rgb
from compas_fab.artists import BaseRobotArtist
from compas.geometry import Vector
from compas.geometry import quaternion_from_matrix

def material_from_color(color=None):
    if color:
        return p3js.MeshLambertMaterial(color=color)
    else:
        return p3js.MeshLambertMaterial(color='#cccccc')

def draw_mesh(mesh, color=None):
    vertices, faces = mesh.to_vertices_and_faces()
    hexcolor = rgb_to_hex(color[:3]) if color else '#cccccc'
    vertexcolors = [hexcolor] * len(vertices)
    faces = [f + [None, [vertexcolors[i] for i in f], None] for f in faces]
    geo = p3js.Geometry(vertices=vertices, faces=faces)
    geo.exec_three_obj_method('computeFaceNormals')
    return p3js.Mesh(geometry=geo, material=p3js.MeshLambertMaterial(vertexColors='VertexColors'), position=[0, 0, 0])


class RobotArtist(BaseRobotArtist):
    
    def __init__(self, robot):
        super(RobotArtist, self).__init__(robot)

    def transform(self, geometry, transformation):
        R = transformation.matrix
        m = [R[0][0], R[1][0], R[2][0], R[0][1], R[1][1], R[2][1], R[0][2], R[1][2], R[2][2]]
        qw, qx, qy, qz = quaternion_from_matrix(R)
        geometry.quaternion = [qx, qy, qz, qw]
        geometry.position = [R[0][3], R[1][3], R[2][3]]

    def draw_geometry(self, mesh, color=None):
        vertices, faces = mesh.to_vertices_and_faces()
        hexcolor = rgb_to_hex(color[:3]) if color else '#cccccc'
        vertexcolors = [hexcolor] * len(vertices)
        faces = [f + [None, [vertexcolors[i] for i in f], None] for f in faces]
        geo = p3js.Geometry(vertices=vertices, faces=faces)
        geo.exec_three_obj_method('computeFaceNormals')
        return p3js.Mesh(geometry=geo, material=p3js.MeshLambertMaterial(vertexColors='VertexColors'), position=[0, 0, 0])
    
    def _apply_transformation_on_transformed_link(self, item, transformation):
        # We transform absolute, so we need to calculate transformation + init 
        absolute_transformation = transformation * item.init_transformation
        self.transform(item.native_geometry, absolute_transformation)
        item.current_transformation = transformation

class ThreeJsViewer(object):
    
    def __init__(self, width=600, height=400):
        light = p3js.DirectionalLight(color='#ffffff', position=[0, 0, 1], intensity=0.5)
        self.camera = p3js.PerspectiveCamera(position=[0, 0, 1], fov=50, children=[light])
        self.width = 600
        self.height = 400
        self.geometry = []
    
    def camera_autozoom(self, camera, objects, offset=1.25, controls=None):
        boundingBox = p3js.Box3()
        """
        boundingBox.setFromObject(object)
        center = boundingBox.getCenter()
        size = boundingBox.getSize()
        
        maxDim = Math.max( size.x, size.y, size.z )
        fov = camera.fov * ( Math.PI / 180 );
        let cameraZ = Math.abs( maxDim / 4 * Math.tan( fov * 2 ) );
        cameraZ *= offset; // zoom out a little so that objects don't fill the screen
        camera.position.z = cameraZ;
        const minZ = boundingBox.min.z;
        const cameraToFarEdge = ( minZ < 0 ) ? -minZ + cameraZ : cameraZ - minZ;
        camera.far = cameraToFarEdge * 3
        camera.updateProjectionMatrix()

        if controls:
          controls.target = center
          controls.maxDistance = cameraToFarEdge * 2
          controls.saveState()
        else:
            camera.lookAt(center)
        """
   
    def show(self):





        children = [p3js.AmbientLight(color='#dddddd'), self.camera]
        children += list(self.geometry)

        axesHelper = p3js.AxesHelper()
        #axesHelper.geometry.rotateX(-3.14159/2.0)
        gridHelper = p3js.GridHelper(10, 10)
        
        scene = p3js.Scene(children=children, background="#aaaaaa")
        scene.add(axesHelper)
        scene.add(gridHelper)
        renderer = p3js.Renderer(scene=scene, camera=self.camera, 
                                 controls=[p3js.OrbitControls(controlling=self.camera)],
                                 width=self.width, height=self.height)
        display(renderer)
    

    def draw_box(self, box, color=None):
        geo = p3js.BoxBufferGeometry(width=box.xsize, 
                                     height=box.zsize, 
                                     depth=box.ysize,
                                     widthSegments=box.xsize, 
                                     heightSegments=box.zsize,
                                     depthSegments=box.ysize)
        mat = material_from_color(color)
        mesh = p3js.Mesh(geometry=geo, material=mat)
        mesh.position = list(box.frame.point + Vector(box.xsize/2, box.ysize/2, box.zsize/2))
        mesh.quaternion = box.frame.quaternion.xyzw
        self.geometry.append(mesh)

    def draw_mesh(self, mesh, color=None, id=None):
        if color == None:
            color = 0x777777
        if id == None:
            id = str(uuid.uuid1())
        geo = mesh2mcg(mesh)
        mat = mcg.MeshLambertMaterial(color=color)
        viewer[id].set_object(mcg.Mesh(geo, mat))

    def draw_line(self, line, color, line_width=1):
        positions = [[list(line[0]), list(line[1])]]
        colors = [[color, color]]
        g = p3js.LineSegmentsGeometry(positions=positions, colors=colors)
        m = p3js.LineMaterial(linewidth=line_width, vertexColors='VertexColors')
        self.geometry.append(p3js.LineSegments2(g, m))
    
    def draw_lines(self, lines, colors, line_width=1):
        positions = np.array(lines)
        colors = [[colors[i], colors[i]] for i, line in enumerate(lines)]
        g = p3js.LineSegmentsGeometry(positions=positions, colors=colors)
        m = p3js.LineMaterial(linewidth=line_width, vertexColors='VertexColors')
        self.geometry.append(p3js.LineSegments2(g, m))
    
    def draw_frame(self, frame, size=1, line_width=1):
        lines = [[frame.point, frame.point + frame.xaxis * size],
                 [frame.point, frame.point + frame.yaxis * size],
                 [frame.point, frame.point + frame.zaxis * size]]
        colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.draw_lines(lines, colors, line_width=line_width)
        #self.draw_line([frame.point, frame.point + frame.xaxis * size], [1, 0, 0], line_width=line_width)
        #self.draw_line([frame.point, frame.point + frame.yaxis * size], [0, 1, 0], line_width=line_width)
        #self.draw_line([frame.point, frame.point + frame.zaxis * size], [0, 0, 1], line_width=line_width)

    def draw_sphere(self, sphere, color=None, id=None):
        import meshcat.transformations as tf
        if color == None:
            color = 0x777777
        if id == None:
            id = str(uuid.uuid1())
        s = mcg.Sphere(sphere.radius)
        viewer[id].set_object(s), mcg.MeshLambertMaterial(color=color)
        viewer[id].set_transform(tf.translation_matrix(list(sphere.point)))
        return id


    def draw_mesh_edges(self, mesh, color=None, id=None):
        keys = list(mesh.edges())
        lines = []
        for u, v in keys:
            lines.append({
                'start': mesh.vertex_coordinates(u),
                'end'  : mesh.vertex_coordinates(v),
            })
        viewer_draw_lines(viewer, lines, color, id)