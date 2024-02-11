
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


'''
More info about the ACTIVE and PLAYING playlist
seperation in the src / cons_and_vars.py
'''
def update_active_playlist_vars_and_widgets():
    ''' Used / update values after playlist change '''
    cv.active_db_table = cv.paylist_list[cv.active_playlist_index] # cv.active_db_table = playlist_3 / playlist_1 /  ..
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
    ''' Used / update values after a track started in a new playlist '''
    cv.playing_db_table = cv.paylist_list[cv.playing_playlist_index] # cv.playing_db_table = playlist_4 / playlist_2, ..
    cv.playing_pl_title = settings[cv.playing_db_table]['playlist_title']
    cv.playing_pl_last_track_index = settings[cv.playing_db_table]['last_track_index']
    # LIST WIDGETS
    cv.playing_pl_name = cv.playlist_widget_dic[cv.playing_db_table]['name_list_widget']
    cv.playing_pl_queue = cv.playlist_widget_dic[cv.playing_db_table]['queue_list_widget']
    cv.playing_pl_duration = cv.playlist_widget_dic[cv.playing_db_table]['duration_list_widget']
    
    cv.playing_pl_tracks_count = cv.playing_pl_name.count()


def save_playing_playlist_and_playing_last_track_index():
    settings['playing_playlist'] = cv.active_playlist_index
    settings[cv.playing_db_table]['last_track_index'] = cv.playing_pl_last_track_index
    save_json(settings, PATH_JSON_SETTINGS)


def save_playing_pl_last_track_index():
    settings[cv.playing_db_table]['last_track_index'] = cv.playing_pl_last_track_index
    save_json(settings, PATH_JSON_SETTINGS)


def save_active_pl_last_track_index():
    settings[cv.active_db_table]['last_track_index'] = cv.active_pl_last_track_index
    save_json(settings, PATH_JSON_SETTINGS)


def place_record_into_db(duration, path):
    '''
    A DB record: row_id, duration, current_duration, path
    row_id populating automatically
    QListwidget list first index: 0 // SQLite DB first index: 1
    '''
    cur.execute("INSERT INTO {0}(duration, current_duration, path) VALUES (?, ?, ?)".format(cv.active_db_table), (duration, 0, str(path)))


def save_db():
    connection.commit()


def update_raw_current_duration_db(raw_current_duration, list_row_id):
    cur.execute("UPDATE {0} SET current_duration = {1} WHERE row_id = {2}".format(cv.playing_db_table, raw_current_duration, list_row_id+1))
    connection.commit()


def remove_record_db(list_row_id):
    cur.execute("DELETE FROM {0} WHERE row_id = ?".format(cv.active_db_table), (list_row_id+1,))
    cur.execute("UPDATE {0} SET row_id = row_id - 1 WHERE row_id > ?".format(cv.active_db_table), (list_row_id+1,) )
    connection.commit()


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
    ''' 
    Generating
    ----------- 
    - file path -> track name -> track name to display 
    - file path -> QMediaPlayer -> duration -> duration to display
                                            -> SUM all files duration
                                                in the playlist
    Other
    -------                                      
    - place file`s path and file`s duration to the DB
        - commit/save DB will actioned outside this function
    - add the values to the list widgets
        - the queue list widget value is just a placeholder           
    '''

    track_name = Path(track_path).stem
    av_player_duration.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    raw_duration = av_player_duration.player.duration()
    cv.active_pl_sum_duration += raw_duration
    cv.playlist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = cv.active_pl_sum_duration

    duration = generate_duration_to_display(raw_duration)
    place_record_into_db(raw_duration, track_path)

    row_id = cv.active_pl_name.count() + 1
    new_track_name = f'{row_id}. {track_name}'
    
    add_new_list_item(new_track_name, cv.active_pl_name)
    add_new_list_item('', cv.active_pl_queue)
    add_new_list_item(duration, cv.active_pl_duration)


def add_new_list_item(new_item, list_widget, align_center = None):
    list_item_size = QSize()
    list_item_size.setHeight(25)
    list_item_size.setWidth(0)

    list_item = QListWidgetItem(new_item, list_widget)
    list_item.setSizeHint(list_item_size)
    list_item_style_update(
        list_item,
        inactive_track_font_style,
        'black',
        'white')
    if align_center:
        list_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVertical_Mask)
    else:
        list_item.setTextAlignment(Qt.AlignmentFlag.AlignVertical_Mask)


def add_queue_window_list_widgets_header(new_item, list_widget):
    ''' Queue number | Title | Playlist | Duration '''
    list_item_size = QSize()
    list_item_size.setHeight(25)
    list_item_size.setWidth(0)

    list_item = QListWidgetItem(new_item, list_widget)
    list_item.setSizeHint(list_item_size)
    list_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVertical_Mask)
    list_item_style_update(
        list_item,
        inactive_track_font_style,
        'black',
        '#D5DFE2')    


