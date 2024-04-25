"""
Hover your mouse over a node. Press left mouse button to select it.
Detect nodes using a collision ray. Move collision ray around with the mouse.
"""
from panda3d.core import (CollisionTraverser, CollisionRay, CollisionNode,
                          GeomNode, CollisionHandlerQueue)
from direct.showbase.DirectObject import DirectObject

from classes.settings import Globals as G

RAY_MOUSE_TASK = "ray_mouse_task"


class NodeSelector(DirectObject):

    def __init__(self, class_object=None):
        DirectObject.__init__(self)
        self.kitchen = None
        self.class_object = class_object
        self.camera = None
        self.render = None
        self.mouse_watcher = None
        self.ray_node = None
        self.mouse_ray = None
        self.ray_collision_node = None
        self.collision_handler = None
        self.collision_handler = CollisionHandlerQueue()
        self.coll_traverser = CollisionTraverser("coll_traverser")

    def generate(self):
        self.create_ray_collision()
        self.accept(G.LEFT_MOUSE_BUTTON, self.select_node)
        self.kitchen.taskMgr.add(self.sync_ray_with_mouse_pos, RAY_MOUSE_TASK)

    def create_ray_collision(self):
        self.mouse_ray = CollisionRay()
        self.mouse_ray.set_direction(0, 1, 0)
        self.ray_collision_node = CollisionNode("mouse_ray")
        self.ray_collision_node.add_solid(self.mouse_ray)
        self.ray_collision_node.set_from_collide_mask(
            GeomNode.get_default_collide_mask())

        self.ray_node = self.kitchen.scene_camera.attach_new_node(
                                                self.ray_collision_node)

    def select_node(self):
        # check if mouse is in the display_region
        if not self.kitchen.scene_mw.has_mouse():
            return

        # detect what is being collided.
        self.coll_traverser.add_collider(self.ray_node, self.collision_handler)
        self.coll_traverser.traverse(self.kitchen.scene_render)
        if (not self.class_object
                or not self.collision_handler.get_num_entries()):
            return

        self.collision_handler.sort_entries()
        # Look through entries for the closest selected node that is valid.
        for entry in range(0, self.collision_handler.get_num_entries()):
            node = self.get_node_from_handler(entry)
            valid_node = self.verify_node(node)
            if valid_node:
                self.kitchen.update_selected_node(node)
                break

        # If we keep the collider, the ray will do unnecessary extra work.
        self.coll_traverser.remove_collider(self.ray_node)

    def verify_node(self, node):
        if node and hasattr(self.class_object, "set_node"):
            if node.get_name() in G.SPECIAL_NODES:
                return False  # this node got the fake timbs
            else:
                return True  # we found a valid node

    def get_node_from_handler(self, index):
        node = self.collision_handler.getEntry(index).get_into_node_path()
        if node == self.render or node.is_hidden():
            return None  # Do NOT allow render or hidden nodes to be selected.

        # the special flag lets you pick nodes that aren't reparented to render
        while True:
            if node.get_name() == "":
                """Ignore nodes without names."""
            elif (node.get_parent() == self.kitchen.scene_render or
                  node.get_name()[0] in G.SPECIAL_NODE_IFIER_FLAG):
                break
            node = node.get_parent()

        return node

    def sync_ray_with_mouse_pos(self, task):
        if self.kitchen.scene_mw.has_mouse():
            mouse = self.kitchen.scene_mw.get_mouse()
            self.mouse_ray.set_from_lens(self.kitchen.scene_camera.node(),
                                         mouse.x, mouse.y)

        return task.again

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen

    def cleanup(self):
        self.kitchen.taskMgr.remove(RAY_MOUSE_TASK)
        self.ignore_all()
