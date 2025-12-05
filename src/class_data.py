from dataclasses import dataclass
from pathlib import Path
from json import load, dump
import re
import shutil
import sqlite3
import sys


def open_json():
    with open(PATH_JSON_SETTINGS) as f:
        json_dic = load(f)
    return json_dic

def save_json():
    with open(PATH_JSON_SETTINGS, 'w') as f:
        dump(settings, f, indent=2)
    return


def open_thumbnail_history_json():
    with open(PATH_THUMBNAIL_HISTORY) as f:
        json_dic = load(f)
    return json_dic

def save_thumbnail_history_json():
    with open(PATH_THUMBNAIL_HISTORY, 'w') as f:
        dump(thumbnail_history, f, indent=2)
    return

WORKING_DIRECTORY = Path().resolve()
PATH_JSON_SETTINGS = Path(WORKING_DIRECTORY, 'settings.json')
settings = open_json()

PATH_THUMBNAILS = str(Path(WORKING_DIRECTORY, 'thumbnails'))
PATH_THUMBNAIL_HISTORY = Path(PATH_THUMBNAILS, '_thumbnail_history.json')

""" 
    To make sure if the thumbnail_history json saving is interrupted 
    the app starts next time without any issue / necessary json fix
"""
try:
    thumbnail_history = open_thumbnail_history_json()
except:
    thumbnail_history = {"failed": {}, "completed": {}}


"""
    The rest of the DB functions are in:
    - src / func_coll
    - src / playlists
    
    OS related databases for ease of switching between multiple OS` on the same device
    More information in the README
"""
os_linux: bool = (sys.platform == 'linux')
if os_linux:
    connection = sqlite3.connect('playlist_db_linux.db')
else:
    connection = sqlite3.connect('playlist_db_win.db')
cur = connection.cursor()

def get_playlists_amount_from_db():
    cur.execute("""SELECT COUNT(*) FROM sqlite_master WHERE type='table'""")
    return cur.fetchall()[0][0]


