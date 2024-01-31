'''
    BUTTON FUNCTIONS DECLARED BELOW:
    --------------------------------
    - Add track
    - Add directory
    - Remove track - *more added/compiled in MAIN
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
    - Settings
    - Stop
    - Toggle playlist
    - Toogle video
    - Duration info (text)
    - Speaker / mute (picture)
'''


from PyQt6.QtWidgets import QFileDialog, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

import os

from .cons_and_vars import Path, save_json, cv, settings, PATH_JSON_SETTINGS
from .func_coll import (
    remove_record_db,
    generate_track_list_detail,
    add_record_grouped_actions,
    update_duration_sum_var_after_track_remove,
    save_playing_last_track_index,
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

        self.button_image_start = QIcon(f'skins/{cv.skin_selected}/start.png')
        self.button_image_pause = QIcon(f'skins/{cv.skin_selected}/pause.png')
        self.button_image_repeat = QIcon(f'skins/{cv.skin_selected}/repeat.png')
        self.button_image_repeat_single = QIcon(f'skins/{cv.skin_selected}/repeat_single.png')

    ''' 
    PLAYLIST SECTION
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
    def button_add_dir_clicked(self):
        track_path_list = []
        error_path_list = []
        dialog_add_dir = QFileDialog()
        dialog_add_dir.setWindowTitle("Select a directory")
        dialog_add_dir.setFileMode(QFileDialog.FileMode.Directory)
        dialog_add_dir.exec()
        if dialog_add_dir.result():
            for dir_path, dir_names, file_names in os.walk(dialog_add_dir.selectedFiles()[0]):
                for file in file_names:
                    if file[-4:] in cv.MEDIA_FILES:
                        track_path_list.append(Path(dir_path, file))
            if len(track_path_list) > 0:
                for track_path in track_path_list:
                    try:
                        add_record_grouped_actions(track_path, self.av_player_duration)
                    except:
                        error_path_list.append(track_path)
                if error_path_list:
                    for item in error_path_list:
                        print(f'ERROR - {item}')


    ''' BUTTON PLAYLIST - REMOVE TRACK '''
    def button_remove_track_clicked(self):

        update_duration_sum_var_after_track_remove()
        
        current_row_index = cv.active_pl_name.currentRow()
        # LAST TRACK INDEX
        if  current_row_index < cv.playing_pl_last_track_index:
            # cv.last_track_index -= 1
            # cv.playing_track_index -= 1
            cv.playing_pl_last_track_index -= 1
            save_playing_last_track_index()
        # DB
        remove_record_db(current_row_index)
        # PLAYLIST
        cv.active_pl_name.takeItem(current_row_index)
        cv.active_pl_queue.takeItem(current_row_index)
        cv.active_pl_duration.takeItem(current_row_index)
        # RENAME PLAYLIST
        row_id_db = current_row_index + 1
        cur.execute("SELECT * FROM {0} WHERE row_id >= ?".format(cv.active_db_table), (row_id_db,))
        playlist = cur.fetchall()
        for item in playlist:
            track_row_db, list_name, duration = generate_track_list_detail(item)
            cv.active_pl_name.item(track_row_db-1).setText(list_name)
        



    ''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
    def button_remove_all_track_clicked(self):
        # DB
        cur.execute("DELETE FROM {0}".format(cv.active_db_table))
        connection.commit()
        # PLAYLIST
        cv.active_pl_name.clear()
        cv.active_pl_queue.clear()
        cv.active_pl_duration.clear()


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
    PLAY SECTION
    '''
    ''' BUTTON PLAY SECTION - PLAY / PAUSE '''
    def button_play_pause_clicked(self):
        if self.av_player.player.isPlaying():
            self.av_player.player.pause()
            self.av_player.paused = True
            self.setIcon(self.button_image_start)
            self.av_player.screen_saver_on()
        elif self.av_player.paused:
            self.av_player.player.play()
            self.av_player.paused = False
            self.setIcon(self.button_image_pause)
            self.av_player.screen_saver_on_off()
        elif not self.av_player.player.isPlaying() and not self.av_player.paused:
            self.play_funcs.play_track()
            if self.av_player.player.isPlaying(): # ignoring empty playlist
                self.setIcon(self.button_image_pause)
        
    
    # TRIGGERED BY THE DOUBLE-CLICK IN THE PLAYLIST
    def button_play_pause_via_list(self):
        self.setIcon(self.button_image_pause)
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
            self.setIcon(self.button_image_repeat)
        # REPEAT PLAYLIST
        elif cv.repeat_playlist == 2:
            self.setFlat(1)
        # REPEAT SINGLE TRACK
        else:
            self.setIcon(self.button_image_repeat_single)
        
        settings['repeat_playlist'] = cv.repeat_playlist
        save_json(settings, PATH_JSON_SETTINGS)
    

    ''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
    def button_toggle_shuffle_pl_clicked(self):
        if cv.shuffle_playlist_on:
            cv.shuffle_playlist_on = False
            self.setFlat(0)
        else:
            cv.shuffle_playlist_on = True
            self.setFlat(1)
        
        settings['shuffle_playlist_on'] = cv.shuffle_playlist_on
        save_json(settings, PATH_JSON_SETTINGS)
    