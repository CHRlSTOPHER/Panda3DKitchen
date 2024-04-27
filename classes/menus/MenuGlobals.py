from classes.settings.Globals import EDITOR
ENTITY_MODE_BUTTONS = [
    ["Actor", (-0.653, 0.0, -0.755), (0.217, 0.121, 0.15), (0, 0.053)],
    ["Prop", (-0.197, 0.0, -0.755), (0.208, 0.127, 0.156), (0.045, 0.008)],
    ["Texture", (0.256, 0.0, -0.755), (0.217, 0.121, 0.15), (0, 0.041)],
    ["Particle", (0.691, 0.0, -0.755), (0.199, 0.097, 0.141), (-0.003, 0.116)]
]
DISABLED_COLOR = (.9, .9, .9, 1)
DISABLED_COLOR_2 = (.5, .5, .5, 1)
ENABLED_COLOR = (1, 1, 1, 1)
SELECTED_BUTTON_COLOR = (0, .2, .2, 1)
FRAME_COLOR = {
    'library': (.9, .9, .7, 1),
    'scene': (.7, .9, .9, 1)
}
COLOR_SCALE = {
    'library': (.8, .8, .8, 1),
    'scene': (.8, .8, .8, 1)
}

BASE_CANVAS_SIZE = (-1, 1, 0, 1)
ENTITY_FRAME_POS = (-1.38, 0, 0)
SCENE_FRAME_POS = (1.475, 0, 0)
SCROLL_FRAME_COLOR = (.6, .6, .6, 1)
BIG_BUTT_SCALE_X = 1.16
BIG_BUTT_SCALE_Z = 1.27
CANVAS_LIMIT = 14
CANVAS_COLUMNS = 4
CANVAS_START_X = -.88
CANVAS_START_Z = .88
CANVAS_BUTTON_SCALE = (.094, 1, .105)
CANVAS_INCREMENT_X = .228
CANVAS_INCREMENT_Z = .251

CLICK_DRAG_CUR = "click-drag-indicator.cur"
BUTTON_MOVE_TASK = 'button_move'
FOLDER = "folder-color.png"
TRASH = "trash-can-color.png"
INSPECT = "inspect-color.png"
CAMERA_TEXTURE = 'capture-cam-color.png'
DICE_TEXTURE = 'rng-dice-color.png'
CANCEL_TEXTURE = 'cancel.png'
CHECK_TEXTURE = "checkmark.png"
SWAP_TEXTURE = "swap.png"
SCALE_ALL_TEXTURE = "scale-all.png"
SCALE_ONE_TEXTURE = "scale-one.png"
COMPUTER_FONT = "fonts/computer.otf"
MENU_VERT_1 = "menu1.jpg"
MENU_HOR_1 = "menu2.jpg"
MENU_HOR_2 = "menu3.png"
MENU_HOR_3 = "menu4.jpg"
VALUE = 'verticalScroll_value'

EDITOR_MAP_PATH = f"{EDITOR}/maps/"
