from pathlib import Path
import time
import os

from PyQt6.QtCore import pyqtSignal, QThread, QUrl

from .class_data import cv
from .class_bridge import br
from .func_coll import (
    generate_duration_to_display,
    is_active_and_add_to_track_playlist_same,
    update_add_track_to_pl_widget_vars
    )
from .logger import logger_basic



class ThreadAddMedia(QThread):
    result_ready = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.source = None
        self.time_sleep = 0.01

    def run(self):
        update_add_track_to_pl_widget_vars()

        # SOURCE FROM DROP EVENT - MyWindow()
        if isinstance(self.source, list):
            for url in self.source:
                url_path = str(url.toLocalFile())

                if Path(url_path).is_dir():
                    self.add_dir(url_path)

                elif Path(url_path).suffix in cv.MEDIA_FILES:
                    # if Path(url_path).is_file():
                    raw_duration = self.generate_duration_info(url_path)
                    self.result_ready.emit(url_path, raw_duration)
                    time.sleep(self.time_sleep)
            self.update_duration_sum_widget()

        # SOURCE FROM ADD TRACK BUTTON
        elif Path(self.source).is_dir():
            self.add_dir(self.source)

        # SOURCE FROM ADD DIRECTORY BUTTON
        elif Path(self.source).is_file():
            raw_duration = self.generate_duration_info(self.source)
            self.result_ready.emit(self.source, raw_duration)
            self.update_duration_sum_widget()


    def add_dir(self, dir_path):
        cv.adding_records_at_moment = True
        logger_basic('Adding directory: Loop - start')
        for dir_path_b, dir_names, file_names in os.walk(dir_path):
            for file in file_names:
                if Path(file).suffix in cv.MEDIA_FILES:  # music_title.mp3 -> mp3
                    track_path = str(Path(dir_path_b, file))
                    raw_duration = self.generate_duration_info(track_path)
                    # same result with metaData:
                    # raw_duration = br.av_player_duration.player.metaData().value(br.av_player_duration.player.metaData().Key.Duration)
                    self.result_ready.emit(track_path, raw_duration)
                    time.sleep(self.time_sleep)   # avoid freezing app / video play
        self.update_duration_sum_widget()
        cv.adding_records_at_moment = False
        logger_basic('Adding directory: Loop - stop')


    def add_file(self, track_path):
        raw_duration = self.generate_duration_info(track_path)
        self.result_ready.emit(self.source, raw_duration)
        self.update_duration_sum_widget()


    def generate_duration_info(self, track_path):
        br.av_player_duration.player.setSource(QUrl.fromLocalFile(track_path))
        raw_duration = br.av_player_duration.player.duration()
        cv.add_track_to_pl_sum_duration += raw_duration
        return raw_duration


    def update_duration_sum_widget(self):
        """
        Staying on the same playlist while adding media
        or change back to the playlist where and while
        adding tracks was still in process
        """
        if is_active_and_add_to_track_playlist_same():
            cv.active_pl_tracks_count = cv.add_track_to_pl_name.count()
            br.duration_sum_widg.setText(generate_duration_to_display(cv.add_track_to_pl_sum_duration))
