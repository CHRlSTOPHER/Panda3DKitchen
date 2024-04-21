from direct.gui.DirectGui import DirectSlider, DirectFrame, DirectButton, DGG
from panda3d.core import TextNode

UPDATE_TASK = "update_slider_task"
SET_TIME_TASK = "set_time_task"
START_TIME = "00:00:00"
START_DURATION = "00000"


class SequenceSliderGui(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, pos=(0, 0, .15), scale=.8)
        self.slider = None
        self.seq_time = None
        self.track_time = None
        self.pause_button = None
        self.back_button = None
        self.forward_button = None
        self.initialiseoptions(SequenceSliderGui)

    def load_gui(self, range):
        self.reparent_to(self.kitchen.a2dBottomCenter)
        self.slider = DirectSlider(self, range=range, pos=(0, 0, 0),
                                   value=0, pageSize=.1, scale=.9)
        self.seq_time = DirectFrame(text=START_TIME, parent=self,
                                    pos=(.35, 0, .12), scale=(.13, 1, .13),
                                    text_align=TextNode.ALeft)
        self.track_time = DirectFrame(text=START_DURATION, parent=self,
                                      pos=(-.8, 0, .12),
                                      scale=(.13, 1, .13),
                                      text_align=TextNode.ALeft)
        self.pause_button = DirectButton(text="||", parent=self,
                                         pos=(0, 0, .119),
                                         scale=(.24, 1, .127))
        self.back_button = DirectButton(text="<", parent=self,
                                        pos=(-.145, 0, .12),
                                        scale=(.24, 1, .205))
        self.forward_button = DirectButton(text=">", parent=self,
                                           pos=(.145, 0, .12),
                                           scale=(.24, 1, .205))


class SequenceSlider(SequenceSliderGui):

    def __init__(self):
        SequenceSliderGui.__init__(self)
        self.kitchen = None
        self.within = False

        self.sequence = None
        self.duration = None
        self.time = 0
        self.pause = False
        self.manual_pause = True
        self.seq_time = None
        self.track_time = None

        self.pause_button = None
        self.back_button = None
        self.forward_button = None

    def generate(self):
        if self.sequence:
            self.duration = self.sequence.get_duration()
            self.load_gui((0, self.duration))
            self.bind_buttons()
            self.kitchen.taskMgr.doMethodLater(.01, self.update_slider,
                                               UPDATE_TASK)

    def bind_buttons(self):
        self.pause_button['command'] = self.toggle_button
        self.back_button['command'] = self.move_back
        self.forward_button['command'] = self.move_forward

        # Thumb is defined in the DirectSlider class.
        self.slider.thumb.bind(DGG.B1PRESS, self.toggle_time)
        self.slider.thumb.bind(DGG.B1RELEASE, self.toggle_time)
        self.slider.thumb.bind(DGG.WITHIN, self.set_within, extraArgs=[True])
        self.slider.thumb.bind(DGG.WITHIN, self.set_within, extraArgs=[False])

    def toggle_time(self, mouse_data):
        self.pause = not self.pause
        if self.pause:
            # Pause Sequence. Start task that updates time by input.
            self.sequence.pause()
            self.kitchen.taskMgr.doMethodLater(.01, self.set_slider_time,
                                               SET_TIME_TASK)
            self.kitchen.taskMgr.remove(UPDATE_TASK)
        else:
            # Resume Sequence. Start task that updates time by time passed.
            if not self.manual_pause:
                self.sequence.resume()
                self.kitchen.taskMgr.doMethodLater(.01, self.update_slider,
                                                   UPDATE_TASK)
                self.kitchen.taskMgr.remove(SET_TIME_TASK)

    def toggle_button(self):  # toogle pause button
        self.manual_pause = not self.manual_pause
        if self.manual_pause:
            self.sequence.pause()
        else:
            self.sequence.resume()
            self.kitchen.taskMgr.doMethodLater(.01, self.update_slider,
                                               UPDATE_TASK)
            self.kitchen.taskMgr.remove(SET_TIME_TASK)

    def update_slider(self, task):  # automatic time passage
        if not self.manual_pause:  # check if user pressed pause button
            current_time = self.sequence.getT()
            self.slider['value'] = current_time
            self.update_visible_time(current_time)
            return task.again

    def set_slider_time(self, task):  # manual user input
        self.sequence.setT(self.slider['value'])
        self.update_visible_time(self.slider['value'])
        return task.again

    def move_back(self):
        # The number below needs to be changed later.
        # It doesn't scale properly for longer animations.
        frame = self.slider['value'] - .01
        self.set_time(frame)

    def move_forward(self):
        frame = self.slider['value'] + .01
        self.set_time(frame)

    def set_time(self, frame):
        self.slider['value'] = frame
        self.sequence.setT(frame)
        self.update_visible_time(frame)

    def update_visible_time(self, frame):
        minutes = int(frame / 60.0)
        seconds = int(frame % 60)
        milliseconds = int(frame / .01 % 100)

        new_time = ""
        for measure in [minutes, seconds, milliseconds]:
            if measure < 10:
                measure = f"0{measure}"
            new_time += f"{measure}:"

        self.seq_time['text'] = new_time[:8]
        self.track_time['text'] = str(round(self.sequence.getT(), 2))

    def get_within(self):
        return self.within

    def set_sequence(self, sequence):
        self.sequence = sequence

    def set_within(self, within, mouse_data):
        self.within = within

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
