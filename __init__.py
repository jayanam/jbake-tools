# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "JBake Tools",
    "author" : "Jayanam",
    "description" : "Blender Addon to simplify baking image maps",
    "blender" : (2, 80, 0),
    "version" : (0, 1, 0),
    "location" : "View3D",
    "category" : "Object"
}

# Blender imports
import bpy
from bpy.props import *

from . jb_panel import *
from . jb_operators import *

# Low poly object to bake onto
bpy.types.Scene.low_poly = PointerProperty(type=bpy.types.Object)

# High poly object with the details to bake
bpy.types.Scene.high_poly = PointerProperty(type=bpy.types.Object)

classes = ( JB_PT_Panel, JB_Bake_Op )

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)