import bpy
from bpy.types import Panel

class JB_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Bake objects"
    bl_category = "JBake"
    
    def draw(self, context):
       
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.prop(context.scene, "low_poly", text="Low Poly")

        row = layout.row()
        row.prop(context.scene, "high_poly", text="High Poly")

        row = layout.row()
        row.operator('object.bake_op', text='Bake maps', icon='MOD_BOOLEAN')

class JB_PT_Settings_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Bake settings"
    bl_category = "JBake"
    
    def draw(self, context):
       
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(context.scene.render.bake, "cage_extrusion", text="Extrusion")

        row = layout.row()
        row.prop(context.scene.render.bake, "max_ray_distance", text="Max Ray Distance")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "img_bake_width", text="Width")

        col = row.column()
        col.prop(context.scene, "img_bake_height", text="Height")