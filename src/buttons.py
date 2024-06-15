'''
BUTTON FUNCTIONS DECLARED BELOW:
--------------------------------
- Add track
- Add directory
- Remova all tracks (Clear playlist) - *more added/compiled in MAIN

- Set button style/stylesheet functions

- Play/pause
- Play/pause via list
- Previous track
- Next track
- Toggle repeat
- Toggle shuffle



BUTTON FUNCTIONS DECLARED IN MAIN:
----------------------------------
- Remove track
- Settings
- Stop
- Toggle playlist
- Toogle video
- Duration info (text)
- Speaker / mute (picture)
'''


from PyQt6.QtWidgets import QFileDialog, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

import os
from pathlib import Path

from .icons import MyIcon
from .logging import logger_runtime, logger_basic
from .cons_and_vars import save_json, cv, settings, PATH_JSON_SETTINGS
from .func_coll import (
    add_record_grouped_actions,
    save_db,
    remove_queued_tracks_after_playlist_clear,
    cur, # db
    connection, # db
    settings,   # json dic
    PATH_JSON_SETTINGS,
    )

ICON_SIZE = 20  # ICON/PICTURE IN THE BUTTONS


class MyButtons(QPushButton):

    def __init__(
            self,
            title,
            tooltip,
            av_player=None,
            av_player_duration=None,
            play_funcs=None,
            icon = None):
        super().__init__()

        self.setText(title)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setToolTipDuration(2000)
        self.setFont(QFont('Times', 9, 600))
        if icon:
            self.setIcon(icon)
            self.setText(None)
            self.setIconSize(QSize(cv.icon_size, cv.icon_size))
        self.av_player = av_player
        self.av_player_duration = av_player_duration
        self.play_funcs = play_funcs
        self.icon_img = MyIcon()



    '''
    ########################
        PLAYLIST SECTION
    ########################
    '''
    ''' BUTTON PLAYLIST - ADD TRACK '''
    def button_add_track_clicked(self):
        ''' BUTTON - MUSIC '''
        dialog_add_track = QFileDialog()
        dialog_add_track.setWindowTitle("Select a media file")
        dialog_add_track.setNameFilters(cv.FILE_TYPES_LIST)
        dialog_add_track.exec()
        if dialog_add_track.result():
            add_record_grouped_actions(dialog_add_track.selectedFiles()[0], self.av_player_duration)


    ''' BUTTON PLAYLIST - ADD DIRECTORY '''
    @logger_runtime
    def button_add_dir_clicked(self):
        error_path_list = []
        dialog_add_dir = QFileDialog()
        dialog_add_dir.setWindowTitle("Select a directory")
        dialog_add_dir.setFileMode(QFileDialog.FileMode.Directory)
        dialog_add_dir.exec()
        if dialog_add_dir.result():
            logger_basic('button_add_dir_clicked: Loop - start')
            cv.adding_records_at_moment = True
            for dir_path, dir_names, file_names in os.walk(dialog_add_dir.selectedFiles()[0]):
                for file in file_names:
                    if file.split('.')[-1] in cv.MEDIA_FILES:   # music_title.mp3 -> mp3
                        try:
                            add_record_grouped_actions(Path(dir_path, file), self.av_player_duration)
                        except:
                            error_path_list.append(Path(dir_path, file))
                if error_path_list:
                    for item in error_path_list:
                        logger_basic(f'ERROR: {item}')

            cv.active_pl_tracks_count = cv.active_pl_name.count() # use the latest track amount
            
            try:
                save_db()
                logger_basic('button_add_dir_clicked: DB Saved')
            except:
                logger_basic('ERROR: button_add_dir_clicked: Saving DB')
            cv.adding_records_at_moment = False


    ''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
    def button_remove_all_track_clicked(self):
        # QUEUE
        remove_queued_tracks_after_playlist_clear()
        # DB
        cur.execute("DELETE FROM {0}".format(cv.active_db_table))
        connection.commit()
        # PLAYLIST
        cv.active_pl_name.clear()
        cv.active_pl_queue.clear()
        cv.active_pl_duration.clear()

        cv.track_change_on_main_playlist_new_search_needed = True


    ''' BUTTON PLAYLIST - SET STYLE '''
    def set_style_playlist_buttons(self):
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.2 #F0F0F0, stop: 0.8 #F0F0F0, stop: 1 #C2C2C2);"
                            "color: grey;"   # font
                            "border: 1px solid grey;"
                            "border-radius: 4px;"
                            "margin: 3 px;" # 3 px != 3px
                            "}"
                        "QPushButton::pressed"
                            "{"
                            "background-color : #C2C2C2;"
                            "}"
                        )
    

    ''' BUTTON PLAYLIST - SETTINGS - SET STYLE '''
    def set_style_settings_button(self):
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.2 #F0F0F0, stop: 0.8 #F0F0F0, stop: 1 #C2C2C2);"
                            "color: grey;"   
                            "border: 1px solid grey;"
                            "border-radius: 4px;"
                            "margin: 3px;" # 3 px != 3px, diff. pre. style sheet
                            "}"
                        "QPushButton::pressed"
                            "{"
                            "background-color : #C2C2C2;"
                            "}"
                        )
    

    ''' BUTTON PLAYLIST - DURATION INFO - SET STYLE '''
    def set_style_duration_info_button(self):
        self.setFont(QFont('Times', 14, 600))
        self.setFlat(1)
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "color: grey;"   
                            "}"
                        )


    ''' 
    #####################
        PLAY SECTION    
    #####################
    '''
    ''' BUTTON PLAY SECTION - PLAY / PAUSE '''
    def button_play_pause_clicked(self):
        if self.av_player.player.isPlaying():
            self.av_player.player.pause()
            self.av_player.paused = True
            self.setIcon(self.icon_img.start)
            self.av_player.screen_saver_on()
        elif self.av_player.paused:
            self.av_player.player.play()
            self.av_player.paused = False
            self.setIcon(self.icon_img.pause)
            self.av_player.screen_saver_on_off()
        elif not self.av_player.player.isPlaying() and not self.av_player.paused:
            self.play_funcs.play_track()
            if self.av_player.player.isPlaying(): # ignoring empty playlist
                self.setIcon(self.icon_img.pause)
        
    
    # TRIGGERED BY THE DOUBLE-CLICK IN THE PLAYLIST
    def button_play_pause_via_list(self):
        self.setIcon(self.icon_img.pause)
        self.play_funcs.play_track()
    

    ''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
    def button_prev_track_clicked(self):

        if cv.playing_track_index == None:
            cv.playing_track_index = cv.playing_pl_name.currentRow() 
        if cv.playing_pl_name.count() > 0:
            if cv.playing_track_index != 0:
                cv.playing_track_index -= 1
                self.play_funcs.play_track(cv.playing_track_index)
            else:
                cv.playing_track_index = cv.playing_pl_name.count() - 1
                self.play_funcs.play_track(cv.playing_track_index)
    

    ''' BUTTON PLAY SECTION - NEXT TRACK '''
    def button_next_track_clicked(self):
        self.play_funcs.play_next_track()
    

    ''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
    def button_toggle_repeat_pl_clicked(self):
        cv.repeat_playlist =  (cv.repeat_playlist + 1) % 3
        
        # NO REPEAT
        if cv.repeat_playlist == 1:
            self.setFlat(0)
            self.setIcon(self.icon_img.repeat)
            self.av_player.text_display_on_video(1500, 'Repeat: OFF') 
        # REPEAT PLAYLIST
        elif cv.repeat_playlist == 2:
            self.setFlat(1)
            self.av_player.text_display_on_video(1500, 'Repeat: Playlist') 
        # REPEAT SINGLE TRACK
        else:
            self.setIcon(self.icon_img.repeat_single)
            self.av_player.text_display_on_video(1500, 'Repeat: Single track') 
        
        settings['repeat_playlist'] = cv.repeat_playlist
        save_json(settings, PATH_JSON_SETTINGS)
    

    ''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
    def button_toggle_shuffle_pl_clicked(self):
        if cv.shuffle_playlist_on:
            cv.shuffle_playlist_on = False
            self.setFlat(0)
            self.av_player.text_display_on_video(1500, 'Shuffle: OFF')            
        else:
            cv.shuffle_playlist_on = True
            self.setFlat(1)
            self.av_player.text_display_on_video(1500, 'Shuffle: ON') 
        
        settings['shuffle_playlist_on'] = cv.shuffle_playlist_on
        save_json(settings, PATH_JSON_SETTINGS)
    