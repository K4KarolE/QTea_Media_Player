from PyQt6.QtGui import QIcon
from .class_data import cv


class MyIcon():
    def __init__(self):
        self.window_icon = QIcon(f'skins/{cv.skin_selected}/window_icon.png')

        self.start = QIcon(f'skins/{cv.skin_selected}/start.png')
        self.pause = QIcon(f'skins/{cv.skin_selected}/pause.png')
        self.stop = QIcon(f'skins/{cv.skin_selected}/stop.png')
        self.previous = QIcon(f'skins/{cv.skin_selected}/previous.png')
        self.next = QIcon(f'skins/{cv.skin_selected}/next.png')
        self.repeat = QIcon(f'skins/{cv.skin_selected}/repeat.png')
        self.repeat_single = QIcon(f'skins/{cv.skin_selected}/repeat_single.png')
        self.shuffle = QIcon(f'skins/{cv.skin_selected}/shuffle.png')

        self.toggle_video = QIcon(f'skins/{cv.skin_selected}/toggle_vid.png')
        self.toggle_playlist = QIcon(f'skins/{cv.skin_selected}/toggle_playlist.png')
        self.settings = QIcon(f'skins/{cv.skin_selected}/settings.png')

        self.speaker = QIcon(f'skins/{cv.skin_selected}/speaker.png')
        self.speaker_muted = QIcon(f'skins/{cv.skin_selected}/speaker_muted.png')

        self.queue = QIcon(f'skins/{cv.skin_selected}/queue.png')
        self.queue_blue = QIcon(f'skins/{cv.skin_selected}/queue_blue.png')
        self.de_queue = QIcon(f'skins/{cv.skin_selected}/de_queue.png')
        self.folder = QIcon(f'skins/{cv.skin_selected}/folder.png')
        self.remove = QIcon(f'skins/{cv.skin_selected}/remove.png')

        self.search = QIcon(f'skins/{cv.skin_selected}/search.png')
        self.clear_queue = QIcon(f'skins/{cv.skin_selected}/bin.png')

        self.start_with_default_player = QIcon(f'skins/{cv.skin_selected}/start_with_default_player.png')
        
        ## VIDEO AREA - CONTEXTMENU / RIGHT CLICK
        # TOGGLE BETWEEN ALTERNATIVE WINDOW SIZE / POSITION
        self.alter = QIcon(f'skins/{cv.skin_selected}/alter.png')
        # FOR THE SELECTED AUDIO AND SUBTITLE TRACK 
        self.selected = QIcon(f'skins/{cv.skin_selected}/dot.png')