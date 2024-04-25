import tkinter as tk
from tkinter import filedialog

from panda3d.core import ConfigVariableList

from classes.settings.Globals import SUPPORTED_FILETYPES

PATH_NOT_FOUND = ("cannot be not found using the directories defined in "
                  "'external-resources' (json/files.json)")


# Returns the directory relative to resources and the file name.
def get_resource_and_filename(title="", initialdir="", multiple=False, file_type=None):

    def get_resource_directory(file_location):
        item_name = ""
        filepath = ""
        path_found = False
        for model_path in ConfigVariableList("model-path"):
            if model_path in file_location:
                path_found = True
                break  # we found the model path we're looking for.

        if path_found:
            # remove the model path from the file location
            filepath = file_location.replace(model_path, "")
            path_list = filepath.split('/')
            path_list.reverse()
            # grab the first item from the list and remove the file extension.
            item_name = path_list[0].split('.')[0]

            # cut off forward slash at the start of the path if there is one.
            if filepath[0] == "/":
                filepath = filepath[1:]

        elif file_location != "":
            print(f'"{file_location}" {PATH_NOT_FOUND}')

        return item_name, filepath

    root = tk.Tk()
    root.withdraw()  # Hide the tk box that pops up.

    filedialog_kwargs = dict()

    specific_filetypes = SUPPORTED_FILETYPES.get(file_type)
    if specific_filetypes:
        file_extensions = set()
        for file_extension in specific_filetypes:
            file_extensions.add((file_type, f"*{file_extension}"))
        filedialog_kwargs["filetypes"] = file_extensions

    if multiple:
        file_location = (filedialog.askopenfilenames(
            title = title, initialdir = initialdir,
            **filedialog_kwargs
        ))
    else:
        file_location = filedialog.askopenfilename(
            title = title, initialdir = initialdir,
            **filedialog_kwargs
        )
    root.destroy()

    if not multiple:
        return get_resource_directory(file_location)

    item_names = []
    item_directories = []
    for location in file_location:
        item_name, item_directory = get_resource_directory(location)
        item_names.append(item_name)
        item_directories.append(item_directory)

    return item_names, item_directories
