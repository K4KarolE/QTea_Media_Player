
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
PATH_JSON_SETTINGS = Path(WORKING_DIRECTORY, 'settings.json')
settings = open_json(PATH_JSON_SETTINGS)

@dataclass
class Data:
    skin_selected = settings['skin_selected']

    icon_size = 20

    active_tab = settings['last_used_tab']
    repeat_playlist = settings['repeat_playlist']
    shuffle_playlist_on = settings['shuffle_playlist_on']
    volume = settings['volume']
    
    active_db_table = None  # widget
    active_playlist = None  # widget
    active_pl_duration = None
    last_track_index = None

    # PLAYLIST
    paylist_widget_dic = {
        "paylist_0": {
            "name_list_widget": "none",
            "duration_list_widget": "none"
            },
        "paylist_1": {
            "name_list_widget": "none",
            "duration_list_widget": "none"
            },
        "paylist_2": {
            "name_list_widget": "none",
            "duration_list_widget": "none"
            }
        }       
    paylist_list = list(paylist_widget_dic.keys())

    MEDIA_FILES = "Media files (*.mp3 *.wav *.flac *.midi *.aac *.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
    AUDIO_FILES = "Audio files (*.mp3 *.wav *.flac *.midi *.aac)"
    VIDEO_FILES = "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
    FILE_TYPES_LIST = [MEDIA_FILES, AUDIO_FILES, VIDEO_FILES, 'All Files']