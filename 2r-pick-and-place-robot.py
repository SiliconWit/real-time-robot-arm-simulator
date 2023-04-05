# Import the necessary libraries for the pick and place robot simulation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
from matplotlib import transforms

# Define the lengths of the robot arm links (L1 and L2)
L1 = 6  # Adjust link length
L2 = 6  # Adjust link length

# Link thickness
link_thickness = 0.5

# Define the initial and final coordinates of the box to be moved by the robot
x_initial, y_initial = -10, -5
x_final, y_final = 10, -5

# Define the inverse kinematics function to calculate the joint angles given the end-effector position
def inverse_kinematics(x, y, offset=0):
    # Calculate the distance from the base joint to the target position
    d = np.sqrt(x**2 + (y + offset)**2)
    
    # Calculate the angle between the two links using the law of cosines
    a = np.arccos((L1**2 + L2**2 - d**2) / (2 * L1 * L2))

    # Calculate the angle alpha2
    alpha2 = np.radians(180) - a
    
    # Calculate the angle of the first link with respect to the horizontal axis
    b = np.arctan2(y + offset, x) - np.arctan2(L2 * np.sin(alpha2), L1 + L2 * np.cos(alpha2))
    
    return b, alpha2 + b

# Define the dimensions of the box to be moved
box_width, box_height = 1, 1

# Calculate the joint angles for the robot's home position, initial position and final position
theta1_home, theta2_home = inverse_kinematics(-5, 5)
theta1_initial, theta2_initial = inverse_kinematics(x_initial, y_initial, offset=box_height/2)
theta1_final, theta2_final = inverse_kinematics(x_final, y_final, offset=box_height/2)

# Define the forward kinematics function to calculate the end-effector position given the joint angles
def forward_kinematics(theta1, theta2, offset=0):
    # Calculate the position of the first joint (x1, y1)
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    
    # Calculate the position of the second joint (x2, y2)
    x2 = x1 + L2 * np.cos(theta2)
    y2 = y1 + L2 * np.sin(theta2) - offset
    
    return x1, y1, x2, y2

# Define the create_link function to create a robot arm link with a given length, angle, and thickness
def create_link(x, y, length, angle, thickness=link_thickness, joint_shift=0):
    link = FancyBboxPatch((x + joint_shift, y - thickness/2), length - joint_shift, thickness, boxstyle="round,pad=0.01,rounding_size=0.15")
    t = transforms.Affine2D().rotate_around(x, y, angle) + ax.transData
    link.set_transform(t)
    return link

# Define a function to compute the shortest angle difference between two angles (a1 and a2)
def shortest_angle_diff(a1, a2):
    diff = a2 - a1
    return (diff + np.pi) % (2 * np.pi) - np.pi

