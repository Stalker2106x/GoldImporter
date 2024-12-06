#  ***** GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#  ***** GPL LICENSE BLOCK *****

# addon information
bl_info = {
    "name": "Import GoldSrc BSP format",
    "author": "Maxime Martens (forked from Andrew Palmer work with contributions from Ian Cunningham)",
    "version": (1, 4),
    "blender": (4, 0, 0),
    "location": "File > Import > GoldSrc BSP v30 (.bsp)",
    "description": "Import geometry and entities from a GoldSrc BSP v30 file.",
    "wiki_url": "https://github.com/stalker2106x/GoldImporter",
    "category": "Import",
}

# reload submodules if the addon is reloaded 
if "bpy" in locals():
    import importlib
    importlib.reload(bsp_importer)
else:
    from . import bsp_importer

# imports
import bpy, os, time
from bpy.types import AddonPreferences, Operator, Panel;
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator

#
# addon preferences
#

class GoldImporterPreferences(AddonPreferences):
    bl_idname = __package__

    wadpath: StringProperty(
        name="Extracted WAD Path",
        subtype='DIR_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "wadpath")

#
# main
#

class GoldImporter(bpy.types.Operator, ImportHelper):
    bl_idname       = "goldimporter.bsp"
    bl_description  = "Import geometry from GoldSrc BSP v30 file format (.bsp)"
    bl_label        = "Import BSP"
    bl_options      = {'UNDO'}

    filename_ext = ".bsp"
    filter_glob: StringProperty(
        default="*.bsp",
        options={'HIDDEN'},
    )

    files: bpy.props.CollectionProperty(
            type=bpy.types.PropertyGroup
    )

    brightness_adjust: FloatProperty(
        name="Texture Brightness",
        description="Adjust the brightness of imported textures.",
        min=-1.0, max=1.0,
        default=0.0,
    )

    scale: FloatProperty(
        name="Scale",
        description="Adjust the size of the imported geometry.",
        min=0.0, max=1.0,
        soft_min=0.0, soft_max=1.0,
        default=0.03125, # 1 Meter = 32 Quake units
    )

    create_materials: BoolProperty(
        name="Create materials",
        description="Import textures from the configured folder and apply to geometry.",
        default=True,
    )

    import_lights: BoolProperty(
        name="Import all lights",
        description="Create light objects in Blender from any light data in the BSP file.",
        default=True,
    )

    import_brush_entities: BoolProperty(
        name="Import brush entities",
        description="Import extra brush entities like triggers and other special brushes.",
        default=False,
    )

    import_point_entities: BoolProperty(
        name="Import point entities",
        description="Import all point entities.",
        default=False,
    )
    
    stitch_changelevel: BoolProperty(
        name="Stitch changelevel with existing",
        description="Imported bsp will attempt to stitch its trigger_changelevel to match currently existing ones with appropriate name.",
        default=True,
    )
    
    def execute(self, context):
        time_start = time.time()
        preferences = context.preferences.addons[__package__].preferences
        options = {
            'scale' : self.scale,
            'brightness_adjust': self.brightness_adjust,
            'scale': self.scale,
            'create_materials': self.create_materials,
            'import_lights': self.import_lights,
            'import_brush_entities': self.import_brush_entities,
            'import_point_entities': self.import_point_entities,
            'stitch_changelevel': self.stitch_changelevel,
        }
        # Process BSP(s)
        path = os.path.dirname(self.filepath)
        print(path)
        for entry in self.files:
            entrypath = f"{path}/{entry.name}"
            print(f"Importing file: {entrypath}")
            bsp_importer.import_bsp(context, entrypath, preferences, options)
        print("Elapsed time: %.2fs" % (time.time() - time_start))
        return {'FINISHED'}


classes = (
    GoldImporterPreferences,
    GoldImporter,
)

def menu_func(self, context):
    self.layout.operator(GoldImporter.bl_idname, text="GoldSrc BSP (.bsp)")


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
