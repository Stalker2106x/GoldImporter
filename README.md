# GoldImporter
## GoldSrc (Half life) BSP Importer for Blender

__This repository is a Goldsrc fork of the original [blender_io_mesh_bsp](https://github.com/andyp123/blender_io_mesh_bsp/) released by andyp123__

An add-on for [Blender](https://www.blender.org/) that makes it possible to import Goldsrc BSP files, (including textures stored in the BSP) as materials. It works with Blender 4.0+

![Imported level (c0a0)](https://raw.githubusercontent.com/stalker2106x/goldimporter/master/README_img/c0a0.png)

## Features
- Imports all BSP models as mesh
- Imports all lights as blender lights
- Imports all entities as empty and add fields as custom properties
- Stitches matching trigger_changelevel between imports

## Installation
1. Download the latest release from GitHub by clicking [here](https://github.com/stalker2106x/goldimporter/releases/).
2. In Blender, open Preferences (Edit > Preferences) and switch to the Add-ons section.
3. Select 'Install Add-on from file...' and select the ZIP file that you downloaded.
4. Search for the add-on in the list (enter 'BSP' to quickly find it) and enable it.
5. Check addon preferences and provide "Extracted WAD path", which is a folder containing all textures used in your map in PNG format, all lowercase.
You can obtain them by extracting Half-life WADs using any WAD tool such as [wad3-cli](https://github.com/Stalker2106x/wad3-cli)

## Usage

You will be able to import GoldSrc bsp files from __File > Import > Goldsrc BSP (.bsp)__.
Selecting this option will open the file browser and allow you to select a file to load.

__NOTE: GoldImporter uses external textures, check addon preferences to configure your WAD folder__

### Scale (default: 0.03125)
Changes the size of the imported geometry. The size of a unit in Quake is not the
same as in Blender. Scale is set so that 32 units in Quake is 1m in Blender, so setting
scale to 1 will make everything huge.

### Create Materials (default: On)
Enable or Disable the creation of materials and storing of texture data in the .blend
file.

### Remove Hidden (default: On)
There are some objects in a typical Quake BSP, such as triggers, that are hidden in the
game, but included in the BSP. Disable this to import these objects too. Importing
hidden objects can make it hard to see all the details in the BSP.

### Brightness Adjust (default: 0.0)
Adjust the value of this setting to increase or decrease the brightness of imported
textures.

### Worldspawn Only (default: Off)
Worldspawn is the name given to the first model inside a BSP file. It represents the
static level geometry. Subseqent models in the BSP are dynamic, such as doors, platforms
and triggers. Enabling this will only import this first model.

### Create Lights (default: On)
Import any light entity data in the BSP as lights in Blender. This works quite well for
older maps, but modern maps often have static light data stripped from the BSP, since
it doesn't ever change, so the only type of light data that will be imported is for
lights that are animated or have an ambient effect.

### Create Cameras (default: On)
Import info_intermission and info_player_start as cameras in Blender. Created cameras
will face the same direction as in the BSP file, and the camera field of view will be
set to match the default 90 degree FOV of Quake.

### Create Entities (default: Off)
Import certain entity types as empties in Blender. By default, this will only import
monsters, weapons and items. This is useful if you have imported a mesh you would like
to place in the level at the same location as an entity in the game.

### Import All (default: On)
Rather than just importing a few entity types, this will import all entities contained
in the BSP as empties. Useful if an entity you need the location of is not included by
the default Create Entities option.

## Collections
When a BSP is imported into Blender, the level geometry will be put in a collection
named after the file. Entities and lights will also be placed into collections. If the
map name is e1m1.bsp, the resulting collections will look like this:
* 'e1m1' - level geometry
* 'e1m1_entities' - entities
* 'e1m1_lights' - lights

## View Settings
Once a BSP has been imported, you might want to tweak some viewport settings to better
see the geometry. I recommend using the Solid/Workbench display mode and adjusting the
following:

* __Color__: Texture
* __Backface Culling__: On
* __Specular Lighting__: Off

As of version 0.0.9, the importer will attempt to set up any active 3d views to use this
kind of shading, saving you the hassle. Disabling Overlays is also recommended.
