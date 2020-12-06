import bpy
from bpy.types import Panel

class JB_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "JBake"
    bl_category = "JBake"
    
    def draw(self, context):
       
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        layout.prop(context.scene, "low_poly", text="Low Poly")

        row = layout.row()
        layout.prop(context.scene, "high_poly", text="High Poly")

        row = layout.row()
        row.operator('object.bake_op', text='Bake maps', icon='MOD_BOOLEAN')