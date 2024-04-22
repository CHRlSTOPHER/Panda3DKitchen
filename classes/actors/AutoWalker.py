"""
Actors will inherit this class to automatically transition between
animations like neutral and walk/run/etc.
Only 'neutral' and 'walk' animations are set by default.
"""
import json
import math

from panda3d.core import Vec3

from classes.settings import Globals as G

json_settings = json.loads(open(G.SETTINGS_JSON).read())

AUTO_WALKER_TASK = "auto_walker_task"
ANIM_TRANSITION_TASK = "anim_transition_task"

NEUTRAL = 0
WALKING = 1
RUNNING = 2
CONTROL_RATE = .1


class AutoWalker:

    def __init__(self, actor, speed=13, run_threshold=1.25, run_div=2.0,
                 neutral_anim="neutral", walk_anim="walk", run_anim=None):
        self.kitchen = None
        self.actor = actor
        self.speed = speed
        self.run_threshold = run_threshold
        self.run_div = run_div
        self.neutral_anim = neutral_anim
        self.walk_anim = walk_anim
        self.run_anim = run_anim

        self.old_anim_state = 0
        self.new_anim_state = 0
        self.old_anim_control = 0
        self.new_anim_control = 0
        self.anims = [neutral_anim, walk_anim, run_anim]

        self.previous_pos = actor.get_pos()
        self.previous_hpr = actor.get_hpr()

    def generate(self):
        if json_settings[G.AUTO_WALKER]:
            self.kitchen.taskMgr.add(self.update_actor_anim_task,
                                     AUTO_WALKER_TASK)

    def update_actor_anim_task(self, task):
        self.update_actor_anim()
        self.previous_pos = self.actor.get_pos()
        self.previous_hpr = self.actor.get_hpr()
        return task.again

    def update_actor_anim(self):
        magnitude = self.find_magnitude()
        direction = 1  # Default value. No movement is occurring.
        if magnitude != 1:
            # big scale moves farther. small scale moves not as much.
            magnitude /= self.actor.get_sy()
            direction = self.find_direction()
        elif self.actor.get_hpr() != self.previous_hpr:
            magnitude = self.find_turn_rate()

        # "With both direction and magnitude! OH YEAH!!!" -Vector.
        # https://www.youtube.com/watch?v=nw9QoYL_8tI
        playrate = direction * magnitude

        # This checks if we need to change the current anim to something else.
        self.check_anim_state(magnitude)

        if self.new_anim_state == RUNNING:
            playrate /= self.run_div  # run play rates are often too fast.
        for anim in self.anims:
            self.actor.set_play_rate(playrate, anim)

    def find_magnitude(self):
        # the distance formula lmao
        x1, y1, z1 = self.previous_pos
        x2, y2, z2 = self.actor.get_pos()
        magnitude = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        if not magnitude:
            magnitude = 1 / self.speed

        return magnitude * self.speed

    def find_direction(self):  # Thanks Ashy. Those were fat math solutions lol
        forward_vector = Vec3(0, 1, 0)
        forward_vector = self.kitchen.scene_render.getRelativeVector(
                                                    self.actor, forward_vector)
        velocity = self.actor.get_pos() - self.previous_pos
        actor_direction = forward_vector.dot(velocity)
        direction = 1
        if actor_direction < 0:
            direction = -1

        return direction

    def find_turn_rate(self):
        h1, p1, r1 = self.previous_hpr
        h2, p2, r2 = self.actor.get_hpr()
        magnitude = math.sqrt((h2 - h1) ** 2 + (p2 - p1) ** 2 + (r2 - r1) ** 2)
        return magnitude

    def check_anim_state(self, magnitude):
        # check if actor stopped moving.
        if magnitude == 1.0 and self.new_anim_state != NEUTRAL:
            self.new_anim_state = NEUTRAL
        # check if actor started moving while under run limit
        elif (magnitude < self.run_threshold
              and self.new_anim_state != WALKING
              and magnitude != 1):
            self.new_anim_state = WALKING
        # check if actor started moving without a run anim (default to walking)
        elif (not self.run_anim
              and self.new_anim_state != WALKING
              and magnitude != 1):
            self.new_anim_state = WALKING
        # check if actor started going over run speed limit
        elif (magnitude >= self.run_threshold
              and self.run_anim
              and self.new_anim_state != RUNNING):
            self.new_anim_state = RUNNING

        self.apply_anim()

    def apply_anim(self):
        if self.old_anim_state == self.new_anim_state:
            return  # stop the main task from constantly applying the anim

        old_anim = self.anims[self.old_anim_state]
        new_anim = self.anims[self.new_anim_state]
        self.old_anim_state = self.new_anim_state

        # stop any currently running tasks and reset controls.
        self.kitchen.taskMgr.remove(ANIM_TRANSITION_TASK)
        if self.old_anim_control == 0:  # the previous transition finished.
            self.old_anim_control = 1
            self.new_anim_control = 0
        else:  # the last anim transitioning is being interrupted.
            self.old_anim_control = 1 - self.old_anim_control
            self.new_anim_control = 1 - self.new_anim_control

        # enable blend for a short time and transition between animations.
        self.actor.enable_blend()
        self.actor.loop(old_anim, 0)  # 0 lets the anim start at current pose.
        self.actor.loop(new_anim, 0)
        self.kitchen.taskMgr.add(self.transition_between_anims,
                                 ANIM_TRANSITION_TASK, appendTask=True,
                                 extraArgs=[old_anim, new_anim])

    def transition_between_anims(self, old_anim, new_anim, task):
        if self.new_anim_control > 0.99:
            self.actor.disable_blend()
            return task.done

        self.old_anim_control = round(self.old_anim_control - CONTROL_RATE, 2)
        self.new_anim_control = round(self.new_anim_control + CONTROL_RATE, 2)
        self.actor.set_control_effect(old_anim, self.old_anim_control)
        self.actor.set_control_effect(new_anim, self.new_anim_control)

        return task.cont

    def set_multiplier(self, speed):
        self.speed = speed

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen

    def cleanup_walker(self):
        self.kitchen.taskMgr.remove(AUTO_WALKER_TASK)
        self.kitchen.taskMgr.remove(ANIM_TRANSITION_TASK)
