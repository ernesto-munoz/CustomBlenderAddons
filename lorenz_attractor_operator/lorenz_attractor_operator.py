import bpy
from bpy.props import IntProperty


class LorenzAttractorOperator(bpy.types.Operator):
    """Lorenz Attractor"""
    bl_idname = "object.lorenz_attractor"
    bl_label = "Lorenz Attractor Operator"
    bl_options = {'REGISTER', 'UNDO'}

    A = 10
    B = 28
    C = 8.0 / 3.0

    vertex_by_frame = IntProperty(
        name='Vertex by Frame',
        description='Vertex by Frame.',
        default=15,
        min=0,
    )

    start_frame = IntProperty(
        name='Start Frame',
        description='Start frame of the animation.',
        default=0,
        min=0,
    )

    end_frame = IntProperty(
        name='Start Frame',
        description='Start frame of the animation.',
        default=100
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # start_frame, end_frame = self.get_frame_range_from_context(context=context)

        # mesh = bpy.data.meshes.new('lorenz')
        curve_data = bpy.data.curves.new('lorenz_data', type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = 2

        num_vertices = (self.end_frame - self.start_frame) * self.vertex_by_frame
        # mesh.vertices.add(num_vertices)
        # mesh.edges.add(num_vertices - 1)
        polyline = curve_data.splines.new('NURBS')
        polyline.points.add(num_vertices)


        # initial x, y, z position
        x = 0.01
        y = 0
        z = 0

        # create points of the mesh
        for i in range(0, num_vertices):
            dt = 0.01 # delta time
            dx = (self.A * (y - x)) * dt
            dy = (x * (self.B - z) - y) * dt
            dz = (x * y - self.C * z) * dt
            x += dx
            y += dy
            z += dz

            polyline.points[i].co = (x, y, z, 1) # why w?

            # mesh.vertices[i].co = (x, y, z)
            # if i < num_vertices - 1:
            #     mesh.edges[i].vertices = (i, i + 1)

        # create object with data
        obj = bpy.data.objects.new('lorenz_obj', curve_data)

        # create bevel circle and assign it
        bpy.ops.curve.primitive_bezier_circle_add(location=(0.0, 0.0, 0.0), radius=0.2)
        bcircle = context.scene.objects.active
        bcircle.name = 'lorenz_bevel'
        obj.data.bevel_object = bcircle


        # set the animation
        obj.data.bevel_factor_end = 0.0
        obj.data.keyframe_insert(data_path='bevel_factor_end', frame=(self.start_frame))
        obj.data.bevel_factor_end = 1.0
        obj.data.keyframe_insert(data_path='bevel_factor_end', frame=(self.end_frame))

        # context.scene.objects.link(obj)
        context.scene.objects.link(obj)
        context.scene.objects.active = obj
        return {'FINISHED'}

    def get_frame_range_from_context(self, context):
        return context.scene.frame_start, context.scene.frame_end

def menu_constructor(self, context):m
    self.layout.operator(LorenzAttractorOperator.bl_idname)

def register():
    bpy.utils.register_class(LorenzAttractorOperator)
    bpy.types.VIEW3D_MT_object.append(menu_constructor)

def unregister():
    bpy.utils.unregister_class(LorenzAttractorOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_constructor)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.lorenz_attractor()

# import bpy
# import os
#
# PATH = 'E:\PycharmProjects\Blender Scripts'
# SCRIPT = 'lorenz_attractor_operator.py'
#
# filename = os.path.join(PATH, SCRIPT)
# exec(compile(open(filename).read(), filename, 'exec'))