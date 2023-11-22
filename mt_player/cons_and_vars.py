
from dataclasses import dataclass
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
PATH_JSON_PAYLIST = Path(WORKING_DIRECTORY, 'paylist_dic.json')
PATH_JSON_SETTINGS = Path(WORKING_DIRECTORY, 'settings.json')

settings = open_json(PATH_JSON_SETTINGS)

@dataclass
class Data:
    active_tab = settings['last_used_tab']
    active_db_table = None
    active_playlist = None
    active_pl_duration = None
