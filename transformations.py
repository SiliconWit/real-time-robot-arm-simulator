import math
from mathutils import Vector, Matrix
from typing import Tuple
import random
from blender_utils import get_world_trans
Axes = {
    "X":{
        "id"  :0,
        "vec" : (1,0,0)
    },
    "Y":{
        "id"  : 1,
        "vec" : (0,1,0)
    },
    "Z":{
        "id"  :2,
        "vec" : (0,0,1)
    }
}

class Plane:
    def __init__(self, pt1:Vector, pt2:Vector, pt3:Vector) -> Tuple[Vector, Vector]:
        edge_1 = pt2 - pt1
        edge_2 = pt3 - pt1
        normal = edge_1.cross(edge_2).normalized()
        self.point = pt1
        self.normal = normal
        return (normal, pt1)


# Define the lambda functions for cosine and sine
C = lambda angle: math.cos(math.radians(angle))
S = lambda angle: math.sin(math.radians(angle))

# Define the rotation matrix functions
def rotation_matrix_x(angle_degrees):
    angle = angle_degrees
    return Matrix([
        [1, 0, 0, 0],
        [0, C(angle), -S(angle), 0],
        [0, S(angle), C(angle), 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(angle_degrees):
    angle = angle_degrees
    return Matrix([
        [C(angle), 0, S(angle), 0],
        [0, 1, 0, 0],
        [-S(angle), 0, C(angle), 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_z(angle_degrees):
    angle = angle_degrees
    return Matrix([
        [C(angle), -S(angle), 0, 0],
        [S(angle), C(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


'''
Finds the angular difference between 2 objects about an axis 
with respect to local coordinates
'''
def angle_diff_r(target, source, axis ):
    sourceN = source.location.normalized()
    targetN = target.location.normalized() 
    diff = targetN - (sourceN - Vector((0,0,0)))
    
    if axis == 0:
        rads = math.atan2( diff[2], diff[1] )
    elif axis == 1:
        rads = math.atan2( diff[2], diff[0] )
    elif axis == 2:
        rads = math.atan2( diff[1], diff[0] )
    else:
        rads = 0
    
    return rads,  math.degrees(rads) 

'''
Finds the angular difference between 2 objects about an axis 
with respect to world coordinates
'''
def angle_diff_a(target, source, axis ):
    sourceN = source.matrix_world.to_translation()
    targetN = target.matrix_world.to_translation()
    diff = (targetN - (sourceN - Vector((0,0,0))))
    
    if axis == 0:
        rads = math.atan2( diff[2], diff[1] )
    elif axis == 1:
        rads = math.atan2( diff[2], diff[0] )
    elif axis == 2:
        rads = math.atan2( diff[1], diff[0] )
    else:
        rads = 0
    
    return math.degrees(rads) 

def angle_diff(origin, start_obj, end_obj, plane):
   pass

def set_global_position(obj, new_position):
    # Get the object's current matrix_world
    current_matrix = obj.matrix_world

    # Create a new translation matrix from the desired new_position
    translation_matrix = Matrix.Translation(new_position)

    # Extract the current object's rotation and scale
    _, rotation, scale = current_matrix.decompose()

    # Create new rotation and scale matrices
    rotation_matrix = rotation.to_matrix().to_4x4()
    scale_matrix = Matrix.Diagonal(scale.to_4d()).to_4x4()

    # Calculate the new matrix_world by combining the new translation, rotation, and scale matrices
    obj.matrix_world = translation_matrix @ rotation_matrix @ scale_matrix

def rotate_to( obj, axis, angle ):
    axis_c = axis.upper()
    if(axis_c == 'X'):
        rotation_matrix = rotation_matrix_x(angle)
    elif(axis_c == 'Y'):
        rotation_matrix = rotation_matrix_y(angle)
    elif(axis_c == 'Z'):
        rotation_matrix = rotation_matrix_z(angle)
    else:
        rotation_matrix = rotation_matrix_x(angle)
    
    # Get the rotation Matrix
    rotTrans = obj.matrix_world @ rotation_matrix
    obj.rotation_euler = rotTrans.to_euler()
    return rotTrans.to_euler()

def rotate_object_local_axis(obj, axis, angle_degrees):
    """
    Rotate an object about one of its local axes by a specified angle.

    Args:
        obj (bpy.types.Object): The object to be rotated.
        axis (str): The local axis to rotate around. Valid values are 'X', 'Y', or 'Z'.
        angle_degrees (float): The angle of rotation in degrees.
    """
    # Check if the input axis is valid
    if axis not in {'X', 'Y', 'Z'}:
        raise ValueError("Invalid axis. Valid values are 'X', 'Y', or 'Z'.")

    # Create the rotation matrix
    angle_radians = math.radians(angle_degrees)
    if axis == 'X':
        rotation_matrix = Matrix.Rotation(angle_radians, 4, 'X')
    elif axis == 'Y':
        rotation_matrix = Matrix.Rotation(angle_radians, 4, 'Y')
    else:
        rotation_matrix = Matrix.Rotation(angle_radians, 4, 'Z')

    # Apply the rotation to the object
    obj.matrix_world = obj.matrix_world @ obj.matrix_world.to_3x3().to_4x4().inverted() @ rotation_matrix @ obj.matrix_world.to_3x3().to_4x4()
    # rot_trans = obj.matrix_world @ obj.matrix_world.to_3x3().to_4x4().inverted() @ rotation_matrix @ obj.matrix_world.to_3x3().to_4x4()
    # return tor

def project_object( obj, ref, static_axis ):
    rand = lambda : random.random()
    # Create a virtual plane using 3 points 
    point_1 = Vector((rand(), rand(), get_world_trans(ref)[static_axis]))
    point_2 = Vector((rand(), rand(), get_world_trans(ref)[static_axis]))
    point_3 = Vector((rand(), rand(), get_world_trans(ref)[static_axis]))
    
    # Calculate the normal vector of the plane
    edge_1 = point_2 - point_1
    edge_2 = point_3 - point_1
    normal = edge_1.cross(edge_2).normalized()
    
    # Calculate Projection
    dist = ( get_world_trans(obj) - point_1).dot(normal)
    projected_position = get_world_trans(obj) - (dist * normal)
    
    return projected_position
