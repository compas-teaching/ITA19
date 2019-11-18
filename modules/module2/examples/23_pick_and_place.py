import os
import sys
from compas.geometry import Vector
from compas.geometry import Frame
from compas.datastructures import Mesh
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import Configuration

from assembly import Assembly

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
ASSEMBLY_PATH = os.path.abspath(os.path.join(HERE, ".."))
sys.path.append(ASSEMBLY_PATH)

# define end-effector mesh and frame
ee_mesh = Mesh.from_stl(os.path.join(DATA, "vacuum_gripper.stl"))
ee_frame = Frame([0.07, 0, 0], [0, 0, 1], [0, 1, 0])

# define picking frame and configuration
picking_frame = Frame([-0.43, 0, 0], [1, 0, 0], [0, 1, 0])
picking_configuration = Configuration.from_revolute_values([-5.961, 4.407, -2.265, 5.712, 1.571, -2.820])

save_vector = Vector(0, 0, 0.05)
picking_frame_savelevel = picking_frame.copy()
picking_frame_savelevel.point += save_vector


# load assembly
assembly = Assembly.from_json(PATH_FROM)

with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)
    tool_acm = robot.set_end_effector(ee_mesh, ee_frame)





    # Iterate over the keys in the assembly
    for key in sequence:

        start_configuration = picking_configuration

        # Read the placing frame from brick, zaxis down
        o, uvw = assembly_block_placing_frame(assembly, key)
        placing_frame = Frame(o, uvw[1], uvw[0])

        # Calculate saveframe at placing frame
        saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

        # Check ik for placing_frame and saveframe_place
        # Only if both work, save to assembly
        try:
            response = robot.inverse_kinematics(frame_WCF=saveframe_place,
                                                start_configuration=start_configuration,
                                                group=group,
                                                constraints=None,
                                                attempts=20)
            start_configuration = response.configuration
            try:
                response = robot.inverse_kinematics(frame_WCF=placing_frame,
                                                    start_configuration=start_configuration,
                                                    group=group,
                                                    constraints=None,
                                                    attempts=20)
                start_configuration = response.configuration
                print("Brick with key %d is buildable" % key)
                # Update attribute
                assembly.set_vertex_attribute(key, 'is_buildable', True)

            except RosError as error:
                print("Brick with key %d is NOT buildable" % key, error)
        except RosError as error:
            print("Brick with key %d is NOT buildable" % key, error)

assembly.to_json(PATH_TO)

robot.client.close()
robot.client.terminate()