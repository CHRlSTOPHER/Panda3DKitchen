import json

from panda3d.core import NodePath

from classes.camera.FovScrollWheel import FovScrollWheel
from classes.camera.CameraRotater import CameraRotater
from classes.settings import Globals as G

KBS = json.loads(open(G.KEYBINDINGS_JSON).read())
BASE_MOVE_RATE = .1
BASE_TURN_RATE = .5


class CameraMover(CameraRotater, NodePath, FovScrollWheel):

    def __init__(self):
        CameraRotater.__init__(self, "temp_node2")
        self.kitchen = None
        self.move = True
        self.move_speed = BASE_MOVE_RATE
        self.turn_speed = BASE_TURN_RATE
        NodePath.__init__(self, "temp_node")


    def generate(self):
        NodePath.__init__(self, self.kitchen.camera)
        CameraRotater.__init__(self, self.kitchen.camera)
        FovScrollWheel.__init__(self, None, self.kitchen.scene_camera,
                                self.kitchen.scene_mw)
        super().generate()
        self.define_move_options()
        self.listen_for_key_inputs()

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
        taskMgr.add(self.move_task, f"move_{key}",
                    extraArgs=[key, direction], appendTask=True)

    def move_task(self, key, index, task):
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

    def get_move_speed(self):
        return self.move_speed

    def get_turn_speed(self):
        return self.turn_speed

    def get_move_options(self):
        return self.move_options

    def set_move(self, move):
        self.move = move

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen