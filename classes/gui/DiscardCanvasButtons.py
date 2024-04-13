import os

from direct.gui.DirectGui import DGG

from classes.file.HandleJsonData import delete_json_entries
from classes.file.HandleXMLData import delete_xml_entries
from classes.settings import Globals as G

RED_COLOR = (.9, .4, .4, 1)
BASE_GUI_COLOR = (.8, .8, .8, 1)
BRIGHT_RED = (.9, 0, 0, 1)


class DiscardCanvasButtons:

    def __init__(self, menu_name, preview_menu, reload_menu, scroll_frame,
                 trash_button, confirm_button, left_button,
                 json=False, xml=False):
        self.menu_name = menu_name
        # preview menu stores the mode types
        self.preview_menu = preview_menu
        self.reload_menu = reload_menu
        self.scroll_frame = scroll_frame
        self.trash_button = trash_button
        self.confirm_button = confirm_button
        self.left_button = left_button
        self.trash_mode = False
        self.frame_buttons = []
        self.discarded_buttons = []
        self.discarded_names = []
        self.last_button_color = (1, 1, 1, 1)
        self.last_color_scale = (.75, .75, .75, 1)
        self.json = json
        self.xml = xml

        self.bind()

    def bind(self):
        self.trash_button['command'] = self.toggle_trash_mode
        self.confirm_button['command'] = self.confirm_removal

    def toggle_trash_mode(self, restore=True):
        self.trash_mode = not self.trash_mode
        # reset preview window
        self.preview_menu.set_mode()

        self.preview_menu.disable_all_buttons(self.trash_mode)
        if self.trash_mode:
            self.enable_trash_mode()
        else:
            self.disable_trash_mode(restore)
            self.refresh_lists()

        self.define_button_colors()

    def define_button_colors(self):
        if self.frame_buttons:
            first_button = self.frame_buttons[0]
            self.last_button_color = first_button['frameColor']
            self.last_color_scale = first_button.get_color_scale()

    def enable_trash_mode(self):
        self.confirm_button.show()
        self.left_button.hide()
        self.trash_button['frameColor'] = RED_COLOR
        self.trash_button.set_color_scale(.9, .75, .75, 1)
        self.update_button_commands(self.discard)

    def disable_trash_mode(self, restore):
        self.confirm_button.hide()
        self.left_button.show()
        self.trash_button['frameColor'] = BASE_GUI_COLOR
        self.trash_button.set_color_scale(1, 1, 1, 1)
        if restore:
            self.update_button_commands(None)
            self.restore_selected_buttons()

    def update_button_commands(self, command):
        self.determine_frame_buttons()
        # store the buttons commands before overwriting them
        for button in self.frame_buttons:
            button['command'] = command
            if command:
                button['extraArgs'] = [button]

    def discard(self, button):
        button.set_color_scale(.85, .85, .85, 1)
        button['frameColor'] = BRIGHT_RED
        button['relief'] = DGG.SUNKEN
        button['command'] = self.restore
        self.discarded_buttons.append(button)

    def restore(self, button):
        button.set_color_scale(self.last_color_scale)
        button['frameColor'] = self.last_button_color
        button['relief'] = DGG.RAISED
        button['command'] = self.discard
        index = self.discarded_buttons.index(button)
        self.discarded_buttons.pop(index)

    def confirm_removal(self):
        mode = self.preview_menu.mode
        self.remove_discarded_files(mode)

        if self.json:
            delete_json_entries(mode, self.discarded_names)
        if self.xml:
            delete_xml_entries(mode, self.discarded_names)
        self.reload_menu.reload()
        self.toggle_trash_mode(restore=False)

    def remove_discarded_files(self, mode):
        for button in self.discarded_buttons:
            # store these names, so we can remove them from the database.
            name = button.get_name()
            self.discarded_names.append(name)

            if self.json:  # remove the image file
                image_path = (base.root_folder +
                              f"{G.RESOURCES}{G.EDITOR}{mode}/{name}{G.PNG}")
                self.remove_file(image_path)

    def remove_file(self, image_path):
        if self.preview_menu.mode == 'Texture':
            return  # no image file is saved for textures.

        try:
            os.remove(image_path)
        except FileNotFoundError as FNFE:
            print(FNFE)

    def restore_selected_buttons(self):
        for button in self.frame_buttons:
            button.set_color_scale(*self.last_color_scale)
            button['frameColor'] = self.last_button_color
            button['command'] = None
            button['relief'] = DGG.RAISED

    def refresh_lists(self):
        self.frame_buttons = []
        self.discarded_buttons = []
        self.discarded_names = []

    def determine_frame_buttons(self):
        mode_class = self.preview_menu.get_mode_class()
        self.frame_buttons = mode_class.get_buttons_dict[self.menu_name]()
