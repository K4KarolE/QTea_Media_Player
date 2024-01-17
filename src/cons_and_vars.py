
from dataclasses import dataclass
from pathlib import Path
from json import load, dump
import re


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

    ''' SUPPORTING VARIABLES '''
    skin_selected = settings['skin_selected']
    repeat_playlist = settings['repeat_playlist']
    shuffle_playlist_on = settings['shuffle_playlist_on']
    volume = settings['volume']
    icon_size = 20  # used for the buttons
    playing_track_index = 0
    is_speaker_muted = False
    audio_tracks_amount = 0
    audio_track_played = 0
    
    '''
    ACTIVE UTILITY VALUES
    src / func_coll.py / active_utility()
    Updated after every playlist/tab change
    '''
    active_tab = settings['last_used_tab']
    active_playlist_title = None
    last_track_index = 0
    active_db_table = None  
    active_pl_name = None   # widget
    active_pl_duration = None   # widget
    active_pl_sum_duration = 0
    
    ''' DURATION FROM DB / DISPLAY READY DURATION VALUE '''
    track_full_duration = 0
    track_full_duration_to_display = 0

    ''' DISPLAYED DURATION COUNT DOWN TYPES '''
    is_duration_to_display_straight = True
    duration_to_display_straight = 0
    duration_to_display_back = 0

    ''' GENERAL TAB - SETTINGS WINDOW '''
    small_jump = settings['general_settings']['small_jump']
    medium_jump = settings['general_settings']['medium_jump']
    big_jump = settings['general_settings']['big_jump']
    always_on_top = settings['general_settings']['always_on_top']

    general_settings_dic = {
        'small_jump': {
            'text': 'Small jump (second)',
            'value': small_jump,
            'line_edit_widget': ''
        },
        'medium_jump': {
            'text': 'Medium jump (second)',
            'value': medium_jump,
            'line_edit_widget': ''
        },
        'big_jump': {
            'text': 'Big jump (second)',
            'value': big_jump,
            'line_edit_widget': ''
        },
        'always_on_top': {
            'text': 'Always on top',
            'value': always_on_top,
            'line_edit_widget': ''
        },
    }


    ''' HOTKEYS TAB - SETTINGS WINDOW '''
    small_jump_backward = settings['hotkey_settings']['small_jump_backward']
    small_jump_forward = settings['hotkey_settings']['small_jump_forward']
    medium_jump_backward = settings['hotkey_settings']['medium_jump_backward']
    medium_jump_forward = settings['hotkey_settings']['medium_jump_forward']
    big_jump_backward = settings['hotkey_settings']['big_jump_backward']
    big_jump_forward = settings['hotkey_settings']['big_jump_forward']
    volume_mute = settings['hotkey_settings']['volume_mute']
    volume_up = settings['hotkey_settings']['volume_up']
    volume_down = settings['hotkey_settings']['volume_down']
    audio_tracks_rotate = settings['hotkey_settings']['audio_tracks_rotate']
    play_pause = settings['hotkey_settings']['play_pause']
    next_track = settings['hotkey_settings']['next_track']
    previous_track = settings['hotkey_settings']['previous_track']


    hotkey_settings_dic = {
        'small_jump_backward': {
            'text': 'Small jump backward',
            'value': small_jump_backward,
            'line_edit_widget': ''
        },
        'small_jump_forward': {
            'text': 'Small jump forward',
            'value': small_jump_forward,
            'line_edit_widget': ''
        },
        'medium_jump_backward': {
            'text': 'Medium jump backward',
            'value': medium_jump_backward,
            'line_edit_widget': ''
        },
        'medium_jump_forward': {
            'text': 'Medium jump forward',
            'value': medium_jump_forward,
            'line_edit_widget': ''
        },
        'big_jump_backward': {
            'text': 'Big jump backward',
            'value': big_jump_backward,
            'line_edit_widget': ''
        },
        'big_jump_forward': {
            'text': 'Big jump forward',
            'value': big_jump_forward,
            'line_edit_widget': ''
        },
        'volume_mute': {
            'text': 'Volume - Mute',
            'value': volume_mute,
            'line_edit_widget': ''
        },
        'volume_up': {
            'text': 'Volume - Increase',
            'value': volume_up,
            'line_edit_widget': ''
        },
        'volume_down': {
            'text': 'Volume - Decrease',
            'value': volume_down,
            'line_edit_widget': ''
        },
        'audio_tracks_rotate': {
            'text': 'Audio track - use next',
            'value': audio_tracks_rotate,
            'line_edit_widget': ''
        },
        'play_pause': {
            'text': 'Play / pause',
            'value': play_pause,
            'line_edit_widget': ''
        },
        'previous_track': {
            'text': 'Play previous track',
            'value': previous_track,
            'line_edit_widget': ''
        },
        'next_track': {
            'text': 'Play next track',
            'value': next_track,
            'line_edit_widget': ''
        }
    }


    ''' REGEX FOR SETTINGS WINDOW / HOTKEYS VALIDATION '''
    ''' More info in the docs / learning / regex_for_hotkey_validation.py '''
    keys_list = ['Shift', 'Alt', 'Enter', 'Space', 'Ctrl', 'Del', 'Left', 'Right', 'Backspace', '[a-zA-Z0-9]', '[.+-]']

    # ONE KEY
    exp_1 = r''
    for item in keys_list[0:-1]:
        exp_1 = exp_1 + f'^{item}$|'
    exp_1 = exp_1 + f'^{keys_list[-1]}$'

    # TWO KEYS
    exp_2 = r'('
    for item in keys_list[0:-1]:
        exp_2 = exp_2 + f'^{item}|'
    exp_2 = exp_2 + f'^{keys_list[-1]})\+('

    for item in keys_list[0:-1]:
        exp_2 = exp_2 + f'{item}$|'
    exp_2 = exp_2 + f'{keys_list[-1]}$)'

    # THREE KEYS
    exp_3 = r'('
    for item in keys_list[0:-1]:
        exp_3 = exp_3 + f'^{item}|'
    exp_3 = exp_3+ f'^{keys_list[-1]})\+('

    for item in keys_list[0:-1]:
        exp_3 = exp_3 + f'{item}|'
    exp_3 = exp_3+ f'{keys_list[-1]})\+('

    for item in keys_list[0:-1]:
        exp_3 = exp_3 + f'{item}$|'
    exp_3 = exp_3+ f'{keys_list[-1]}$)'

    search_regex = re.compile(f'{exp_1}|{exp_2}|{exp_3}')



    ''' FILE TYPES '''
    '''
        MEDIA_FILES - used to select the correct files from the selected dictionary
                    - `AD - Add Directory` button

        FILE_TYPES_LIST - used to sort the files in the file dialog window
                        - `AT - Add Track` button
    '''
    MEDIA_FILES = "Media files (*.mp3 *.wav *.flac *.midi *.aac *.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
    AUDIO_FILES = "Audio files (*.mp3 *.wav *.flac *.midi *.aac)"
    VIDEO_FILES = "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
    FILE_TYPES_LIST = [MEDIA_FILES, AUDIO_FILES, VIDEO_FILES]
    


    ''' PLAYLISTS '''
    '''
        The dictionary used to:
        - create playlist-tabs in src/tabs.py
        - be able to access to the right widget
    '''
    paylist_widget_dic = {}

    playlist_amount = 20
    for i in range(0, playlist_amount):
        pl_name = f'playlist_{i}'
        paylist_widget_dic[pl_name] = {
            'name_list_widget': '',
            'duration_list_widget': '',
            'active_pl_sum_duration': 0
            }
      
    paylist_list = list(paylist_widget_dic)


cv = Data()