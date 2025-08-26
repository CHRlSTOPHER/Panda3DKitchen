from direct.gui.DirectGui import DGG
from direct.directtools.DirectGrid import DirectGrid
from panda3d.core import NodePath, Camera, MouseWatcher

from classes.scene.SceneWindowGui import SceneWindowGui
from classes.settings import Globals as G

SCENE_BUFFER = [1920, 1080]
SCENE_REGION = [0.268, 0.735, 0.278, 0.755]
BG_COLOR = (.7, .65, .7, 1)
FOV_ERROR_TEXT = "The FOV value entered is not an integer."


class SceneWindow(SceneWindowGui):

    def __init__(self):
        SceneWindowGui.__init__(self)
        self.scene_region = None
        self.scene_cam = None
        self.scene_render = None
        self.scene_mouse_watcher = None
        self.kitchen = None
        self.within = False
        self.grid = None

    def generate(self):
        self.load_gui()
        self.load_scene_region()
        self.bind_gui()
        self.grid = DirectGrid(parent=self.scene_render)

    def bind_gui(self):
        self.scene_window.bind(DGG.WITHIN, self.set_within, extraArgs=[True])
        self.scene_window.bind(DGG.WITHOUT, self.set_within, extraArgs=[False])
        self.grid_checkbox['command'] = self.toggle_grid
        self.fov_entry['command'] = self.update_fov

    def toggle_grid(self, show):
        if show:
            self.grid.show()
        else:
            self.grid.hide()

    def load_scene_region(self):
        # First, make display region that will render the main scene
        self.scene_region = self.kitchen.win.makeDisplayRegion(*SCENE_REGION)
        self.scene_region.set_clear_color_active(1)
        self.scene_region.set_clear_color(BG_COLOR)

        # Second, we need a camera for the new display region
        scene_cam_node = Camera('main_cam')
        self.scene_cam = NodePath(scene_cam_node)
        self.scene_cam.node().get_lens().set_fov(G.DEFAULT_FOV)
        self.scene_region.setCamera(self.scene_cam)

        # Third, define the main area nodes will be reparented object too.
        self.scene_render = NodePath('main_render')
        self.scene_cam.reparent_to(self.scene_render)

        # Fourth, add a mouse watcher to use for node selector/fov scroll
        self.scene_mouse_watcher = MouseWatcher()
        self.kitchen.mouseWatcher.get_parent().attach_new_node(
            self.scene_mouse_watcher)
        self.scene_mouse_watcher.set_display_region(self.scene_region)

        # Fifth, fix display region aspect ratio.
        aspect_ratio = self.kitchen.get_aspect_ratio()
        self.scene_cam.node().get_lens().set_aspect_ratio(aspect_ratio)

    def update_fov(self, fov):
        # check if fov is an integer between min and max values
        if fov.isdigit:
            fov = int(fov)
            fov = min(fov, G.MAXIMUM_SCROLL_FOV)
            fov = max(fov, G.MINIMUM_SCROLL_FOV)
            self.kitchen.camera_mover.set_fov(fov)
        else:
            print(FOV_ERROR_TEXT)

    def set_within(self, state, mouse_data):
        self.within = state

    def get_window(self):
        return self.scene_window

    def get_within(self):
        return self.within

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
        super().set_kitchen(kitchen)
