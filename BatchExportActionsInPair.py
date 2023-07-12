# TODO armature and mesh picker
# TODO better label/descriptions
import bpy


bl_info = {
    'name': 'Batch Export Mesh and Armature Actions in Pair',
    'blender': (3, 6, 0),
    'category': 'Import+Export',
    'author': 'Akyuu',
}


# noinspection PyUnusedLocal
class AkyuuScripts(bpy.types.Panel):
    bl_label = 'export Actions and Shapekeys'
    bl_idname = 'OBJECT_PT_Akyuu_ExportActionShapekey'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Some Scripts'

    def draw(self, context):
        layout = self.layout
        layout.operator('akyuu.export_operator')


# noinspection PyUnusedLocal
class ExportActionShapekeyOperator(bpy.types.Operator):
    bl_idname = 'akyuu.export_operator'
    bl_label = 'Export in Pair'
    bl_description = '''Export one Armature and one Mesh with a pair of Action and Shape Key animation to an FBX file,
The Action prefix must be AS_ and the Shape Key animation prefix must be SS_

input example: AS_Walk, SS_Walk, AS_Jump, SS_Jump
output: Armature_AS_Walk.FBX, Armature_AS_Jump.FBX

already contains recommended UE export settings
only one Armature and only one Mesh must be selected in the viewport before using'''

    @staticmethod
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) == 2:
            if selected_objects[0].type == 'MESH' and selected_objects[1].type == 'ARMATURE':
                mesh_object = selected_objects[0]
                armature_object = selected_objects[1]
            elif selected_objects[0].type == 'ARMATURE' and selected_objects[1].type == 'MESH':
                mesh_object = selected_objects[1]
                armature_object = selected_objects[0]
            else:
                raise ValueError('The selected objects are not a mesh and an armature')
        else:
            raise ValueError('There are not exactly two objects selected')

        for action in bpy.data.actions:
            if action.name.startswith('AS_'):
                armature_object.animation_data.action = action
                shape_key_action = bpy.data.actions.get(action.name.replace('AS_', 'SS_'))
                mesh_object.data.shape_keys.animation_data.action = shape_key_action
                # outdated fake bpy
                # noinspection PyArgumentList
                bpy.ops.export_scene.fbx(
                    # path
                    filepath=f'{bpy.path.abspath("//")}{armature_object.name}_{action.name}.fbx',
                    # include
                    use_selection=True, use_visible=False, use_active_collection=False,
                    object_types={'MESH', 'ARMATURE'}, use_custom_props=False,
                    # transform
                    global_scale=1.0, apply_scale_options='FBX_SCALE_NONE',
                    axis_forward='Y', axis_up='Z',
                    apply_unit_scale=True, use_space_transform=False, bake_space_transform=False,
                    # geometry
                    mesh_smooth_type='FACE', use_subsurf=False,
                    use_mesh_modifiers=False, use_mesh_modifiers_render=False,
                    use_mesh_edges=False, use_triangles=False, use_tspace=False,
                    colors_type='SRGB', prioritize_active_color=False,
                    # armature
                    primary_bone_axis='Y', secondary_bone_axis='X',
                    bake_anim=True, armature_nodetype='NULL',
                    use_armature_deform_only=False, add_leaf_bones=False,
                    # bake animation
                    bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=False,
                    bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0
                )
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AkyuuScripts)
    bpy.utils.register_class(ExportActionShapekeyOperator)


def unregister():
    bpy.utils.unregister_class(AkyuuScripts)
    bpy.utils.unregister_class(ExportActionShapekeyOperator)


if __name__ == '__main__':
    register()
