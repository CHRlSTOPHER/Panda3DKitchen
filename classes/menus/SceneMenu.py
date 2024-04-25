from panda3d.core import NodePath, Filename
from direct.gui.DirectGui import DirectButton

from classes.apps import AppGlobals as AG
from classes.file.HandleXMLData import append_node_data, get_node_data
from classes.gui.DiscardCanvasButtons import DiscardCanvasButtons
from classes.menus.CanvasMenu import CanvasMenu
from classes.menus.SceneGui import SceneGui
from classes.scene.SceneLoader import SceneLoader

SCENE_BUTTON_COLOR = (.7, .9, .9, 1)
SELECTED_BUTTON_COLOR = (0, .2, .2, 1)


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
        self.discard_frame = DiscardCanvasButtons('scene',
                                                  self.kitchen,
                                                  self,
                                                  self.scene_scroll,
                                                  self.scene_trash,
                                                  self.scene_confirm,
                                                  self.scene_inspect, xml=True)
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
        mode = self.kitchen.preview_menu.get_mode()
        nodepath_list = self.nodepaths.get(mode)
        # cleanup all scene buttons
        for button in mode_class.scene_buttons:
            button.destroy()

        # remake all scene buttons in preview mode's scene_button dict.
        self.load_picture_list(node_data, command=self.update_selected_node,
                               color=SCENE_BUTTON_COLOR)

    def update_selected_node(self, node):
        # check if the on clicked on the DirectButton in the menu.
        if isinstance(node, DirectButton):
            # Figure out what node the user wants based on the name
            node = self.get_node_by_name(node)

        self.kitchen.node_mover.set_node(node)
        # along with changing the selected node, change the menu
        mode = node.get_name().split("|")[3]
        self.preview_menu.set_mode(mode)
        # switch to scene menu if not already active,
        if not self.kitchen.library_menu.swap_menu:
            self.kitchen.library_menu.swap_menus()

        button = self.find_button_in_list(node.get_name())
        if button:
            self.color_selected_button(button)

    def get_node_by_name(self, node):
        name = node.get_name()
        mode = name.split("|")[3]
        for node in self.nodepaths[mode]:
            if name in node.get_name():
                return node
        return None

    def find_button_in_list(self, name):
        node_name = name  # store name
        mode = name.split("|")[3]  # get the mode that is stored in the name,
        preview_mode = self.kitchen.preview_menu.modes[mode]
        # search through the button list for the button with the matching name,
        for button in preview_mode.scene_buttons:
            if node_name == button.get_name():
                return button
        return None

    def color_selected_button(self, selected_button):
        for button in self.canvas_buttons.current_button_set:
            button['frameColor'] = SCENE_BUTTON_COLOR
        selected_button['frameColor'] = SELECTED_BUTTON_COLOR

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
        super().set_kitchen(kitchen)
