import bpy
from mathutils import Vector, Euler
from math import radians, degrees, acos
from typing import Union
import random

import os, sys
blend_file_dir = os.path.dirname(bpy.data.filepath)
sys.path.append(blend_file_dir)
from robotics_utils import setup_robot_default

from blender_utils import *
from transformations import *

# Global initialisation of target, 
# end-effector, and lenths of Link 1 and 2
tg = None  
ee = None
l1l = 0 
l2l = 0

# Dictionary holding robot link parameters
obj_rotations = {
    "Base": {
        "axis"  : 'Z',
        "_axis" : 2,
        "start" : Euler((0,0,0)),
        "end"   : Euler((0,0,0))
    },
    "Link1": {
        "axis"  : 'Y',
        "_axis" : 1,
        "start" : Euler((0,0,0)),
        "end"   : Euler((0,0,0))
    },
    "Link2": {
        "axis"  : 'Y',
        "_axis" : 1,
        "start" : Euler((0,0,0)),
        "end"   : Euler((0,0,0))
    },
}

# Checks whether the target is within reach of the robot arm.
def isReachable(_tg, _ee, dist):
    global ee, tg, l1l, l2l
    return (_tg.matrix_world.to_translation() -_eeee.matrix_world.to_translation()).length < dist

def fabrik( iterations, target, tolerance = 0.01 ):
    '''
    Implementation of the FABRIK Algorithm
    Args:
        iterations (int): Number of times the joint positions will be calculated
        target(bpy.types.Object): Blender Object representing the end pose
        tolerance (float): threshold in meters below which no more iterations take place
    '''
    global ee,l1l, l2l,l1, l2
    
    l_pos = dict()    
    l_pos["l1"] = l1.matrix_world.to_translation()
    l_pos["l2"] = l2.matrix_world.to_translation()
    l_pos["ee"] = ee.matrix_world.to_translation()
    print(f"L1: {l1}, L2: {l2} ")
    origPos = l_pos["l1"].copy()
    n_pos = dict()
    tg_pos = get_world_trans(target)
    
    for i in range(iterations):        
        if( (l_pos["ee"]-tg_pos).length < tolerance ):
            break;
        
        # Backward Trace
        n_pos["ee"]  = tg_pos
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

def base_ik(base, tg):
    projection = project_object( tg, base, 2 ) 

    angle = get_angle( 
        get_world_trans(base),
        local_orientation(base)[0],
        projection,
        2)
    print(angle)
    #rotate_object_local_axis( base, 'Z', angle[1] )
    return angle[0]
   
def animate_robot(end_frame = 90):
    '''
    Animates the robot arm from frame frame 0 to end_frame
    Args:
        end_frame(int) : The last frame of the animation
    '''
    clear_timeline()
    set_animation_frame_range(0,end_frame)    
    scene = bpy.context.scene
    
    for obj_name, data in obj_rotations.items(): 
        obj = bpy.data.objects.get(obj_name)
        
        # Clear any existing animation data for the object
        obj.animation_data_clear()
        
        # Set the rotation at frame 0
        scene.frame_set(0)
        obj.rotation_euler = data["start"]
        obj.keyframe_insert(data_path="rotation_euler", frame=0)
        
        scene.frame_set(end_frame)
        obj.rotation_euler = data["end"]
        obj.keyframe_insert(data_path="rotation_euler", frame=end_frame)
    
    play_animation()
  
def simulate_robot():
    '''
    Main Function
    - Caches the Robot arm components
    - Calls the IK Functions
    - Triggers the Animation Function
    '''
    global ee, tg, l1,l2, base,l1l, l2l
    base = bpy.data.objects["Base"]
    l1 = bpy.data.objects["Link1"]
    l2 = bpy.data.objects["Link2"]
    tg = bpy.data.objects["Target"]
    ee = bpy.data.objects["EndEffector"]

    l1l = (l1.matrix_world.to_translation() - l2.matrix_world.to_translation()).length
    l2l = (ee.matrix_world.to_translation() - l2.matrix_world.to_translation()).length

    pos, angle1, angle2 = fabrik(100, tg)
    angle0 = base_ik(base, tg)
    
    set_global_position( ee, pos['ee'] )
    #set_global_position( l2, pos['l2'] )
#    set_global_position( l1, pos['l1'] )
    #rotate_object_local_axis(l1, 'Y', degrees(angle1))
    #l2.rotation_euler[1] = angle2

    obj_rotations["Link1"]["end"][ obj_rotations["Link1"]["_axis"] ] = angle1
    obj_rotations["Link2"]["end"][ obj_rotations["Link2"]["_axis"] ] = angle2
    obj_rotations["Base"]["end"][ obj_rotations["Base"]["_axis"] ] = angle0
    animate_robot()

# Define the operator for spawning the robot arm
class ResetOperator(bpy.types.Operator):
    bl_idname = "object.reset_scene"
    bl_label = "Reset Scene"

    def execute(self, context):
        stop_animation()
        setup_robot_default()
        return {'FINISHED'}

# Define Operator for starting the IK Execution
class RunIKOperator(bpy.types.Operator):
    bl_idname = "object.run_ik"
    bl_label = "Run IK"

    def execute(self, context):
        simulate_robot()
        return {'FINISHED'}

# Define the custom panel
class RoboticsPanel(bpy.types.Panel):
    bl_label = "Robotics Panel"
    bl_idname = "OBJECT_PT_Robotics"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Robotics"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.reset_scene")
        layout.operator("object.run_ik")

# Register the custom panel and operator
def register():
    bpy.utils.register_class(ResetOperator) 
    bpy.utils.register_class(RunIKOperator)
    bpy.utils.register_class(RoboticsPanel)

# Deregister the custom panel and operator
def unregister():
    bpy.utils.unregister_class(RoboticsPanel)
    bpy.utils.register_class(ResetOperator) 
    bpy.utils.register_class(RunIKOperator)

if __name__ == "__main__":
    register()