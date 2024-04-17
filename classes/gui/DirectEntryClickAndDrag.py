from direct.gui.DirectGui import DGG
from direct.showbase.DirectObject import DirectObject

UPDATE_TASK = "update_dced_task"
MODIFY_TASK = "modify_node_trasform_task"
MODIFY_SPEED = {
    "XYZ": 1.0,
    "HPR": 5.0,
    "SXSYSZ": 0.1,
    "FOV": 1.0
}


class DirectEntryClickAndDrag(DirectObject):

    def __init__(self, entry, func_catalog=None):
        DirectObject.__init__(self)
        self.entry = entry
        self.func_catalog = func_catalog
        self.entry_name = entry.get_name()
        self.node = None
        self.last_value = None
        self.mouse_start_x = 0
        self.in_focus = False
        self.combined_toggle = True
        self.bind_entries()

    def bind_entries(self):
        self.entry.bind(DGG.B1PRESS, self.modify_task_toggle, extraArgs=[True])
        self.entry.bind(DGG.B1RELEASE, self.modify_task_toggle,
                        extraArgs=[False])
        self.entry['command'] = self.update_value
        self.entry['focusInCommand'] = self.set_in_focus
        self.entry['focusOutCommand'] = self.set_out_focus
        self.accept('control-a', self.delete_entry)

    # When the user presses enter, update the entry value.
    def update_value(self, mouse_data=None):
        if not self.func_catalog:
            return
        # check if the entry number is valid
        # remove the decimal and - num sign if there is one.
        value = self.entry.get().replace(".", "").replace("-", "")
        set = self.func_catalog[self.entry_name][1]
        if value.isnumeric():
            # set the node value to the entry text value
            set(float(self.entry.get()))
        elif value == "": # set node and entry to 0 if empty.
            self.entry.set(str(0))
            set(float(self.entry.get()))

    def modify_task_toggle(self, press, mouse_data):
        if press:
            self.mouse_start_x = base.mouseWatcherNode.get_mouse_x()
            taskMgr.add(self.modify_entry, MODIFY_TASK)
        else:
            taskMgr.remove(MODIFY_TASK)

    # when the user clicks and drags, move value based on how far mouse is
    def modify_entry(self, task):
        if not self.func_catalog:
            return
        mouse_x = base.mouseWatcherNode.get_mouse_x()
        # define the get and set functions for the desired transform func
        get = self.func_catalog[self.entry_name][0]
        set = self.func_catalog[self.entry_name][1]
        # determine which way to go
        if mouse_x > self.mouse_start_x:
            increment = mouse_x - self.mouse_start_x
        else:
            increment = -(self.mouse_start_x - mouse_x)

        modify_speed = self.get_modify_speed()
        # check if the entry is in the combined entries and
        # check if it's okay to do multiple entry adjustments at once.
        if self.entry_name in self.combined_entries and self.combined_toggle:
            for entry_name in self.combined_entries:
                get = self.func_catalog[entry_name][0]
                set = self.func_catalog[entry_name][1]
                set(get() + (increment * modify_speed))
        else:
            set(get() + (increment * modify_speed))
        return task.again

    def delete_entry(self):
        if self.in_focus:
            self.entry.set("0.00")
            set = self.func_catalog[self.entry_name][1]
            set(0.00) # set transform to 0.00

    def disable_entry(self):
        self.entry['state'] = DGG.DISABLED
        self.entry.set("") # clear entry
        self.func_catalog = {}
        self.node = None

    def enable_entry(self):
        if self.node:
            get_transform = self.func_catalog.get(self.entry_name)[0]
            converted_float = round(float(get_transform()), 2)
            self.entry.set(str(converted_float))
        self.entry['state'] = DGG.NORMAL

    def get_modify_speed(self):
        for speed_type in MODIFY_SPEED:
            if self.entry_name in speed_type:
                return MODIFY_SPEED.get(speed_type)

    def set_in_focus(self):
        self.in_focus = True

    def set_out_focus(self):
        self.in_focus = False

    def get_entry(self):
        return self.entry

    def get_last_value(self):
        return self.last_value

    def set_last_value(self, value):
        self.last_value = value

    def get_func_catalog(self):
        return self.func_catalog

    def set_func_catalog(self, func_catalog):
        self.func_catalog = func_catalog

    def get_node(self):
        if self.node:
            return self.node
        else: # node is empty and cannot be called what-so-ever
            return None

    # pass in a list of entry names. if one of them is modified, they all are.
    def set_combined_entries(self, entry_names):
        self.combined_entries = entry_names

    def set_combined_toggle(self, toggle):
        self.combined_toggle = toggle

    def set_node(self, node):
        self.node = node
