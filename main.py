
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout 
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem, QPushButton, QMainWindow
from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import QUrl, Qt, QEvent
from PyQt6.QtGui import QMovie, QIcon, QFont

# from PyQt6.QtWidgets import QTabWidget, QLabel
# from PyQt6.QtWidgets import QLineEdit
# from PyQt6.QtCore import QSize, QTimer, QTime

import os
import sys
import sqlite3

from mt_player import Path
from mt_player import MTPlayer
# from player import open_json, save_json
# from player import PATH_JSON_PLAYLIST


def add_record_db(duration, path):
    cur.execute("INSERT INTO playlist_table(duration, path) VALUES (?, ?)", (duration, str(path)))
    connection.commit()

def remove_record_db(list_row_id):
    cur.execute(f"DELETE FROM playlist_table WHERE row_id = ?", (list_row_id,))
    cur.execute(f"UPDATE playlist_table SET row_id = row_id - 1 WHERE row_id > ?", (list_row_id,) )
    connection.commit()

def get_row_id_db(path): 
    return cur.execute(f"SELECT row_id FROM playlist_table WHERE path = ?", (str(path),)).fetchall()[-1][0] 
    # [-1][0]: adding same track multiple times --> row_id: picked the latest's one

def get_path_db(): 
    return cur.execute(f"SELECT * FROM playlist_table WHERE row_id = ?",
                        (listWidget.currentRow() + 1,)).fetchall()[0][2]

def get_duration_db():
    return int(cur.execute(f"SELECT * FROM playlist_table WHERE row_id = ?",
                           (listWidget.currentRow() + 1,)).fetchall()[0][1])

def generate_track_list_name(item):
    duration_list = f'{int(int(item[1])/60/1000)}:{int(int(item[1])%60)}'
    return f'{item[0]}. {Path(item[2]).stem} - {duration_list}'

def add_record_grouped_actions(track_path, music_duration):
    track_name = Path(track_path).stem
    # DURATION
    music_duration.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    duration = music_duration.player.duration()
    duration_list = f'{int(duration/60/1000)}:{int(duration%60)}'
    # DB
    add_record_db(duration, track_path)
    row_id = get_row_id_db(track_path)
    # PLAYLIST
    list_name = f'{row_id}. {track_name} - {duration_list}'
    QListWidgetItem(list_name, listWidget).setFont(inactive_track_font_style)


''' PLAYLIST DB '''
connection = sqlite3.connect('playlist.db')
cur = connection.cursor()


''' STYLE '''
inactive_track_font_style = QFont('Times', 11, 500)
active_track_font_style = QFont('Times', 11, 600)


''' APP '''
app = QApplication(sys.argv)
window = QWidget()
window.resize(1600, 750)
window.setWindowIcon(QIcon(str(Path(Path(__file__).parent, 'skins/window_icon.png'))))
window.setWindowTitle("Mad Tea media player")



''' PLAYER '''
mt_player = MTPlayer()
""" 
    mt_player_duration
    -------------------
    only used for duration calculation -->
    able to add new track(s) without interrupting 
    the playing (mt_player)
"""
mt_player_duration = MTPlayer(False)    


''' 
#######################
        WINDOWS              
#######################
'''
# FOR BUTTONS: ADD TRACK, REMOVE TRACK, ..
under_playlist_window = QMainWindow()

# FOR BUTTONS: PLAY/STOP, PAUSE, ..
under_play_slider_window = QMainWindow()


''' 
########################
        LISTWIDGET                    
########################
'''
listWidget = QListWidget(window)
listWidget.setSpacing(3)
# double click action declared after 'play_track' func



''' 
#######################
        BUTTONS              
#######################
'''
MEDIA_FILES = "Media files (*.mp3 *.wav *.flac *.midi *.aac *.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
AUDIO_FILES = "Audio files (*.mp3 *.wav *.flac *.midi *.aac)"
VIDEO_FILES = "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
FILE_TYPES_LIST = [MEDIA_FILES, AUDIO_FILES, VIDEO_FILES, 'All Files']

U_PLIST_BUTTON_WIDTH = 50
U_PLIST_BUTTON_HEIGHT = 30

def button_x_pos(num):
    return (U_PLIST_BUTTON_WIDTH + 3) * num

