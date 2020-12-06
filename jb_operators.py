import bpy
from bpy.types import Operator

class JB_Bake_Op(Operator):
    bl_idname = "object.bake_op"
    bl_label = "Bake maps"
    bl_description = "Bake image maps for low and high poly objects" 
    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(cls, context):
      low_poly = context.scene.low_poly
      high_poly = context.scene.high_poly

      return low_poly and high_poly
         
    def execute(self, context):

      # TODO: Bake the image maps from high poly to low poly
      return {'FINISHED'}