def list_item_style_update(list_item, font_style, font_color, font_bg_color):
    list_item.setFont(font_style)   #QFont
    list_item.setForeground(QColor(font_color)) #'blue'
    list_item.setBackground(QColor(font_bg_color))


def update_and_save_volume_slider_value(new_value, slider):
    cv.volume = new_value
    slider.setValue(int(new_value*100))
    settings['volume'] = new_value
    save_json(settings, PATH_JSON_SETTINGS)


def save_volume_slider_value(new_value):
    cv.volume = new_value
    settings['volume'] = new_value
    save_json(settings, PATH_JSON_SETTINGS)


def update_duration_sum_var_after_track_remove():
    raw_duration = get_duration_db(cv.active_pl_name.currentRow(), cv.active_db_table)
    cv.active_pl_sum_duration -= raw_duration
    cv.playlist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = cv.active_pl_sum_duration


def queue_window_add_track():
    title_order_number = f'{str(cv.active_pl_name.currentRow() + 1)}.'
    title = cv.active_pl_name.currentItem().text().strip(title_order_number)
    duration = cv.active_pl_duration.currentItem().text()
    queue_number = f'{str(len(cv.queue_tracks_list))}.'
    add_new_list_item(queue_number, cv.queue_widget_dic['queue_list_widget']['list_widget'], True)
    add_new_list_item(title, cv.queue_widget_dic['name_list_widget']['list_widget'])
    add_new_list_item(cv.active_pl_title, cv.queue_widget_dic['playlist_list_widget']['list_widget'], True)
    add_new_list_item(duration, cv.queue_widget_dic['duration_list_widget']['list_widget'], True)


def queue_tab_add_track_from_search_tab(playlist, track_index, title):
    playlist_title = cv.playlist_widget_dic[playlist]['line_edit'].text()
    duration = cv.playlist_widget_dic[playlist]['duration_list_widget'].item(track_index).text()
    queue_number = f'{str(len(cv.queue_tracks_list))}.'
    add_new_list_item(queue_number, cv.queue_widget_dic['queue_list_widget']['list_widget'], True)
    add_new_list_item(title, cv.queue_widget_dic['name_list_widget']['list_widget'])
    add_new_list_item(playlist_title, cv.queue_widget_dic['playlist_list_widget']['list_widget'], True)
    add_new_list_item(duration, cv.queue_widget_dic['duration_list_widget']['list_widget'], True)


def queue_window_remove_track(current_queue_index):
    ''' +1: Queue playlist first row: Order Number, Title, Queue, Duration '''
    current_window_queue_index = current_queue_index + 1    
    for item in cv.queue_widget_dic:
        cv.queue_widget_dic[item]['list_widget'].takeItem(current_window_queue_index)
    
    queue_list_widget = cv.queue_widget_dic['queue_list_widget']['list_widget']
    for index in range(1, queue_list_widget.count()):
        queue_number = f'{index}.'
        queue_list_widget.item(index).setText(queue_number)


def queue_add_remove_track():
    ''' queue_tracking_title - unique value pair/list to track the queued records
        queue_tracking_title = [current playlist, current row/track index]
        queue_playlists_list = [queue_tracking_title 1, queue_tracking_title 2, ...]

        queue_playlists_list - collecting all the playlist where at least one track is queued
        queue_playlists_list = [playlist title 1, playlist title 2, ..]

        add record to queue -> queue_tracking_title generated -> added to the queue_playlists_list
                            -> current playlist added to the queue_playlists_list
                            -> queue list widget text/order number update
                            -> list widgets style update
    '''

    cv.queue_tracking_title = [cv.active_db_table, cv.current_track_index]

    ''' QUEUED TRACK '''
    if not cv.queue_tracking_title in cv.queue_tracks_list:

        cv.queue_tracks_list.append(cv.queue_tracking_title)
        cv.queue_playlists_list.append(cv.active_db_table)

        queue_order_number = f'[{len(cv.queue_tracks_list)}]'
        cv.active_pl_queue.item(cv.current_track_index).setText(queue_order_number)
        
        # AVOID UPDATING CURRENTLY PLAYING TRACK STYLE - ONLY QUEUE NUMBER UPDATE
        if cv.queue_tracking_title != [cv.playing_db_table, cv.playing_pl_last_track_index]:

            update_queued_track_style(cv.current_track_index)
        
        queue_window_add_track()
        
    
        ''' DEQUEUE / STANDARD TRACK '''
    else:
        current_queue_index = cv.queue_tracks_list.index(cv.queue_tracking_title)
        queue_window_remove_track(current_queue_index)
        cv.queue_tracks_list.remove(cv.queue_tracking_title)
        cv.queue_playlists_list.remove(cv.active_db_table)
        cv.active_pl_queue.item(cv.current_track_index).setText('')
        update_queued_tracks_order_number()

        if cv.current_track_index != cv.playing_pl_last_track_index:
        
            update_dequeued_track_style(cv.current_track_index)


def update_queued_track_style(current_track_index):
    for list_widget in cv.active_pl_list_widgets_list:
        list_item_style_update(
            list_widget.item(current_track_index), 
            inactive_track_font_style,
            'black',
            '#D5DFE2'
            )

