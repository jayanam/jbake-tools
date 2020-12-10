import bpy
from bpy.types import Operator

class JB_Bake_Op(Operator):
    bl_idname = "object.bake_op"
    bl_label = "Bake maps"
    bl_description = "Bake image maps for low and high poly objects" 
    bl_options = {'REGISTER'} 

    def __init__(self):
      self.__baking = False
    
    @classmethod
    def poll(cls, context):

      low_poly = context.scene.low_poly
      high_poly = context.scene.high_poly

      return (low_poly and high_poly) or self.__baking

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
        img_node = node_tree.nodes.new('ShaderNodeTexImage')
        img_name = bpy.context.scene.low_poly.name + "_" + "normal"
        img_width = bpy.context.scene.img_bake_width
        img_height = bpy.context.scene.img_bake_height

        image = bpy.data.images.new(img_name, width=img_width, height=img_height)
        image.colorspace_settings.name = "Non-Color"

        img_node.image = image
        return img_node

    def create_normal_map(self, node_tree):
        return node_tree.nodes.new('ShaderNodeNormalMap')

    def get_node(self, node_type, node_tree):
      for node in node_tree.nodes:
        if node.type == node_type:
          return node

      return None

    def bake_normal_map(self):
      bpy.ops.object.bake(type="NORMAL", use_selected_to_active=True)

    def execute(self, context):

      self.__baking = True
  
      low_poly = context.scene.low_poly
      high_poly = context.scene.high_poly

      if len(low_poly.data.materials) == 0:
        err_material = "Assign a material to {0} before baking"
        self.report({'ERROR'}, err_material.format(low_poly.name) )
        return {'CANCELLED'}    

      node_tree = low_poly.data.materials[0].node_tree
      
      # Bake the image maps from high poly to low poly

      # 1. Check if the low poly object has a principled shader
      pri_shader_node = self.get_node("BSDF_PRINCIPLED", node_tree)
      if(pri_shader_node is None):
        return {'CANCELLED'}

      low_poly.hide_set(False)
      low_poly.select_set(True) 
      bpy.ops.object.mode_set(mode='OBJECT')

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
      
      # Use Cycles as renderer
      bpy.context.scene.render.engine = 'CYCLES'

      bpy.ops.object.select_all(action='DESELECT')

      hp_hide = high_poly.hide_get()

      high_poly.hide_set(False)
      high_poly.select_set(True) 

      low_poly.select_set(True)
      bpy.context.view_layer.objects.active = low_poly

      self.bake_normal_map()

      high_poly.hide_set(hp_hide)
      bpy.ops.object.select_all(action='DESELECT')

      self.__baking = False

      return {'FINISHED'}