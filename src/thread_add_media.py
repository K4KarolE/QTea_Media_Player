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
from .logger import logger_check
from .message_box import MyMessageBoxError


class ThreadAddMedia(QThread):
    """ Phase A,
        - Adding media from different sources (via button or drop - file, files, dictionary)
        - "run()":
            - Extracting the track path(s) and adding to the "self.track_path_list"
            - Once the previous step completed, loading the first media >> starting Phase B

        Phase B,
        - Once the media is loaded >> signal is triggered >> duration is ready to be generated
            src / av_player / TrackDuration / mediaStatusChanged signal
        - Track path and duration values passed to the
            src / window_main / MyWindow / add_track_to_playlist_via_thread()
        - If more item in the "self.track_path_list" the Phase B loop continues
            by loading the next media in
        """
    result_ready = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.source = None
        self.track_path_list = []
        self.invalid_media_self_track_path_list = []
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
        if self.track_path_list:
            self.track_path_list_action()


    def add_dir(self, dir_path):
        cv.adding_records_at_moment = True
        for dir_path_b, _, file_names in os.walk(dir_path):
            file_names.sort()
            for file in file_names:
                if not self.is_file_title_ignored(file) and Path(file).suffix in cv.MEDIA_FILES:
                        track_path = str(Path(dir_path_b, file))
                        self.track_path_list.append(track_path)

    def is_file_title_ignored(self, file):
        return (cv.add_dir_ignore_file_titles_including and
                cv.add_dir_ignore_file_titles_including.lower() in file.lower())


    @logger_check
    def player_set_source(self, track_path):
        """ Triggers the src / av_player / TrackDuration class / mediaStatusChanged signal """
        br.av_player_duration.player.setSource(QUrl.fromLocalFile(track_path))


    @logger_check
    def return_thread_generated_values(self, invalid_media = False):
        """ Triggered via the src / av_player / TrackDuration class`
            mediaStatusChanged signal

            From "src / av_player / TrackDuration" the invalid media status
            triggers once for adding multiple media at the same time
            and triggers twice for adding single media >>
            hence the "if self.track_path_list" validation
        """
        if invalid_media:
            if self.track_path_list:
                self.invalid_media_self_track_path_list.append(self.track_path_list[0])
                self.track_path_list.pop(0)
                self.last_track_added = None
        else:
            raw_duration = br.av_player_duration.player.duration()

            self.result_ready.emit(self.track_path_list[0], raw_duration)
            self.last_track_added = self.track_path_list[0]
            self.track_path_list.pop(0)

            cv.add_track_to_pl_sum_duration += raw_duration
            self.update_duration_sum_widget()

        if self.track_path_list:
            self.track_path_list_action()
        else:
            cv.adding_records_at_moment = False
            if is_active_and_add_to_track_playlist_same():
                cv.active_pl_tracks_count = cv.add_track_to_pl_name.count()
            if self.invalid_media_self_track_path_list:
                MyMessageBoxError('Invalid Media' , self.generate_invalid_media_error_msg_text())
                # invalid_media_self_track_path_list set back to the default empty list
                # in the self.generate_invalid_media_error_msg_text() to make sure
                # the message window displayed only once for a single invalid media
                # otherwise it would be displayed twice


    def track_path_list_action(self):
        """ If: To avoid: adding the same media after each other
                Skipping the ".setSource" phase, the previous, same media
                is already loaded in for the duration generation
                Please see the comment above in the __init__ constructor
            Else: start / continue the media adding loop
        """
        if self.last_track_added == self.track_path_list[0]:
            self.return_thread_generated_values()
        else:
            self.player_set_source(self.track_path_list[0])


    def update_duration_sum_widget(self):
        """
            Staying on the same playlist while adding media
            or change back to the playlist where and while
            adding tracks was still in progress
        """
        if is_active_and_add_to_track_playlist_same():
            br.duration_sum_widg.setText(generate_duration_to_display(cv.add_track_to_pl_sum_duration))


    def generate_invalid_media_error_msg_text(self):
        string_to_print = "Not able to add the below invalid media: \n\n"
        for _ in self.invalid_media_self_track_path_list:
            string_to_print = string_to_print + Path(_).name + '\n'
        self.invalid_media_self_track_path_list = []
        return string_to_print