from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from .class_data import cv
from .logger import logger_runtime

@logger_runtime
class MyIcon:
    """
    The qtea_logo_svg.svg file is not listed below, it is used in packaging for Linux
    """
    def __init__(self):
        self.window_icon = QIcon(f'skins/{cv.skin_dir}/window_icon.ico')

        self.start = QIcon(f'skins/{cv.skin_dir}/start.png')
        self.pause = QIcon(f'skins/{cv.skin_dir}/pause.png')
        self.stop = QIcon(f'skins/{cv.skin_dir}/stop.png')
        self.previous = QIcon(f'skins/{cv.skin_dir}/previous.png')
        self.next = QIcon(f'skins/{cv.skin_dir}/next.png')
        self.repeat = QIcon(f'skins/{cv.skin_dir}/repeat.png')
        self.repeat_single = QIcon(f'skins/{cv.skin_dir}/repeat_single.png')
        self.shuffle = QIcon(f'skins/{cv.skin_dir}/shuffle.png')

        self.toggle_video = QIcon(f'skins/{cv.skin_dir}/toggle_vid.png')
        self.toggle_playlist = QIcon(f'skins/{cv.skin_dir}/toggle_playlist.png')
        self.settings = QIcon(f'skins/{cv.skin_dir}/settings.png')

        self.thumbnail = QIcon(f'skins/{cv.skin_dir}/thumbnail.png')

        default_thumbnail_img_size = 50
        self.thumbnail_default = (QPixmap(f'skins/{cv.skin_dir}/qtea_logo.png')
                                  .scaledToWidth(default_thumbnail_img_size, Qt.TransformationMode.SmoothTransformation))

        self.thumbnail_default_video = (QPixmap(f'skins/{cv.skin_dir}/video.png')
                                  .scaledToWidth(default_thumbnail_img_size, Qt.TransformationMode.SmoothTransformation))
        self.thumbnail_playing_video = (QPixmap(f'skins/{cv.skin_dir}/video_playing.png')
                                        .scaledToWidth(default_thumbnail_img_size,Qt.TransformationMode.SmoothTransformation))

        self.thumbnail_default_audio= (QPixmap(f'skins/{cv.skin_dir}/audio.png')
                                        .scaledToWidth(default_thumbnail_img_size, Qt.TransformationMode.SmoothTransformation))
        self.thumbnail_playing_audio = (QPixmap(f'skins/{cv.skin_dir}/audio_playing.png')
                                        .scaledToWidth(default_thumbnail_img_size, Qt.TransformationMode.SmoothTransformation))

        self.thumbnail_backup = (QPixmap(f'skins/{cv.skin_dir}/queue.png')
                                        .scaledToWidth(default_thumbnail_img_size, Qt.TransformationMode.SmoothTransformation))


        self.speaker = QIcon(f'skins/{cv.skin_dir}/speaker.png')
        self.speaker_muted = QIcon(f'skins/{cv.skin_dir}/speaker_muted.png')

        self.queue = QIcon(f'skins/{cv.skin_dir}/queue.png')
        self.queue_blue = QIcon(f'skins/{cv.skin_dir}/queue_blue.png')
        self.de_queue = QIcon(f'skins/{cv.skin_dir}/de_queue.png')
        self.folder = QIcon(f'skins/{cv.skin_dir}/folder.png')
        self.remove = QIcon(f'skins/{cv.skin_dir}/remove.png')

        self.search = QIcon(f'skins/{cv.skin_dir}/search.png')
        self.clear_queue = QIcon(f'skins/{cv.skin_dir}/bin.png')
        self.clear_queue_current_playlist = QIcon(f'skins/{cv.skin_dir}/bin_half.png')
        self.clear_multi_selection = QIcon(f'skins/{cv.skin_dir}/clear_multi_selection.png')

        self.start_with_default_player = QIcon(f'skins/{cv.skin_dir}/start_with_default_player.png')
        self.minimal_interface = QIcon(f'skins/{cv.skin_dir}/minimal_interface.png')
        self.quit = QIcon(f'skins/{cv.skin_dir}/quit.png')
        
        ## VIDEO AREA - CONTEXTMENU / RIGHT CLICK
        # TOGGLE BETWEEN ALTERNATIVE WINDOW SIZE / POSITION
        self.alter = QIcon(f'skins/{cv.skin_dir}/alter.png')
        # FOR THE SELECTED AUDIO AND SUBTITLE TRACK 
        self.selected = QIcon(f'skins/{cv.skin_dir}/dot.png')