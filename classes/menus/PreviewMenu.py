from os import listdir
from os.path import isfile, join

from panda3d.core import Fog, NodePath
from direct.interval.IntervalGlobal import Sequence, LerpFunc, Func
from direct.gui.DirectGui import DGG

from classes.menus.PreviewGui import PreviewGui
from classes.menus.PreviewModes import (ActorMenu, PropMenu,
                                        TextureMenu, ParticleMenu)
from classes.props.PlaneModel import PlaneModel
from classes.scene.SceneWindow import SCENE_REGION
from classes.settings import Globals as G

DISABLED_COLOR = (.9, .9, .9, 1)
ENABLED_COLOR = (1, 1, 1, 1)
ENTITY_FRAME_POS = [0.0, 0.0, -0.159]
ENTITY_FRAME_SCALE = [0.514, 0.943, 0.713]
MINI_FRAME_POS = [0.5, 0.0, -0.267]
MINI_FRAME_SCALE = [0.49, 0.919, 0.689]

MODES = {
    'Actor': ActorMenu,
    'Prop': PropMenu,
    'Texture': TextureMenu,
    'Particle': ParticleMenu,
}
BG_PATH = f"{G.RESOURCES}{G.EDITOR}bgs"


class PreviewMenu(PreviewGui):

    def __init__(self):
        PreviewGui.__init__(self)
        self.preview_bg = None
        self.preview_window = None
        self.kitchen = None
        self.preview_render = None
        self.preview_cam = None
        self.preview_buffer = None
        self.within = False
        self.fog = None
        self.bg_textures = []
        self.current_bg = 0
        self.item_name = None
        self.item_location = None
        self.mode = 'Actor'
        self.modes = {}
        self.mode_buttons = []
        self.last_mode = None
        self.add_item = False
        self.mini_window = False
        self.hide_preview_nodes = []
        self.last_disabled_button = None

    def generate(self):
        self.load_gui()
        self.load_preview_buttons()
        for name, mode in MODES.items():
            self.modes[name] = mode()
            self.modes[name].set_kitchen(self.kitchen)

        self.load_preview_region()
        self.add_fog()
        self.load_backgrounds()
        self.bind_buttons()
        self.hide_special_buttons()
        self.change_preview_size()

        # load assets
        for mode in ['Particle', 'Texture', 'Prop', 'Actor']:  # reverse order
            self.set_mode(mode, self.entity_mode_buttons[mode], reload=True)

    def load_preview_region(self):
        self.preview_window = PlaneModel(pos=(0.0133, 0, 0.0788),
                                         scale=(.87, 1, .655))
        self.preview_buffer = self.kitchen.win.make_texture_buffer('preview',
                                                                   512, 512)
        self.preview_cam = self.kitchen.make_camera(self.preview_buffer)
        self.preview_render = NodePath('preview_render')

        self.preview_cam.reparent_to(self.preview_render)
        self.preview_window.set_texture(self.preview_buffer.get_texture(), 1)
        self.preview_window.reparent_to(self.entity_frame)
        self.preview_cam.node().get_lens().set_fov(G.PREVIEW_FOV)
        self.preview_buffer.set_active(1)

        # preview bg
        self.preview_bg = PlaneModel(pos=(0, 1000, 0), scale=320)
        self.preview_bg.reparent_to(self.preview_render)

        # define this here since this we finally defined preview_window.
        self.hide_preview_nodes = [self.preview_window,
                                   self.left_arrow, self.right_arrow]

    def add_fog(self):
        self.fog = Fog("Photo Fog")  # Play on Photo Fun
        self.fog.set_color(1, 1, 1)
        self.fog.set_exp_density(0)
        self.preview_render.set_fog(self.fog)

    def load_backgrounds(self):
        self.bg_textures = []
        for item in listdir(BG_PATH):
            if isfile(join(BG_PATH, item)):
                texture = self.kitchen.load_texture(f"{G.EDITOR}bgs/{item}")
                self.bg_textures.append(texture)

        if self.bg_textures:  # Make sure there's actually a file lol.
            self.preview_bg.set_texture(self.bg_textures[0])

    def bind_buttons(self):
        for name in self.entity_mode_buttons:
            button = self.entity_mode_buttons[name]
            button['command'] = self.set_mode
            button['extraArgs'] = [name, button]
            self.mode_buttons.append(button)

        self.left_arrow['command'] = self.change_background
        self.right_arrow['command'] = self.change_background
        self.shrink_icon['command'] = self.change_preview_size
        self.camera_button['command'] = (self.kitchen.library_menu.
                                         handle_image_data)
        self.modes[self.mode].define_rng_button(self.random_anim_button)
        self.cancel_button['command'] = self.cancel_preview

        self.entity_frame.bind(DGG.WITHIN, self.set_within, extraArgs=[True])
        self.entity_frame.bind(DGG.WITHOUT, self.set_within, extraArgs=[False])

    def change_background(self, direction):
        self.current_bg += direction

        if self.current_bg > len(self.bg_textures) - 1:  # overflow
            self.current_bg = 0
        elif self.current_bg < 0:  # underflow
            self.current_bg = len(self.bg_textures) - 1

        if self.bg_textures:
            self.preview_bg.set_texture(self.bg_textures[self.current_bg], 1)

    def change_preview_size(self):
        self.mini_window = not self.mini_window
        if self.mini_window:
            self.show_mini_window()
            self.toggle_scene_objects(True)
        else:
            self.hide_mini_window()
            self.toggle_scene_objects(False)

    def toggle_scene_objects(self, toggle):
        if self.kitchen.node_mover and self.kitchen.camera_mover:
            if toggle:
                self.kitchen.node_mover.enable_entries()
                self.kitchen.node_mover.set_click(True)
                self.kitchen.camera_mover.enable()
            else:
                self.kitchen.node_mover.disable_entries()
                self.kitchen.node_mover.set_click(False)
                self.kitchen.camera_mover.disable()

    def show_mini_window(self):
        self.cancel_preview()  # close preview if they have it open
        self.entity_button_frame.wrt_reparent_to(self.mini_frame)
        self.entity_title.wrt_reparent_to(self.mini_frame)
        self.entity_frame.reparent_to(self.kitchen.a2dBottomLeft)

        self.entity_button_frame.set_pos(-0.006, 0.0, 2.286)
        self.entity_frame.set_pos(*MINI_FRAME_POS)
        self.entity_frame.set_scale(*MINI_FRAME_SCALE)
        self.entity_frame['frameSize'] = (-.98, .98, .420, .99)
        self.entity_frame['geom_scale'] = (0, 0, 0)

        self.kitchen.scene_region.set_dimensions(*SCENE_REGION)
        self.mini_frame.show()
        self.kitchen.scene_window.get_window().show()
        for node in self.hide_preview_nodes:
            node.hide()

    def hide_mini_window(self):
        self.entity_button_frame.wrt_reparent_to(self.entity_frame)
        self.entity_title.wrt_reparent_to(self.entity_frame)
        self.entity_frame.reparent_to(self.kitchen.aspect2d)

        self.entity_button_frame.set_pos((0, 0, 0))
        self.entity_frame.set_pos(*ENTITY_FRAME_POS)
        self.entity_frame.set_scale(*ENTITY_FRAME_SCALE)
        self.entity_frame['frameSize'] = (-1, 1, -1, 1)
        self.entity_frame['geom_scale'] = (1, 1, 1)

        self.kitchen.scene_region.set_dimensions(0, 0, 0, 0)
        self.mini_frame.hide()
        self.kitchen.scene_window.get_window().hide()
        for node in self.hide_preview_nodes:
            node.show()

    def cancel_preview(self):
        self.set_mode(reload=False)

    def set_mode(self, mode=None, disable_button=None, reload=False):
        # clean up any leftover assets
        if not mode:
            self.modes[self.mode].cleanup_entity()
        else:
            self.last_mode = mode
            self.modes[mode].cleanup_entity()
            self.mode = mode
            # update the buttons that are enabled and disabled.
            self.change_button_states(disable_button)
            self.change_menu_buttons('library')
            self.change_menu_buttons('scene')

        if reload:
            # load the new data from the specified library.
            self.kitchen.library_menu.reload()
            self.kitchen.scene_menu.reload()

        # update canvas sizes
        library_buttons = self.get_mode_class().library_buttons
        scene_buttons = self.get_mode_class().scene_buttons
        self.kitchen.library_menu.update_canvas_size(library_buttons)
        self.kitchen.scene_menu.update_canvas_size(scene_buttons)

        self.hide_special_buttons()  # buttons used for specific modes

    def change_button_states(self, disable_button):
        i = 0
        for mode in MODES:
            button = self.mode_buttons[i]
            button['state'] = DGG.NORMAL
            button['relief'] = DGG.RAISED
            button.set_color_scale(ENABLED_COLOR)
            geom = PlaneModel(f"{G.EDITOR}/maps/add-{mode}.png")
            button['geom'].remove_node()
            button['geom'] = geom
            i += 1

        if not disable_button:
            disable_button = self.entity_mode_buttons.get(self.last_mode)
        disable_button['state'] = DGG.DISABLED  # disable click
        colored_geom = PlaneModel(
            f"{G.EDITOR}/maps/add-{self.mode}-color.png")
        disable_button.set_color_scale(DISABLED_COLOR)
        colored_geom.set_color_scale(1.1, 1.1, 1.1, 1)
        disable_button['geom'] = colored_geom
        disable_button['relief'] = DGG.SUNKEN
        self.last_disabled_button = disable_button

    def disable_all_buttons(self, disable):
        if disable:
            for i in range(len(MODES)):
                button = self.mode_buttons[i]
                button['state'] = DGG.DISABLED
                button.set_color_scale(.5, .5, .5, 1)
        else:
            self.change_button_states(self.last_disabled_button)

    def change_menu_buttons(self, key):
        for name in self.modes:
            button_list = self.modes[name].get_buttons_dict[key]()
            for button in button_list:
                button.hide()

        button_list = self.modes[self.mode].get_buttons_dict[key]()
        for button in button_list:
            button.show()

    def flash_screen(self):
        mode_class = self.get_mode_class()

        def flash(density):
            self.fog.set_exp_density(density)

        def fade(alpha):
            mode_class.entity.set_alpha_scale(alpha)

        Sequence(
            LerpFunc(flash, duration=.35, fromData=0, toData=1),
            LerpFunc(flash, duration=.35, fromData=1, toData=0),
            LerpFunc(fade, duration=.3, fromData=1, toData=0),
            Func(mode_class.cleanup_entity),
        ).start()

    def hide_special_buttons(self):
        self.camera_button.hide()
        self.random_anim_button.hide()
        self.cancel_button.hide()
        self.entity_button_frame.show()

    def show_dice(self):
        self.random_anim_button.show()

    def show_preview_buttons(self, _camera):
        self.entity_button_frame.hide()
        if _camera:
            self.camera_button.show()
        self.cancel_button.show()

    def get_mode(self):
        return self.mode

    def get_mode_class(self):
        return self.modes[self.mode]

    def set_within(self, state, mouse_data):
        self.within = state

    def get_within(self):
        return self.within

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
        super().set_kitchen(kitchen)
