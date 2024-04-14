import json

from direct.gui.DirectGui import DGG
from panda3d.core import NodePath, Camera, MouseWatcher

from classes.camera.FovScrollWheel import FovScrollWheel
from classes.scene.SceneWindowGui import SceneWindowGui
from classes.settings import Globals as G

SCENE_BUFFER = [1920, 1080]
SCENE_REGION = [0.268, 0.735, 0.278, 0.755]
BG_COLOR = (.7, .65, .7, 1)


class SceneWindow(SceneWindowGui, FovScrollWheel):

    def __init__(self):
        SceneWindowGui.__init__(self)
        self.within = False

        self.generate()
        # wait until the display region is generated to call the scene objects.
        FovScrollWheel.__init__(self, None, base.scene_cam,
                                base.scene_mouse_watcher)

    def generate(self):
        self.load_scene_region()
        self.bind_gui()

    def bind_gui(self):
        self.scene_window.bind(DGG.WITHIN, self.set_within, extraArgs=[True])
        self.scene_window.bind(DGG.WITHOUT, self.set_within, extraArgs=[False])

    def load_scene_region(self):
        json_settings = json.loads(open(G.SETTINGS_JSON).read())
        fov = json_settings['fov']

        # First, make display region that will render the main scene
        base.scene_region = base.win.makeDisplayRegion(*SCENE_REGION)
        base.scene_region.set_clear_color_active(1)
        base.scene_region.set_clear_color(BG_COLOR)

        # Second, we need a camera for the new display region
        scene_cam_node = Camera('main_cam')
        base.scene_cam = NodePath(scene_cam_node)
        base.scene_cam.node().get_lens().set_fov(fov)
        base.scene_region.setCamera(base.scene_cam)

        # Third, define the main area nodes will be reparented object too.
        base.scene_render = NodePath('main_render')
        base.scene_cam.reparent_to(base.scene_render)

        # Fourth, add a mouse watcher to use for node selector/fov scroll
        base.scene_mouse_watcher = MouseWatcher()
        base.mouseWatcher.get_parent().attach_new_node(
            base.scene_mouse_watcher)
        base.scene_mouse_watcher.set_display_region(base.scene_region)

        # Fifth, fix display region aspect ratio.
        aspect_ratio = base.get_aspect_ratio()
        base.scene_cam.node().get_lens().set_aspect_ratio(aspect_ratio)

    def set_within(self, state, mouse_data):
        self.within = state

    def get_window(self):
        return self.scene_window

    def get_within(self):
        return self.within
