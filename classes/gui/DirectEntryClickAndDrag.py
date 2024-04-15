from direct.gui.DirectGui import DGG

UPDATE_TASK = "update_dced_task"
MODIFY_TASK = "modify_node_trasform_task"
MODIFY_SPEED = {
    "XYZ": 1.0,
    "HPR": 5.0,
    "SXSYSZ": 0.1,
    "FOV": 1.0
}


class DirectEntryClickAndDrag:

    def __init__(self, entry, func_catalog=None):
        self.entry = entry
        self.func_catalog = func_catalog
        self.entry_name = entry.get_name()
        self.last_value = None
        self.mouse_start_x = 0
        self.in_focus = False
        self.bind_entries()

    def bind_entries(self):
        self.entry.bind(DGG.B1PRESS, self.modify_task_toggle, extraArgs=[True])
        self.entry.bind(DGG.B1RELEASE, self.modify_task_toggle,
                        extraArgs=[False])
        self.entry['command'] = self.update_value
        self.entry['focusInCommand'] = self.set_in_focus
        self.entry['focusOutCommand'] = self.set_out_focus

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
        current_value = get()
        # determine which way to go
        if mouse_x > self.mouse_start_x:
            increment = mouse_x - self.mouse_start_x
        else:
            increment = -(self.mouse_start_x - mouse_x)

        modify_speed = self.get_modify_speed()
        set(current_value + (increment * modify_speed))
        return task.again

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
