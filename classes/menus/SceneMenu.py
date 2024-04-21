from classes.apps import AppGlobals as AG
from classes.file.HandleXMLData import append_node_data, get_node_data
from classes.gui.DiscardCanvasButtons import DiscardCanvasButtons
from classes.menus.CanvasMenu import CanvasMenu
from classes.menus.SceneGui import SceneGui
from classes.scene.SceneLoader import SceneLoader


class SceneMenu(SceneGui, CanvasMenu, SceneLoader):

    def __init__(self, preview_menu):
        SceneGui.__init__(self)
        SceneLoader.__init__(self)
        CanvasMenu.__init__(self, preview_menu, self.scene_frame,
                            self.scene_scroll, 'scene')
        self.kitchen = None
        self.discard_frame = None
        self.add_item = False

    def generate(self):
        self.load_gui()
        CanvasMenu.__init__(self, self.kitchen.preview_menu, self.scene_frame,
                            self.scene_scroll, 'scene')
        self.generate_canvas()
        self.discard_frame = DiscardCanvasButtons('scene',
                                                  self.kitchen.preview_menu,
                                                  self,
                                                  self.scene_scroll,
                                                  self.scene_trash,
                                                  self.scene_confirm,
                                                  self.scene_inspect, xml=True)

    def add_item_to_xml(self, item_name):
        mode = self.preview_menu.get_mode().lower()
        xml_file = base.project_location + "/{}" + ".xml"
        if mode == 'actor' or mode == 'prop':
            xml_file = xml_file.format(f"{mode}s")
            append_node_data(xml_file, mode, item_name)

        self.reload(xml_file)

    def reload(self, xml_file=None, mode=None):
        if not mode:
            mode = self.kitchen.preview_menu.get_mode().lower() + "s"
        if not xml_file:
            xml_file = f"{self.kitchen.project_location}/{mode}.xml"

        if mode != AG.TEXTURES:
            node_data = get_node_data(xml_file)
            self.load_canvas_buttons(node_data)
            self.load_nodes(mode, node_data)

    def load_canvas_buttons(self, node_data):
        mode_class = self.preview_menu.get_mode_class()
        for button in mode_class.scene_buttons:
            button.destroy()

        self.load_picture_list(node_data, color=(.7, .9, .9, 1))

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
        super().set_kitchen(kitchen)
