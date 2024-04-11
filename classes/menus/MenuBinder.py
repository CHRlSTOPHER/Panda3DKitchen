from panda3d.core import PGButton, MouseButton
from direct.gui.DirectGui import DGG

WHEELUP = (PGButton.getPressPrefix() + MouseButton.wheel_up().getName()
           + '-')
WHEELDOWN = (PGButton.getPressPrefix() + MouseButton.wheel_down().getName()
             + '-')


def bind_frame_scrolling(scroll_frame, func_up, func_down):
    # Bind the part that you click and hold to scroll.
    thumb = scroll_frame.verticalScroll.thumb
    thumb.bind(WHEELUP, func_up)
    thumb.bind(WHEELDOWN, func_down)

    # Enable the canvas space and bind the whole thing,
    scroll_frame['state'] = DGG.NORMAL
    scroll_frame.bind(WHEELUP, func_up)
    scroll_frame.bind(WHEELDOWN, func_down)
    scroll_frame.verticalScroll.bind(WHEELUP, func_up)
    scroll_frame.verticalScroll.bind(WHEELDOWN, func_down)
