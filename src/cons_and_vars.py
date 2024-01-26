
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
    is_speaker_muted = False
    audio_tracks_amount = 0
    audio_track_played = 0
    subtitle_tracks_amount = 0
    subtitle_track_played = 0
    window_size_normal = True   # for window_size_toggle
    tabs_without_title_to_hide_index_list = []
    
    ''' 
    TO MANAGE THE PLAYLIST ACTIONS (PREV., NEXT, ..)
    playing_track_index 

    
    TO SAVE THE PLAY AND SELECTION HISTORY:
    From below and src / func_coll.py:
    
    ACTIVE TAB UTILITY
    update_active_tab_vars_and_widgets() -  cv.active_pl_last_track_index
    
    PLAYING TAB UTILITY
    update_playing_tab_vars_and_widgets() - cv.playing_pl_last_track_index
    '''
    playing_track_index = 0


    ''' 
    ACTIVE AND PLAYING PLAYLISTS/TABS SEPARATION
    More informaration in the README
    '''
    '''
    ACTIVE TAB UTILITY VALUES
    src / func_coll.py / active_tab_utility()
    Updated after every playlist/tab change
    '''
    active_tab = settings['last_used_tab']
    active_db_table = None  
    active_pl_title = None
    active_pl_last_track_index = 0
    active_pl_name = None   # widget
    active_pl_duration = None   # widget
    active_pl_sum_duration = 0
    active_pl_tracks_count = 0

    '''
    PLAYING TAB UTILITY VALUES
    src / func_coll.py / playing_tab_utility()
    '''
    playing_tab = settings['playing_tab']
    playing_db_table = None  
    playing_pl_title = None
    playing_pl_last_track_index = 0
    playing_pl_name = None   # widget
    playing_pl_duration = None   # widget
    playing_pl_tracks_count = 0

    
    ''' DURATION FROM DB / DISPLAY READY DURATION VALUE '''
    track_full_duration = 0
    track_full_duration_to_display = 0

    ''' DURATION FROM DB / DISPLAY READY DURATION VALUE '''
    track_current_duration = 0
    track_current_duration_to_display = 0
    counter_for_duration = 0

    ''' DISPLAYED DURATION COUNT DOWN TYPES '''
    is_duration_to_display_straight = True
    duration_to_display_straight = 0
    duration_to_display_back = 0

    ''' GENERAL TAB - SETTINGS WINDOW '''
    always_on_top = settings['general_settings']['always_on_top']
    continue_playback = settings['general_settings']['continue_playback']
    play_at_startup = settings['general_settings']['play_at_startup']
    small_jump = settings['general_settings']['small_jump']
    medium_jump = settings['general_settings']['medium_jump']
    big_jump = settings['general_settings']['big_jump']
    window_width = settings['general_settings']['window_width']
    window_height = settings['general_settings']['window_height']
    window_alt_width = settings['general_settings']['window_alt_width']
    window_alt_height = settings['general_settings']['window_alt_height']
    # USED FOR VALIDATION
    window_min_width = settings['general_settings']['window_min_width']
    window_min_height = settings['general_settings']['window_min_height']
    # COUNTER for play_at_startup
    played_at_startup_counter = False

    general_settings_dic = {
        'always_on_top': {
            'text': 'Always on top',
            'value': always_on_top,
            'line_edit_widget': ''
        },
        'continue_playback': {
            'text': 'Continue playback',
            'value': continue_playback,
            'line_edit_widget': ''
        },
        'play_at_startup': {
            'text': 'Play at startup',
            'value': play_at_startup,
            'line_edit_widget': ''
        },
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
        'window_width': {
            'text': 'Window width',
            'value': window_width,
            'line_edit_widget': ''
        },
        'window_height': {
            'text': 'Window height',
            'value': window_height,
            'line_edit_widget': ''
        },
        'window_alt_width': {
            'text': 'Window alt. width',
            'value': window_alt_width,
            'line_edit_widget': ''
        },
        'window_alt_height': {
            'text': 'Window alt. height',
            'value': window_alt_height,
            'line_edit_widget': ''
        }
    }

    # used in the src / settings_window.py / field validation - field save 
    gen_sett_boolean_text_list = [
        general_settings_dic['always_on_top']['text'],
        general_settings_dic['continue_playback']['text'],
        general_settings_dic['play_at_startup']['text']
        ]
    
    gen_sett_window_width_text_list = [
        general_settings_dic['window_width']['text'],
        general_settings_dic['window_alt_width']['text']
        ]
    
    gen_sett_window_height_text_list = [
        general_settings_dic['window_height']['text'],
        general_settings_dic['window_alt_height']['text']
        ]
    
    gen_sett_jump_text_list = [
        general_settings_dic['small_jump']['text'],
        general_settings_dic['medium_jump']['text'],
        general_settings_dic['big_jump']['text'],
        ]
    
    general_settings_amount = len(list(general_settings_dic))
    general_settings_last_widget_pos_y = 0  # to calc. the parent widget height


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
    subtitle_tracks_rotate = settings['hotkey_settings']['subtitle_tracks_rotate']
    play_pause = settings['hotkey_settings']['play_pause']
    next_track = settings['hotkey_settings']['next_track']
    previous_track = settings['hotkey_settings']['previous_track']
    repeat_track_playlist_toggle = settings['hotkey_settings']['repeat_track_playlist_toggle']
    shuffle_playlist_toggle = settings['hotkey_settings']['shuffle_playlist_toggle']
    full_screen_toggle = settings['hotkey_settings']['full_screen_toggle']
    playlist_toggle = settings['hotkey_settings']['playlist_toggle']
    window_size_toggle = settings['hotkey_settings']['window_size_toggle']
    paylist_add_track = settings['hotkey_settings']['paylist_add_track']
    paylist_add_directory = settings['hotkey_settings']['paylist_add_directory']
    paylist_remove_track = settings['hotkey_settings']['paylist_remove_track']
    paylist_remove_all_track = settings['hotkey_settings']['paylist_remove_all_track']
    paylist_select_prev_pl = settings['hotkey_settings']['paylist_select_prev_pl']
    paylist_select_next_pl = settings['hotkey_settings']['paylist_select_next_pl']


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
        'subtitle_tracks_rotate': {
            'text': 'Subtitle track - use next',
            'value': subtitle_tracks_rotate,
            'line_edit_widget': ''
        },
        'play_pause': {
            'text': 'Play / Pause',
            'value': play_pause,
            'line_edit_widget': ''
        },
        'previous_track': {
            'text': 'Play - Previous track',
            'value': previous_track,
            'line_edit_widget': ''
        },
        'next_track': {
            'text': 'Play - Next track',
            'value': next_track,
            'line_edit_widget': ''
        },
        'repeat_track_playlist_toggle': {
            'text': 'Toogle - Repeat',
            'value': repeat_track_playlist_toggle,
            'line_edit_widget': ''
        },
        'shuffle_playlist_toggle': {
            'text': 'Toogle - Shuffle',
            'value': shuffle_playlist_toggle,
            'line_edit_widget': ''
        },
        'playlist_toggle': {
            'text': 'Toogle - Playlist',
            'value': playlist_toggle,
            'line_edit_widget': ''
        },
        'full_screen_toggle': {
            'text': 'Toogle - Full screen',
            'value': full_screen_toggle,
            'line_edit_widget': ''
        },
        'window_size_toggle': {
            'text': 'Toogle - Window alt. size',
            'value': window_size_toggle,
            'line_edit_widget': ''
        },
        'paylist_add_track': {
            'text': 'Paylist - Add track',
            'value': paylist_add_track,
            'line_edit_widget': ''
        },
        'paylist_add_directory': {
            'text': 'Paylist - Add directory',
            'value': paylist_add_directory,
            'line_edit_widget': ''
        },
        'paylist_remove_track': {
            'text': 'Paylist - Remove track',
            'value': paylist_remove_track,
            'line_edit_widget': ''
        },
        'paylist_remove_all_track': {
            'text': 'Paylist - Clear playlist',
            'value': paylist_remove_all_track,
            'line_edit_widget': ''
        },
        'paylist_select_prev_pl': {
            'text': 'Paylist - Select next',
            'value': paylist_select_prev_pl,
            'line_edit_widget': ''
        },
        'paylist_select_next_pl': {
            'text': 'Paylist - Select previous',
            'value': paylist_select_next_pl,
            'line_edit_widget': ''
        }
    }

    hotkeys_list = list(hotkey_settings_dic)
    hotkey_settings_last_widget_pos_y = 0  # to calc. the parent widget height


    ''' REGEX FOR SETTINGS WINDOW / HOTKEYS VALIDATION '''
    ''' More info in the docs / learning / regex_for_hotkey_validation.py '''
    keys_list = ['Shift', 'Alt', 'Enter', 'Space', 'Ctrl', 'Del', 'Left', 'Right', 'Up', 'Down', 'Backspace', '[a-zA-Z0-9]', '[.+-]']

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

    playlist_amount = 30
    for i in range(0, playlist_amount):
        pl_name = f'playlist_{i}'
        paylist_widget_dic[pl_name] = {
            'name_list_widget': '',
            'duration_list_widget': '',
            'active_pl_sum_duration': 0
            }
      
    paylist_list = list(paylist_widget_dic)
    paylist_settings_last_widget_pos_y = 0     # to calc. the parent widget height


cv = Data()