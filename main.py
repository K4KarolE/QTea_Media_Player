
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout 
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem, QPushButton
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QMovie, QIcon, QFont

# from PyQt6.QtWidgets import QTabWidget, QLabel
# from PyQt6.QtWidgets import QLineEdit
# from PyQt6.QtCore import QSize, QTimer, QTime

import os
import sys
import sqlite3

from player import Path
from player import Music
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

def get_path_db(row_id): 
    return cur.execute(f"SELECT * FROM playlist_table WHERE row_id = ?", (row_id,)).fetchall()[0][2]

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
inactive_track_font_style = QFont('Consolas', 10, 500)
active_track_font_style = QFont('Consolas', 10, 600)


''' APP '''
app = QApplication(sys.argv)
window = QWidget()
window.resize(1500, 650)
window.setWindowIcon(QIcon(str(Path(Path(__file__).parent, 'skins/window_icon.png'))))
listWidget = QListWidget(window)
window.setWindowTitle("Media Player")

''' PLAYER '''
music = Music()
music_duration = Music(False)


''' 
#######################
        BUTTONS              
#######################
'''
MEDIA_FILES = "Media files (*.mp3 *.wav *.flac *.midi *.aac *.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
AUDIO_FILES = "Audio files (*.mp3 *.wav *.flac *.midi *.aac)"
VIDEO_FILES = "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
FILE_TYPES_LIST = [MEDIA_FILES, AUDIO_FILES, VIDEO_FILES, 'All Files']

''' BUTTON - ADD TRACK '''
def button_add_track_clicked():
    dialog_add_track = QFileDialog()
    dialog_add_track.setWindowTitle("Select a media file")
    dialog_add_track.setNameFilters(FILE_TYPES_LIST)
    dialog_add_track.exec()
    if dialog_add_track.result():
        add_record_grouped_actions(
            dialog_add_track.selectedFiles()[0],
            music_duration
            )

button_add_track = QPushButton(window, text='Add track')
button_add_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_track.clicked.connect(button_add_track_clicked)
button_add_track.setFont(QFont('Times', 10, 600))


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
                    add_record_grouped_actions(track_path, music_duration)
                except:
                    error_path_list.append(track_path)
            if error_path_list:
                for item in error_path_list:
                    print(f'ERROR - {item}')

button_add_dir = QPushButton(window, text='Add directory')
button_add_dir.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_dir.clicked.connect(button_add_dir_clicked)
button_add_dir.setFont(QFont('Times', 10, 600))



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

button_remove_track = QPushButton(window, text='Remove track')
button_remove_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_track.clicked.connect(button_remove_track_clicked)
button_remove_track.setFont(QFont('Times', 10, 600))


''' BUTTON - REMOVE ALL TRACK '''
def button_remove_all_track_clicked():
    # DB
    cur.execute(f"DELETE FROM playlist_table")
    connection.commit()
    # PLAYLIST
    listWidget.clear()

button_remove_all_track = QPushButton(window, text='Remove all tracks')
button_remove_all_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_all_track.clicked.connect(button_remove_all_track_clicked)
button_remove_all_track.setFont(QFont('Times', 10, 600))


''' PLAYLIST DB --> LIST WIDGET '''
cur.execute(f"SELECT * FROM playlist_table")
playlist = cur.fetchall()
for item in playlist:
    list_name = generate_track_list_name(item)
    QListWidgetItem(list_name, listWidget).setFont(inactive_track_font_style)



''' LIST ACTIONS '''
def play_track():
    # FONT
    if music.played_row != None and music.played_row < listWidget.count():
        listWidget.item(music.played_row).setFont(inactive_track_font_style)
    # PATH
    row_id = listWidget.currentRow() + 1
    listWidget.currentItem().setFont(active_track_font_style)
    track_path = get_path_db(row_id)
    # PLAYER
    music.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    music.audio_output.setVolume(0.5)
    music.player.play()
    # COUNTER
    music.played_row = listWidget.currentRow()
listWidget.itemDoubleClicked.connect(play_track)


def play_next_track():
    if (music.player.mediaStatus() == music.player.MediaStatus.EndOfMedia and 
        listWidget.count() != listWidget.currentRow() + 1):
            if music.base_played:
                listWidget.setCurrentRow(music.played_row + 1)
                play_track()
            else:
                music.base_played = True      
music.player.mediaStatusChanged.connect(play_next_track)


''' 
######################
        LAYOUTS                          
######################
'''
layout_hor = QHBoxLayout(window)    
layout_vert_left = QVBoxLayout()
layout_vert_middle = QVBoxLayout()
layout_vert_right = QVBoxLayout()

layout_hor.addLayout(layout_vert_left, 200)
layout_hor.addLayout(layout_vert_middle, 1)
layout_hor.addLayout(layout_vert_right, 99)

# LAYOUT LEFT WIDGETS
widgets_list = [
    button_add_track,
    button_add_dir,
    button_remove_track,
    button_remove_all_track,
    music.video_output
    ]

for widget in widgets_list:
    layout_vert_left.addWidget(widget)

# LAYOUT RIGHT WIDGETS
layout_vert_right.addWidget(listWidget)

# for later
# layout_hor.setStretch(0, 10)

window.show()

sys.exit(app.exec())