# Define the update function for the animation of the pick and place robot simulation
def update(frame, link1, link2):
    # Update the robot arm's joint angles depending on the frame number
    # There are 6 sections in the animation: moving to initial, waiting, picking, waiting, placing, and returning to home position
    # Frame numbers are divided into 6 equal parts, each part corresponding to a different section of the animation

    # 1. Move from the home position to the initial position
    if frame < num_frames / 6:
        # Calculate the current joint angles based on the frame number
        # (interpolate between the home position and the initial position)
        t = frame / (num_frames / 6)
        theta1_diff = shortest_angle_diff(theta1_home, theta1_initial)
        theta2_diff = shortest_angle_diff(theta2_home, theta2_initial)
        theta1 = theta1_home + t * theta1_diff
        theta2 = theta2_home + t * theta2_diff
    # 2. Wait at the initial position
    elif frame < 2 * num_frames / 6:
        # Keep the joint angles constant at the initial position
        t = (frame - num_frames / 6) / (num_frames / 6)
        theta1 = theta1_initial
        theta2 = theta2_initial
    # 3. Pick up the box and move it to the final position
    elif frame < 3 * num_frames / 6:
        # Calculate the current joint angles based on the frame number
        # (interpolate between the initial position and the final position)
        t = (frame - 2 * num_frames / 6) / (num_frames / 6)
        theta1_diff = shortest_angle_diff(theta1_initial, theta1_final)
        theta2_diff = shortest_angle_diff(theta2_initial, theta2_final)
        theta1 = theta1_initial + t * theta1_diff
        theta2 = theta2_initial + t * theta2_diff
    # 4. Wait at the final position
    elif frame < 4 * num_frames / 6:
        # Keep the joint angles constant at the final position
        t = (frame - 3 * num_frames / 6) / (num_frames / 6)
        theta1 = theta1_final
        theta2 = theta2_final
    # 5. Return to the home position from the final position
    elif frame < 5 * num_frames / 6:
        # Calculate the current joint angles based on the frame number
        # (interpolate between the final position and the home position)
        t = (frame - 4 * num_frames / 6) / (num_frames / 6)
        theta1_diff = shortest_angle_diff(theta1_final, theta1_home)
        theta2_diff = shortest_angle_diff(theta2_final, theta2_home)
        theta1 = theta1_final + t * theta1_diff
        theta2 = theta2_final + t * theta2_diff
    # 6. Stay at the home position
    else:
        # Keep the joint angles constant at the home position
        theta1 = theta1_home
        theta2 = theta2_home

    # Update the positions of the links and the joint based on the current joint angles
    # (use forward kinematics to calculate the new end-effector position)
    x1, y1, x2, y2 = forward_kinematics(theta1, theta2, offset=box_height/2)
    t1 = transforms.Affine2D().rotate_around(0, 0, theta1) + ax.transData
    t2 = transforms.Affine2D().rotate_around(x1, y1, theta2) + ax.transData
    link1.set_transform(t1)
    link2.set_transform(t2)
    link2.set_x(x1)
    link2.set_y(y1 - link_thickness/2)

    # Update the joint's position
    joint.center = (x1, y1)

    # Update the position of the box and the box coordinates text based on the frame number
    # If the robot is in the process of picking up the box or placing the box, update the box position
    # Otherwise, keep the box position constant at the initial or final position
    if 2 * num_frames / 6 <= frame < 3 * num_frames / 6:
        box.set_xy((x2 - box_width / 2, y2 - box_height / 2))
        box_coordinates.set_text(f"({x2:.2f}, {y2-box_height/2:.2f})")  # subtract box_height/2 to show actual box position
    elif 5 * num_frames / 6 <= frame < num_frames:
        t = (frame - 5 * num_frames / 6) / (num_frames / 6)
        x_box = x_final + t * (x_initial - x_final)
        y_box = y_final + t * (y_initial - y_final)
        box.set_xy((x_box - box_width / 2, y_box - box_height / 2))
        box_coordinates.set_text(f"({x_box:.2f}, {y_box:.2f})")
    else:
        if frame < num_frames / 6:
            box_coordinates.set_text(f"({x_initial:.2f}, {y_initial:.2f})")
        elif frame < 2 * num_frames / 6:
            box_coordinates.set_text(f"({x_initial:.2f}, {y_initial:.2f})")
        elif frame < 5 * num_frames / 6:
            box_coordinates.set_text(f"({x_final:.2f}, {y_final:.2f})")
        else:
            box_coordinates.set_text(f"({x_initial:.2f}, {y_initial:.2f})")

    return link1, link2, box, box_coordinates, joint


# Set up the plot for the pick and place robot simulation
fig, ax = plt.subplots()
ax.set_xlim(-L1 - L2, L1 + L2)
ax.set_ylim(-L1 - L2, L1 + L2)
ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Create the robot arm links (link1 and link2) and add them to the plot
joint_shift = link_thickness / 2
link1 = create_link(0, 0, L1, theta1_home, joint_shift=joint_shift)
link2 = create_link(0, 0, L2, theta2_home, joint_shift=joint_shift)
ax.add_patch(link1)
ax.add_patch(link2)

# Create the box to be moved by the robot and add it to the plot
box = Rectangle((x_initial - box_width / 2, y_initial - box_height / 2), box_width, box_height, fc='red')
ax.add_patch(box)

# Add a fixed base plate below the base joint to represent the robot's base
base_plate_thickness = 0.5
base_plate_width = 3
base_plate = Rectangle((-base_plate_width/2, -base_plate_thickness), base_plate_width, base_plate_thickness, fc="gray")
ax.add_patch(base_plate)

# Create a circle to represent the joint connecting the two links of the robot
joint_radius = 0.3
joint = Circle((0, 0), joint_radius, facecolor="white", ec="blue", lw=2)
ax.add_patch(joint)

# Create a circle to represent the base joint of the robot
base_joint_radius = 0.3
base_joint = Circle((0, 0), base_joint_radius, facecolor="white", ec="blue", lw=2)
ax.add_patch(base_joint)

# Add the box coordinates text to display the box's position in the plot
box_coordinates = ax.text(0.05, 0.95, "", transform=ax.transAxes, verticalalignment="top")
ax.text(0.5, 0.46, 'orcid.org/0000-0002-7326-7502', transform=ax.transAxes, fontsize=8, color='gray', alpha=0.5, ha='center', va='center', rotation=0)
ax.text(0.95, 0.05, 'SiliconWit.com', transform=ax.transAxes, fontsize=10, color='gray', alpha=0.5, ha='right', va='bottom')

# Create the animation for the pick and place robot simulation
num_frames = 400
ani = FuncAnimation(fig, update, frames=num_frames, fargs=(link1, link2), interval=50, blit=True)

# Show the pick and place robot simulation
plt.show()
