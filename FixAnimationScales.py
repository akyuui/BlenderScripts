# TODO better label/descriptions
import bpy


bl_info = {
    'name': 'Fix Animations Scales',
    'blender': (3, 6, 0),
    'category': 'Import+Export',
    'author': 'Akyuu',
}


class AkyuuScripts(bpy.types.Panel):
    bl_label = "Fix Actions Scale"
    bl_idname = "OBJECT_PT_Akyuu_FixActionsScale"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Some Scripts"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'scale_amount')
        layout.operator("akyuu.scale_operator")


# noinspection PyUnusedLocal
class ScaleActionsOperator(bpy.types.Operator):
    bl_idname = "akyuu.scale_operator"
    bl_label = "Scale Actions"

    @staticmethod
    def execute(self, context):
        scale_amount = context.scene.scale_amount
        try:
            for action in bpy.data.actions:
                for fcurve in action.fcurves:
                    if fcurve.data_path.endswith("location"):
                        for keyframe_point in fcurve.keyframe_points:
                            keyframe_point.co.y *= scale_amount
                            keyframe_point.handle_left.y *= scale_amount
                            keyframe_point.handle_right.y *= scale_amount
        except TypeError:
            pass
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AkyuuScripts)
    bpy.utils.register_class(ScaleActionsOperator)
    bpy.types.Scene.scale_amount = bpy.props.FloatProperty(
        name="Amount",
        description="Scale Amount",
        default=100.0,
        min=-1e10,
        max=1e10,
        soft_min=0,
        soft_max=1000
    )


def unregister():
    bpy.utils.unregister_class(AkyuuScripts)
    bpy.utils.unregister_class(ScaleActionsOperator)
    del bpy.types.Scene.scale_amount


if __name__ == "__main__":
    register()
