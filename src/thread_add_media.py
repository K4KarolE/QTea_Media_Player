from pathlib import Path
import os

from PyQt6.QtCore import pyqtSignal, QThread, QUrl

from .class_data import cv
from .class_bridge import br
from .func_coll import (
    generate_duration_to_display,
    is_active_and_add_to_track_playlist_same,
    update_add_track_to_pl_widget_vars
    )
from . import logger_check


class ThreadAddMedia(QThread):
    """ Phase A,
        - Adding media from different sources (via button or drop - file, files, dictionary)
        - Extracting the track path(s)

        Phase B,
        - Once the media is loaded > signal is triggered > duration is ready to be generated
            src / av_player / TrackDuration / mediaStatusChanged signal
        - Track path and duration values passed to the
            src / MyWindow / add_track_to_playlist_via_thread()
        - If more item in the "self.track_path_list" the Phase B loop continues
            by loading the next media in
        """
    result_ready = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.source = None
        self.track_path_list = []
        self.last_track_added = "" 
        # self.last_track_added - Used to avoid the below scenario:
        # Adding the same media after each other >> the duration player's mediaStatusChanged
        # signal will not be triggered >> the second media will not be added and the
        # duration player get blocked / unresponsive >> not able to add another media


    def run(self):
        update_add_track_to_pl_widget_vars()

        #########################
        # TRACK PATH COLLECTION #
        #########################

        # SOURCE FROM DROP EVENT - MyWindow()
        if isinstance(self.source, list):
            for url in self.source:
                url = str(url.toLocalFile())

                # DIRECTORY
                if Path(url).is_dir():
                    self.add_dir(url)

                # FILE
                elif Path(url).suffix in cv.MEDIA_FILES:
                    self.track_path_list.append(url)

        # SOURCE FROM ADD DIRECTORY BUTTON
        elif Path(self.source).is_dir():
            self.add_dir(self.source)

        # SOURCE FROM ADD TRACK BUTTON
        elif Path(self.source).is_file():
            self.track_path_list.append(self.source)

        ##################################
        # STARTING THE MEDIA ADDING LOOP #
        ##################################
        if self.track_path_list:    # Please see the comment above
            if self.last_track_added == self.track_path_list[0]:
                self.return_thread_generated_values()
            else:
                self.last_track_added = self.track_path_list[0]
                self.player_set_source(self.track_path_list[0])


    def add_dir(self, dir_path):
        cv.adding_records_at_moment = True
        for dir_path_b, _, file_names in os.walk(dir_path):
            file_names.sort()
            for file in file_names:
                if Path(file).suffix in cv.MEDIA_FILES:  # music_title.mp3 -> mp3
                    track_path = str(Path(dir_path_b, file))
                    self.track_path_list.append(track_path)


    @logger_check
    def player_set_source(self, track_path):
        """ Triggers the src / av_player / TrackDuration class / mediaStatusChanged signal """
        br.av_player_duration.player.setSource(QUrl.fromLocalFile(track_path))


    @logger_check
    def return_thread_generated_values(self):
        """ Triggered via the src / av_player / TrackDuration class`
            mediaStatusChanged signal
        """
        raw_duration = br.av_player_duration.player.duration()

        self.result_ready.emit(self.track_path_list[0], raw_duration)
        self.track_path_list.pop(0)

        cv.add_track_to_pl_sum_duration += raw_duration
        self.update_duration_sum_widget()
        
        if self.track_path_list:
            self.player_set_source(self.track_path_list[0])
        else:
            cv.adding_records_at_moment = False
            if is_active_and_add_to_track_playlist_same():
                cv.active_pl_tracks_count = cv.add_track_to_pl_name.count()


    def update_duration_sum_widget(self):
        """
            Staying on the same playlist while adding media
            or change back to the playlist where and while
            adding tracks was still in progress
        """
        if is_active_and_add_to_track_playlist_same():
            br.duration_sum_widg.setText(generate_duration_to_display(cv.add_track_to_pl_sum_duration))