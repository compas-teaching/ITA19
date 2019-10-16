import pythreejs as p3js
from IPython.display import display
import numpy as np
from compas.utilities import rgb_to_hex
from compas_fab.artists import BaseRobotArtist
from compas.geometry import quaternion_from_matrix

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
    
    def camera_autozoom(self, camera, objects, offset=1.25, controls=None):
        boundingBox = p3js.Box3()
        boundingBox.setFromObject(object)
        center = boundingBox.getCenter()
        size = boundingBox.getSize()
        """
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
   
    def show(self, geometry):
        children = [p3js.AmbientLight(color='#dddddd'), self.camera]
        children += list(geometry)
        
        scene = p3js.Scene(children=children)
        renderer = p3js.Renderer(scene=scene, camera=self.camera, 
                                 controls=[p3js.OrbitControls(controlling=self.camera)],
                                 width=self.width, height=self.height)
        display(renderer)