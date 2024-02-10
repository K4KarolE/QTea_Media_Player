
from PyQt6.QtGui import QIcon
from .cons_and_vars import cv


class MyIcon():
    def __init__(self):
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