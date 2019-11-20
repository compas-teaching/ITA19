# Assignments

## Module 2.1

### Project box to xy-plane

1. Create a box and transform it to a certain location.
1. Create a `Projection` (can be orthogonal, parallel or perspective) and project the box' vertices onto the xy-plane.
1. Draw the edges of the projected box corners with an `Artist` of your preference. (tip: `Mesh` will help you there...)

<div align="center"><br><img src="../images/assignment1_1.jpg" width="600" /></div>

### Build your own robot model

1. Build your own robot with a certain number n of links and n - 1 joints. 
1. Create a `Configuration` with certain values and the correct joint types.
1. Create a `RobotArtist` of your preferance (e.g. `compas_fab.ghpython` or `compas_fab.rhino`)
1. Use the artist to `update` the robot with the created configuration, such that it configures into the letter of your choice (or any other identifiable figure).

<div align="center"><br><img src="../images/assignment1_2.jpg" width="600" /></div>


## Module 2.1

1. Create a brick assembly with a single flemish bond and save into `flemish_bond.py` (check example nr. 27). Serialise your assembly into `00_flemish_bond.json`. 
1. In GhPython load the assembly from the saved json file and visualise it to check if all bricks are where they should be (use ghx file example nr. 20). 
1. Now transform the assembly a location where it is a) still within robot reach and b) not too close to the robot to avoid collisions.
1. After transformation save the assembly into `01_flemish_bond_transformed.json`
1. Create a new file `flemish_bond_planning.py` in which you create the assembly from `01_flemish_bond_transformed.json`.
1. Here create a planning scene, add floor, define/load picking_frame, etc. from settings (check example nr. 26.).
1. Iterate over all brick in the assembly and for each brick calculate pick and place paths and append brick to planning scene.
1. Save all paths in the element
1. Serialise assembly into `02_flemish_bond_planned.json`

<div align="center"><br><img src="../images/assignment2_1.jpg" width="600" /></div>