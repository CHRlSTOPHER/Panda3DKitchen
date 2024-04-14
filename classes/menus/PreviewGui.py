from direct.gui.DirectGui import DirectFrame, DirectButton, DGG

from classes.props.PlaneModel import PlaneModel
from classes.settings import Globals as G
from classes.menus import MenuGlobals as MG


class PreviewGui(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, parent=base.a2dBottomLeft)
        self.initialiseoptions(PreviewGui)
        self.entity_frame = None
        self.entity_title = None
        self.mini_frame = None
        self.left_arrow = None
        self.right_arrow = None
        self.shrink_icon = None
        self.entity_button_frame = None
        self.entity_mode_buttons = {}
        self.camera_button = None
        self.random_anim_button = None
        self.cancel_button = None

        self.load_gui()
        self.load_preview_buttons()

    def load_gui(self):
        # define all the geom
        window_geom1 = PlaneModel(MG.EDITOR_MAP_PATH + MG.MENU_VERT_1)
        window_geom2 = PlaneModel(MG.EDITOR_MAP_PATH + MG.MENU_HOR_1)

        ''' PREVIEW WINDOW GUI '''
        self.entity_frame = DirectFrame(parent=self, pad=(0, 0),
                                        geom=window_geom1, suppressMouse=0)
        self.entity_frame.set_name('preview_window')
        # bind frame to check for click and drags.
        self.entity_frame['state'] = DGG.NORMAL

        self.entity_title = DirectFrame(parent=self.entity_frame,
                                        text_font=base.computer_font,
                                        text_fg=(1, 1, 1, 1),
                                        frameVisibleScale=(0, 0),
                                        text="MODE PREVIEW", pad=(0, 0),
                                        pos=(-0.458, 0.0, 0.858),
                                        scale=(0.136, 0.16, 0.085))

        self.entity_button_frame = DirectFrame(parent=self.entity_frame)

        self.mini_frame = DirectFrame(parent=self.entity_frame,
                                      geom=window_geom2,
                                      pos=(0.0, 0.0, 0.699),
                                      scale=(0.997, 1.0, 0.292),
                                      pad=(0, 0))
        self.mini_frame.hide()

        # The 6 entity buttons
        for text, pos, scale, pad in MG.ENTITY_MODE_BUTTONS:
            geom = PlaneModel(f'editor/maps/add-{text}.png')
            button = DirectButton(parent=self.entity_button_frame,
                                  geom=geom,
                                  pos=pos, scale=scale, pad=pad,
                                  frameVisibleScale=(.95, .95))
            self.entity_mode_buttons[text] = button

    def load_preview_buttons(self):
        cam_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.CAMERA_TEXTURE)
        dice_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.DICE_TEXTURE)
        cancel_geom = PlaneModel(MG.EDITOR_MAP_PATH + MG.CANCEL_TEXTURE)

        # arrows to swap between backgrounds
        self.left_arrow = DirectButton(parent=self.entity_frame, text="<",
                                       pos=(-0.933, 0.0, 0.036),
                                       scale=(0.196, 0.265, 0.184),
                                       pad=(0.117, 0.735),
                                       extraArgs=[-1])
        self.right_arrow = DirectButton(parent=self.entity_frame, text=">",
                                        pos=(0.927, 0.0, 0.042),
                                        scale=(0.196, 0.163, 0.175),
                                        pad=(0.132, 0.834),
                                        extraArgs=[1])
        self.shrink_icon = DirectButton(parent=self.entity_frame,
                                        text="-",
                                        pos=(0.789, 0.0, 0.837),
                                        scale=(0.307, 0.463, 0.223),
                                        pad=(0.039, 0.081))

        self.camera_button = DirectButton(parent=self.entity_frame,
                                          geom=cam_geom,
                                          pos=(-0.564, 0.0, -0.754),
                                          scale=(0.246, 0.168, 0.174),
                                          pad=(0.18, -0.111),
                                          frameVisibleScale=(.95, .95))

        self.random_anim_button = DirectButton(parent=self.entity_frame,
                                               geom=dice_geom,
                                               pos=(0.03, 0.0, -0.754),
                                               scale=(0.228, 0.156, 0.156),
                                               pad=(0.255, -0.009),
                                               frameVisibleScale=(
                                                   .95, .95))
        self.cancel_button = DirectButton(parent=self.entity_frame,
                                          geom=cancel_geom,
                                          pos=(0.612, 0.0, -0.751),
                                          scale=(0.213, 0.135, 0.144),
                                          pad=(0.315, 0.066),
                                          frameVisibleScale=(.95, .95))
