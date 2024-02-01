
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


def update_active_playlist_vars_and_widgets():
    cv.active_db_table = cv.paylist_list[cv.active_playlist] # playlist_1, playlist_2, ..
    cv.active_pl_title = settings[cv.active_db_table]['playlist_title']
    cv.active_pl_last_track_index = settings[cv.active_db_table]['last_track_index']
    cv.active_pl_sum_duration = cv.playlist_widget_dic[cv.active_db_table]['active_pl_sum_duration']
    # LIST WIDGETS
    cv.active_pl_name = cv.playlist_widget_dic[cv.active_db_table]['name_list_widget']
    cv.active_pl_queue = cv.playlist_widget_dic[cv.active_db_table]['queue_list_widget']
    cv.active_pl_duration = cv.playlist_widget_dic[cv.active_db_table]['duration_list_widget']
    cv.active_pl_tracks_count = cv.active_pl_name.count()
    cv.active_pl_list_widgets_list = [cv.active_pl_name, cv.active_pl_queue, cv.active_pl_duration]

def update_playing_playlist_vars_and_widgets():
    cv.playing_db_table = cv.paylist_list[cv.playing_playlist] # playlist_1, playlist_2, ..
    cv.playing_pl_title = settings[cv.playing_db_table]['playlist_title']
    cv.playing_pl_last_track_index = settings[cv.playing_db_table]['last_track_index']
    # LIST WIDGETS
    cv.playing_pl_name = cv.playlist_widget_dic[cv.playing_db_table]['name_list_widget']
    cv.playing_pl_queue = cv.playlist_widget_dic[cv.playing_db_table]['queue_list_widget']
    cv.playing_pl_duration = cv.playlist_widget_dic[cv.playing_db_table]['duration_list_widget']
    cv.playing_pl_tracks_count = cv.playing_pl_name.count()

def save_playing_playlist_and_playing_last_track_index():
    settings['playing_playlist'] = cv.active_playlist
    settings[cv.playing_db_table]['last_track_index'] = cv.playing_pl_last_track_index
    save_json(settings, PATH_JSON_SETTINGS)

def save_playing_last_track_index():
    settings[cv.playing_db_table]['last_track_index'] = cv.playing_pl_last_track_index
    save_json(settings, PATH_JSON_SETTINGS)

# A DB record: row_id, duration, path
# row_id populating automatically
# QListwidget list first index: 0 // SQLite DB first index: 1
def add_record_db(duration, path):
    cur.execute("INSERT INTO {0}(duration, current_duration, path) VALUES (?, ?, ?)".format(cv.active_db_table), (duration, 0, str(path)))
    connection.commit()


def update_raw_current_duration_db(raw_current_duration, list_row_id):
    cur.execute("UPDATE {0} SET current_duration = {1} WHERE row_id = {2}".format(cv.playing_db_table, raw_current_duration, list_row_id+1))
    connection.commit()


def remove_record_db(list_row_id):
    cur.execute("DELETE FROM {0} WHERE row_id = ?".format(cv.active_db_table), (list_row_id+1,))
    cur.execute("UPDATE {0} SET row_id = row_id - 1 WHERE row_id > ?".format(cv.active_db_table), (list_row_id+1,) )
    connection.commit()


def get_row_id_db(path):
    return cur.execute("SELECT row_id FROM {0} WHERE path = ?".format(cv.active_db_table), (str(path),)).fetchall()[-1][0] 
    # [-1][0]: adding same track multiple times --> row_id: picked the latest's one


def get_path_db(playing_track_index, db_table):
    return cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(db_table),
                        (playing_track_index + 1,)).fetchall()[0][3]


def get_duration_db(playing_track_index, db_table):
    return int(cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(db_table),
                           (playing_track_index + 1,)).fetchall()[0][1])


def get_all_from_db(playing_track_index, db_table):
    duration = int(cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(db_table),
                           (playing_track_index + 1,)).fetchall()[0][1])
    current_duration = int(cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(db_table),
                           (playing_track_index + 1,)).fetchall()[0][2])
    path = cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(db_table),
                           (playing_track_index + 1,)).fetchall()[0][3]
    
    return duration, current_duration, path


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
        print('ERROR - generate_duration_to_display(raw_duration)')

    return duration


def generate_track_list_detail(db_track_record):
    # [0]:row, [1]:duration, [2]:current_duration, [3]:path
    track_row_db = db_track_record[0]
    track_name = f'{db_track_record[0]}. {Path(db_track_record[3]).stem}'
    duration_to_display = generate_duration_to_display(db_track_record[1])
    return track_row_db, track_name, duration_to_display


def add_record_grouped_actions(track_path, av_player_duration):

    track_name = Path(track_path).stem
    av_player_duration.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    raw_duration = av_player_duration.player.duration()

    cv.active_pl_sum_duration += raw_duration
    cv.playlist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = cv.active_pl_sum_duration

    duration = generate_duration_to_display(raw_duration)
    add_record_db(raw_duration, track_path)

    row_id = cv.active_pl_name.count() + 1
    track_name = f'{row_id}. {track_name}'
    
    add_new_list_item(track_name, cv.active_pl_name)
    add_new_list_item('', cv.active_pl_queue)
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
    raw_duration = get_duration_db(cv.active_pl_name.currentRow(), cv.active_db_table)
    cv.active_pl_sum_duration -= raw_duration
    cv.playlist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = cv.active_pl_sum_duration



def queue_add_remove_track():

    cv.queue_tracking_title = [cv.active_db_table, cv.current_track_index]

    ''' QUEUED TRACK '''
    if not cv.queue_tracking_title in cv.queue_tracks_list:

        cv.queue_tracks_list.append(cv.queue_tracking_title)
        cv.queue_playlists_list.append(cv.active_db_table)

        queue_order_number = f'[{cv.queue_tracks_list.index(cv.queue_tracking_title) + 1}]'
        cv.active_pl_queue.item(cv.current_track_index).setText(queue_order_number)
        
        if cv.current_track_index != cv.playing_pl_last_track_index:

            update_queued_track_style(cv.current_track_index)
        
    
        ''' DEQUEUE / STANDARD TRACK '''
    else:

        cv.queue_tracks_list.remove(cv.queue_tracking_title)
        cv.queue_playlists_list.remove(cv.active_db_table)
        cv.active_pl_queue.item(cv.current_track_index).setText('')

        if cv.current_track_index != cv.playing_pl_last_track_index:
        
            update_dequeued_track_style(cv.current_track_index)


def update_queued_track_style(current_track_index):
    for list_widget in cv.active_pl_list_widgets_list:
        list_item_style_update(
            list_widget.item(current_track_index), 
            inactive_track_font_style,
            'black',
            '#C2C2C2'
            )


def update_dequeued_track_style(current_track_index):
    for list_widget in cv.active_pl_list_widgets_list:
        list_item_style_update(
            list_widget.item(current_track_index),
            inactive_track_font_style,
            'black',
            'white'
            )

def update_queued_tracks_order_number():
    for index, item in enumerate(cv.queue_tracks_list):
        playlist = item[0]
        track_index = item[1]
        queue_list_widget = cv.playlist_widget_dic[playlist]['queue_list_widget']
        queue_new_order_number = f'[{index + 1}]'
        queue_list_widget.item(track_index).setText(queue_new_order_number)

        
            


