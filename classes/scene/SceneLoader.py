import json

from direct.actor.Actor import Actor

from classes.apps import AppGlobals as AG
from classes.settings import Globals as G


class SceneLoader:

    def __init__(self):
        self.actors = []
        self.props = []

    def generate_actor(self, model, anims):
        actor = Actor(model, anims)
        if anims:
            # loop first anim in dict
            actor.loop(next(iter(anims)))
        actor.set_blend(frameBlend=True)
        actor.reparent_to(base.scene_render)
        return actor

    def generate_node(self, model):
        node = loader.load_model(model)
        node.reparent_to(base.scene_render)
        return node

    def set_transforms(self, node, transforms):
        pos, hpr, scale, color, color_scale = transforms
        node.set_pos_hpr_scale(*pos, *hpr, *scale)
        if color != [1, 1, 1, 1]:
            node.set_color(*color)
        if color_scale != [1, 1, 1, 1]:
            node.set_color_scale(*color_scale)

    def load_nodes(self, mode, node_data):
        # slice off the plural
        mode_filename = mode.capitalize()[:-1]
        json_path = f"{G.DATABASE_DIRECTORY}{mode_filename}Library{G.JSON}"
        json_data = json.loads(open(json_path).read())
        # cleanup and load
        if mode == AG.ACTORS:
            for actor in self.actors:
                actor.delete()

            for data_name in node_data:
                name, index, part = data_name.split("|")
                model, anims = json_data[name]
                node = self.generate_actor(model, anims)
                self.set_transforms(node, node_data[data_name])
                self.actors.append(node)

        if mode == AG.PROPS:
            for prop in self.props:
                prop.remove_node()

            for data_name in node_data:
                name, index, part = data_name.split("|")
                model = json_data[name]
                node = self.generate_node(model)
                self.set_transforms(node, node_data[data_name])
                self.props.append(node)

        if mode == AG.PARTICLES:
            print('particles', node_data)