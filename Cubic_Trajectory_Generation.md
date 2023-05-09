# Cubic Trajectory Generation


# Introduction
Trajectory planning involves finding a feasible path for an object to move from an initial state to a desired end state while satisfying constraints and optimizing certain criteria. It is important in robotics, aerospace engineering, autonomous vehicles, and computer graphics for efficient and safe movement of objects.

 ## 1. Methodology
 - Designing the robot in Blender.
 - Use bones to link the Links together using parent child relationship.
 - Implement inverse kinematics using blender constraints.
 - Implement cubic trajectory generation
 - Use frames in blender to animate the robot
## 2. Robot Design Blender
Blender was used in modelling the 3D arm representation of the KUKA
Robot. From KUKA Robot design [Kuka Robot](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.mtwmag.com%2Findustrial-robots-kuka-robotics-india%2F&psig=AOvVaw0DEvxb9Kx2vWlujEhh7bzR&ust=1683718427487000&source=images&cd=vfe&ved=2ahUKEwiolrmHkuj-AhUTmicCHXMVCc0Qr4kDegUIARDsAQ), it is observed that 
3 DOF is used for positioning the end effector.
Using the same concept, simple 
Links was drawn in blender to represent the robot 


## 3. Linking the Links Using Bones
Using bone feature, the links were joined together.
Parent child relationship was used to join them together. In Blender, the term "parent-child relationship" refers to a way of linking two objects together, where one object becomes the "parent" of the other. This means that the child object is connected to and influenced by the parent object, and any changes made to the parent object will affect the child object.

## 4. Implementing Inverse Kinematics in blender
-The first step was to create a rig. This is done using the interconnected bones. 
After setting up the rig, inverse kinematics can be implemented automatically in blender in pose mode.

## 5. Cubic Trajectory Generation
Trajectory planning is the process of generating
 optimal path for robotic arm, AGV or drones 
to follow in order to achieve a desired goal.
Cubic trajectory planning involve using 3rd order 
Polynomial in interpolating the trajectory. The polynomial
Is of the form:

    $x(t)=a0+a1*t+a2*t**2+a3*t**3$

### Sample code for Cubic Trajectory Generation
`#Trajectory Planning using cubic polynomial`

    def cubic_coefficients(q0, qf, t0, tf):
        a0 = q0
        a1 = 0
        a2 = (3 * (qf - q0) / ((tf - t0) ** 2))
        a3 = (-2 * (qf - q0) / ((tf - t0) ** 3))
        return a0, a1, a2, a3

    def cubic_trajectory(t, a0, a1, a2, a3):
        return a0 + a1 * t + a2 * t**2 + a3 * t**3

## 6. Animating the motion of the Robot
Animation was done using the frames in Blender. 
At each frame, the trajectory is computed using the equation for cubic polynomial.
At each frame, the position of the end effector is at different position according to the equation.
### Sample Code For Trajectory Generation at Each Frame
    `#A loop to generate position eqaul to the number of frames`
        t = np.linspace(start_frame-1,last_frame,180)
        for i in t:
        t0 = start_frame
        tf = last_frame
        tframe += start_frame
        End_eff_home = (3,-2,-2)
        End_eff_final = (3,4,2)
        #X coordinates for the trajectory
        q0_xi, q0_xf = End_eff_home[0], End_eff_final[0]
        x0,x1,x2,x3 = cubic_coefficients(q0_xi,q0_xf,t0,tf)
        x_traj= cubic_trajectory(tframe,x0,x1,x2,x3)
        
        #y coordinates for the trajectory
        q0_yi, q0_yf = End_eff_home[1], End_eff_final[1]
        y0,y1,y2,y3 = cubic_coefficients(q0_yi,q0_yf,t0,tf)
        y_traj= cubic_trajectory(tframe,y0,y1,y2,y3)
        
        #z coordinates for the trajectory
        q0_zi, q0_zf = End_eff_home[2], End_eff_final[2]
        z0,z1,z2,z3 = cubic_coefficients(q0_zi,q0_zf,t0,tf)
        z_traj= cubic_trajectory(tframe,z0,z1,z2,z3)
        

        End_eff.keyframe_insert("location", frame = i)
        #line.keyframe_insert("location", frame = i)

        End_eff.location = (x_traj,y_traj,z_traj)
        line.location = (x_traj,y_traj,z_traj)

        End_eff.keyframe_insert("location", frame = last_frame)

## 7. Conclusion
Trajectory planning is a critical aspect of robotics and automation, as it enables machines to perform complex tasks in a variety of environments. Examples of trajectory planning applications include robotic welding, pick-and-place operations, and autonomous navigation.
