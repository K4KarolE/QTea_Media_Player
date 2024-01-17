
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QFont, QColor

from .cons_and_vars import Path, save_json
from .cons_and_vars import cv, settings, PATH_JSON_SETTINGS
import sqlite3

connection = sqlite3.connect('playlist.db')
cur = connection.cursor()
inactive_track_font_style = QFont('Arial', 11, 500)
active_track_font_style = QFont('Arial', 11, 600)


def active_utility():
    cv.active_db_table = cv.paylist_list[cv.active_tab] # playlist_1, playlist_2, ..
    cv.active_playlist_title = settings[cv.active_db_table]['tab_title']
    cv.last_track_index = settings[cv.active_db_table]['last_track_index']
    cv.active_pl_sum_duration = cv.paylist_widget_dic[cv.active_db_table]['active_pl_sum_duration']
    # LIST WIDGETS
    cv.active_pl_name = cv.paylist_widget_dic[cv.active_db_table]['name_list_widget']
    cv.active_pl_duration = cv.paylist_widget_dic[cv.active_db_table]['duration_list_widget']


def save_last_track_index():
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


def get_path_db(playing_track_index):
    return cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(cv.active_db_table),
                        (playing_track_index + 1,)).fetchall()[0][2]


def get_duration_db(playing_track_index):
    return int(cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(cv.active_db_table),
                           (playing_track_index + 1,)).fetchall()[0][1])


def generate_duration_to_display(raw_duration):

    try:
        # SECONDS
        float_seconds = float(raw_duration)/1000%60

        if float_seconds < 59:
            str_seconds = str(int(round(float_seconds, 0)))
        else:
            str_seconds = str(int(float_seconds))
        
        if len(str_seconds) == 1:
            seconds = f'0{str_seconds}'
        else:
            seconds = str_seconds[0:3]
        
        # MINUTES
        int_minutes = int(float(raw_duration)/60/1000)
        if len(str(int_minutes % 60)) == 1:
            minutes = f'0{str(int_minutes % 60)}'
        else:
            minutes = str(int_minutes % 60)


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

    cv.active_pl_sum_duration += raw_duration
    cv.paylist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = cv.active_pl_sum_duration

    duration = generate_duration_to_display(raw_duration)
    add_record_db(raw_duration, track_path)

    row_id = cv.active_pl_name.count() + 1
    track_name = f'{row_id}. {track_name}'
    
    add_new_list_item(track_name, cv.active_pl_name)
    add_new_list_item(duration, cv.active_pl_duration)


def add_new_list_item(new_item, list_widget):
    
    list_item_size = QSize()
    list_item_size.setHeight(25)
    list_item_size.setWidth(0)

    list_item = QListWidgetItem(new_item, list_widget)
    list_item.setSizeHint(list_item_size)
    list_item.setTextAlignment(Qt.AlignmentFlag.AlignVertical_Mask)
    list_item_style_update(
        list_item,
        inactive_track_font_style,
        'black',
        'white')    


def list_item_style_update(list_item, font_style, font_color, font_bg_color):
        list_item.setFont(font_style)   #QFont
        list_item.setForeground(QColor(font_color)) #'blue'
        list_item.setBackground(QColor(font_bg_color))


def update_and_save_volume_slider_value(new_value, slider):
    cv.volume = new_value
    slider.setValue(int(new_value*100))
    settings['volume'] = new_value
    save_json(settings, PATH_JSON_SETTINGS)


def update_duration_sum_var_after_track_remove():
    raw_duration = get_duration_db(cv.active_pl_name.currentRow())
    cv.active_pl_sum_duration -= raw_duration
    cv.paylist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = cv.active_pl_sum_duration
