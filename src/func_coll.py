
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QFont

from .cons_and_vars import Data, Path, save_json
from .cons_and_vars import settings, PATH_JSON_SETTINGS
import sqlite3

cv = Data()
connection = sqlite3.connect('playlist.db')
cur = connection.cursor()
inactive_track_font_style = QFont('Times', 11, 500)
active_track_font_style = QFont('Times', 11, 600)


def active_utility():
    cv.active_db_table = cv.paylist_list[cv.active_tab] # playlist_1, playlist_2, ..
    cv.last_track_index = settings[cv.active_db_table]['last_track_index']
    cv.active_playlist = cv.paylist_widget_dic[cv.active_db_table]['name_list_widget']  # widget
    cv.active_pl_duration = cv.paylist_widget_dic[cv.active_db_table]['duration_list_widget']   # widget


def save_last_track_index():
    cv.last_track_index = cv.active_playlist.currentRow()
    settings[cv.active_db_table]['last_track_index'] = cv.last_track_index
    save_json(settings, PATH_JSON_SETTINGS)


def add_record_db(duration, path):
    cur.execute("INSERT INTO {0}(duration, path) VALUES (?, ?)".format(cv.active_db_table), (duration, str(path)))
    connection.commit()


def remove_record_db(list_row_id):
    cur.execute("DELETE FROM {0} WHERE row_id = ?".format(cv.active_db_table), (list_row_id,))
    cur.execute("UPDATE {0} SET row_id = row_id - 1 WHERE row_id > ?".format(cv.active_db_table), (list_row_id,) )
    connection.commit()


def get_row_id_db(path):
    return cur.execute("SELECT row_id FROM {0} WHERE path = ?".format(cv.active_db_table), (str(path),)).fetchall()[-1][0] 
    # [-1][0]: adding same track multiple times --> row_id: picked the latest's one


def get_path_db():
    return cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(cv.active_db_table),
                        (cv.active_playlist.currentRow() + 1,)).fetchall()[0][2]


def get_duration_db():
    # active_playlist = tabs_playlist.currentWidget()
    return int(cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(cv.active_db_table),
                           (cv.active_playlist.currentRow() + 1,)).fetchall()[0][1])


def generate_duration_to_display(raw_duration):

    try:
        # SECONDS
        str_seconds = str(int(int(raw_duration)/1000%60))
        if str_seconds == '0':
            seconds = '00'
        elif len(str_seconds) == 1:
            seconds = f'0{str_seconds}'
        else:
            seconds = str_seconds[0:2]
        
        # MINUTES
        int_minutes = int(int(raw_duration)/60/1000)
        if int_minutes == 60:
            minutes = '01'
        elif int_minutes in range(10,60):
            minutes = str(int_minutes)
        elif int_minutes in range(0,10):
            minutes = f'0{str(int_minutes)}'
        else:
            minutes = str(int_minutes%60)

        # HOURS
        if int_minutes > 60:
            str_hours = str(int((int_minutes - int_minutes%60)/60))
            duration = f'{str_hours}:{minutes}:{seconds}'
        else:
            duration = f'{minutes}:{seconds}'
    except:
        duration = 'ERROR'

    return duration


def generate_track_list_detail(db_track_record):
    # [0]:row, [1]:duration, [2]:path
    track_name = f'{db_track_record[0]}. {Path(db_track_record[2]).stem}'
    duration = generate_duration_to_display(db_track_record[1])
    return track_name, duration


def add_record_grouped_actions(track_path, av_player_duration):

    track_name = Path(track_path).stem
    av_player_duration.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    raw_duration = av_player_duration.player.duration()
    duration = generate_duration_to_display(raw_duration)
    add_record_db(raw_duration, track_path)

    row_id = cv.active_playlist.count() + 1
    track_name = f'{row_id}. {track_name}'
    
    add_new_list_item(track_name, cv.active_playlist, 'left')
    add_new_list_item(duration, cv.active_pl_duration, 'right')


def add_new_list_item(new_item, list_widget, alignment):
    
    list_item = QListWidgetItem(new_item, list_widget)
    list_item.setFont(inactive_track_font_style)

    if alignment == 'left':
        list_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
    else:
        list_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
