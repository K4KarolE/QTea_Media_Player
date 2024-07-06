
from dataclasses import dataclass


@dataclass
class Bridge:
    icon: object = None
    window: object = None
    av_player: object = None
    av_player_duration: object = None

    play_slider: object = None
    image_logo: object = None
    play_funcs: object = None

    playlists_all: object = None
    window_queue: object = None
    window_settings: object = None

    button_add_track: object = None
    button_add_dir: object = None
    button_remove_track: object = None
    button_remove_all_track: object = None
    button_queue: object = None
    button_settings: object = None

    button_play_pause: object = None
    button_stop: object = None
    button_prev_track: object = None
    button_next_track: object = None
    button_toggle_repeat_pl: object = None
    button_toggle_shuffle_pl: object = None
    button_toggle_playlist: object = None
    button_toggle_video: object = None
    button_duration_inf: object = None
    
    button_speaker: object = None

    duration_sum_widg: object = None    ###
    volume_slider: object = None


br = Bridge()