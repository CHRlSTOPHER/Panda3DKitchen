"""
Set a Node to move and rotate. Modify with keyboard inputs.
The rate you can effect them can also be influenced by keyboard inputs.
"""
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import NodePath

from classes.editors.NodeMoverGui import NodeMoverGui
from classes.gui.DirectEntryClickAndDrag import DirectEntryClickAndDrag
from classes.settings import Globals as G

VALID_ENTRIES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']


class NodeMover(NodeMoverGui, NodePath):

    def __init__(self):
        NodeMoverGui.__init__(self)
        self.kitchen = None
        self.click_and_drags = None
        self.move_options = None
        self.allow_click = True
        self.allow_tasks = True
        self.last_tab_entry = None
        self.scale_toggle = True

    def generate(self):
        self.load_gui()
        self.accept(G.MIDDLE_MOUSE_BUTTON, self.set_node,
                    extraArgs=[self.kitchen.scene_camera])
        self.accept("tab", self.go_to_next_entry, extraArgs=[1])
        self.accept("control-tab", self.go_to_next_entry, extraArgs=[-1])
        self.bind_gui()

    def bind_gui(self):
        self.click_and_drags = []
        for entry in self.entries:
            click_and_drag = DirectEntryClickAndDrag(entry)
            click_and_drag.set_combined_entries(['SX', 'SY', 'SZ'])
            click_and_drag.set_kitchen(self.kitchen)
            self.click_and_drags.append(click_and_drag)
        for object in self.click_and_drags[-3:]:  # Scale entries
            object.set_delete_value(1.0)

        self.scale_one['command'] = self.toggle_scale_type
        self.scale_all['command'] = self.toggle_scale_type

    def toggle_scale_type(self):
        self.scale_toggle = not self.scale_toggle
        # scale all axis
        if self.scale_toggle:
            for object in self.click_and_drags:
                object.set_combined_toggle(True)
            self.scale_one.hide()
            self.scale_all.show()
        # scale one axis
        else:
            for object in self.click_and_drags:
                object.set_combined_toggle(False)
            self.scale_one.show()
            self.scale_all.hide()

    def set_node(self, node, outline=True):
        if node and self.allow_click:
            NodePath.__init__(self, node)
            # apply necessary steps for direct entries
            for drag in self.click_and_drags:
                drag.set_func_catalog(self.get_func_catalog())
                drag.set_node(node)
                drag.enable_entry()
            self.kitchen.taskMgr.remove("update_de_entries")
            self.kitchen.taskMgr.doMethodLater(.01, self.update_entries,
                                               "update_de_entries")

            if outline:
                # outline node code here
                pass

    def deselect_node(self):
        self.node = None
        self.disable_entries()
        self.kitchen.taskMgr.remove("update_de_entries")

    # update very often in case node mover changed the transform values
    def update_entries(self, task):
        object = self.click_and_drags[0]
        if not object.get_node():
            self.disable_entries()
            return task.done

        for object in self.click_and_drags:
            entry = object.get_entry()
            name = entry.get_name()
            func_catalog = object.get_func_catalog()

            get_value = func_catalog.get(name)[0]
            self.validate_entry_data(entry)
            float_value = round(float(get_value()), 2)  # round float to .00
            string_value = str(float_value)  # convert back to string
            last_value = object.get_last_value()

            # check if the value changed
            if string_value == last_value:
                continue  # skip to the next value if it did not change

            # update if it did change
            entry.set(string_value)
            entry.setCursorPosition(6)
            object.set_last_value(string_value)

        return task.again

    def disable_entries(self):
        for object in self.click_and_drags:
            object.disable_entry()

    def enable_entries(self):
        for object in self.click_and_drags:
            object.enable_entry()

    # make sure the entry only has valid numerical values
    def validate_entry_data(self, entry):
        value = entry.get()
        string_value = ""
        for character in value:
            if character in VALID_ENTRIES:
                string_value += character
            elif character not in VALID_ENTRIES:
                entry['focus'] = 0  # stop anymore invalid entries
        entry.set(string_value)

    def get_func_catalog(self):
        func_catalog = {
            'X': [self.get_x, self.set_x],
            'Y': [self.get_y, self.set_y],
            'Z': [self.get_z, self.set_z],
            'H': [self.get_h, self.set_h],
            'P': [self.get_p, self.set_p],
            'R': [self.get_r, self.set_r],
            'SX': [self.get_sx, self.set_sx],
            'SY': [self.get_sy, self.set_sy],
            'SZ': [self.get_sz, self.set_sz]
        }

        return func_catalog

    def toggle_click(self):
        self.allow_click = not self.allow_click

    def set_click(self, click):
        self.allow_click = click

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen

    def cleanup(self):
        self.allow_tasks = False
        self.ignore_all()
