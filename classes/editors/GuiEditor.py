"""
Barely functional. I would not advise using it in its current state.
"""
from panda3d.core import KeyboardButton
from direct.showbase.DirectObject import DirectObject

INCREMENT = .003


class GuiEditor(DirectObject):

    def __init__(self, gui=None, with_args=True):
        DirectObject.__init__(self)
        self.transform_inputs = {}
        self.gui = gui
        self.with_args = with_args
        self.single_scale_inputs = None
        self.pad_inputs = None

        if gui:
            self.set_gui(gui, with_args)

    def load_input_dict(self):
        self.transform_inputs = {
            'w': [self.gui.get_z, self.gui.set_z, INCREMENT],
            's': [self.gui.get_z, self.gui.set_z, -INCREMENT],
            'a': [self.gui.get_x, self.gui.set_x, -INCREMENT],
            'd': [self.gui.get_x, self.gui.set_x, INCREMENT],
            'q': [self.gui.get_scale, self.gui.set_scale, -INCREMENT],
            'e': [self.gui.get_scale, self.gui.set_scale, INCREMENT],
        }

    def load_inputs(self):
        self.pad_inputs = {
            'arrow_left': (-INCREMENT, 0),
            'arrow_right': (INCREMENT, 0),
            'arrow_up': (0, INCREMENT),
            'arrow_down': (0, -INCREMENT),
        }
        self.single_scale_inputs = {
            'arrow_left': [self.gui.get_sx, self.gui.set_sx, -INCREMENT],
            'arrow_right': [self.gui.get_sx, self.gui.set_sx, INCREMENT],
            'arrow_up': [self.gui.get_sz, self.gui.set_sz, INCREMENT],
            'arrow_down': [self.gui.get_sz, self.gui.set_sz, -INCREMENT]
        }

        # pos and scale inputs
        for input in self.transform_inputs:
            get = self.transform_inputs[input][0]
            set = self.transform_inputs[input][1]
            value = self.transform_inputs[input][2]
            task = input + '_task'
            self.accept(input, self.move_task, extraArgs=[get, set,
                                                          value, task])
            self.accept(input + "-up", taskMgr.remove, extraArgs=[task])

        # padding inputs
        for input in self.pad_inputs:
            value = self.pad_inputs[input]
            task = input + '_task'
            self.accept(input, self.pad_task, extraArgs=[value, task])
            self.accept(input + "-up", taskMgr.remove, extraArgs=[task])

        # scaling single axis inputs
        for input in self.single_scale_inputs:
            get = self.single_scale_inputs[input][0]
            set = self.single_scale_inputs[input][1]
            value = self.single_scale_inputs[input][2]
            task = f"shift-{input}-task"
            self.accept("shift-" + input, self.single_scale_task,
                        extraArgs=[get, set, value, task])

    def move_task(self, get, set, value, task):
        def move_gui(get, set, value, task):
            current_pos = get()
            set(current_pos + value)
            self.print_gui_data()
            return task.again

        taskMgr.add(move_gui, task, appendTask=True,
                    extraArgs=[get, set, value])

    def pad_task(self, value, task):
        def pad_gui(value, task):
            padding = self.gui['pad']
            new_padding = (padding[0] + value[0], padding[1] + value[1])
            self.gui['pad'] = new_padding
            self.print_gui_data()
            return task.again

        taskMgr.add(pad_gui, task, appendTask=True, extraArgs=[value])

    def single_scale_task(self, get, set, value, task):
        def single_scale_gui(get, set, value, task):
            current_scale = get()
            set(current_scale + value)
            self.print_gui_data()

            shift = base.mouseWatcherNode.isButtonDown(KeyboardButton.shift())
            up = base.mouseWatcherNode.isButtonDown(KeyboardButton.up())
            down = base.mouseWatcherNode.isButtonDown(KeyboardButton.down())
            left = base.mouseWatcherNode.isButtonDown(KeyboardButton.left())
            right = base.mouseWatcherNode.isButtonDown(
                KeyboardButton.right())
            self.keys = {'up': up, 'down': down, 'left': left, 'right': right}

            key = str(task).split('-')[1].split('_')[1]
            if not shift or not self.keys[key]:
                return task.done
            return task.again

        taskMgr.add(single_scale_gui, task, appendTask=True,
                    extraArgs=[get, set, value])

    def print_gui_data(self):
        x, y, z = self.gui.get_pos()
        sx, sy, sz = self.gui.get_scale()
        x, y, z, sx, sy, sz = [round(i, 3) for i in [x, y, z, sx, sy, sz]]
        pad = self.gui['pad']
        pad = (round(pad[0], 3), round(pad[1], 3))

        if self.with_args:
            print(f'pos={(x, y, z)},\nscale={sx, sy, sz},\npad={pad},')
        else:
            print(f'{(x, y, z)}, {sx, sy, sz}, {pad},')

    def set_gui(self, gui, with_args=True):
        self.gui = gui
        self.with_args = with_args
        self.load_input_dict()
        self.load_inputs()
