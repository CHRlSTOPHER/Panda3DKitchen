"""
Set a Node to move and rotate. Modify with keyboard inputs.
The rate you can effect them can also be influenced by keyboard inputs.
"""
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import NodePath
import json

from classes.editors.NodeMoverGui import NodeMoverGui
from classes.gui.DirectEntryClickAndDrag import DirectEntryClickAndDrag
from classes.settings import Globals as G

KBS = json.loads(open(G.KEYBINDINGS_JSON).read())
VALID_ENTRIES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']
BASE_MOVE_RATE = .1
BASE_TURN_RATE = .5


class NodeMover(NodeMoverGui, NodePath, DirectEntryClickAndDrag):

    def __init__(self, node=None, _camera=None):
        NodeMoverGui.__init__(self)
        self.move_options = None
        self.move_speed = BASE_MOVE_RATE
        self.turn_speed = BASE_TURN_RATE
        self.allow_click = True
        self.allow_tasks = True
        self.last_tab_entry = None
        self.move = True

        # The assigned key below will set the camera as the node being moved.
        if _camera:
            cam = _camera
        else:
            cam = camera

        self.generate(node, cam)

    def generate(self, node, cam):
        self.accept(G.MIDDLE_MOUSE_BUTTON, self.set_node, extraArgs=[cam])
        self.accept("tab", self.go_to_next_entry, extraArgs=[1])
        self.accept("shift-tab", self.go_to_next_entry, extraArgs=[-1])
        self.bind_gui()
        self.set_node(node)
        self.listen_for_key_inputs()

    def bind_gui(self):
        self.click_and_drags = []
        for entry in self.entries:
            click_and_drag = DirectEntryClickAndDrag(entry, self)
            self.click_and_drags.append(click_and_drag)

    def set_node(self, node, flash_red=True):
        if node and self.allow_click:
            NodePath.__init__(self, node)
            self.define_move_options()

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

    def listen_for_key_inputs(self):
        index = 0
        # Add input detection for node transformations.
        for key in KBS:
            if key == G.NM_SPEEDS[0][0]:
                break  # stop at speed modifiers.
            self.accept(KBS[key], self.start_movement, extraArgs=[key, index])
            self.accept(KBS[key] + "-up", self.stop_move_task, extraArgs=[key])
            index += 1

        # Add input detection for speeds adjustments.
        for key, speed in G.NM_SPEEDS:
            if key == G.NM_SPEEDS[-1][0]:
                break  # stop at the default speed.
            self.accept(f"{KBS[key]}", self.change_speed, extraArgs=[speed])
            self.accept(f"{KBS[key]}-up", self.change_speed, extraArgs=[1])

    def start_movement(self, key, direction):
        self.validate_entry_values()
        taskMgr.add(self.move_task, f"move_{key}",
                    extraArgs=[key, direction], appendTask=True)

    def validate_entry_values(self):
        for entry in self.entries:
            value = entry.get()
            new_value = ""
            for digit in value:
                # Only accept numbers, num signs, or decimals
                if digit in VALID_ENTRIES:
                    new_value += digit
            entry.set(new_value)
            # Do not accept direct entry changes once node mover has started
            entry['focus'] = 0

    def move_task(self, key, index, task):
        if not self.move_options or not self.allow_tasks:
            return task.done

        if not self.move:
            return task.again

        move_option = self.move_options[index]
        set_transform = move_option[0]

        # These transformations need relative movement.
        if set_transform == self.setX or set_transform == self.setY:
            get_speed, direction = move_option[1], move_option[2]
            set_transform(self, get_speed() * direction)
        else:
            get_transform, get_speed = move_option[1], move_option[2]
            direction = move_option[3]
            set_transform(get_transform() + get_speed() * direction)

        return task.again

    def stop_move_task(self, key):
        taskMgr.remove(f"move_{key}")

    def define_move_options(self):
        base_speed = G.NM_SPEEDS[-1][1]
        self.move_options = [
            # in this instance, camel case is easier to read imo
            [self.setY, self.get_move_speed, base_speed],
            [self.setX, self.get_move_speed, -base_speed],
            [self.setY, self.get_move_speed, -base_speed],
            [self.setX, self.get_move_speed, base_speed],
            [self.setZ, self.getZ, self.get_move_speed, base_speed],
            [self.setZ, self.getZ, self.get_move_speed, -base_speed],

            [self.setP, self.getP, self.get_turn_speed, base_speed],
            [self.setP, self.getP, self.get_turn_speed, -base_speed],
            [self.setH, self.getH, self.get_turn_speed, base_speed],
            [self.setH, self.getH, self.get_turn_speed, -base_speed],
            [self.setR, self.getR, self.get_turn_speed, base_speed],
            [self.setR, self.getR, self.get_turn_speed, -base_speed],
        ]

    def change_speed(self, speed):
        self.move_speed = BASE_MOVE_RATE / speed
        self.turn_speed = BASE_TURN_RATE / speed

    def toggle_click(self):
        self.allow_click = not self.allow_click

    def get_move_speed(self):
        return self.move_speed

    def get_turn_speed(self):
        return self.turn_speed

    def get_move_options(self):
        return self.move_options

    def set_click(self, click):
        self.allow_click = click

    def set_move(self, move):
        self.move = move

    def cleanup(self):
        self.allow_tasks = False
        self.ignore_all()
