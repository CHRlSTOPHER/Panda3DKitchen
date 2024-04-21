import os

from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.ShowBase import ShowBase

from classes.camera.CameraMover import CameraMover
from classes.editors.GuiEditor import GuiEditor
from classes.editors.NodeMover import NodeMover
from classes.editors.NodeSelector import NodeSelector
from classes.menus.LibraryMenu import LibraryMenu
from classes.menus.PreviewMenu import PreviewMenu
from classes.menus.SceneMenu import SceneMenu
from classes.scene.SceneWindow import SceneWindow
from classes.settings.Settings import load_settings
from classes.menus.StartMenu import StartMenu
from classes.settings import Globals as G
from classes.menus import MenuGlobals as MG

CWD = os.getcwd()
load_settings(CWD)
COMPUTER_FONT = f"{G.EDITOR}{MG.COMPUTER_FONT}"


class Panda3DKitchen(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.root_folder = CWD
        self.scene_window = SceneWindow()
        self.start_menu = StartMenu()
        self.gui_editor = GuiEditor()
        self.camera_mover = CameraMover()
        self.node_mover = NodeMover()
        self.node_selector = NodeSelector()
        self.preview_menu = PreviewMenu()
        self.library_menu = LibraryMenu(self.preview_menu)
        self.scene_menu = SceneMenu(self.preview_menu)
        self.class_objects = [self.start_menu, self.gui_editor,
                              self.camera_mover, self.node_mover,
                              self.node_selector, self.library_menu,
                              self.scene_menu, self.preview_menu]
        self.scene_camera = None
        self.scene_render = None
        self.scene_mw = None
        self.scene_region = None
        self.project_location = None

        self.load_model = self.loader.load_model
        self.load_texture = self.loader.load_texture
        self.load_music = self.loader.load_music
        self.load_sfx = self.loader.load_sfx
        self.load_font = self.loader.load_font
        self.load_particle = ParticleEffect

        self.computer_font = self.load_font(COMPUTER_FONT)

    def generate_classes(self):
        self.scene_window.generate()
        self.scene_camera = self.scene_window.scene_cam
        self.scene_render = self.scene_window.scene_render
        self.scene_region = self.scene_window.scene_region
        self.scene_mw = self.scene_window.scene_mouse_watcher
        for object in self.class_objects:
            object.generate()

    def define_variable_names(self):
        self.library_window = self.library_menu.library_window
        self.library_scroll = self.library_menu.library_scroll
        self.library_trash = self.library_menu.library_trash

    def set_project_location(self, project_location):
        self.project_location = project_location

    def set_kitchens(self):
        self.scene_window.set_kitchen(self)
        for object in self.class_objects:
            object.set_kitchen(self)


kitchen = Panda3DKitchen()
kitchen.disable_mouse()
kitchen.set_kitchens()
kitchen.run()