def update_dequeued_track_style_from_queue_window(playlist, track_index):
    ''' Dequeued track in queue window -> update playlist '''
    for item in list(cv.playlist_widget_dic[playlist])[0:3]:
        list_widget = cv.playlist_widget_dic[playlist][item]
        list_item_style_update(
            list_widget.item(track_index), 
            inactive_track_font_style,
            'black',
            'white'
            )

def update_queued_track_style_from_search_tab(playlist, track_index):
    ''' Search tab - result -> add to queue -> update playlist '''
    for item in list(cv.playlist_widget_dic[playlist])[0:3]:
        list_widget = cv.playlist_widget_dic[playlist][item]
        list_item_style_update(
            list_widget.item(track_index), 
            inactive_track_font_style,
            'black',
            '#D5DFE2'
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


def update_queued_tracks_after_track_deletion():

    if cv.active_db_table in cv.queue_playlists_list:

        cv.queue_tracking_title = [cv.active_db_table, cv.current_track_index]

        # DELETING A QUEUED TRACK
        if cv.queue_tracking_title in cv.queue_tracks_list:
            current_queue_index = cv.queue_tracks_list.index(cv.queue_tracking_title)
            queue_window_remove_track(current_queue_index)

            cv.queue_tracks_list.remove(cv.queue_tracking_title)
            cv.queue_playlists_list.remove(cv.active_db_table)
            update_queued_tracks_order_number()
        
        # DELETING A TRACK ABOVE THE QUEUED TRACK(S)
        for item in cv.queue_tracks_list:   # item = [playlist_3, 6]
            if cv.active_db_table == item[0]:
                if cv.current_track_index < item[1]:
                    item[1] = item[1] - 1
        

def remove_queued_tracks_after_playlist_clear():

    if cv.active_db_table in cv.queue_playlists_list:

        queue_tracks_list_item_to_remove = []

        for item in cv.queue_tracks_list:   # item = [playlist_3, 6]
            if cv.active_db_table == item[0]:
                queue_tracks_list_item_to_remove.append(item)
    
        for item in queue_tracks_list_item_to_remove: 
            current_queue_index = cv.queue_tracks_list.index(item)
            queue_window_remove_track(current_queue_index)

            cv.queue_tracks_list.remove(item)
            cv.queue_playlists_list.remove(item[0])        
        
        update_queued_tracks_order_number()


def remove_track_from_playlist():
    '''
    Remove actioned via Remove Track button or right click in the playlist / menu / Remove
    -> new sum duration = sum duration - removed track`s duration
    -> update queue order numbers if the removed tracked was queued
    -> remove the track's list widget items(name, queue, duration)
    -> update track index values if necessary
    -> remove record from DB and update DB records row_id value where necessary
    -> rename the remaining track's name where necessary (13.MMMBop -> 12.MMMBop )
    '''

    update_duration_sum_var_after_track_remove()

    update_queued_tracks_after_track_deletion()
    
    current_row_index = cv.active_pl_name.currentRow()
    
    # PLAYLIST
    cv.active_pl_name.takeItem(current_row_index)
    cv.active_pl_queue.takeItem(current_row_index)
    cv.active_pl_duration.takeItem(current_row_index)
    # TRACK INDEX UPDATE
    if  cv.active_db_table == cv.playing_db_table:
        if current_row_index < cv.playing_pl_last_track_index:
            cv.playing_pl_last_track_index -= 1
            cv.active_pl_last_track_index -=1
            save_playing_pl_last_track_index()
        if current_row_index < cv.playing_track_index:
            cv.playing_track_index -= 1
    elif cv.active_db_table != cv.playing_db_table and current_row_index < cv.playing_pl_last_track_index:
        cv.active_pl_last_track_index -=1
        save_active_pl_last_track_index()
    # DB
    remove_record_db(current_row_index)
    # RENAME TRACKS' NAME
    row_id_db = current_row_index + 1
    cur.execute("SELECT * FROM {0} WHERE row_id >= ?".format(cv.active_db_table), (row_id_db,))
    playlist = cur.fetchall()
    for item in playlist:
        track_row_db, list_name, duration = generate_track_list_detail(item)
        cv.active_pl_name.item(track_row_db-1).setText(list_name)
    
    cv.active_pl_tracks_count = cv.active_pl_name.count()


def get_playlist_details_from_queue_tab_list(current_row_index):
    queue_tracking_title = cv.queue_tracks_list[current_row_index]
    playlist = queue_tracking_title[0]
    playlist_index = cv.paylist_list.index(playlist)
    track_index = queue_tracking_title[1]
    return playlist, playlist_index, track_index, queue_tracking_title


def get_playlist_details_from_seacrh_tab_list(current_row_index):
    playlist = cv.search_result_dic[current_row_index]['playlist'] 
    playlist_index = cv.paylist_list.index(playlist)
    track_index = cv.search_result_dic[current_row_index]['track_index']
    return playlist, playlist_index, track_index