''' BUTTON - ADD TRACK '''
def button_add_track_clicked():
    dialog_add_track = QFileDialog()
    dialog_add_track.setWindowTitle("Select a media file")
    dialog_add_track.setNameFilters(FILE_TYPES_LIST)
    dialog_add_track.exec()
    if dialog_add_track.result():
        add_record_grouped_actions(
            dialog_add_track.selectedFiles()[0],
            mt_player_duration
            )

button_add_track = QPushButton(under_playlist_window, text='AT')
button_add_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_track.setToolTip('Add track')
button_add_track.setToolTipDuration(2000)
button_add_track.setFont(QFont('Times', 10, 600))
button_add_track.setGeometry(0, 0, U_PLIST_BUTTON_WIDTH, U_PLIST_BUTTON_HEIGHT)
button_add_track.clicked.connect(button_add_track_clicked)


''' BUTTON - ADD DIRECTORY '''
def button_add_dir_clicked():
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
                    add_record_grouped_actions(track_path, mt_player_duration)
                except:
                    error_path_list.append(track_path)
            if error_path_list:
                for item in error_path_list:
                    print(f'ERROR - {item}')

button_add_dir = QPushButton(under_playlist_window, text='AD')
button_add_dir.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_dir.setToolTip('Add directory')
button_add_dir.setToolTipDuration(2000)
button_add_dir.setFont(QFont('Times', 10, 600))
button_add_dir.setGeometry(button_x_pos(1), 0, U_PLIST_BUTTON_WIDTH, U_PLIST_BUTTON_HEIGHT)
button_add_dir.clicked.connect(button_add_dir_clicked)



''' BUTTON - REMOVE TRACK '''
def button_remove_track_clicked():
    # DB
    row_id_db = listWidget.currentRow() + 1
    remove_record_db(row_id_db)
    # PLAYLIST
    listWidget.takeItem(listWidget.currentRow())
    rename_playlist(row_id_db)


def rename_playlist(row_id_db):
    cur.execute(f"SELECT * FROM playlist_table WHERE row_id >= ?", (row_id_db,))
    playlist = cur.fetchall()
    for item in playlist:
        list_name = generate_track_list_name(item)
        listWidget.item(row_id_db-1).setText(list_name)
        row_id_db +=1

button_remove_track = QPushButton(under_playlist_window, text='RT')
button_remove_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_track.setToolTip('Remove track')
button_remove_track.setToolTipDuration(2000)
button_remove_track.setFont(QFont('Times', 10, 600))
button_remove_track.setGeometry(button_x_pos(2), 0, U_PLIST_BUTTON_WIDTH, U_PLIST_BUTTON_HEIGHT)
button_remove_track.clicked.connect(button_remove_track_clicked)

''' BUTTON - REMOVE ALL TRACK '''
def button_remove_all_track_clicked():
    # DB
    cur.execute(f"DELETE FROM playlist_table")
    connection.commit()
    # PLAYLIST
    listWidget.clear()

button_remove_all_track = QPushButton(under_playlist_window, text='RAL')
button_remove_all_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_all_track.setToolTip('Remove all track')
button_remove_all_track.setToolTipDuration(2000)
button_remove_all_track.setFont(QFont('Times', 10, 600))
button_remove_all_track.setGeometry(button_x_pos(3), 0, U_PLIST_BUTTON_WIDTH, U_PLIST_BUTTON_HEIGHT)
button_remove_all_track.clicked.connect(button_remove_all_track_clicked)


''' BUTTON - PLAY/STOP '''
def button_button_play_stop_clicked():
    if mt_player.player.isPlaying():
        mt_player.player.stop()
    else:
        play_track()

button_play_stop = QPushButton(under_play_slider_window, text='Play / Stop')
button_play_stop.setCursor(Qt.CursorShape.PointingHandCursor)
button_play_stop.clicked.connect(button_button_play_stop_clicked)
button_play_stop.setFont(QFont('Times', 10, 600))


''' PLAYLIST DB --> LIST WIDGET '''
cur.execute(f"SELECT * FROM playlist_table")
playlist = cur.fetchall()
for item in playlist:
    list_name = generate_track_list_name(item)
    QListWidgetItem(list_name, listWidget).setFont(inactive_track_font_style)



