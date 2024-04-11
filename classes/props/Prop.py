from panda3d.core import NodePath


class Prop(NodePath):

    def __init__(self, model_path, name="~prop", parent=None,
                 pos=(0, 0, 0), hpr=(0, 0, 0), scale=(1, 1, 1),
                 color=None, child=None):
        if child:
            NodePath.__init__(self,
                              loader.loadModel(model_path).find(f'**/{child}'))
        else:
            NodePath.__init__(self, loader.loadModel(model_path))

        self.set_name(name)
        if parent:
            self.reparent_to(parent)
        self.set_pos_hpr_scale(*pos, *hpr, *scale)
        if color:
            self.set_color(*color)