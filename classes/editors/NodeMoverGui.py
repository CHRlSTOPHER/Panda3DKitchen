from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectGui import DirectFrame

from classes.menus import MenuGlobals as MG
from classes.props.PlaneModel import PlaneModel

DIRECT_POS = [
    ['X', (-0.689, 0.763, 0.172)],
    ['Y', (-0.689, 0.0, -0.222)],
    ['Z', (-0.689, 0.0, -0.621)],
    ['H', (-0.109, 0.763, 0.172)],
    ['P', (-0.109, 0.0, -0.222)],
    ['R', (-0.109, 0.0, -0.621)],
    ['SX', (0.476, 0.0, 0.174)],
    ['SY', (0.476, 0.0, -0.224)],
    ['SZ', (0.476, 0.0, -0.62)],
]


class NodeMoverGui(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, parent=base.a2dTopCenter)
        self.initialiseoptions(NodeMoverGui)
        self.entries = []

        self.load_gui()

    def load_gui(self):
        geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.MENU_HOR_3)
        self.mover_frame = DirectFrame(parent=self, geom=geom,
                                       pos=(0.0, 0.0, -0.219),
                                       scale=(0.511, 0.424, 0.211))

        self.mover_title = DirectFrame(parent=self.mover_frame,
                                       text_font=base.computer_font,
                                       text_fg=(1, 1, 1, 1), relief=0,
                                       text="NODE MOVER",
                                       pos=(-0.639, 0.0, 0.69),
                                       scale=(0.106, 0.166, 0.205))
        # base.gui_editor.set_gui(self.mover_title)

        for label, pos in DIRECT_POS:
            self.create_direct_entry(label, pos)

    def create_direct_entry(self, label, pos, text="0.00"):
        if label[0] == "S":
            text = "1.00"
        entry = DirectEntry(parent=self.mover_frame, initialText=text,
                            pos=pos, width=4, scale=(0.088, 0.763, 0.253),
                            geom_scale=(.75, .75, .75), relief=0)
        entry.set_name(label)

        DirectFrame(parent=self.mover_frame, text=label, relief=0,
                    pos=(pos[0]-.124, pos[1], pos[2]-.011),
                    scale=(0.1, 0.766, 0.256), text_fg=(0, 0, 0, 1))
        self.entries.append(entry)
