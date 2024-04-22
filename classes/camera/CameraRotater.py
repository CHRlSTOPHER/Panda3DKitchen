"""
Modify the H and P values of the camera with mouse movement.
Enable and Disable the Mode with the RMB.
"""
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties

from classes.settings import Globals as G

SENSITIVITY = G.ROTATIONAL_CAM_MOUSE_SENSITIVITY
ROT_CAM_TASK = "rot_cam_task"
DELAY = .001


class CameraRotater(DirectObject):

    def __init__(self, camera):
        DirectObject.__init__(self)

        self.kitchen = None
        self.camera = camera
        self.window_properties = WindowProperties()
        self.toggle_value = False
        self.disabled = False
        self.cam_task = True

    def generate(self):
        self.accept(G.RIGHT_MOUSE_BUTTON, self.toggle_orb_cam)

    def toggle_orb_cam(self):
        if self.disabled or not self.kitchen.preview_menu.mini_window:
            return

        self.toggle_value = not self.toggle_value
        self.window_properties.set_cursor_hidden(self.toggle_value)

        if self.toggle_value:
            self.recenter_mouse_cursor()
            self.kitchen.taskMgr.do_method_later(DELAY, self.rot_cam_task,
                                                 ROT_CAM_TASK)
        else:
            self.kitchen.taskMgr.remove(ROT_CAM_TASK)

        self.kitchen.win.request_properties(self.window_properties)

    def recenter_mouse_cursor(self):
        mouse_x_center = self.kitchen.win.get_x_size() // 2
        mouse_y_center = self.kitchen.win.get_y_size() // 2

        self.kitchen.win.move_pointer(0, mouse_x_center, mouse_y_center)

    def rot_cam_task(self, task):
        if self.cam_task:
            self.recenter_mouse_cursor()
            self.update_cam_orientation()
            return task.cont
        else:
            return task.done

    def update_cam_orientation(self):
        if self.kitchen.mouseWatcherNode.hasMouse():
            x_pos = self.kitchen.mouseWatcherNode.get_mouse_x()
            y_pos = self.kitchen.mouseWatcherNode.get_mouse_y()

            # move camera based on mouse movement during frame.
            # factor fov into the equation. small fov, reduce move speed.
            fov_mod = self.kitchen.camLens.get_fov()[0] / G.FOV_MODIFIER
            new_cam_h_value = (self.camera.get_h()
                               - (x_pos * SENSITIVITY * fov_mod))
            new_cam_p_value = (self.camera.get_p()
                               + (y_pos * SENSITIVITY * fov_mod))

            self.camera.set_h(new_cam_h_value)
            self.camera.set_p(new_cam_p_value)

    def disable(self):
        self.toggle_value = False
        self.toggle_orb_cam()  # turn it off in case by some miracle it was on.
        self.disabled = True

    def enable(self):
        self.disabled = False

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen

    def cleanup(self):
        if not self.toggle_value:
            self.toggle_orb_cam()
        self.cam_task = False
        self.ignore_all()
