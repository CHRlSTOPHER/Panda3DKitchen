import json

from direct.gui.DirectGui import DirectFrame, DirectEntry, DGG

from classes.menus import MenuGlobals as MG
from classes.props.PlaneModel import PlaneModel
from classes.settings import Globals as G


class SceneWindowGui(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, parent=aspect2d)
        self.scene_window = None
        self.fov_title = None
        self.fov_entry = None

        self.initialiseoptions(SceneWindowGui)
        self.load_gui()

    def load_gui(self):
        window_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.MENU_HOR_2)
        self.scene_window = DirectFrame(parent=aspect2d,
                                        geom=window_geom,
                                        geom_pos=(0, 0, -.125),
                                        geom_scale=(1, 1, .89),
                                        pos=(0.0, 0.0, 0.072),
                                        scale=(0.884, 0.909, 0.639),
                                        frameVisibleScale=(0, 0),
                                        suppressMouse=0)
        self.scene_window.set_name('scene_window')
        self.scene_window['state'] = DGG.NORMAL

        self.fov_title = DirectFrame(parent=self.scene_window,
                                     text="FOV", relief=0,
                                     pos=(-0.867, 0.0, -0.939),
                                     scale=(0.067, 0.088, 0.088))

        settings = json.loads(open(G.SETTINGS_JSON).read())
        self.fov_entry = DirectEntry(parent=self.scene_window,
                                     pos=(-0.753, 0.0, -0.936),
                                     scale=(0.073, 0.1, 0.1), width=2,
                                     initialText=str(settings['fov']),
                                     frameVisibleScale=(0, 0))
