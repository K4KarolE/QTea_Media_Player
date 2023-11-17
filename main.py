
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout 
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
    cur.execute(f"INSERT INTO playlist_table(duration, path) VALUES ('{duration}', '{path}')")
    connection.commit()

def remove_record_db(list_row_id):
    cur.execute(f"DELETE FROM playlist_table WHERE row_id = '{list_row_id}'")
    cur.execute(f"UPDATE playlist_table SET row_id = row_id - 1 WHERE row_id > '{list_row_id}'")
    connection.commit()

def get_row_id_db(path): 
    cur.execute(f"SELECT row_id FROM playlist_table WHERE path = '{path}'")
    record = cur.fetchall()
    return record[-1][0]    # adding same track multiple times --> row_id: picked the latest's one

def get_path_db(row_id): 
    cur.execute(f"SELECT * FROM playlist_table WHERE row_id = '{row_id}'")
    record = cur.fetchall()
    print(record[0][2])

def generate_track_list_name(item):
    duration_list = f'{int(int(item[1])/60/1000)}:{int(int(item[1])%60)}'
    list_name = f'{item[0]}. {Path(item[2]).stem} - {duration_list}'
    return list_name


''' PLAYLIST DB '''
connection = sqlite3.connect('playlist.db')
cur = connection.cursor()

''' PLAYER '''
music = Music()



''' APP '''
app = QApplication(sys.argv)
window = QWidget()
window.resize(600, 500)
window.setWindowIcon(QIcon(str(Path(Path(__file__).parent, 'skins/window_icon.png'))))
listWidget = QListWidget(window)
window.setWindowTitle("Media Player")

''' BUTTONS '''
# BUTTON - ADD TRACK
def button_add_track_clicked():
    music_duration = Music()

    dialog_add_track = QFileDialog()
    dialog_add_track.setWindowTitle("Select an MP3 file")
    dialog_add_track.setNameFilter("MP3 files (*.mp3)")
    dialog_add_track.exec()
    if dialog_add_track.result():
        track_name = Path(dialog_add_track.selectedFiles()[0]).stem
        track_path = dialog_add_track.selectedFiles()[0]
        # DURATION
        music_duration.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
        duration = music_duration.player.duration()
        duration_list = f'{int(duration/60/1000)}:{int(duration%60)}'
        # DB
        add_record_db(duration, track_path)
        row_id = get_row_id_db(track_path)
        # PLAYLIST
        list_name = f'{row_id}. {track_name} - {duration_list}'
        QListWidgetItem(list_name, listWidget)

button_add_track = QPushButton(window, text='Add track')
button_add_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_track.clicked.connect(button_add_track_clicked)
button_add_track.setFont(QFont('Times', 10, 600))


# BUTTON - ADD DIRECTORY
def button_add_dir_clicked():
    music_duration = Music()
    track_path_list = []

    dialog_add_dir = QFileDialog()
    dialog_add_dir.setWindowTitle("Select a directory")
    dialog_add_dir.setFileMode(QFileDialog.FileMode.Directory)
    dialog_add_dir.exec()
    if dialog_add_dir.result():
        for dir_path, dir_names, file_names in os.walk(dialog_add_dir.selectedFiles()[0]):
            for file in file_names:
                if file[-4:] in ['.mp3', '.wav']:
                    track_path_list.append(Path(dir_path, file))
        if len(track_path_list) > 0:
            for track_path in track_path_list:
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
                QListWidgetItem(list_name, listWidget)

button_add_dir = QPushButton(window, text='Add directory')
button_add_dir.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_dir.clicked.connect(button_add_dir_clicked)
button_add_dir.setFont(QFont('Times', 10, 600))



# BUTTON - REMOVE TRACK
def button_remove_track_clicked():
    # DB
    row_id_db = listWidget.currentRow() + 1
    remove_record_db(row_id_db)
    # PLAYLIST
    listWidget.takeItem(listWidget.currentRow())
    rename_playlist(row_id_db)


def rename_playlist(row_id_db):
    cur.execute(f"SELECT * FROM playlist_table WHERE row_id >= '{row_id_db}'")
    playlist = cur.fetchall()
    for item in playlist:
        list_name = generate_track_list_name(item)
        listWidget.item(row_id_db-1).setText(list_name)
        row_id_db +=1

button_remove_track = QPushButton(window, text='Remove track')
button_remove_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_track.clicked.connect(button_remove_track_clicked)
button_remove_track.setFont(QFont('Times', 10, 600))


# BUTTON - REMOVE ALL TRACK
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
    QListWidgetItem(list_name, listWidget)



''' LIST ACTIONS '''
def play_track():
    row_id = listWidget.currentRow() + 1
    track_path = cur.execute(f"SELECT path FROM playlist_table WHERE row_id = {row_id}").fetchall()[0][0]
    music.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    music.audio_output.setVolume(0.5)
    music.player.play()
listWidget.itemDoubleClicked.connect(play_track)



''' LAYOUT '''
widgets_list = [
    button_add_track,
    button_add_dir,
    button_remove_track,
    button_remove_all_track,
    listWidget
    ]
    
window_layout = QVBoxLayout(window)
for widget in widgets_list:
    window_layout.addWidget(widget)
window.setLayout(window_layout)

window.show()

sys.exit(app.exec())