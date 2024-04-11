import json

from classes.settings import Globals as G

FILES_JSON = "json/files.json"


def update_json_file(path, save_data):
    with open(path) as f:
        data = json.load(f)

    data.update(save_data)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)


# Store the last selected directory for a project into the json file
def update_json_last_selected(folder_location, keyword):
    if folder_location == "":
        return  # Don't replace the last project with an empty string.
    update_json_file(FILES_JSON, {keyword: folder_location})


def update_library_database(mode, save_data):
    path = f"{G.DATABASE_DIRECTORY}{mode}Library.json"
    update_json_file(path, save_data)


def delete_json_data(path, entries):
    with open(path) as f:
        data = json.load(f)

    for entry in entries:
        del data[entry]

    with open(path, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)


def delete_json_entries(mode, entries):
    path = f"{G.DATABASE_DIRECTORY}{mode}Library.json"
    delete_json_data(path, entries)