''' LIST ACTIONS '''
def play_track():
    if listWidget.count() > 0:
        """ 
            If playlist cleared and new track(s) added
            Pressing Play/Stop --> first track played
        """
        if listWidget.currentRow() < 0:
            listWidget.setCurrentRow(0)
        # FONT
        if mt_player.played_row != None and mt_player.played_row < listWidget.count():
            listWidget.item(mt_player.played_row).setFont(inactive_track_font_style)
        listWidget.currentItem().setFont(active_track_font_style)
        # PATH / DURATION / SLIDER
        track_path = get_path_db()
        track_duration = get_duration_db()
        play_slider.setMaximum(track_duration)
        # PLAYER
        mt_player.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
        # mt_player.audio_output.setVolume(0.5)
        mt_player.player.play()
        # COUNTER
        mt_player.played_row = listWidget.currentRow()
        # WINDOW TITLE
        window.setWindowTitle(f'{Path(track_path).stem} - Mad Tea media player')


def play_next_track():
    if (mt_player.player.mediaStatus() == mt_player.player.MediaStatus.EndOfMedia and 
        listWidget.count() != listWidget.currentRow() + 1):
            if mt_player.base_played:
                listWidget.setCurrentRow(mt_player.played_row + 1)
                play_track()
            else:
                mt_player.base_played = True      
mt_player.player.mediaStatusChanged.connect(play_next_track)


listWidget.itemDoubleClicked.connect(play_track)


''' 
######################
        SLIDER                          
######################
'''

play_slider = QSlider()
# wihout the groove's bg color --> 
# not able to change the handle's size
play_slider.setStyleSheet(
                        "QSlider::groove"
                            "{"
                            "background: #C2C2C2;"
                            "height: 10px;"
                            "border-radius: 4px;"
                            "}"

                        "QSlider::handle"
                            "{"
                            "border: 1px solid grey;"
                            "border-radius: 8px;"
                            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C2C2C2, stop:1 #E8E8E8);"
                            "width: 15px;"
                            "margin: -3 px;  /* expand outside the groove */"
                            "}"

                        "QSlider::sub-page"
                            "{"
                            "background: #287DCC;"
                            "}"
                        )
                            
# setParent(window_type)
play_slider.setOrientation(Qt.Orientation.Horizontal)
# play_slider.setMinimum(0)
# play_slider.setMaximum(100)
# play_slider.setValue(0)
play_slider.setCursor(Qt.CursorShape.PointingHandCursor)

def player_set_position():
    if mt_player.base_played:
        mt_player.player.setPosition(play_slider.value())

play_slider.sliderReleased.connect(player_set_position)


def play_slider_set_value():
    if mt_player.base_played and not play_slider.isSliderDown():
        play_slider.setValue(mt_player.player.position())

mt_player.player.positionChanged.connect(play_slider_set_value)


''' 
######################
        LAYOUTS                          
######################
'''
'''
    
    -----------------
    |       ||       |
    |       || PLIST |
    |  VID  ||_______|  
    |_______||_______|
    |________________|
    |________________|
   
'''

layout_base = QVBoxLayout(window)
layout_hor_top = QHBoxLayout()
layout_ver_bottom = QVBoxLayout()

layout_base.addLayout(layout_hor_top, 90)
layout_base.addLayout(layout_ver_bottom, 10)
# layout_base.addLayout(layout_bottom_buttons)

layout_vert_left = QVBoxLayout()
layout_vert_middle = QVBoxLayout()
layout_vert_right = QVBoxLayout()

layout_hor_top.addLayout(layout_vert_left, 200)
layout_hor_top.addLayout(layout_vert_middle, 1)
layout_hor_top.addLayout(layout_vert_right, 99)

# LAYOUT ADD WIDGETS
layout_vert_left.addWidget(mt_player.video_output)
layout_vert_right.addWidget(listWidget, 95)
layout_vert_right.addWidget(under_playlist_window, 5)
layout_ver_bottom.addWidget(play_slider)
layout_ver_bottom.addWidget(under_play_slider_window)

# TODO: layout_hor.setStretch(0, 10)


window.show()

sys.exit(app.exec())