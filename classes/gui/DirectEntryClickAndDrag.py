from direct.gui.DirectGui import DGG

UPDATE_TASK = "update_dced_task"
MODIFY_TASK = "modify_node_trasform_task"


class DirectEntryClickAndDrag:

    def __init__(self, entry, node):
        self.node = node
        self.entry = entry
        self.entry_name = entry.get_name()
        self.func_catalog = {}
        self.last_value = 0
        self.mouse_x = 0
        self.last_mouse_x = 0
        self.in_focus = False

        self.define_func_catalog()
        self.bind_entries()
        # Choose the float below because it felt like a good speed.
        # Not too slow, but not so fast that it is wastefully updating.
        taskMgr.doMethodLater(.03, self.update_entry, UPDATE_TASK)

    def define_func_catalog(self):
        self.func_catalog = {
            'X': [self.node.get_x, self.node.set_x],
            'Y': [self.node.get_y, self.node.set_y],
            'Z': [self.node.get_z, self.node.set_z],
            'H': [self.node.get_h, self.node.set_h],
            'P': [self.node.get_p, self.node.set_p],
            'R': [self.node.get_r, self.node.set_r],
            'SX': [self.node.get_sx, self.node.set_sx],
            'SY': [self.node.get_sy, self.node.set_sy],
            'SZ': [self.node.get_sz, self.node.set_sz],
        }
        # check if get_fov exists.
        if hasattr(self.node, "get_fov"):
            self.func_catalog['FOV'] = [self.node.get_fov, self.node.set_fov]

    def bind_entries(self):
        self.entry.bind(DGG.B1PRESS, self.modify_node, extraArgs=[True])
        self.entry.bind(DGG.B1RELEASE, self.modify_node, extraArgs=[False])
        self.entry['command'] = self.update_value
        self.entry['focusInCommand'] = self.set_in_focus
        self.entry['focusOutCommand'] = self.set_out_focus

    def update_value(self, mouse_data=None):
        # check if the entry number is valid
        # remove the decimal and - num sign if there is one.
        value = self.entry.get().replace(".", "").replace("-", "")
        if value.isnumeric():
            set = self.func_catalog[self.entry_name][1]
            # set the node value to the entry text value
            set(float(self.entry.get()))

    def modify_node(self, press, mouse_data):
        pass # MODIFY_TASK

    # update very often in case node mover changed the transform values
    def update_entry(self, task):
        # call the get() func and round the value
        get = self.func_catalog[self.entry_name][0]
        value = round(float(get()), 2)

        if self.last_value == value:
            return task.again # no need to update the same value

        self.entry.set(str(value))
        self.entry.setCursorPosition(6)  # Mandatory camel case >:(
        self.last_value = value
        return task.again

    def set_in_focus(self):
        self.in_focus = True

    def set_out_focus(self):
        self.in_focus = False