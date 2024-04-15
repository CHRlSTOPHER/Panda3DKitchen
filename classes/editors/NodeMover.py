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
        self.click_and_drags = None
        self.move_options = None
        self.allow_click = True
        self.allow_tasks = True
        self.last_tab_entry = None

        self.generate()

    def generate(self):
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
            taskMgr.doMethodLater(.03, self.update_entries,
                                  "update_de_entries")
            for drag in self.click_and_drags:
                drag.set_func_catalog(self.get_func_catalog(node))

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
        for object in self.click_and_drags:
            entry = object.get_entry()
            name = entry.get_name()
            func_catalog = object.get_func_catalog()

            get_value = func_catalog.get(name)[0]
            value = get_value()  # return the transform value based on the name
            float_value = round(float(value), 2)  # round float to .00
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

    # make sure the entry only had valid numerical values
    def validate_entry(self, value):
        valid_value = ""
        for digit in value:
            # Only accept numbers, num signs, or decimals
            if digit in VALID_ENTRIES:
                valid_value += digit
        if value != valid_value:  # stop user from typing while moving.
            self.entry['focus'] = 0
        return valid_value

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
