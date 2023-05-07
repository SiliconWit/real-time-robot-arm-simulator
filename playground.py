import bpy
from mathutils import Vector
from math import radians, degrees, acos
from typing import Union
import random

import os, sys
blend_file_dir = os.path.dirname(bpy.data.filepath)
sys.path.append(blend_file_dir)


from blender_utils import *
from transformations import *


def isReachable():
    return (tg.matrix_world.to_translation() - ee.matrix_world.to_translation()).length < (l1l+l2l)

def get_angle(ref_point:Vector, from_point:Vector, to_point:Vector) -> Union[float, float]:
    '''
        Gives the angle between 2 vectors
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
    angle_sign = 1 if a.cross(b)[1] >= 0 else -1
    _angle = acos(a.dot(b)/( a.length * b.length )) * angle_sign
    
    return _angle, degrees(_angle)

def fabrik( iterations, target, tolerance = 0.01 ):
    if ( not isReachable() ):
        return
    
    l_pos = dict()    
    l_pos["l1"] = l1.matrix_world.to_translation()
    l_pos["l2"] = l2.matrix_world.to_translation()
    l_pos["ee"] = ee.matrix_world.to_translation()
    origPos = l_pos["l1"].copy()
    n_pos = dict()
    tg_pos = get_world_trans(target)
    
    for i in range(iterations):        
        if( (l_pos["ee"]-tg_pos).length < tolerance ):
            break;
        
        # Backward Trace
        n_pos["ee"]  = Vector(tg_pos)
        n_pos["l2"] = n_pos["ee"] + ( (l_pos["l2"] - n_pos["ee"]).normalized() * l2l)
        n_pos["l1"] = n_pos["l2"] + ( (l_pos["l1"] - n_pos["l2"]).normalized() * l1l)

        # Forward Trace
        l_pos["l1"] = origPos
        l_pos["l2"] = l_pos["l1"] + ( (n_pos["l2"] - l_pos["l1"] ).normalized() * l1l)
        l_pos["ee"] = l_pos["l2"] + ( (n_pos["ee"] - l_pos["l2"] ).normalized() * l2l) 
        
    
    
    ee_offset = ee.matrix_world.to_translation() + Vector((l_pos["l2"][0],0,0))
    l1_angle, _ = get_angle( l_pos["l1"], get_world_trans(l2) , l_pos["l2"])
    
    _l2_offset = l_pos["l2"] + ((l_pos["l2"] - l_pos["l1"]).normalized() * l2l)

    l2_angle, _ = get_angle( l_pos["l2"], _l2_offset, l_pos["ee"])
    return l_pos, l1_angle, l2_angle
    
base = bpy.data.objects["Base"]
l1 = bpy.data.objects["Link1"]
l2 = bpy.data.objects["Link2"]
tg = bpy.data.objects["Target"]
ee = bpy.data.objects["EndEffector"]

l1l = (l1.matrix_world.to_translation() - l2.matrix_world.to_translation()).length
l2l = (ee.matrix_world.to_translation() - l2.matrix_world.to_translation()).length

pos, angle1, angle2 = fabrik(100, tg)



set_global_position( ee, pos['ee'] )
#set_global_position( l2, pos['l2'] )
set_global_position( l1, pos['l1'] )
print(degrees(angle1))
print(degrees(angle2))
rotate_object_local_axis(l1, 'Y', degrees(angle1))
l2.rotation_euler[1] = angle2


def rotate_base():
    projection = project_object( tg, base, 2 ) 

    angle = get_angle( 
        get_world_trans(base),
        local_orientation(base)[0],
        projection
    )
    
    print(angle)
    rotate_object_local_axis( base, 'Z', angle[1] )

rotate_base()


