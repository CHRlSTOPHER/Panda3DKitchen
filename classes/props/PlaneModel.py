"""
Creates a procedurally generated plane in a 3D space.
"""
from panda3d.core import (NodePath, SamplerState,
                          TextureStage, TransparencyAttrib,
                          GeomVertexArrayFormat, GeomVertexFormat,
                          GeomVertexData, GeomVertexWriter,
                          GeomTriangles, Geom, GeomNode)
import math


class PlaneModel(NodePath):

    def __init__(self, texture_path=None, rows=1, columns=1,
                 pos=(0, 0, 0), scale=(1, 1, 1), color=(1, 1, 1, 1),
                 parent=None, frame=None, name="plane_model", reload=False):
        self.texture_path = texture_path
        self.rows = rows
        self.columns = columns
        self.node_parent = parent
        self.reload = reload

        NodePath.__init__(self, self.generate_plane_model())
        if texture_path:
            self.apply_texture()
        self.set_pos(pos)
        self.set_scale(scale)
        self.set_color(*color)
        if frame is not None:
            self.set_frame(frame)
        self.set_name(name)

    def generate_plane_model(self):
        array = GeomVertexArrayFormat()

        array.add_column("vertex", 3, Geom.NTFloat32, Geom.CPoint)  # Vertices
        array.add_column("normal", 3, Geom.NTFloat32, Geom.CPoint)  # Normal
        array.add_column("color", 4, Geom.NTFloat32, Geom.CTexcoord)  # Color
        array.add_column("texcoord", 2, Geom.NTFloat32, Geom.CTexcoord)  # UV

        format = GeomVertexFormat()
        format.add_array(array)
        format = GeomVertexFormat.register_format(format)

        # Trivia: If the model changes frequently,
        # Geom.UHDynamic can be used to not cache data
        vdata = GeomVertexData('name', format, Geom.UHStatic)
        vdata.set_num_rows(4)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        self.add_vertex_and_uv_coords(vertex, texcoord, normal, color)

        prim = GeomTriangles(Geom.UHStatic)
        prim.add_vertices(0, 1, 2)
        prim.add_vertices(1, 3, 2)

        # add the GeomVertexData & GeomPrimitive object to a GeomNode.
        # Return the GeomNode as NodePath's __init__ arg.
        geom = Geom(vdata)
        geom.add_primitive(prim)
        node = GeomNode('gnode')
        node.add_geom(geom)
        if self.node_parent:
            node = self.node_parent.attach_new_node(node)

        return node

    def add_vertex_and_uv_coords(self, vertex, texcoord, normal, color):
        # Divide by column/row to narrow the uv scale (origin is bottom left)
        vertex.add_data3(1, 0, 1)
        normal.add_data3(0, 0, 1)
        color.add_data4(1, 1, 1, 1)
        texcoord.add_data2(1 / self.columns, 1 / self.rows)

        vertex.add_data3(-1, 0, 1)
        normal.add_data3(0, 0, 1)
        color.add_data4(1, 1, 1, 1)
        texcoord.add_data2(0, 1 / self.rows)

        vertex.add_data3(1, 0, -1)
        normal.add_data3(0, 0, 1)
        color.add_data4(1, 1, 1, 1)
        texcoord.add_data2(1 / self.columns, 0)

        vertex.add_data3(-1, 0, -1)
        normal.add_data3(0, 0, 1)
        color.add_data4(1, 1, 1, 1)
        texcoord.add_data2(0, 0)

    def apply_texture(self):
        if isinstance(self.texture_path, list):
            texture = loader.load_texture(self.texture_path[0], self.texture_path[1], okMissing=True)
        else:
            texture = loader.load_texture(self.texture_path, okMissing=True)
        # Failover texture
        if not texture:
            texture = loader.load_texture("editor/maps/icon-unknown.png")
        self.set_texture(texture, 1)

        if self.reload:
            texture.reload()

        # improve the texture rendering
        texture.set_magfilter(SamplerState.FT_nearest)
        self.set_transparency(TransparencyAttrib.MDual)

    def set_frame(self, index):
        # Get the remainder. Ex: if column is 4, remainder can be 0-3.
        # We divide by the max columns to get a float between 0 and 1.
        u = (index % self.columns) / self.columns

        # ex: 6/4 = 1.5. rows only move down after all columns in a row.
        # thus, we floor the float and only look at the integer value.
        # when the integer value changes, the v value will shift.
        v = math.floor(index / self.rows) / self.rows

        # This will make offset origin go from the bottom left to top left.
        v += 1.0 / self.rows
        self.set_tex_offset(TextureStage.get_default(), u, -v)
