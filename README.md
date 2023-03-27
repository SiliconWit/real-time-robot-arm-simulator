# Real-Time Robot Arm Simulator

## Description:

This project aims to develop an open-source, real-time robot arm simulator inspired by the [KUKA KR 700 PA palletizing robot](https://github.com/SiliconWit/real-time-robot-arm-simulator/blob/main/KUKA-KR-700-PA.pdf). The primary focus is on educational purposes and performing simple industrial tasks, such as pick-and-place operations with a payload of approximately 0.5 kg. The robotic arm will be built using NEMA stepper motors, motor drivers, and an Atmega or STM controller. The simulator will be developed using Blender for 3D modeling, rigging, and simulation, along with Python or Rust scripting for communication and synchronization with the physical robotic arm.

The main goal of this project is to create a virtual representation of the robotic arm that accurately mirrors its real-world counterpart's behavior and allows users to visualize, interact with, and control the robotic arm through the simulator interface. This will provide a valuable open-source educational tool for understanding robotic systems, as well as a platform for testing and refining control algorithms before deploying them in real-world environments.

## The project will involve the following steps:

- *3D Modeling:* Create a detailed 3D model of the robotic arm and its components in Blender, inspired by the KUKA KR 700 PA palletizing robot, ensuring that the dimensions and characteristics accurately represent the real-world robot.

- *Rigging:* Rig the robot arm in Blender, creating a control system that corresponds to the joints and actuators of the real robot.

- *Scripting:* Develop scripts using Python or Rust within Blender to interface with the Atmega or STM controller, stepper motors, and motor drivers, enabling communication between the simulator and the physical robot.

- *Real-time Simulation:* Implement real-time simulation in Blender, using Python or Rust to synchronize the simulator's behavior with the real robot. This will involve continuously updating the simulator's position and orientation based on sensor data from the real robot.

- *User Interface:* Design a user interface within Blender that allows users to interact with and control the simulator, send commands to the physical robot, and visualize sensor data and system status.

- *Documentation and Tutorials:* Create comprehensive documentation and tutorials explaining the project's structure, components, and usage, as well as providing guidance for setting up the hardware and software required for the simulator.

***

We invite contributors to join this project and help us create an open-source, accessible, and easy-to-use robot arm simulator inspired by the KUKA KR 700 PA. Your contributions can include improvements to the 3D model, rigging, scripting, user interface, or documentation, as well as bug reports and feature suggestions. We look forward to working together to make this project a valuable resource for the robotics and education communities.

***

## Possible Unique Aspects:

While there are already existing open-source, real-time robot arm simulators, this particular project can differentiate itself from others through the following aspects:

- *Target Audience:* Designed specifically for students and educators, the simulator focuses on accessibility and ease of use.
- *Hardware Compatibility:* Compatible with NEMA stepper motors, motor drivers, and Atmega or STM controllers, it caters to various hardware setups.
- *KUKA KR 700 PA Inspiration:* By drawing inspiration from the industry-standard KUKA KR 700 PA palletizing robot, the project ensures a realistic and practical learning experience.
- *Blender Integration:* Leveraging Blender for 3D modeling, rigging, and simulation, and Python or Rust for scripting, the project benefits from Blender's powerful features and wide user community.
- *Customizability:* As an open-source project, the simulator promotes innovation and encourages contributions from the robotics community through easy modification, extension, and adaptation.

## Starter Project: 2R Pick and Place Robot Arm Simulation 

This is interactive Python-based starter project, based on https://www.siliconwit.com/robotics. This project simulates a 2-link (2R) robotic arm performing a pick and place task, providing an introduction to various robotics concepts, such as:

- Forward and Inverse Kinematics
- Robot Arm Geometry
- Quaternions in Robotics
- Animation and Visualization
- Pick and Place Task
- Trajectory Planning
- Error Handling and Limits
- Practical Applications

The simulation uses matplotlib for visualization and animation, and numpy for mathematical calculations. It covers the entire pick and place process, starting from the robot's home position, moving to the initial position, picking up the box, moving to the final position, placing the box, and returning to the home position. The simulation also displays the box's position in real-time during the animation.

Dive into this project, adjust the parameters, **improve it**, and enhance your understanding of robotics!
