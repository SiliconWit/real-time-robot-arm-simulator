import math
from mathutils import Vector, Matrix
from typing import Tuple, Union
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
    '''
    Projects a Blender Object onto a given plane
    Args:
        obj (bpy.type.Object) : Object to Project
        ref (bpy.type.Object) : Object that is a reference for the plane
        static_axis (int) : Local axis of ref normal to the plane
    Return: 
        (Vector) : A projection of obj 
    '''
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

def get_angle(ref_point:Vector, from_point:Vector, to_point:Vector, axis=1) -> Union[float, float]:
    '''
        Gives the angle between 2 vectors
        Utilises Vector properties
        Args:
            ref_point (Vector): A common reference point for the 2 vectors
            from_point (Vector): Start Vector
            to_point (Vector): End Vector
        Returns:
            float: Angle In Radians
            float: Angle In Degrees
    '''
    a = from_point -  ref_point 
    b = to_point - ref_point
    angle_sign = 1 if a.cross(b)[axis] >= 0 else -1
    clipped_cos_angle = max(min(a.dot(b)/( a.length * b.length ), 1), -1) 
    _angle = math.acos( clipped_cos_angle ) * angle_sign
    
    return _angle, math.degrees(_angle)