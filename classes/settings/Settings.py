""" SETTINGS CONFIG, AN ESSENTIAL FILE FOR BASIC NEEDS """
import json

from panda3d.core import loadPrcFileData, CullBinManager, Filename

from classes.settings import Globals as G


def load_prc_data(var, value):
    loadPrcFileData("", f"{var} {value}")

def load_settings(current_path):
    # Define json data
    json_settings = json.loads(open(G.SETTINGS_JSON).read())
    file_settings = json.loads(open(G.FILE_JSON).read())

    # Define external resource directories.
    model_paths = file_settings[G.EXTERNAL_RESOURCES]
    # Define and add the default resource directory
    default_path = f"{current_path}/{G.RESOURCES}"
    model_paths.append(default_path)

    # Add resource directories to the prc model-path variable
    for path in model_paths:
        loadPrcFileData("", f"model-path {Filename(path)}")

    # load all prc_settings from file
    for var, value in json_settings.items():
        load_prc_data(var, value)

    # Shadow bin for drop shadows
    cbm = CullBinManager.getGlobalPtr()
    cbm.addBin('shadow', CullBinManager.BTBackToFront, 20)
