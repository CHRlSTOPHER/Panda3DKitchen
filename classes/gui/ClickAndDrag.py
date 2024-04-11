from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DGG

CLICK_DRAG_TASK = "click_and_drag_task"


class ClickAndDrag(DirectObject):

    def __init__(self, gui_components):
        DirectObject.__init__(self)
        self.gui_components = gui_components
        self.parent = None
        self.mouse_node = aspect2d.attach_new_node('mouse_node', sort=999999)

        self.set_up_click_and_drag()

    def set_up_click_and_drag(self):
        taskMgr.add(self.move_mouse_task, CLICK_DRAG_TASK)

        for gui in self.gui_components:
            gui['state'] = DGG.NORMAL
            gui.bind(DGG.B1PRESS, self.press, extraArgs=[gui])
            gui.bind(DGG.B1RELEASE, self.release, extraArgs=[gui])

    def move_mouse_task(self, task):
        if base.mouseWatcherNode.has_mouse():
            mouse_pos = base.mouseWatcherNode.get_mouse()
            self.mouse_node.set_pos(render2d, mouse_pos.x, 0, mouse_pos.y)
        return task.cont

    def press(self, gui, mouse_data):
        self.parent = gui.get_parent()
        gui.wrt_reparent_to(self.mouse_node)

    def release(self, gui, mouse_data):
        gui.wrt_reparent_to(self.parent)
