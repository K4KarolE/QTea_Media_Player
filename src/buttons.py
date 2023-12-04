from PyQt6.QtWidgets import QFileDialog, QPushButton
from PyQt6.QtCore import QUrl, Qt, QEvent, QSize
from PyQt6.QtGui import QIcon, QFont

import os

from .cons_and_vars import Path, save_json, settings, PATH_JSON_SETTINGS
from .func_coll import (
    remove_record_db,
    generate_track_list_detail,
    add_record_grouped_actions,
    cv, # data
    cur, # db
    connection, # db
    settings,   # json dic
    PATH_JSON_SETTINGS,
    )

ICON_SIZE = 20  # ICON/PICTURE IN THE BUTTONS


class MyButtons(QPushButton):

    def __init__(
            self,
            parent,
            title,
            tooltip,
            av_player=None,
            av_player_duration=None,
            play_funcs=None,
            icon = None):
        super().__init__()

        self.setParent(parent)
        self.setText(title)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setToolTipDuration(2000)
        self.setFont(QFont('Times', 10, 600))
        if icon:
            self.setIcon(icon)
            self.setText(None)
            self.setIconSize(QSize(cv.icon_size, cv.icon_size))

        self.av_player = av_player
        self.av_player_duration = av_player_duration
        self.play_funcs = play_funcs

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
        # LAST TRACK INDEX
        if  cv.active_pl_name.currentRow() < cv.last_track_index:
            cv.last_track_index = cv.last_track_index - 1
            settings[cv.active_db_table]['last_track_index'] = cv.last_track_index
            save_json(settings, PATH_JSON_SETTINGS)
        # DB
        row_id_db = cv.active_pl_name.currentRow() + 1
        remove_record_db(row_id_db)
        # PLAYLIST
        cv.active_pl_name.takeItem(cv.active_pl_name.currentRow())
        cv.active_pl_duration.takeItem(cv.active_pl_name.currentRow())
        # RENAME PLAYLIST
        cur.execute("SELECT * FROM {0} WHERE row_id >= ?".format(cv.active_db_table), (row_id_db,))
        playlist = cur.fetchall()
        for item in playlist:
            list_name, duration = generate_track_list_detail(item)
            cv.active_pl_name.item(row_id_db-1).setText(list_name)
            row_id_db +=1


    ''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
    def button_remove_all_track_clicked(self):
        # DB
        cur.execute("DELETE FROM {0}".format(cv.active_db_table))
        connection.commit()
        # PLAYLIST
        cv.active_pl_name.clear()
        cv.active_pl_duration.clear()


    ''' 
    PLAY SECTION
    '''
    ''' BUTTON PLAY SECTION - PLAY / PAUSE '''
    def button_play_pause_clicked(self):
        button_image_start = QIcon('skins/default/start.png')
        button_image_pause = QIcon('skins/default/pause.png')

        if self.av_player.played_row == None:
            self.play_funcs.play_track()
            self.setIcon(button_image_pause)
        elif self.av_player.player.isPlaying():
            self.av_player.player.pause()
            self.av_player.paused = True
            self.setIcon(button_image_start)
        elif self.av_player.paused:
            self.av_player.player.play()
            self.av_player.paused = False
            self.setIcon(button_image_pause)
        elif not self.av_player.player.isPlaying() and not self.av_player.paused:
            self.play_funcs.play_track()
            self.setIcon(button_image_pause)
    
    def button_play_pause_via_list(self):
        button_image_pause = QIcon('skins/default/pause.png')
        self.setIcon(button_image_pause)
        self.play_funcs.play_track()


    ''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
    def button_prev_track_clicked(self):
        if cv.active_pl_name.count() > 0 and self.av_player.played_row != None:

            if cv.shuffle_playlist_on:
                cv.active_pl_name.setCurrentRow(cv.last_track_index)
            elif cv.active_pl_name.currentRow() != 0:
                cv.active_pl_name.setCurrentRow(self.av_player.played_row - 1)
            else:
                cv.active_pl_name.setCurrentRow(cv.active_pl_name.count() - 1)
            self.play_funcs.play_track()
    

    ''' BUTTON PLAY SECTION - NEXT TRACK '''
    def button_next_track_clicked(self):
        if cv.active_pl_name.count() > 0 and self.av_player.played_row != None:
            self.play_funcs.play_next_track()
    

    ''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
    def button_toggle_repeat_pl_clicked(self):
        button_image_repeat = QIcon(f'skins/{cv.skin_selected}/repeat.png')
        button_image_repeat_single = QIcon(f'skins/{cv.skin_selected}/repeat_single.png')
        cv.repeat_playlist =  (cv.repeat_playlist + 1) % 3
        
        if cv.repeat_playlist == 1:
            self.setFlat(0)
            self.setIcon(button_image_repeat)
        elif cv.repeat_playlist == 2:
            self.setFlat(1)
        else:
            self.setIcon(button_image_repeat_single)
        
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