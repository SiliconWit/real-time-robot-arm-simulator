import os, json
import bpy
from mathutils import Vector
import math
import random

import os, sys
blend_file_dir = os.path.dirname(bpy.data.filepath)
sys.path.append(blend_file_dir)
import blender_utils as ut

# Confifuration of the robot
robotconfig = {
    "base": {
        "limits": [0, 232],
        "dimensions": [0.12, 0.1],
        "position": [0,0,0],
        "axis": "Z",
        "parent" : None
    },
    "link1": {
        "limits": [-90, 90],
        "dimensions": [0.05, 0.4],
        "position": [0,0,0.1],
        "axis": "Y",
        "parent" : "Base"
    },
    "link2": {
        "limits": [0, 343],
        "dimensions": [0.05, 0.4],
        "position": [0,0,0.5],
        "axis": "Y",
        "parent" : "Link1"
    },
    "EE":{
        "position": [0,0,0.90]
    }
}

class RobotRevLink():
    def __init__(self, name, config) -> None:
        self.name = name
        self.radius = config["dimensions"][0]
        self.length = config["dimensions"][1]
        self.limits = config["limits"]
        self.axis = config["axis"]
        self.parent = config["parent"]
        self.create_link(config["position"])
        self.set_constraints()
        

    def create_link(self, location:tuple):
        """
        Creates a link based given a radius and length.
        Also sets the pivot of the object to the center of the bottom face 
        """
        radius = self.radius
        length = self.length
        offset = Vector(location) + (Vector((0,0,1)) * length/2)
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, location=offset) 
        bpy.context.object.name = self.name
        self.obj = bpy.context.object

        # Set origin to the center of the lower face
        bpy.context.object.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
        bpy.context.scene.cursor.location = (location[0], location[1], location[2])
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
        bpy.context.scene.cursor.location = (0, 0, 0)  
    
    def get_object(self) -> bpy.types.Object:
        return ut.get_object_by_name(self.name)

    def set_constraints(self):
        ut.select_obj(self.name)
        self.obj.constraints.new("LIMIT_ROTATION")
        
        if( self.axis == 'X' ):
            self.obj.constraints["Limit Rotation"].use_limit_y = True
            bpy.context.object.constraints["Limit Rotation"].min_x = math.radians(self.limits[0])
            bpy.context.object.constraints["Limit Rotation"].max_x = math.radians(self.limits[1])
            bpy.ops.constraint.apply(constraint="Limit Rotation", owner='OBJECT')

        
        if( self.axis == 'Y' ):
            self.obj.constraints["Limit Rotation"].use_limit_y = True
            bpy.context.object.constraints["Limit Rotation"].min_y = math.radians(self.limits[0])
            bpy.context.object.constraints["Limit Rotation"].max_y = math.radians(self.limits[1])
            bpy.ops.constraint.apply(constraint="Limit Rotation", owner='OBJECT')

        
        if( self.axis == 'Z' ):
            self.obj.constraints["Limit Rotation"].use_limit_z = True
            bpy.context.object.constraints["Limit Rotation"].min_z = math.radians(self.limits[0])
            bpy.context.object.constraints["Limit Rotation"].max_z = math.radians(self.limits[1])
            bpy.ops.constraint.apply(constraint="Limit Rotation", owner='OBJECT')

    def set_parent(self, parent=""):
        if len(parent) > 0:
            ut.set_parent( self.name, parent )

        elif(self.parent != None):
            ut.set_parent( self.name, self.parent )
    
    def create_endeffector(self, position, name = "EndEffector" ):
        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=position)
        bpy.context.object.empty_display_size = 0.05
        bpy.context.object.name = name
        # ut.set_parent( name, self.name )
        self.ee = bpy.ops.object
    
    def get_child(self):
        self.obj.children[0] if( self.obj.children[0] ) else None
        
    def spawn_target(self):
        random_loc = Vector(random.uniform( 0, 0.3) for _ in range(3))
        offset_point = ut.get_world_trans(self.obj)
        offset_point[2] += self.length/2 
        # random_loc = Vector( ( random.uniform( -0.25, 0.25), offset_point[2] + self.length/2,random.uniform( -0.25, 0.25) ) )
        _location = offset_point + random_loc
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, align='WORLD', location=_location )
        bpy.context.active_object.name = "Target"
    
def setup_robot(robotconfig, RobotRevLink):
    ut.clear_scene()
    RobotRevLink( "Base", robotconfig["base"] )
    link2 = RobotRevLink( "Link1", robotconfig["link1"] )
    link3 = RobotRevLink( "Link2", robotconfig["link2"] )
    link2.set_parent()
    link3.set_parent()
    link3.create_endeffector( robotconfig["EE"]["position"] )
    link3.spawn_target()

def setup_robot_default():
    setup_robot(robotconfig, RobotRevLink)

# Define the custom operator
class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.reset_scene"
    bl_label = "Reset Scene"

    def execute(self, context):
        setup_robot(robotconfig, RobotRevLink)
        return {'FINISHED'}

# Define the custom panel
class SimplePanel(bpy.types.Panel):
    bl_label = "Reset Scene Panel"
    bl_idname = "OBJECT_PT_reset_scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Robotics"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.reset_scene")

# Register the custom panel and operator
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(SimplePanel)

def unregister():
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(SimpleOperator)

if __name__ == "__main__":
    register()
