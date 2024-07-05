
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

br = Bridge()