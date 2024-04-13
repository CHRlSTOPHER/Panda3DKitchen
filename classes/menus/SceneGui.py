from direct.gui.DirectGui import (DirectFrame, DirectButton,
                                  DirectScrolledFrame)

from classes.props.PlaneModel import PlaneModel
from classes.settings import Globals as G
from classes.menus import MenuGlobals as MG


class SceneGui:

    def __init__(self):
        self.scene_window = None
        self.scene_scroll = None
        self.scene_title = None
        self.scene_inspect = None
        self.scene_trash = None
        self.computer_font = loader.load_font(f"{G.EDITOR}{MG.COMPUTER_FONT}")

        self.load_gui()

    def load_gui(self):
        trash_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.TRASH)
        inspect_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.INSPECT)
        window_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.MENU_VERT_1)
        check_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.CHECK_TEXTURE)

        self.scene_frame = DirectFrame(parent=base.a2dLeftCenter,
                                        geom=window_geom,
                                        pos=(0.502, 0.0, -0.003),
                                        scale=(0.493, 0.697, 0.571),
                                        suppressMouse=0)
        self.scene_frame.hide()

        self.scene_scroll = DirectScrolledFrame(
            parent=self.scene_frame,
            pos=(-0.001, 0.0, 0.102),
            scale=(1.777, 0.955, 1.277),
            canvasSize=MG.BASE_CANVAS_SIZE,
            frameColor=MG.SCROLL_FRAME_COLOR,
            autoHideScrollBars=False)
        self.scene_scroll.horizontalScroll.hide()
        self.scene_scroll.verticalScroll['frameColor'] = (.5, .5, .5, 1)

        self.scene_title = DirectFrame(parent=self.scene_frame,
                                       text_font=self.computer_font,
                                       text_fg=(1, 1, 1, 1),
                                       frameVisibleScale=(0, 0),
                                       text="SCENE ITEMS", pad=(0, 0),
                                       pos=(-0.483, 0.0, 0.843),
                                       scale=(0.16, 0.196, 0.106))
        self.scene_inspect = DirectButton(self.scene_frame,
                                          geom=inspect_geom,
                                          pos=(-0.441, 0.0, -0.732),
                                          scale=(0.214, 0.199, 0.172),
                                          pad=(0.993, 0.057))
        self.scene_trash = DirectButton(self.scene_frame, geom=trash_geom,
                                        pos=(0.456, 0.0, -0.732),
                                        scale=(0.202, 0.142, 0.19),
                                        pad=(1.11, -0.054))
        self.scene_confirm = DirectButton(self.scene_frame,
                                  geom=check_geom,
                                  pos=(-0.438, 0.0, -0.735),
                                  scale=(0.229, 0.142, 0.187),
                                  pad=(0.873, -0.054))