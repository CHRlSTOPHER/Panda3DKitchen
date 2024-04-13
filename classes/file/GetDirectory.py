import tkinter as tk
from tkinter import filedialog

from panda3d.core import ConfigVariableList

PATH_NOT_FOUND = ("cannot be not found using the directories defined in "
                  "'external-resources' (json/files.json)")


# Returns the directory relative to resources and the file name.
def get_resource_and_filename(title="", initialdir="", multiple=False):

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
    if multiple:
        file_location = (filedialog.askopenfilenames(
                            title=title, initialdir=initialdir))
    else:
        file_location = filedialog.askopenfilename(
                            title=title, initialdir=initialdir)
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
