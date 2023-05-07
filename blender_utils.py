import bpy
from bpy.types import Object
from typing import Union
'''
List of Utility Functions
'''

def world_trans(obj):
    '''
    Gets the position and rotation of an object with 
    reference to  the global coordinates(Fixed Frame)
    '''
    loc = obj.matrix_world.to_translation()
    rot = obj.matrix_world.to_euler()
    return loc, rot

def get_object_by_name(name: str):
    '''
    Retrieve a Blender Object by name
    '''
    obj = bpy.data.objects.get(name)
    if obj:
        print(f"Object '{name}' found: {obj}")
    else:
        raise ValueError(f"Object '{name}' not found in the scene.")
    del obj
    return bpy.data.objects.get(name)


def set_animation_frame_range(start_frame, end_frame):
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

# Clear all keyframes for all objects in the scene
def clear_timeline():
    for obj in bpy.context.scene.objects:
        obj.animation_data_clear()

def add_rotation_keyframe(obj, frame, rotation_euler):
    '''
    Set Rotation Keyfame on a Blender Object
    '''
    bpy.context.scene.frame_set(frame)
    obj.rotation_euler = rotation_euler
    obj.keyframe_insert(data_path='rotation_euler', frame=frame)

def select_obj(object_name: str) -> None:
    """Make the given object active by its name and deselect others."""
    scene = bpy.context.scene
    obj = bpy.data.objects.get(object_name)
    
    if obj is not None:
        # Deselect all other objects
        for other_obj in bpy.context.selected_objects:
            other_obj.select_set(False)
        
        # Set the specified object as active and select it
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
    else:
        print(f"Object with name '{object_name}' not found.")

    return obj

def set_parent( child_n, parent_n ):
    parent = get_object_by_name(parent_n)
    child = get_object_by_name(child_n)
    bpy.ops.object.select_all(action='DESELECT')

    child.select_set(True)
    parent.select_set(True)
    bpy.context.view_layer.objects.active = parent
    
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

def get_child(obj_n:str) -> Union[bpy.type.Object, None]:
    '''
    Get the first child of a blender object

    Args:
        obj_n (bpy.type.Object) : The Blender Parent Object Type

    Returns:
        bpy.types.Object
    '''
    obj = get_object_by_name(obj_n)
    if( len(obj.childrend) > 0 ):
        if( isinstance( obj.childrend[0], bpy.types.Object ) ):
            return obj.childrend[0]
        else:
            return None
    else:
        return None



def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
