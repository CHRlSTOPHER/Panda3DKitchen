from direct.gui.DirectGui import (DirectFrame, DirectButton,
                                  DirectScrolledFrame)

from classes.menus import MenuGlobals as MG
from classes.props.PlaneModel import PlaneModel
from classes.settings import Globals as G


class LibraryGui:

    def __init__(self):
        self.library_window = None
        self.library_scroll = None
        self.library_title = None
        self.library_folder = None
        self.library_trash = None
        self.computer_font = loader.load_font(f"{G.EDITOR}{MG.COMPUTER_FONT}")

        self.load_gui()

    def load_gui(self):
        folder_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.FOLDER)
        trash_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.TRASH)
        window_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.MENU_VERT_1)
        check_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.CHECK_TEXTURE)
        swap_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.SWAP_TEXTURE)

        self.library_window = DirectFrame(parent=base.a2dLeftCenter,
                                          geom=window_geom,
                                          pos=(0.502, 0.0, -0.003),
                                          scale=(0.493, 0.697, 0.571),
                                          suppressMouse=0)

        self.library_scroll = DirectScrolledFrame(
            parent=self.library_window,
            pos=(-0.001, 0.0, 0.102),
            scale=(1.777, 0.955, 1.277),
            canvasSize=MG.BASE_CANVAS_SIZE,
            frameColor=MG.SCROLL_FRAME_COLOR,
            autoHideScrollBars=False)
        self.library_scroll.horizontalScroll.hide()
        self.library_scroll.verticalScroll['frameColor'] = (.5, .5, .5, 1)

        self.library_title = DirectFrame(parent=self.library_window,
                                         text_font=self.computer_font,
                                         text_fg=(1, 1, 1, 1),
                                         frameVisibleScale=(0, 0),
                                         text="LIBRARY ITEMS",
                                         pos=(-0.42, 0.0, 0.846),
                                         scale=(0.154, 0.181, 0.1))

        self.swap_button = DirectButton(parent=self.library_window,
                                        geom=swap_geom,
                                        pos=(0.801, 0.0, 0.873),
                                        scale=(0.061, 0.097, 0.055),
                                        pad=(0.282, 0.156))

        self.library_folder = DirectButton(self.library_window,
                                           geom=folder_geom,
                                           pos=(-0.441, 0.0, -0.732),
                                           scale=(0.22, 0.205, 0.178),
                                           pad=(0.939, 0.012))

        self.library_trash = DirectButton(self.library_window, geom=trash_geom,
                                          pos=(0.456, 0.0, -0.732),
                                          scale=(0.202, 0.142, 0.19),
                                          pad=(1.11, -0.054))

        self.library_confirm = DirectButton(self.library_window,
                                            geom=check_geom,
                                            pos=(-0.438, 0.0, -0.735),
                                            scale=(0.229, 0.142, 0.187),
                                            pad=(0.873, -0.054))
        self.library_confirm.hide()
