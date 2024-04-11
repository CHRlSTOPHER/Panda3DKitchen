from classes.gui.ClickAndDrag import ClickAndDrag
from classes.scene.SceneWindow import SceneWindow
from classes.menus.PreviewMenu import PreviewMenu
from classes.menus.LibraryMenu import LibraryMenu
from classes.menus.SceneMenu import SceneMenu

# half assed editor class only here for implementing new gui
from classes.editors.GuiEditor import GuiEditor


class MasterMenu:

    def __init__(self, sequence=None, gui_editor=False):
        self.sequence = sequence
        base.gui_editor = gui_editor
        self.preview_menu = None
        self.library_menu = None
        self.scene_menu = None
        self.sequence_manager = None
        self.menu_frames = None
        self.last_mouse_x = 0
        self.last_mouse_y = 0

        self.generate()
        self.click_and_drag = ClickAndDrag(self.menu_frames)

    def generate(self):
        if base.gui_editor:
            base.gui_editor = GuiEditor()

        self.preview_menu = PreviewMenu()
        self.library_menu = LibraryMenu(self.preview_menu)
        self.scene_menu = SceneMenu(self.preview_menu)
        # technically not a menu, but is functionally intertwined.
        self.scene_window = SceneWindow()

        self.menu_frames = [
            # self.preview_menu.entity_frame,
            # self.library_menu.library_window,
            # self.scene_menu.scene_frame,
            # self.scene_window.scene_window,
        ]

        self.connect_menus()

        for menu in [self.library_menu, self.scene_menu, self.preview_menu]:
            menu.generate()

    def connect_menus(self):
        self.preview_menu.set_library_menu(self.library_menu)
        self.preview_menu.set_scene_menu(self.scene_menu)
        self.library_menu.set_scene_menu(self.scene_menu)
        self.preview_menu.set_scene_window(self.scene_window)
        self.library_menu.set_scene_window(self.scene_window)

    def cleanup(self):
        self.preview_menu.entity_frame.destroy()
        self.library_menu.library_window.destroy()
        self.scene_menu.scene_frame.destroy()
