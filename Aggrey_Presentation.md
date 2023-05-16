# Project Name: 3R ROBOT ARM SIMULATOR DEVELOPMENT IN BLENDER

## Contents
1. **Preamble**
      - Objectives
2. **3D Modelling**
3. **Rigging and  Joint Constraints**
4. **Scripting**
5. **Simulation**
7. **Future Works**

# Preamble
This project aims to develop an open-source, real-time robot arm simulator inspired by the design of the KUKA KR 700 PA palletizing robot. 

![3D Model](https://github.com/MagnumGreya/Presentation_Files/blob/main/Kuka.png?raw=true)
 
## Objectives
- #### 3D Modeling:
  Create a detailed 3D model of the robotic arm and its components in Blender, inspired by the KUKA KR 700 PA palletizing robot.

- #### Rigging: 
  Rig the robot arm in Blender, creating a control system that corresponds to the joints and actuators of the real robot.

- #### Scripting: 
  Develop scripts using Python.



# Methodology
 ## The project involved the following steps
 - *3D Modeling:* 
 
   Involved creating a detailed 3D model of the robotic arm and its components using SolidWorks Software(version 2023) while ensuring that the dimensions of each component acurately represent the real world components. The CAD design was then imported into Blender (version 3.4.1) using third party software i.e Onshape software

   ![3D Model](https://github.com/MagnumGreya/Presentation_Files/blob/main/Solidwworks.jpg?raw=true)    ![3D Model](https://github.com/MagnumGreya/Presentation_Files/blob/main/Blender1.png?raw=true)

- *Rigging:* 

  It is the process of creating a digital skeleton for a 3D model that can be animated. Inverse Kinematics: Control a chain of bones by specifying the end points target

  ![3D Model](https://github.com/MagnumGreya/Presentation_Files/blob/main/Rig.png?raw=true) ![3D Model](https://github.com/MagnumGreya/Presentation_Files/blob/main/Joint_constraints.png?raw=true)



- *Scripting:* 

  A Script to automatically insert keyframes for automated rendering was developed using blender-python

  ![3D Model](https://github.com/MagnumGreya/Presentation_Files/blob/main/Script.png?raw=true)


- *Simulation:* 

  A simulation of the robot's motion following a prespecified profile

  ![Visualization](https://github.com/MagnumGreya/Presentation_Files/blob/main/ezgif.com-gif-maker.gif?raw=true)

# Future Developments

- *User Interface Design:* 

  Design a user interface within Blender that allows users to interact with and control the simulator, send commands to the physical robot, and visualize sensor data and system status.

- Documenting the Project 

  Create comprehensive documentation and tutorials explaining the project's structure, components, and usage, as well as providing guidance for setting up the hardware and software required for the simulator.



