""" SETTINGS CONFIG, AN ESSENTIAL FILE FOR BASIC NEEDS """
import json

from panda3d.core import loadPrcFileData, CullBinManager

from classes.settings import Globals as G

def load_settings(current_path):
    # Define json data
    json_settings = json.loads(open(G.SETTINGS_JSON).read())
    file_settings = json.loads(open(G.FILE_JSON).read())

    # Define default resources
    default_path = current_path + G.RESOURCES
    model_paths = [default_path]
    # Define external resources and add to list of model paths
    for resource_dir in file_settings[G.EXTERNAL_RESOURCES]:
        model_paths.append(resource_dir)

    # Add resource directories to model path prc file
    for path in model_paths:
        loadPrcFileData("", f"model-path {path}")

    loadPrcFileData("", f"default-model-extension "
                        f"{json_settings['default_model_extension']}")

    loadPrcFileData("", f"window-title {G.WINDOW_TITLE}")
    loadPrcFileData("", f"icon-filename {G.EDITOR}{G.ICON_FILENAME}")

    loadPrcFileData("", f"depth-bits {json_settings['bits']}")
    loadPrcFileData("", "framebuffer-multisample"
                        f"{json_settings[G.FRAMEBUFFER_MULTISAMPLE]}")
    loadPrcFileData("", f"multisamples {json_settings[G.MULTISAMPLES]}")
    if json_settings[G.FULL_SCREEN]:
        loadPrcFileData("", "fullscreen #t")
    loadPrcFileData("", f"win-size {json_settings[G.WINDOW_SIZE]}")
    loadPrcFileData("", f"undecorated {json_settings[G.BORDERLESS]}")
    loadPrcFileData("", f"show-frame-rate-meter {json_settings[G.FPS_METER]}")

    # Shadow bin for drop shadows
    cbm = CullBinManager.getGlobalPtr()
    cbm.addBin('shadow', CullBinManager.BTBackToFront, 20)
