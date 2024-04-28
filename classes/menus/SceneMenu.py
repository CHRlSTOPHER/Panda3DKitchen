from panda3d.core import Filename, NodePath
from direct.gui.DirectGui import DirectButton

from classes.apps import AppGlobals as AG
from classes.file.HandleXMLData import append_node_data, get_node_data
from classes.gui.DiscardCanvasButtons import DiscardCanvasButtons
from classes.menus.CanvasMenu import CanvasMenu
from classes.menus.SceneGui import SceneGui
from classes.scene.SceneLoader import SceneLoader
from classes.menus import MenuGlobals as MG


class SceneMenu(SceneGui, CanvasMenu, SceneLoader):

    def __init__(self):
        SceneGui.__init__(self)
        SceneLoader.__init__(self)
        CanvasMenu.__init__(self)
        self.kitchen = None
        self.discard_frame = None
        self.add_item = False
        self.last_node = None
        self.last_button = None
        self.grid = None

    def generate(self):
        self.load_gui()
        self.generate_canvas(self.kitchen.preview_menu, self.scene_frame,
                             self.scene_scroll, 'scene')
        self.discard_frame = DiscardCanvasButtons(
            menu_name='scene',
            kitchen=self.kitchen,
            reload_menu=self,
            scroll_frame=self.scene_scroll,
            trash_button=self.scene_trash,
            confirm_button=self.scene_confirm,
            left_button=self.scene_inspect,
            command=self.update_selected_node,
            xml=True
        )
        self.grid = self.generate_grid()

    def add_item_to_xml(self, item_name):
        mode = self.kitchen.preview_menu.get_mode().lower()
        xml_file = self.kitchen.project_location + "/{}" + ".xml"
        if mode == 'actor' or mode == 'prop':
            xml_file = xml_file.format(f"{mode}s")
            append_node_data(xml_file, mode, item_name)

        self.reload(xml_file)

    def reload(self, xml_file=None, mode=None):
        if mode == AG.TEXTURES:
            return
        if not mode:
            mode = self.kitchen.preview_menu.get_mode().lower() + "s"
        if not xml_file:
            xml_file = f"{self.kitchen.project_location}/{mode}.xml"

        xml_file = Filename().fromOsSpecific(xml_file)

        node_data = get_node_data(xml_file.toOsSpecific())
        self.load_nodes(mode, node_data)
        self.load_canvas_buttons(node_data)

    def load_canvas_buttons(self, node_data):
        mode_class = self.kitchen.preview_menu.get_mode_class()
        # cleanup all scene buttons
        for button in mode_class.scene_buttons:
            button.destroy()

        # remake all scene buttons in preview mode's scene_button dict.
        self.load_picture_list(node_data, command=self.update_selected_node,
                               color=MG.FRAME_COLOR['scene'])

    def update_selected_node(self, node):
        name = None
        if node:
            name = node.get_name()
        scene_trash_mode = self.discard_frame.trash_mode
        library_trash_mode = self.kitchen.library_menu.discard_frame.trash_mode

        # check if the user clicked on a DirectButton or the actual node.
        if isinstance(node, DirectButton):
            button = node
            node = self.get_node_by_name(name)
        elif isinstance(node, NodePath):
            node = node
            button = self.get_button_by_name(name)
        elif not node:
            button = None
        else:
            print(f'"{node}" is not a valid selection.')
            return  # we don't know what the frick this thing is.

        # add selection to discard list instead of selecting it to move around.
        if scene_trash_mode:
            mode_of_node = None
            if node:
                mode_of_node = node.get_name().split("|")[3]
            # only allow user to add nodes that match the current mode.
            # verify that the node mode matches the current menu mode.
            if mode_of_node == self.discard_frame.mode:
                self.select_node_for_discarding(node)
            else:
                return  # don't set this node as last node / button

        elif library_trash_mode:
            if node:
                print("Cannot select scene nodes in \"Library Delete\" mode.")

        elif node:
            # update which node is selected in the scene.
            self.kitchen.node_mover.set_node(node)
            if node:
                self.update_menu(node, button)

            self.last_node = node
            self.last_button = button

    def select_node_for_discarding(self, node):
        print(node)

    def update_menu(self, node, button):
        # reset color on last button and apply color to selected button.
        if self.last_button:
            self.last_button['frameColor'] = MG.FRAME_COLOR['scene']
        button['frameColor'] = MG.SELECTED_BUTTON_COLOR

        # along with changing the selected node, change the menu
        mode = node.get_name().split("|")[3]
        self.preview_menu.set_mode(mode)

        # switch to scene menu if not already active.
        if not self.kitchen.library_menu.swap_menu:
            self.kitchen.library_menu.swap_menus()

    def get_node_by_name(self, name):
        mode = name.split("|")[3]
        for node in self.nodepaths[mode]:
            if name in node.get_name():
                return node
        return None

    def get_button_by_name(self, name):
        node_name = name  # store name
        mode = name.split("|")[3]  # get the mode that is stored in the name.
        preview_mode = self.kitchen.preview_menu.modes[mode]
        # search through the button list for the button with the matching name,
        for button in preview_mode.scene_buttons:
            if node_name == button.get_name():
                return button
        return None

    def get_last_button(self):
        return self.last_button

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
        super().set_kitchen(kitchen)
