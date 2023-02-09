bl_info = {
    "name": "PAC FRAMER",
    "author": "Pimentel Bastien",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "VIEW 3D > UI > PAC_FRAMER",
    "description": "Add keyframes for renderer and viewport visibility",
    "warning": "TO USE WITH render_score.py IN PANEL 'SCRIPTING'",
    "doc_url": "",
    "category": "Création Numérique",
}

import bpy
                       
class PAC_FRAMER_OT_add_keyframes(bpy.types.Operator):
    bl_idname = "pac_framer.add_keyframes"
    bl_label = "Add Keyframes to Timeline"
    
    current_frame = bpy.props.FloatProperty("Current frame")
    
    def execute(self, context):
        selected = bpy.context.active_object
        cur_frame = bpy.context.scene.frame_current
        
        selected.hide_viewport = False
        selected.hide_render = False
        selected.keyframe_insert(data_path="hide_viewport", frame = cur_frame - 1)
        selected.keyframe_insert(data_path="hide_render", frame = cur_frame - 1)
                
        selected.hide_viewport = True
        selected.hide_render = True
        selected.keyframe_insert(data_path="hide_viewport", frame = cur_frame)
        selected.keyframe_insert(data_path="hide_render", frame = cur_frame)
        
        return {'FINISHED'}

class PAC_FRAMER_OT_delete_keyframes(bpy.types.Operator):
    bl_idname = "pac_framer.delete_keyframes"
    bl_label = "Delete Keyframes in Timeline"
    
    def execute(self, context):
        
        selected = bpy.context.active_object
        start_frame = bpy.context.scene.frame_start
        registered_frame = bpy.context.scene.frame_current
        
        bpy.context.scene.frame_set(start_frame)
                
        bpy.context.active_object.animation_data_clear()
        
        bpy.context.scene.frame_set(registered_frame)
        
        return {'FINISHED'}
    
class PAC_FRAMER_OT_change_frame(bpy.types.Operator):
    bl_idname = "pac_framer.change_frame"
    bl_label = "Change Current Frame in Timeline"
    
    def execute(self, context):
        scene = context.scene
        toolbox = scene.toolbox
        
        frame = toolbox.frame
        
        bpy.context.scene.frame_set(frame)
        
        return {'FINISHED'}
        
class Properties(bpy.types.PropertyGroup):
    frame: bpy.props.IntProperty(name = "Go to frame", soft_min = 1)

class PAC_FRAMER_PT_MainPanel(bpy.types.Panel):
    bl_label = "PAC FRAMER"
    bl_idname = "pac_framer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PAC FRAMER"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        toolbox = scene.toolbox
        
        row = layout.row()
        row.label(text="Current frame: " + str(bpy.context.scene.frame_current))
        row = layout.row()
        row.label(text="First frame: " + str(bpy.context.scene.frame_start))
        row = layout.row()
        row.label(text="Last frame: " + str(bpy.context.scene.frame_end))
        row = layout.row()
        layout.prop(toolbox, "frame")
        
        layout.operator("pac_framer.add_keyframes", text = "PAC FRAME !", icon = "GHOST_ENABLED")
        layout.operator("pac_framer.delete_keyframes", text = "delete frames...", icon = "GHOST_DISABLED")
        layout.operator("pac_framer.change_frame", text = "Change current frame", icon = "DECORATE_KEYFRAME")


classes = [Properties, PAC_FRAMER_OT_change_frame, PAC_FRAMER_PT_MainPanel, PAC_FRAMER_OT_add_keyframes, PAC_FRAMER_OT_delete_keyframes]
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.toolbox = bpy.props.PointerProperty(type = Properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.toolbox

if __name__ == "__main__":
    register()