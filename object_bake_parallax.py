bl_info = {
    "name": "Bake Parallax",
    "author": "MZIskandar ",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "Properties > Render > Bake Parallax",
    "description": "Bake Parallax from selected object to active object image slot",
    "warning": "",
    "wiki_url": "https://github.com/UPBGE/blender-addons/wiki/Bake-Parallax-addon",
    "category": "Object",
    }

import bpy

class mzBakeProcess(bpy.types.Operator):
    bl_idname = 'object.mzbake_parallax'
    bl_label = 'Bake Parallax'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        #-----------------------------------------------------
        context.scene.render.use_bake_selected_to_active = True
        context.scene.render.bake_type = 'DISPLACEMENT'
        bpy.ops.object.bake_image()

        mzHeightMap = context.active_object.data.uv_textures.active.data[0].image

        mzHeightPxs = mzHeightMap.pixels[:]
        context.scene.render.bake_type = 'NORMALS'
        bpy.ops.object.bake_image()

        img = context.active_object.data.uv_textures.active.data[0].image

        pixels = img.pixels[:]
        pixels = list(img.pixels)
        for i in range(3, len(pixels), 4):
            pixels[i] = mzHeightPxs[i-1]
        img.pixels[:] = pixels
        img.update()

        return {'FINISHED'}

class mzBakeParallax(bpy.types.Panel):
    bl_label = 'Bake Parallax'
    bl_idname = 'OBJECT_PT_mzBakeParallax'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_GAME'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('object.mzbake_parallax', text='Bake Parallax')
    
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_class(__name__)

if __name__ == "__main__":
    register()
