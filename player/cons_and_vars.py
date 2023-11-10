
# from dataclasses import dataclass
from pathlib import Path
from json import load, dump
# import shutil


def open_json(path_json):
    with open(path_json) as f:
        json_dic = load(f)
    return json_dic

def save_json(json_dic, path_json):
    with open(path_json, 'w') as f:
        dump(json_dic, f, indent=2)
    return

WORKING_DIRECTORY = Path().resolve()
PATH_JSON_PLAYLIST = Path(WORKING_DIRECTORY, 'track_list.json')

