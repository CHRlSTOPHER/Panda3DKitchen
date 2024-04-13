import os
import sys
from pathlib import Path
from lxml import etree as ET
import json

import tkinter as tk
from tkinter import filedialog
import shutil

from classes.file.HandleXMLData import add_default_transform

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectFrame

from classes.apps.AppGlobals import XML_FILE_NAMES, PROPS
from classes.file.HandleJsonData import (FILES_JSON,
                                         update_json_last_selected)
from classes.editors.SceneEditor import SceneEditor
from classes.menus.MasterMenu import MasterMenu

BUTTONS = [
    ("CREATE", (-.19, 0, -.77), (.103, .103, .103)),
    ("LOAD", (.19, 0, -.77), (.111, .108, .104)),
    ("DELETE", (-.19, 0, -.902), (.109, .109, .109)),
    ("MOVE", (.193, 0, -.902), (.103, .103, .108)),
]
GUI_EDITOR = False
NODE_MOVER = True


class Startup(ShowBase):

    def __init__(self, root_folder):
        ShowBase.__init__(self)

        base.root_folder = root_folder
        base.project_location = None
        base.node_mover = None
        base.top_window = None
        self.project_frame = None
        self.display_regions = None
        self.commands = [
            self.create_project,
            self.load_project,
            self.delete_project,
            self.move_project,
        ]

        base.disable_mouse()
        base.set_background_color(0, .502, .502, 1)
        self.load_gui()
        self.accept('escape', exit)

    def load_gui(self):
        self.project_frame = DirectFrame(pos=(0, 0, .1), scale=1.1)
        i = 0
        for name, pos, scale in BUTTONS:
            DirectButton(parent=self.project_frame, text=name,
                         pos=pos, scale=scale, command=self.commands[i])
            i += 1

    def create_project(self):
        base.project_location = self.get_folder_location()
        if not base.project_location:
            return
        # create xml files
        for name in XML_FILE_NAMES:
            file = f"{base.project_location}/{name}.xml"
            # check if file already exists.
            file_check = Path(file)
            if file_check.is_file():
                print(f"{name}.xml already exists.")
                continue  # the file exists. don't overwrite.
            # otherwise, create the file.
            root = ET.Element(name)
            tree = ET.ElementTree(root)
            # add camera data to the prop xml file
            if name == PROPS:
                item = ET.SubElement(root, 'prop', name='camera', index='0')
                root_node = ET.SubElement(item, 'root_node')
                add_default_transform(root_node)
            tree.write(file, pretty_print=True, encoding="utf-8")

    def load_project(self):
        base.project_location = self.get_folder_location()
        # check if all project xml files are present.
        valid_files = self.validate_file(approve_mode=True)
        if not valid_files:
            print("Not all project files are present.")
            return

        # Add directory to path in case directory is in a different location.
        sys.path.append(base.project_location)
        self.project_frame.stash()

        # Load up all the editor tools
        base.master_menu = MasterMenu(gui_editor=GUI_EDITOR)
        base.scene_editor = SceneEditor([camera, base.scene_cam],
                                        base.scene_mouse_watcher,
                                        base.scene_region,
                                        base.scene_render,
                                        rot_cam_disable=False)
        if GUI_EDITOR or not NODE_MOVER:
            base.node_mover.set_move(False)

    def delete_project(self):
        base.project_location = self.get_folder_location()
        self.validate_file(delete_mode=True)

    def move_project(self):
        old_folder_location = self.get_folder_location()
        if not old_folder_location:
            return
        new_folder_location = self.get_folder_location()
        if not new_folder_location:
            return

        try:
            shutil.move(old_folder_location, new_folder_location)
        except FileNotFoundError as FNFE:
            print(FNFE)
        except PermissionError as PE:
            print(PE)

    def validate_file(self, approve_mode=False, delete_mode=False):
        for filename in XML_FILE_NAMES:
            file = f"{base.project_location}/{filename}.xml"
            # if file exists and mode is delete, remove file.
            if os.path.exists(file) and delete_mode:
                os.remove(file)
            # if file does not exist and mode is approved, return False.
            if not os.path.exists(file) and approve_mode:
                return False
        return True  # otherwise default to True.

    def get_folder_location(self):
        root = tk.Tk()
        root.withdraw()  # Hide the tk box that pops up.
        json_files = json.loads(open(FILES_JSON).read())
        last_project = json_files["last-project"]
        folder_location = filedialog.askdirectory(initialdir=last_project)
        root.destroy()
        update_json_last_selected(folder_location, "last-project")

        return folder_location
