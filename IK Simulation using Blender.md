<a name="br1"></a>**FABRIK Simulationusing Blender**

Andrew Kibor - E222-01-0431/2022




<a name="br2"></a>**Inverse Kinematics**

➔ A Computational Problem for an

articulated structure. ➔ Input is a desired pose.

➔ Joint angles or parameters of the

structure are to be determined

➔ Pose : position and orientation of

||target||Credit: [root-motion](http://www.root-motion.com/finalikdox/html/page6.html)|
| :- | :- | :- | :- |




<a name="br3"></a>**IK Solver Algorithms**

Cyclic Coordinate Descent Jacobian-based methods FABRIK

Credit: [BMC](https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2F1471-2105-6-159/MediaObjects/12859_2005_Article_484_Fig1_HTML.jpg)[ ](https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2F1471-2105-6-159/MediaObjects/12859_2005_Article_484_Fig1_HTML.jpg)[Bioinformatics](https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2F1471-2105-6-159/MediaObjects/12859_2005_Article_484_Fig1_HTML.jpg)

Credit: [Hindawi](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.hindawi.com%2Fjournals%2Fjr%2F2021%2F5568702%2F&psig=AOvVaw3Z-cPaVtlp9cyU9n9XPjp_&ust=1683617659043000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCJDjz9ea5f4CFQAAAAAdAAAAABAE)




<a name="br4"></a>**The FABRIK Solver**

➔ Acronym for Forward And Backward Reaching Inverse Kinematics

➔ Goal: Minimise distance between target and end-effector -

Heuristic

➔ Joint positions are adjusted iteratively towards a convergence.

➔ Computationally efficient; uses vectors

➔ Versatile in its applications




<a name="br5"></a>**FABRIK Solver: Forward & Backwardprocedures**

Credit: <https://doi.org/10.1063/1.4983058>




<a name="br6"></a>**Building a 3 DOF robot**

➔ Based on Blender and Blender-

Python API.

➔ The Build: 3 links(Base, Link1 and

Link2), End-Effector and Target

➔ Primitive shapes for all build

component

➔ All revolute joints.

➔ Spawned on the click of a button




<a name="br7"></a>**Logic of Execution & Demo**

||<p>Create UI</p><p>` `Panel</p>||Run fabrik()|
| :- | :- | :- | :- |
||<p>Spawn</p><p>Robot Arm</p>||<p>Calculate</p><p>` `Angles</p>|
|<p>Get</p><p>References</p>||<p>Transform</p><p>` `Robot</p>|
Iteration in the FABRIK function




<a name="br8"></a>**Challenges and Recommendations**

Some of the challenges and limitations encountered include

➔ Base rotations only work well for the 1st quadrant of the XY plane➔ Lack of Joint Representations

➔ Limited User Interactions

The following can be undertaken to improve the simulator

➔ Use of a robot 3D model➔ Perform a real world action




<a name="br9"></a>**Biggest Lesson Learnt: Vectors ꢀꢀ**

➔ Vectors are simple but powerful

➔ Creating an Imaginary plane

➔ Vector Normalisation(Orientation)

➔ Magnitude(Distance)

➔ Cross and Dot Products(Finding Angle Deltas)




<a name="br10"></a>**Vector-Based Operations**

Finding Angle between 2 Vectors Projecting a point onto a plane

|<p>def get\_angle(ref\_point:Vector, from\_point:Vector,</p><p>to\_point:Vector) -> Union[float, float]:</p><p>a = from\_point - ref\_point</p><p>b = to\_point - ref\_point</p><p>angle\_sign = 1 if a.cross(b)[1] >= 0 else -1</p><p>\_angle = acos(a.dot(b)/( a.length \* b.length )) \*</p><p>angle\_sign</p><p>return \_angle, degrees(\_angle)</p>||<p>def project\_object( obj, ref, static\_axis ):</p><p>` `rand = lambda : random.random()</p><p>` `*# Create a virtual plane using 3 points*</p><p>` `point\_1 = Vector((rand(), rand(),</p><p>get\_world\_trans(ref)[static\_axis]))</p><p>` `point\_2 = Vector((rand(), rand(),</p><p>get\_world\_trans(ref)[static\_axis]))</p><p>` `point\_3 = Vector((rand(), rand(),</p><p>get\_world\_trans(ref)[static\_axis]))</p>|
| :- | :- | :- |
*# Calculate the normal vector of the plane* edge\_1 = point\_2 - point\_1 edge\_2 = point\_3 - point\_1

normal = edge\_1.cross(edge\_2).normalized()

*# Calculate Projection*

` `dist = ( get\_world\_trans(obj) - point\_1).dot(normal) projected\_position = get\_world\_trans(obj) - (dist \*normal)

return projected\_position




<a name="br11"></a>**Thank you.**




<a name="br12"></a>**Codebase Summary**

**Scripts**

❏ **playground.cs** : Main File. Entry point.❏ **robotics\_utils.py** : Creates the 3 DOF robot arm

❏ **transformations.py**: Handles geometric

and kinematic actions

❏ **blender\_utils.py** : Calls blender-

intrinsic functions

**Instructions**

1\. Launch Blender

2\. Open playground.cs in the script editor

3\. Run the script to to create the “Robotics” panel.

4\. Click on the “Reset Scene” button to spawn

the robot

5\. Click on the “Run IK” button.
