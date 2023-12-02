from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QPushButton,

    )
from PyQt6.QtCore import QUrl, Qt, QEvent
from PyQt6.QtGui import QIcon, QFont

from .cons_and_vars import Path, save_json, settings, PATH_JSON_SETTINGS
from .func_coll import (
    save_last_track_index,
    remove_record_db,
    get_path_db,
    get_duration_db,
    generate_track_list_detail,
    add_record_grouped_actions,
    cv, # data
    cur, # db
    connection, # db
    settings,   # json dic
    PATH_JSON_SETTINGS,
    )

import os



MEDIA_FILES = "Media files (*.mp3 *.wav *.flac *.midi *.aac *.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
AUDIO_FILES = "Audio files (*.mp3 *.wav *.flac *.midi *.aac)"
VIDEO_FILES = "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
FILE_TYPES_LIST = [MEDIA_FILES, AUDIO_FILES, VIDEO_FILES, 'All Files']


class MyButtons(QPushButton):

    def __init__(self, parent, title, tooltip, clicked_action):
        super().__init__()
        self.setParent(parent)
        self.setText(title)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setToolTipDuration(2000)
        self.setFont(QFont('Times', 10, 600))
        self.clicked.connect(clicked_action)



class MyButtonsFunc():
    def __init__(self, av_player, av_player_duration):
        self.av_player = av_player
        self.av_player_duration = av_player_duration

    ''' 
    PLAYLIST SECTION
    '''
    ''' BUTTON PLAYLIST - ADD TRACK '''
    def button_add_track_clicked(self):
        dialog_add_track = QFileDialog()
        dialog_add_track.setWindowTitle("Select a media file")
        dialog_add_track.setNameFilters(FILE_TYPES_LIST)
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
                    if file[-4:] in MEDIA_FILES:
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
    # TODO                 