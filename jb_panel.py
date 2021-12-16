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
        split = row.split(factor=0.4,align=True)
        col = split.column()
        col.label(text='Low Poly')

        col = split.column()
        col.prop(context.scene, "low_poly", text="")

        row = layout.row()
        split = row.split(factor=0.4,align=True)
        col = split.column()
        col.label(text='High Poly')

        col = split.column()
        col.prop(context.scene, "high_poly", text="")

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

        row = layout.row()
        row.prop(context.scene.render.bake, "use_cage", text="Use Cage")

        if context.scene.render.bake.use_cage:
            row = layout.row()
            split = row.split(factor=0.4,align=True)
            col = split.column()
            col.label(text='Cage Object')

            col = split.column()
            col.prop(context.scene.render.bake, "cage_object", text="")