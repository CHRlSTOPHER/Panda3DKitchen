"""
Adjust the Camera Fov by scrolling the Mouse Wheel.
Limited range between 0-180.
"""
import json
from direct.showbase.DirectObject import DirectObject

from classes.settings import Globals as G

SCROLL_AMOUNT = int(G.FOV_SCROLL_AMOUNT)
MINIMUM_FOV = G.MINIMUM_SCROLL_FOV + G.FOV_SCROLL_AMOUNT
MAXIMUM_FOV = G.MAXIMUM_SCROLL_FOV - G.FOV_SCROLL_AMOUNT


class FovScrollWheel(DirectObject):

    def __init__(self, fov, _camera, mouse_watcher):
        DirectObject.__init__(self)

        if not fov:  # Default to the fov in settings.
            json_settings = json.loads(open(G.SETTINGS_JSON).read())
            fov = json_settings['fov']

        self.camera = _camera
        self.mouse_watcher = mouse_watcher

        self.current_fov = fov
        self.new_fov = fov
        self.fov_increment = 1

        self.accept(G.MOUSE_WHEEL_UP, self.zoom_in)
        self.accept(G.MOUSE_WHEEL_DOWN, self.zoom_out)

    def zoom_in(self):
        if (self.new_fov - SCROLL_AMOUNT >= MINIMUM_FOV
                and self.mouse_watcher.has_mouse()):
            self.new_fov = self.new_fov - SCROLL_AMOUNT
            self.set_fov(self.new_fov)

    def zoom_out(self):
        if (self.new_fov + SCROLL_AMOUNT <= MAXIMUM_FOV
                and self.mouse_watcher.has_mouse()):
            self.new_fov = self.new_fov + SCROLL_AMOUNT
            self.set_fov(self.new_fov)

    def set_fov(self, fov):
        self.camera.node().get_lens().set_fov(fov)

    def cleanup(self):
        self.ignore_all()
