from direct.gui.DirectGui import DGG

from classes.gui.CanvasButtons import CanvasButtons
from classes.menus.MenuBinder import bind_frame_scrolling
from classes.menus import MenuGlobals as MG


class CanvasMenu:

    def __init__(self, preview_menu, window, scroll, menu_name):
        self.preview_menu = preview_menu
        self.window = window
        self.scroll = scroll
        self.menu_name = menu_name
        self.mode_class_buttons = None
        self.canvas_buttons = None
        self.within = False

    def generate_canvas(self):
        self.canvas_buttons = CanvasButtons()
        self.canvas_buttons.set_scroll_frame(self.scroll)
        self.bind_canvas_gui()

    def bind_canvas_gui(self):
        bind_frame_scrolling(self.scroll, self.scroll_up, self.scroll_down)
        self.window.bind(DGG.WITHIN, self.set_within, extraArgs=[True])
        self.window.bind(DGG.WITHOUT, self.set_within, extraArgs=[False])

    def update_canvas_size(self, buttons):
        self.canvas_buttons.set_current_button_set(buttons)
        self.canvas_buttons.update_canvas_size()
        self.canvas_buttons.update_canvas_range()

    def load_picture_list(self, data_dict, button_increase=False,
                          button_copy=None, add_to_scene=None, color=None):
        mode = self.preview_menu.get_mode()
        class_mode = self.preview_menu.get_mode_class()
        frame_buttons = class_mode.set_buttons_dict[self.menu_name]
        bind_list = [self.scroll_up, self.scroll_down]

        if button_increase:
            bind_list.append(self.button_increase)
            bind_list.append(self.button_decrease)
        if button_copy:
            bind_list.append(button_copy)
        if add_to_scene:
            bind_list.append(add_to_scene)

        self.canvas_buttons.load_picture_list(mode, data_dict,
                                              frame_buttons, bind_list,
                                              color=color)

    def scroll_up(self, mouse_data):
        self.scroll[MG.VALUE] -= 1

    def scroll_down(self, mouse_data):
        self.scroll[MG.VALUE] += 1

    def button_increase(self, button, mouse_data):
        sx, sy, sz = button.get_scale()
        scale = (sx * 1.16, 1, sz * 1.16)
        button.set_scale(scale)

    def button_decrease(self, button, mouse_data):
        sx, sy, sz = button.get_scale()
        scale = (sx / 1.16, 1, sz / 1.16)
        button.set_scale(scale)

    def set_preview_menu(self, menu):
        self.preview_menu = menu

    def set_within(self, state, mouse_data):
        self.within = state

    def get_within(self):
        return self.within
