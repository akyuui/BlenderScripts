import bpy


y_scale = 100

try:
    for action in bpy.data.actions:
        for fcurve in action.fcurves:
            if fcurve.data_path.endswith("location"):
                for keyframe_point in fcurve.keyframe_points:
                    keyframe_point.co.y *= y_scale
                    keyframe_point.handle_left.y *= y_scale
                    keyframe_point.handle_right.y *= y_scale
except TypeError:
    pass
