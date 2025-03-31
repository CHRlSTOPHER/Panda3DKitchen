import json

from direct.actor.Actor import Actor

from classes.apps import AppGlobals as AG
from classes.settings import Globals as G


class SceneLoader:

    def __init__(self):
        self.kitchen = None
        self.nodepaths = {
            'Actor': [],
            'Prop': [],
            'Particle': []
        }

    def generate_actor(self, model, anims):
        actor = Actor(model, anims)
        if anims:
            # loop first anim in dict
            actor.loop(next(iter(anims)))
        actor.set_blend(frameBlend=True)
        actor.reparent_to(self.kitchen.scene_render)
        return actor

    def generate_node(self, model):
        node = self.kitchen.load_model(model)
        node.reparent_to(self.kitchen.scene_render)
        return node

    def set_transforms(self, node, transforms):
        pos, hpr, scale, color, color_scale = transforms
        node.set_pos_hpr_scale(*pos, *hpr, *scale)
        if color != [1, 1, 1, 1]:
            node.set_color(*color)
        if color_scale != [1, 1, 1, 1]:
            node.set_color_scale(*color_scale)

    def load_node(self, mode, name, full_name):
        node = None
        json_data = self.get_json_data(mode.lower() + "s")

        if mode == AG.ACTOR:
            model, anims = json_data[name]
            node = self.generate_actor(model, anims)
            node.set_name(full_name)
            self.nodepaths.get('Actor').append(node)

        if mode == AG.PROP:
            if name not in G.SPECIAL_NODES:
                model = json_data[name]
                node = self.generate_node(model)
                node.set_name(full_name)
                self.nodepaths.get('Prop').append(node)

        if mode == AG.PARTICLES:
            return None

        return node

    def load_nodes(self, mode, node_data):
        json_data = self.get_json_data(mode)
        # cleanup and load
        if mode == AG.ACTORS:
            for actor in self.nodepaths.get('Actor'):
                actor.delete()

            self.nodepaths['Actor'] = []
            for data_name in node_data:
                full_name = data_name  # store name before it gets split
                name, index, part, mode = data_name.split("|")
                model, anims = json_data[name]
                node = self.generate_actor(model, anims)
                node.set_name(full_name)
                self.set_transforms(node, node_data[data_name])
                self.nodepaths.get('Actor').append(node)

        if mode == AG.PROPS:
            for prop in self.nodepaths.get('Prop'):
                prop.remove_node()

            self.nodepaths['Prop'] = []
            for data_name in node_data:
                full_name = data_name  # store name before it gets split
                name, index, part, mode = data_name.split("|")
                if name not in G.SPECIAL_NODES:
                    model = json_data[name]
                    node = self.generate_node(model)
                    node.set_name(full_name)
                    self.set_transforms(node, node_data[data_name])
                    self.nodepaths.get('Prop').append(node)
                elif name == 'camera':
                    self.set_transforms(self.kitchen.scene_camera,
                                        node_data[data_name])

        if mode == AG.PARTICLES:
            self.nodepaths['Particle'] = []
            return

    def get_json_data(self, mode):
        # slice off the plural
        mode_filename = mode.capitalize()[:-1]
        json_path = f"{G.DATABASE_DIRECTORY}{mode_filename}Library{G.JSON}"
        return  json.loads(open(json_path).read())

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
