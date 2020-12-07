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

    def add_link_by_index(self, node_tree, node, node2, output_name, input_index):
        node_tree.links.new(node.outputs[output_name], node2.inputs[input_index])   

    def add_link(self, node_tree, node, node2, output_name, input_name, non_color_data = False):
        
        node_tree.links.new(node.outputs[output_name], node2.inputs[input_name])
        
        if(hasattr(node, "color_space")):
            if(non_color_data):
                node.color_space = "NONE"
            else:
                node.color_space = "COLOR"

    def create_normal_img(self, node_tree):
        return node_tree.nodes.new('ShaderNodeTexImage')

    def create_normal_map(self, node_tree):
        return node_tree.nodes.new('ShaderNodeNormalMap')

    def get_node(self, node_type, node_tree):
      for node in node_tree.nodes:
        if node.type == node_type:
          return node

      return None

    def execute(self, context):

      low_poly = context.scene.low_poly
      high_poly = context.scene.high_poly
      node_tree = low_poly.data.materials[0].node_tree
      
      # Bake the image maps from high poly to low poly

      # 1. Check if the low poly object has a principled shader
      pri_shader_node = self.get_node("BSDF_PRINCIPLED", node_tree)
      if(pri_shader_node is None):
        return {'CANCELED'}

      # 2. Check if there is a normal map attached already.
      #    If not, create a normal map and attach it
      normal_map_node = None
      if not pri_shader_node.inputs["Normal"].is_linked:
        normal_map_node = self.create_normal_map(node_tree)
        self.add_link(node_tree, normal_map_node, pri_shader_node, "Normal", "Normal")
      else:
        normal_map_node = pri_shader_node.inputs["Normal"].links[0].from_node

      # 3. Now check if the normal map has an image texture assigned
      #    If not, create an image texture node and attach it
      normal_img_node = None
      if not normal_map_node.inputs["Color"].is_linked:
        normal_img_node = self.create_normal_img(node_tree)       
        self.add_link(node_tree, normal_img_node, normal_map_node, "Color", "Color", True)
      else:
        normal_img_node = normal_map_node.inputs["Color"].links[0].from_node
      
      bpy.ops.object.mode_set(mode='OBJECT')

      # Use Cycles as renderer
      bpy.context.scene.render.engine = 'CYCLES'

      bpy.ops.object.select_all(action='DESELECT')
      high_poly.select_set(True) 
      low_poly.select_set(True) 
      bpy.context.view_layer.objects.active = low_poly
      bpy.ops.object.bake(type="NORMAL", use_selected_to_active=True)

      return {'FINISHED'}