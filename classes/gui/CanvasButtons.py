import json
import math

from direct.gui.DirectGui import DirectButton, DGG
from panda3d.core import PGButton, MouseButton

from classes.menus import MenuGlobals as MG
from classes.props.PlaneModel import PlaneModel
from classes.settings import Globals as G

WHEELUP = (PGButton.getPressPrefix() + MouseButton.wheel_up().getName()
           + '-')
WHEELDOWN = (PGButton.getPressPrefix() + MouseButton.wheel_down().getName()
             + '-')


class CanvasButtons:

    def __init__(self):
        self.current_button_set = []
        self.scroll_frame = None

    def bind_button(self, button, binds):
        if len(binds) >= 2:  # scroll_up, scroll_down
            button.bind(WHEELUP, binds[0])
            button.bind(WHEELDOWN, binds[1])

        if len(binds) >= 4:  # + button_inc, button_dec
            button.bind(DGG.ENTER, binds[2], extraArgs=[button])
            button.bind(DGG.EXIT, binds[3], extraArgs=[button])

        if len(binds) >= 6:  # + make_button_copy, add_item_to_scene
            button.bind(DGG.B1PRESS, binds[4], extraArgs=[button])
            button.bind(DGG.B1RELEASE, binds[5])

    def update_canvas_size(self):
        # reset base canvas size
        self.scroll_frame['canvasSize'] = MG.BASE_CANVAS_SIZE

        button_total = len(self.current_button_set) - 2

        if button_total > MG.CANVAS_LIMIT:
            # extra buttons is any buttons over the canvas limit
            extra_buttons = button_total - MG.CANVAS_LIMIT

            """Extra rows are the rows beyond the top visible rows.
            We round up since it doesn't matter whether there is one
            or three buttons in the row. As long as there is at least one
            button, we count it as a new row."""
            extra_rows = math.ceil(extra_buttons / MG.CANVAS_COLUMNS)

            # this is the total amount the canvas will be decreased by
            decrease = -extra_rows * MG.CANVAS_INCREMENT_Z

            # the current size of the scroll frame canvas
            bottom_size = self.scroll_frame['canvasSize'][2]
            new_size = (-1, 1, decrease + bottom_size, 1)

            self.scroll_frame['canvasSize'] = new_size

    def update_canvas_range(self):
        button_total = len(self.current_button_set) - 2

        scroll_range = (0, 1)
        # Add to the amount of scrolling ticks mmb can do.
        if button_total > MG.CANVAS_LIMIT:
            button_total = len(self.current_button_set) - 2
            extra_buttons = button_total - MG.CANVAS_LIMIT
            # All this is explained in the function above.
            extra_rows = math.ceil(extra_buttons / MG.CANVAS_COLUMNS)
            scroll_range = (0, extra_rows)

        self.scroll_frame['verticalScroll_range'] = scroll_range

    def load_picture_list(self, mode, database_dict, set_list, binds,
                          color=None):
        if mode == 'Texture':  # load the json file
            json_path = f"{G.DATABASE_DIRECTORY}{G.TEXTURE_LIBRARY}.json"
            texture_json = json.loads(open(json_path).read())

        i = 0
        x, z, = [MG.CANVAS_START_X, MG.CANVAS_START_Z]
        self.current_button_set = []
        for name in database_dict:
            # slice up any complex names
            split_name = name.split("|")[0]
            if split_name in G.SPECIAL_NODES:
                continue # skip over special nodes.

            filepath = f"{G.EDITOR}{mode}/{split_name}.png"
            if mode == 'Texture':  # load the actual file.
                filepath = texture_json[split_name]

            try:
                geom = PlaneModel(filepath, reload=True)
            except OSError:
                continue

            button = DirectButton(parent=self.scroll_frame.getCanvas(),
                                  geom=geom,
                                  pos=(x, 0, z), scale=MG.CANVAS_BUTTON_SCALE,
                                  frameVisibleScale=(.91, .91), pad=(.2, .2),
                                  pressEffect=0)
            if color:
                button['frameColor'] = color
            button.set_name(name)  # we'll need the name later on.
            self.bind_button(button, binds)
            self.current_button_set.append(button)

            i += 1
            if i % MG.CANVAS_COLUMNS == 0 and i != 0:
                x = MG.CANVAS_START_X
                z -= MG.CANVAS_INCREMENT_Z
            else:
                x += MG.CANVAS_INCREMENT_X

        set_list(self.current_button_set)
        self.update_canvas_size()
        self.update_canvas_range()

    def set_current_button_set(self, buttons):
        self.current_button_set = buttons

    def set_scroll_frame(self, scroll_frame):
        self.scroll_frame = scroll_frame