@dataclass
class Data:

    """ SUPPORTING VARIABLES """
    track_title: str = None  # to display on video
    skin_selected: str = settings['skin_selected']
    repeat_playlist: int = settings['repeat_playlist']
    shuffle_playlist_on: bool = settings['shuffle_playlist_on']
    shuffle_played_tracks_list = []
    shuffle_played_tracks_list_size: int = 100
    is_play_prev_track_clicked: bool = False
    # is_play_prev_track_clicked:
    # used to make sure not adding tracks to the
    # shuffle_played_tracks_list when play prev track
    volume: float = settings['volume']
    icon_size: int = 20  # used for the buttons
    is_speaker_muted: bool = settings['is_speaker_muted']
    audio_tracks_amount: int = 0
    audio_track_played: int = 0
    subtitle_tracks_amount: int = 0
    subtitle_track_played: int = -1

    screen_index_for_fullscreen: int = -1
    screen_pos_x_for_fullscreen: int = 0
    screen_pos_x_for_fullscreen_via_menu: int = -1

    # Used to avoid the multi selection sync action being triggered by the new row selection
    is_row_changed_sync_pl_in_action: bool = False

    minimal_interface_enabled: bool = False
    window_size_toggle_counter: int = 0
    playlists_without_title_to_hide_index_list = []
    volume_slider_value: int = 0
    current_track_index: int = 0
    currently_playing_track_info_in_window_title: str = ''
    # to disable current duration autosave while
    # files from directory are added
    adding_records_at_moment: bool = False
    PLIST_BUTTONS_HEIGHT: int = 0 # src/buttons_create
    # LINUX
    player_paused_position: int = 0
    os_linux: bool = os_linux

    """ THUMBNAILS / THUMBNAIL VIEW """
    is_ffmpeg_installed: bool = shutil.which("ffmpeg")
    # To avoid circular import: "func_thumbnail" >> << "thumbnail_widget"
    # Used: remove a single track in the thumbnail view
    thumbnail_widget_resize_and_move_to_pos_func_holder: object = None

    thumbnail_db_table: str = None
    thumbnail_last_played_track_index: int = 0
    thumbnail_last_played_track_index_is_valid: bool = False
    thumbnail_last_selected_track_index: int = 0
    thumbnail_last_selected_track_index_is_valid: bool = False
    thumbnail_pl_tracks_count: int = 0
    thumbnail_widget_dic = {}
    thumbnail_widget_last_selected: object = None
    thumbnail_widget_last_played: object = None

    # take over the value of active_db_table, active_pl_last_track_index
    # >> avoid error while generating thumbnails + switching playlists
    thumbnail_img_size: int = settings['general_settings']['thumbnail_img_size']
    thumbnail_main_window_width: int = 0
    thumbnail_main_window_height: int = 0
    widg_and_img_diff: int = 0
    thumbnail_width: int = thumbnail_img_size + widg_and_img_diff
    thumbnail_height: int = thumbnail_img_size + widg_and_img_diff
    thumbnail_new_width: int = thumbnail_width
    thumbnail_pos_gap: int = 1
    thumbnail_pos_base_x: int = 5
    thumbnail_pos_base_y: int = 5
    thumbnail_remove_older_than: int = settings['general_settings']['thumbnail_remove_older_than']
    if os_linux:
        scroll_bar_size: int = 10
    else:
        scroll_bar_size: int = 15 # 10: barely visible


    '''
    QUEUE TRACKING
    queue_tracking_title = [playlist_3, 6] / playlist, track index
    queue_tracks_list = [queue_tracking_title-1, queue_tracking_title-2, ..]
    queue_playlist_list = [playlist_3, playlist_6, ..] - playlists with a queued track
    '''
    queue_tracking_title = []
    queue_tracks_list = []
    queue_playlists_list = []
    queued_tracks_amount: int = 0
    
    
    ''' THE CURRENTLY PLAYING/PAUSED TRACK`S INDEX TRACKING '''
    playing_track_index: int = 0

    ''' 
    ACTIVE AND PLAYING PLAYLISTS SEPARATION
    Playing playlist = playlist where the current track is in the playing or paused state
                    / playlist where the last track was played
    Active playlist = playlist which is currently selected / displayed
    

    TO SAVE THE PLAY AND SELECTION HISTORY:
        - ACTIVE PLAYLIST UTILITY
        - PLAYING PLAYLIST UTILITY
    '''
    '''
    ACTIVE PLAYLIST UTILITY VALUES
    src / func_coll.py / update_active_playlist_vars_and_widgets()
    Updated after every playlist change
    '''
    active_playlist_index: int = settings['last_used_playlist']
    active_db_table: str = None  
    active_pl_title: str = None
    active_pl_last_track_index: int = 0
    active_pl_last_selected_track_index: int = 0
    active_pl_name: object = None       # list widget
    active_pl_queue: object = None      # list widget
    active_pl_duration: object = None   # list widget
    active_pl_sum_duration: int = 0
    active_pl_tracks_count: int = 0

    '''
    PLAYING PLAYLIST UTILITY VALUES
    src / func_coll.py / update_playing_playlist_vars_and_widgets()
    '''
    playing_playlist_index: int = settings['playing_playlist']
    playing_db_table: str = None  
    playing_pl_title: str = None
    playing_pl_last_track_index: int = None
    playing_pl_name: object = None      # list widget
    playing_pl_queue: object = None     # list widget
    playing_pl_duration: object = None  # list widget
    playing_pl_tracks_count: int = 0

    '''
    Used to carry the values from the active_pl_name, active_pl_queue, active_pl_duration vars.
    when adding a directory with huge amount of media to the playlist, which can take a while
    to process + switching playlist in the meanwhile 
    >> avoid to add the rest of the media added to the new playlist
    '''
    add_track_to_db_table: str = None
    add_track_to_pl_name: object = None      # list widget
    add_track_to_pl_queue: object = None      # list widget
    add_track_to_pl_duration: object = None      # list widget
    add_track_to_pl_sum_duration: int = 0

    ''' DURATION FROM DB / DISPLAY READY DURATION VALUE '''
    track_full_duration: int = 0
    track_full_duration_to_display: int = 0

    ''' DURATION FROM DB / DISPLAY READY DURATION VALUE '''
    track_current_duration: int = 0
    track_current_duration_to_display: int = 0
    counter_for_duration: int = 0

    ''' DISPLAYED DURATION COUNT DOWN TYPES '''
    is_duration_to_display_straight: bool = True
    duration_to_display_straight: int = 0
    duration_to_display_back: int = 0

    '''
    GENERAL TAB - SETTINGS WINDOW
    
    Steps to add new general field/value:
    1, In settings.json create a new key-value pair in
    the "general_settings" dictionary
    2, In this file / just below:
        a: declare the new "general" variable
        b: add a new sub-dictionary in
            the general_settings_dic dictionary
        c**: if the new value matching with the already existing
        ones` logic/type (boolean, int-window size,..) add a new
        list item to one of the lists:
            gen_sett_boolean_text_list
            ...
            gen_sett_jump_text_list
    3, Add the new variable to the
        window_settings.py / update_real_time_used_variables()
    
    No further steps needed, the validation will be automatically
    applied at the next user input (Settings window / General tab)

    ** else: visit src / window_settings.py / general_fields_validation()
        to generate new validation rules
    '''
    always_on_top: bool = settings['general_settings']['always_on_top']
    continue_playback: bool = settings['general_settings']['continue_playback']
    play_at_startup: bool = settings['general_settings']['play_at_startup']
    small_jump: int = settings['general_settings']['small_jump']
    medium_jump: int = settings['general_settings']['medium_jump']
    big_jump: int = settings['general_settings']['big_jump']
    window_width: int = settings['general_settings']['window_width']
    window_height: int = settings['general_settings']['window_height']
    window_alt_width: int = settings['general_settings']['window_alt_width']
    window_alt_height: int = settings['general_settings']['window_alt_height']
    window_second_alt_width: int = settings['general_settings']['window_second_alt_width']
    window_second_alt_height: int = settings['general_settings']['window_second_alt_height']
    window_alt_size_repositioning: bool = settings['general_settings']['window_alt_size_repositioning']
    window_auto_resize_to_video_resolution: bool = settings['general_settings']['window_auto_resize_to_video_resolution']
    default_audio_track: int = settings['general_settings']['default_audio_track']
    search_result_parent_dicts_size: int = settings['general_settings']['search_result_parent_dicts_size']
    # thumbnail_img_size, remove_thumbnails_older_than: declared in the "Thumbnails" section above
    # it`s validation in window_settings.py / general_fields_validation() / 100-500px
    # USED FOR VALIDATION
    window_min_width: int = settings['general_settings']['window_min_width']
    window_min_height: int = settings['general_settings']['window_min_height']


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
        },
        'window_second_alt_width': {
            'text': 'Window 2nd alt. width',
            'value': window_second_alt_width,
            'line_edit_widget': ''
        },
        'window_second_alt_height': {
            'text': 'Window 2nd alt. height',
            'value': window_second_alt_height,
            'line_edit_widget': ''
        },
        'window_alt_size_repositioning': {
            'text': 'Window alt. repositioning',
            'value': window_alt_size_repositioning,
            'line_edit_widget': ''
        },
        'window_auto_resize_to_video_resolution': {
            'text': 'Auto resize window\nto video resolution',
            'value': window_auto_resize_to_video_resolution,
            'line_edit_widget': ''
        },
        'default_audio_track': {
            'text': 'Default audio track',
            'value': default_audio_track,
            'line_edit_widget': ''
        },
        'thumbnail_img_size': {
            'text': 'Thumbnail image size',
            'value': thumbnail_img_size,
            'line_edit_widget': ''
        },
        'thumbnail_remove_older_than': {
            'text': 'Remove unused thumbnails\nolder than (days)',
            'value': thumbnail_remove_older_than,
            'line_edit_widget': ''
        },
        'search_result_parent_dicts_size': {
            'text': 'Search result - parent\nfolders` text length',
            'value': search_result_parent_dicts_size,
            'line_edit_widget': ''
        }
    }

    '''
    The below lists used in the src / window_settings.py / general_fields_validation()
    '''
    gen_sett_boolean_text_list = [
        general_settings_dic['always_on_top']['text'],
        general_settings_dic['continue_playback']['text'],
        general_settings_dic['play_at_startup']['text'],
        general_settings_dic['window_alt_size_repositioning']['text'],
        general_settings_dic['window_auto_resize_to_video_resolution']['text']
        ]
    
    gen_sett_window_width_text_list = [
        general_settings_dic['window_width']['text'],
        general_settings_dic['window_alt_width']['text'],
        general_settings_dic['window_second_alt_width']['text']
        ]
    
    gen_sett_window_height_text_list = [
        general_settings_dic['window_height']['text'],
        general_settings_dic['window_alt_height']['text'],
        general_settings_dic['window_second_alt_height']['text']
        ]
    
    gen_sett_jump_text_list = [
        general_settings_dic['small_jump']['text'],
        general_settings_dic['medium_jump']['text'],
        general_settings_dic['big_jump']['text']
        ]
  
    general_settings_amount: int = len(list(general_settings_dic))
    general_settings_last_widget_pos_y: int = 0  # to calc. the parent widget height


    '''
    HOTKEYS TAB - SETTINGS WINDOW
    
    Steps to add new hotkey:
    1, In settings.json create a new key-value pair in
    the "hotkey_settings" dictionary
    2, In this file / just below:
        a: declare the new hotkey variable
        b: add a new sub-dictionary in
            the hotkey_settings_dic dictionary
    3, In the window_main.py / hotkeys_creation() / hotkeys_action_dic
        dictionary add a new key-value pair
    
    No further steps needed, the validation will be automatically
    applied at the next user input (Settings window / Hotkeys tab)    
    '''
    small_jump_backward: str = settings['hotkey_settings']['small_jump_backward']
    small_jump_forward: str = settings['hotkey_settings']['small_jump_forward']
    medium_jump_backward: str = settings['hotkey_settings']['medium_jump_backward']
    medium_jump_forward: str = settings['hotkey_settings']['medium_jump_forward']
    big_jump_backward: str = settings['hotkey_settings']['big_jump_backward']
    big_jump_forward: str = settings['hotkey_settings']['big_jump_forward']
    display_track_info_on_video: str = settings['hotkey_settings']['display_track_info_on_video']
    volume_mute: str = settings['hotkey_settings']['volume_mute']
    volume_up: str = settings['hotkey_settings']['volume_up']
    volume_down: str = settings['hotkey_settings']['volume_down']
    audio_tracks_rotate: str = settings['hotkey_settings']['audio_tracks_rotate']
    audio_output_device_rotate: str = settings['hotkey_settings']['audio_output_device_rotate']
    subtitle_tracks_rotate: str = settings['hotkey_settings']['subtitle_tracks_rotate']
    play_pause: str = settings['hotkey_settings']['play_pause']
    play: str = settings['hotkey_settings']['play']  # play vs play_pause: info in readme / Hotkeys
    stop: str = settings['hotkey_settings']['stop']
    next_track: str = settings['hotkey_settings']['next_track']
    previous_track: str = settings['hotkey_settings']['previous_track']
    repeat_track_playlist_toggle: str = settings['hotkey_settings']['repeat_track_playlist_toggle']
    shuffle_playlist_toggle: str = settings['hotkey_settings']['shuffle_playlist_toggle']
    full_screen_toggle: str = settings['hotkey_settings']['full_screen_toggle']
    playlist_toggle: str = settings['hotkey_settings']['playlist_toggle']
    video_toggle: str = settings['hotkey_settings']['video_toggle']
    window_size_toggle: str = settings['hotkey_settings']['window_size_toggle']
    playlist_add_track: str = settings['hotkey_settings']['playlist_add_track']
    playlist_add_directory: str = settings['hotkey_settings']['playlist_add_directory']
    playlist_remove_track: str = settings['hotkey_settings']['playlist_remove_track']
    playlist_remove_all_track: str = settings['hotkey_settings']['playlist_remove_all_track']
    playlist_select_prev_pl: str = settings['hotkey_settings']['playlist_select_prev_pl']
    playlist_select_next_pl: str = settings['hotkey_settings']['playlist_select_next_pl']
    queue_toggle: str = settings['hotkey_settings']['queue_toggle']
    queue_window: str = settings['hotkey_settings']['queue_window']
    search_window: str = settings['hotkey_settings']['search_window']
    minimal_interface_toggle: str = settings['hotkey_settings']['minimal_interface_toggle']
    remove_black_bars_around_video: str = settings['hotkey_settings']['remove_black_bars_around_video']
    increase_window_size: str = settings['hotkey_settings']['increase_window_size']
    decrease_window_size: str = settings['hotkey_settings']['decrease_window_size']

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
        'display_track_info_on_video': {
            'text': 'Display track info on video',
            'value': display_track_info_on_video,
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
        'audio_output_device_rotate': {
            'text': 'Audio output - use next',
            'value': audio_output_device_rotate,
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
        'play': {
            'text': 'Play',
            'value': play,
            'line_edit_widget': ''
        },
        'stop': {
            'text': 'Stop',
            'value': stop,
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
            'text': 'Toggle - Repeat',
            'value': repeat_track_playlist_toggle,
            'line_edit_widget': ''
        },
        'shuffle_playlist_toggle': {
            'text': 'Toggle - Shuffle',
            'value': shuffle_playlist_toggle,
            'line_edit_widget': ''
        },
        'playlist_toggle': {
            'text': 'Toggle - Playlist area',
            'value': playlist_toggle,
            'line_edit_widget': ''
        },
        'video_toggle': {
            'text': 'Toggle - Video area',
            'value': video_toggle,
            'line_edit_widget': ''
        },
        'full_screen_toggle': {
            'text': 'Toggle - Full screen',
            'value': full_screen_toggle,
            'line_edit_widget': ''
        },
        'window_size_toggle': {
            'text': 'Toggle - Window alt. size',
            'value': window_size_toggle,
            'line_edit_widget': ''
        },
        'playlist_add_track': {
            'text': 'Playlist - Add track',
            'value': playlist_add_track,
            'line_edit_widget': ''
        },
        'playlist_add_directory': {
            'text': 'Playlist - Add directory',
            'value': playlist_add_directory,
            'line_edit_widget': ''
        },
        'playlist_remove_track': {
            'text': 'Playlist - Remove track',
            'value': playlist_remove_track,
            'line_edit_widget': ''
        },
        'playlist_remove_all_track': {
            'text': 'Playlist - Clear playlist',
            'value': playlist_remove_all_track,
            'line_edit_widget': ''
        },
        'playlist_select_prev_pl': {
            'text': 'Playlist - Select previous',
            'value': playlist_select_prev_pl,
            'line_edit_widget': ''
        },
        'playlist_select_next_pl': {
            'text': 'Playlist - Select next',
            'value': playlist_select_next_pl,
            'line_edit_widget': ''
        },
        'queue_toggle': {
            'text': 'Queue / Dequeue track',
            'value': queue_toggle,
            'line_edit_widget': ''
        },
        'queue_window': {
            'text': 'Show Queue window',
            'value': queue_window,
            'line_edit_widget': ''
        },
        'search_window': {
            'text': 'Show Search window',
            'value': search_window,
            'line_edit_widget': ''
        },
        'minimal_interface_toggle': {
            'text': 'Toggle minimal interface',
            'value': minimal_interface_toggle,
            'line_edit_widget': ''
        },
        'remove_black_bars_around_video': {
            'text': 'Remove black bars\naround video',
            'value': remove_black_bars_around_video,
            'line_edit_widget': ''
        },
        'increase_window_size': {
            'text': 'Increase window size',
            'value': increase_window_size,
            'line_edit_widget': ''
        },
        'decrease_window_size': {
            'text': 'Decrease window size',
            'value': decrease_window_size,
            'line_edit_widget': ''
        }
    }

    hotkeys_list = list(hotkey_settings_dic)
    hotkey_settings_last_widget_pos_y: int = 0  # to calc. the parent widget height


    ''' 
    REGEX FOR SETTINGS WINDOW / HOTKEYS VALIDATION
    More info in the docs / learning / regex_for_hotkey_validation.py
    exp_1 = keys_list[any]
    exp_2 = Shift / Ctrl / Alt + [rest of the keys_list]
    Not able to use hotkeys with 3 components: 'Alt + M + K'
    '''
    keys_list = ['Shift', 'Ctrl', 'Alt', 'Enter', 'Space',  'Del', 'Left', 'Right',
                 'Up', 'Down', 'Backspace', '[a-zA-Z0-9]', "[`=/,;'#*.+-]"]

    # ONE KEY
    exp_1 = r'('
    for item in keys_list[0:-1]:
        exp_1 = exp_1 + f'^{item}$|'
    exp_1 = exp_1 + f'^{keys_list[-1]}$)'

    # TWO KEYS
    exp_2 = r'('
    for item in keys_list[:2]:
        exp_2 = exp_2 + f'^{item}|'
    exp_2 = exp_2 + f'^{keys_list[2]}' + r')\+('

    for item in keys_list[3:]:
        exp_2 = exp_2 + f'{item}$|'
    exp_2 = exp_2 + f'{keys_list[-1]}$)'


    search_regex = re.compile(f'{exp_1}|{exp_2}')



    ''' FILE TYPES '''
    '''
        MEDIA_FILES - used to select the correct files from the selected dictionary
                    - `AD - Add Directory` button

        FILE_TYPES_LIST - used to sort the files in the file dialog window
                        - `AT - Add Track` button
    '''
    AUDIO_FILES_EXTS = "*.aac *.dts *.flac *.m4a *.midi *.mp3 *.ogg *.wav"
    AUDIO_FILES = f"Audio files ({AUDIO_FILES_EXTS})"

    VIDEO_FILES_EXTS= "*.avi *.flv *.mkv *.mov *.mpg *.mp4 *.mpeg *.mts *.webm *.wmv"
    VIDEO_FILES = f"Video files ({VIDEO_FILES_EXTS})"

    MEDIA_FILES = f"Media files ({AUDIO_FILES_EXTS} {VIDEO_FILES_EXTS})"
    FILE_TYPES_LIST = [MEDIA_FILES, AUDIO_FILES, VIDEO_FILES, "All files (*.*)"]
    


    ''' PLAYLISTS '''
    ''' The dictionary used to:
        - create playlists in src / playlists.py
        - be able to access to the right widget, support variable
    'name_list_widget', 'queue_list_widget', 'duration_list_widget':
        Standard playlist`s list widget elements
        A playlist row consists all 3 list types next to each other
    'last_selected_track_index':
        Thumbnail style update support var
    'played_thumbnail_style_update_needed':
        To make sure un-played track`s thumbnail view style is correct
        SCENARIO: app started >> non-playing playlist is active + one of the row is selected
        >> switch to thumbnail view >> only the selected thumbnail style is in use
    'thumbnail_window_validation':
        Once the Thumbnail View button is triggered, the current playlist`s properties saved
        in this dictionary to able to determine, if later there is any change made on the playlist
        which requires new thumbnail generation
    '''
    playlist_widget_dic = {}

    playlists_amount: int = get_playlists_amount_from_db()
    for i in range(0, playlists_amount):
        pl_name = f'playlist_{i}'
        playlist_widget_dic[pl_name] = {
            'name_list_widget': '',
            'queue_list_widget': '',
            'duration_list_widget': '',
            'playlist_title': settings['playlists'][pl_name]['playlist_title'],
            'last_selected_track_index': settings['playlists'][pl_name]['last_track_index'],
            'played_thumbnail_style_update_needed': False,
            'active_pl_sum_duration': 0,
            'thumbnail_window': '',
            'thumbnail_window_validation': {
                'tracks_count': 0,
                'duration_sum': 0,
                'thumbnail_img_size': 0,
                'thumbnail_generation_needed': True
            },
            'thumbnail_widgets_dic': {},    # filled via func_thumbnail/generate_thumbnail_dic()
            'line_edit': '',     # used in the Settings window / Playlists
            'button_jump_to_playlist': ''   # used in the Settings window / Playlists
            }
      
    playlist_list = list(playlist_widget_dic)
    playlist_settings_last_widget_pos_y: int = 0     # to calc. the parent widget height


    ''' QUEUE AND SEARCH WINDOW - QUEUE TAB '''
    queue_widget_dic = {
        'queue_list_widget': {
            'list_widget': '',
            'list_widget_title': '#',
            'list_widget_window_ratio': 1,
            'fixed_width': 30
        },
        'name_list_widget':  {
            'list_widget': '',
            'list_widget_title': 'Title',
            'list_widget_window_ratio': 70,
            'fixed_width': None
        },
        'playlist_list_widget':  {
            'list_widget': '',
            'list_widget_title': 'Playlist',
            'list_widget_window_ratio': 30,
            'fixed_width': None
        },
        'duration_list_widget':  {
            'list_widget': '',
            'list_widget_title': 'Duration',
            'list_widget_window_ratio': 1,
            'fixed_width': 80
        }
        }
    
    '''
    QUEUE AND SEARCH WINDOW - SEARCH TAB
    Subdictionary generated for every track in the search result,
    holding information from the main/mother playlists:
    First track:
    cv.search_result_dic[0] = {
                            'track_title': track_title,
                            'playlist': playlist,
                            'track_index': track_index,
                            'queue_number': queue_number
                            }
    '''
    search_result_dic = {}
    search_title_list_widget: str = None   
    search_queue_list_widget: str = None
    track_change_on_main_playlist_new_search_needed: bool = False
    search_result_queued_tracks_index_list = []

cv = Data()