import os
import sys
from pathlib import Path

from direct.showbase.DirectObject import DirectObject
from lxml import etree as ET
import json

import tkinter as tk
from tkinter import filedialog
import shutil

from classes.file.HandleXMLData import add_custom_transform

from direct.gui.DirectGui import DirectButton, DirectFrame

from classes.apps.AppGlobals import XML_FILE_NAMES, PROPS
from classes.file.HandleJsonData import (FILES_JSON,
                                         update_json_last_selected)
from classes.menus import MenuGlobals as MG
from classes.editors.GuiEditor import GuiEditor
from classes.settings import Globals as G

BUTTONS = [
    ("CREATE", (-.19, 0, -.77), (.103, .103, .103)),
    ("LOAD", (.19, 0, -.77), (.111, .108, .104)),
    ("DELETE", (-.19, 0, -.902), (.109, .109, .109)),
    ("MOVE", (.193, 0, -.902), (.103, .103, .108)),
]
GUI_EDITOR = True
NODE_MOVER = True


class StartMenu(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.kitchen = None
        self.commands = [
            self.create_project,
            self.load_project,
            self.delete_project,
            self.move_project,
        ]

        self.load_gui()
        self.accept('escape', exit)

    def generate(self):
        self.kitchen.set_background_color(0, .502, .502, 1)

    def load_gui(self):
        self.project_frame = DirectFrame(pos=(0, 0, .1), scale=1.1)
        i = 0
        for name, pos, scale in BUTTONS:
            DirectButton(parent=self.project_frame, text=name,
                         pos=pos, scale=scale, command=self.commands[i])
            i += 1

    def create_project(self):
        self.project_location = self.get_folder_location()
        if not self.project_location:
            return
        # create xml files
        for name in XML_FILE_NAMES:
            file = f"{self.project_location}/{name}.xml"
            # check if file already exists.
            file_check = Path(file)
            if file_check.is_file():
                print(f"{name}.xml already exists.")
                continue  # the file exists. don't overwrite.
            # otherwise, create the file.
            root = ET.Element(name)
            tree = ET.ElementTree(root)
            # add camera data to the prop xml file by default
            if name == PROPS:
                item = ET.SubElement(root, 'prop', name='camera', index='0')
                root_node = ET.SubElement(item, 'root_node')
                add_custom_transform(root_node, pos=(0, -15, 1))
            tree.write(file, pretty_print=True, encoding="utf-8")

    def load_project(self):
        self.project_location = self.get_folder_location()
        # check if all project xml files are present.
        valid_files = self.validate_file(approve_mode=True)
        if not valid_files:
            print("Not all project files are present.")
            return

        # Add directory to path in case directory is in a different location.
        sys.path.append(self.project_location)
        self.project_frame.stash()
        self.kitchen.set_project_location(self.project_location)
        self.kitchen.generate_classes()
        self.kitchen.define_variable_names()

    def delete_project(self):
        self.project_location = self.get_folder_location()
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
            file = f"{self.project_location}/{filename}.xml"
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

    def set_kitchen(self, kitchen):
        self.kitchen = kitchen
