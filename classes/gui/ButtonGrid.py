"""
A 3x3 button grid example:
   0  |  1  |  2
   --------------
   3  |  4  |  5
   --------------
   6  |  7  |  8
"""
from direct.gui.DirectGui import DirectFrame, DirectButton

from classes.props.PlaneModel import PlaneModel

KEY = "key"
VALUE = "value"
BOTH = "both"


class ButtonGrid(DirectFrame):

    def __init__(self, parent, pos, scale, texture,
                 rows, columns, db_scale, collection, command, extra_arg,
                 base_x, base_z, x_increment, z_increment, x_regression=0,
                 fvs=(1, 1)):
        if not parent:
            parent = aspect2d
        DirectFrame.__init__(self, parent, pos=pos, scale=scale)
        self.initialiseoptions(ButtonGrid)

        self.texture = texture
        self.rows = rows
        self.columns = columns
        self.db_scale = db_scale  # directbutton scale
        self.collection = collection
        self.command = command
        self.extra_arg = extra_arg
        self.base_x = base_x
        self.base_z = base_z
        self.x_increment = x_increment
        self.z_increment = z_increment
        self.x_regression = x_regression
        self.fvs = fvs

        self.buttons = []

        if isinstance(collection, dict):
            self.dict_grid()
        elif isinstance(collection, list):
            self.list_grid()
        else:
            print("The collection type needs to be a dict or list.")

    def dict_grid(self):
        x, z = [self.base_x, self.base_z]
        uv_frame = 0
        x_limit = abs(self.base_x + ((self.columns - 1) * self.x_increment))
        for key, value in self.collection.items():
            if self.extra_arg == KEY:
                extra_arg = [key]
            elif self.extra_arg == VALUE:
                extra_arg = [value]
            elif self.extra_arg == BOTH:
                extra_arg = [key, value]
            else:
                extra_arg = None

            geom = PlaneModel(self.texture, rows=self.rows,
                              columns=self.columns)
            geom.set_frame(uv_frame)
            DirectButton(self, geom=geom, pos=(x, 0, z), scale=self.db_scale,
                         command=self.command, extraArgs=extra_arg)
            uv_frame += 1
            if x >= x_limit:  # Reset x back to the far left and move down.
                x = self.base_x
                z -= self.z_increment
            else:
                x += self.x_increment  # Move next GUI to the right.

    def list_grid(self):
        x, z = [self.base_x, self.base_z]
        uv_frame = 0
        x_limit = abs(self.base_x + ((self.columns - 1) * self.x_increment))
        for item in self.collection:
            geom = PlaneModel(self.texture, rows=self.rows,
                              columns=self.columns)
            geom.set_frame(uv_frame)
            DirectButton(self, geom=geom, pos=(x, 0, z), scale=self.db_scale,
                         command=self.command, extraArgs=[item],
                         frameVisibleScale=self.fvs)
            if x >= x_limit:  # Reset x back to the far left. Move down.
                x = self.base_x + self.x_regression
                z -= self.z_increment
                self.x_regression += self.x_regression
            else:
                x += self.x_increment  # Move next GUI to the right.

            uv_frame += 1
