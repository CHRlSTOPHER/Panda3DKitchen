import os

from direct.gui.DirectGui import DGG

from classes.file.HandleJsonData import delete_json_entries
from classes.file.HandleXMLData import delete_xml_entries
from classes.settings import Globals as G
from classes.menus import MenuGlobals as MG

RED_COLOR = (.901, .4105, .4105, 1.0)
BASE_GUI_COLOR = (.8, .8, .8, 1)
BRIGHT_RED = (.91, .01, .01, 1.00)


class DiscardCanvasButtons:

    def __init__(self, menu_name, kitchen, reload_menu, scroll_frame,
                 trash_button, confirm_button, left_button,
                 command=None, json=False, xml=False):
        self.kitchen = kitchen
        self.menu_name = menu_name
        self.preview_menu = kitchen.preview_menu
        self.reload_menu = reload_menu
        self.scroll_frame = scroll_frame
        self.trash_button = trash_button
        self.confirm_button = confirm_button
        self.left_button = left_button
        self.command = command
        self.trash_mode = False
        self.mode = None
        self.frame_buttons = []
        self.discarded_buttons = []
        self.discarded_names = []
        self.color_scale = None
        self.frame_color = None
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

    def enable_trash_mode(self):
        self.confirm_button.show()
        self.left_button.hide()
        self.trash_button['frameColor'] = RED_COLOR
        self.trash_button.set_color_scale(.9, .75, .75, 1)
        self.update_button_commands(self.discard)
        self.restore_buttons(command=False)  # clear selected button coloring.
        self.kitchen.node_mover.deselect_node()

    def disable_trash_mode(self, restore):
        self.confirm_button.hide()
        self.left_button.show()
        self.trash_button['frameColor'] = BASE_GUI_COLOR
        self.trash_button.set_color_scale(1, 1, 1, 1)
        if restore:
            self.update_button_commands(None)
            self.restore_buttons()

        # reapply node selection
        last_node = self.kitchen.scene_menu.last_node
        last_button = self.kitchen.scene_menu.get_last_button()
        if last_node and last_button:
            self.kitchen.node_mover.set_node(last_node)
            last_button['frameColor'] = MG.SELECTED_BUTTON_COLOR

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
        self.handle_scene_node(button)

    def restore(self, button):
        self.handle_scene_node(button, force_clear=True)
        button.set_color_scale(self.color_scale)
        button['frameColor'] = self.frame_color
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
            delete_xml_entries(self.kitchen.project_location,
                               mode, self.discarded_names)
        self.reload_menu.reload()
        self.toggle_trash_mode(restore=False)

    def remove_discarded_files(self, mode):
        for button in self.discarded_buttons:
            # store these names, so we can remove them from the database.
            name = button.get_name()
            self.discarded_names.append(name)

            if self.json:  # remove the image file
                image_path = (self.kitchen.root_folder +
                              f"{G.RESOURCES}{G.EDITOR}{mode}/{name}{G.PNG}")
                self.remove_file(image_path)

    def remove_file(self, image_path):
        if self.preview_menu.mode == 'Texture':
            return  # no image file is saved for textures.

        try:
            os.remove(image_path)
        except FileNotFoundError as FNFE:
            print(FNFE)

    def restore_buttons(self, command=True):
        for button in self.frame_buttons:
            button.set_color_scale(*self.color_scale)
            self.handle_scene_node(button, force_clear=True)

            button['frameColor'] = self.frame_color
            if command:
                button['command'] = self.command
                button['relief'] = DGG.RAISED

    def refresh_lists(self):
        self.frame_buttons = []
        self.discarded_buttons = []
        self.discarded_names = []

    def determine_frame_buttons(self):
        mode_class = self.preview_menu.get_mode_class()
        self.mode = self.preview_menu.get_mode()  # we use this later.
        self.frame_buttons = mode_class.get_buttons_dict[self.menu_name]()
        self.color_scale = MG.ENABLED_COLOR
        self.frame_color = MG.FRAME_COLOR[self.menu_name]

    def handle_scene_node(self, button, node=None, force_clear=False):
        # check if the node is a scene node
        name_arg_length = len(button.get_name().split("|"))
        if name_arg_length == MG.SCENE_NAME_ARGS:
            node = self.kitchen.scene_menu.get_node_by_name(button.get_name())

        if node:
            r, g, b, a = node.get_color_scale()
            color_scale = [round(color, 2) for color in [r, g, b, a]]
            if force_clear:
                node.clear_color_scale()
            elif color_scale == [*BRIGHT_RED]:
                # the user is deselecting the node. restore it to normal.
                node.clear_color_scale()
                self.restore(button)
            else:
                node.set_color_scale(BRIGHT_RED)
