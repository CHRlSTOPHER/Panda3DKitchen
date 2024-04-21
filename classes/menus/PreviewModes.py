import random
import math

from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume, TransparencyAttrib

from classes.file.HandleJsonData import update_library_database
from classes.props.PlaneModel import PlaneModel


def get_distance(item):
    # get y2 and y1 for the distance formula
    y2 = item.get_tight_bounds()[0][1]
    y1 = item.get_tight_bounds()[1][1]
    distance = math.sqrt((y2 - y1) ** 2)
    if distance > 60:  # Cap max y value below 90 ( 60 * 1.5 )
        distance = 60
    if distance < 3:  # Move objects that are too close to the camera.
        distance = 3

    return distance


class ActorMenu:

    def __init__(self):
        self.kitchen = None
        self.library_buttons = []
        self.scene_buttons = []
        self.entity = None
        self.anim_list = None
        self.actor = None
        self.rng_button = None
        self.last_anim = None
        self.get_buttons_dict = {
            'library': self.get_library_buttons,
            'scene': self.get_scene_buttons,
        }
        self.set_buttons_dict = {
            'library': self.set_library_buttons,
            'scene': self.set_scene_buttons,
        }

    def load_entity(self, directory):
        self.actor = Actor()
        self.entity = self.actor
        self.actor.load_model(directory)
        if self.anim_list:
            # load anims and set the actor to the first frame of the first anim
            self.actor.load_anims(self.anim_list)
            first_anim = next(iter(self.anim_list))
            self.actor.pose(first_anim, 3)
        self.actor.set_transparency(TransparencyAttrib.MDual)
        self.actor.reparent_to(self.kitchen.preview_render)
        self.actor.node().set_bounds(OmniBoundingVolume())
        self.actor.node().set_final(1)

        if self.anim_list:
            self.actor.load_anims(self.anim_list)
            first_anim = next(iter(self.anim_list))
            self.actor.pose(first_anim, 3)

        # get y2 and y1 for the distance formula
        distance = get_distance(self.actor)
        self.kitchen.node_mover.set_node(self.actor, flash_red=False)
        self.kitchen.node_mover.set_pos(0, distance * 2.0, -(distance / 2.0))
        self.kitchen.node_mover.set_click(False)

    def set_anims(self, anim_names, anim_dirs):
        self.anim_list = {}
        for i in range(0, len(anim_names)):
            self.anim_list[f"{anim_names[i]}"] = f"{anim_dirs[i]}"

    def randomize_anim(self):
        anim = self.last_anim
        if self.anim_list:
            # keep going until a new anim is picked -- rarely loops
            while anim == self.last_anim:
                anim, location = random.choice(list(self.anim_list.items()))
                frames = self.actor.get_num_frames(anim)
                random_frame = random.randint(0, frames)
                self.actor.pose(anim, random_frame)
                # leave if there is only 1 anim in the list
                if len(self.anim_list) == 1:
                    break

    def define_rng_button(self, button):
        self.rng_button = button
        self.rng_button['command'] = self.randomize_anim

    def save_item(self, item_name, item_location):
        save_data = {item_name: [item_location, self.anim_list]}
        update_library_database("Actor", save_data)

    def cleanup_entity(self):
        if self.actor:
            self.actor.cleanup()

    def get_library_buttons(self):
        return self.library_buttons

    def get_scene_buttons(self):
        return self.scene_buttons

    def set_library_buttons(self, buttons):
        self.library_buttons = buttons

    def set_scene_buttons(self, buttons):
        self.scene_buttons = buttons
    
    def set_kitchen(self, kitchen):
        self.kitchen = kitchen


class PropMenu:

    def __init__(self):
        self.kitchen = None
        self.library_buttons = []
        self.scene_buttons = []
        self.entity = None
        self.prop = None
        self.get_buttons_dict = {
            'library': self.get_library_buttons,
            'scene': self.get_scene_buttons,
        }
        self.set_buttons_dict = {
            'library': self.set_library_buttons,
            'scene': self.set_scene_buttons,
        }

    def load_entity(self, directory):
        self.prop = loader.load_model(directory)
        self.entity = self.prop
        self.prop.set_transparency(TransparencyAttrib.MDual)
        self.prop.reparent_to(self.kitchen.preview_render)
        self.prop.node().set_bounds(OmniBoundingVolume())
        self.prop.node().set_final(1)

        distance = get_distance(self.prop)
        self.kitchen.node_mover.set_node(self.prop, flash_red=False)
        self.kitchen.node_mover.set_pos(0, distance * 2.0, -(distance / 2.0))
        self.kitchen.node_mover.set_click(False)

    def save_item(self, item_name, item_location):
        save_data = {item_name: item_location}
        update_library_database("Prop", save_data)

    def cleanup_entity(self):
        if self.prop:
            self.prop.remove_node()

    def get_library_buttons(self):
        return self.library_buttons

    def get_scene_buttons(self):
        return self.scene_buttons

    def set_library_buttons(self, buttons):
        self.library_buttons = buttons

    def set_scene_buttons(self, buttons):
        self.scene_buttons = buttons
    
    def set_kitchen(self, kitchen):
        self.kitchen = kitchen


class TextureMenu:

    def __init__(self):
        self.kitchen = None
        self.library_buttons = []
        self.scene_buttons = []
        self.entity = None
        self.textures = {}
        self.get_buttons_dict = {
            'library': self.get_library_buttons,
            'scene': self.get_scene_buttons,
        }
        self.set_buttons_dict = {
            'library': self.set_library_buttons,
            'scene': self.set_scene_buttons,
        }

        self.texture_node = None

    def load_entity(self, directory):
        if isinstance(directory, str):
            self.texture_node = PlaneModel(directory,
                                           parent=self.kitchen.preview_render)
            self.texture_node.set_y(3)

    def set_textures(self, names, dirs):
        self.textures = {}
        for i in range(0, len(names)):
            self.textures[f"{names[i]}"] = f"{dirs[i]}"

    def save_item(self, item_name, item_location):  # don't remove these args.
        save_data = self.textures
        update_library_database("Texture", save_data)

    def cleanup_entity(self):
        if self.texture_node:
            self.texture_node.remove_node()

    def get_library_buttons(self):
        return self.library_buttons

    def get_scene_buttons(self):
        return self.scene_buttons

    def set_library_buttons(self, buttons):
        self.library_buttons = buttons

    def set_scene_buttons(self, buttons):
        self.scene_buttons = buttons
    
    def set_kitchen(self, kitchen):
        self.kitchen = kitchen


class ParticleMenu:

    def __init__(self):
        self.kitchen = None
        self.entity = None
        self.library_buttons = []
        self.scene_buttons = []
        self.get_buttons_dict = {
            'library': self.get_library_buttons,
            'scene': self.get_scene_buttons,
        }
        self.set_buttons_dict = {
            'library': self.set_library_buttons,
            'scene': self.set_scene_buttons,
        }

    def load_entity(self, directory):
        pass

    def cleanup_entity(self):
        pass

    def get_library_buttons(self):
        return self.library_buttons

    def get_scene_buttons(self):
        return self.scene_buttons

    def set_library_buttons(self, buttons):
        self.library_buttons = buttons

    def set_scene_buttons(self, buttons):
        self.scene_buttons = buttons
    
    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
