"""
Set a Node to move and rotate. Modify with keyboard inputs.
The rate you can effect them can also be influenced by keyboard inputs.
"""
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.gui.DirectGui import DGG
from panda3d.core import NodePath

from classes.editors.NodeMoverGui import NodeMoverGui
from classes.gui.DirectEntryClickAndDrag import DirectEntryClickAndDrag
from classes.settings import Globals as G

VALID_ENTRIES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']


class NodeMover(NodeMoverGui, NodePath):

    def __init__(self, camera):
        NodeMoverGui.__init__(self)
        self.click_and_drags = None
        self.move_options = None
        self.allow_click = True
        self.allow_tasks = True
        self.last_tab_entry = None

        self.generate(camera)

    def generate(self, cam):
        self.accept(G.MIDDLE_MOUSE_BUTTON, self.set_node, extraArgs=[cam])
        self.accept("tab", self.go_to_next_entry, extraArgs=[1])
        self.accept("shift-tab", self.go_to_next_entry, extraArgs=[-1])
        self.bind_gui()

    def bind_gui(self):
        self.click_and_drags = []
        for entry in self.entries:
            click_and_drag = DirectEntryClickAndDrag(entry)
            self.click_and_drags.append(click_and_drag)

    def set_node(self, node, flash_red=True):
        if node and self.allow_click:
            NodePath.__init__(self, node)
            # apply necessary steps for direct entries
            for drag in self.click_and_drags:
                drag.set_func_catalog(self.get_func_catalog(node))
                drag.set_node(node)
                drag.enable_entry()
            taskMgr.doMethodLater(.03, self.update_entries,
                                  "update_de_entries")

            if not flash_red:
                return
            # Make a short sequence to show it was selected.
            og_color_scale = node.get_color_scale()
            node.set_color_scale(G.RED)
            Sequence(
                Func(self.toggle_click), Wait(.3),
                Func(node.set_color_scale, *og_color_scale),
                Func(self.toggle_click)
            ).start()

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

    def get_func_catalog(self, node):
        func_catalog = {
            'X': [node.get_x, node.set_x],
            'Y': [node.get_y, node.set_y],
            'Z': [node.get_z, node.set_z],
            'H': [node.get_h, node.set_h],
            'P': [node.get_p, node.set_p],
            'R': [node.get_r, node.set_r],
            'SX': [node.get_sx, node.set_sx],
            'SY': [node.get_sy, node.set_sy],
            'SZ': [node.get_sz, node.set_sz],
        }
        return func_catalog

    def toggle_click(self):
        self.allow_click = not self.allow_click

    def set_click(self, click):
        self.allow_click = click

    def cleanup(self):
        self.allow_tasks = False
        self.ignore_all()
