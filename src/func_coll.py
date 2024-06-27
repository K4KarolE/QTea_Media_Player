
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QFont, QColor

from .cons_and_vars import save_json
from .cons_and_vars import cv, settings, PATH_JSON_SETTINGS
from .logging import logger_basic

import sqlite3
from pathlib import Path
import os

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


def walk_and_add_dir(dir_path, av_player_duration):
    ''' 
        Used to add a directory and all it`s files
        and subdirectories to the playlist and DB   
    '''
    error_path_list = []
    logger_basic('Adding directory: Loop - start')
    cv.adding_records_at_moment = True
    for dir_path_b, dir_names, file_names in os.walk(dir_path):
        for file in file_names:
            if file.split('.')[-1] in cv.MEDIA_FILES:   # music_title.mp3 -> mp3
                try:
                    add_record_grouped_actions(Path(dir_path_b, file), av_player_duration)
                except:
                    error_path_list.append(Path(dir_path_b, file))
        if error_path_list:
            for item in error_path_list:
                logger_basic(f'ERROR: {item}')

    cv.active_pl_tracks_count = cv.active_pl_name.count() # use the latest track amount
    
    try:
        save_db()
        logger_basic('Adding directory: DB Saved')
    except:
        logger_basic('ERROR: adding directory: Saving DB')
    
    cv.adding_records_at_moment = False


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
    '''
        When the function is used:
        If the `Continue playback` is enabled,
        every 5 seconds the duration of the currently
        playing track is saved, so the next startup
        the track can be played from them latest point*
        * = -(0-5) seconds
    '''
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
    - file path -> QMediaPlayer -> duration -> duration to display +
    SUM all files duration in the playlist
    
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
    '''
        Used to generate the queue playlist first row, titles of the columns:
        Order Number | Track title | Playlist | Duration
    '''
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
    if settings['is_speaker_muted']:
        settings['is_speaker_muted'] = False
    save_json(settings, PATH_JSON_SETTINGS)


def save_volume_slider_value(new_value):
    cv.volume = new_value
    settings['volume'] = new_value
    save_json(settings, PATH_JSON_SETTINGS)


def save_speaker_muted_value():
    settings['is_speaker_muted'] = cv.is_speaker_muted
    save_json(settings, PATH_JSON_SETTINGS)


def update_duration_sum_var_after_track_remove():
    raw_duration = get_duration_db(cv.active_pl_name.currentRow(), cv.active_db_table)
    cv.active_pl_sum_duration -= raw_duration
    cv.playlist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = cv.active_pl_sum_duration


def queue_window_add_track():
    ''' 
        On the (main window / any playlist) a track
        added to the queue --> track`s information populating
        on the Queue & Search window / Queue tab / queue list:
        Order Number | Track title | Playlist | Duration
    '''
    title_order_number = f'{str(cv.active_pl_name.currentRow() + 1)}.'
    title = cv.active_pl_name.currentItem().text().lstrip(title_order_number)
    duration = cv.active_pl_duration.currentItem().text()
    queue_number = f'{str(len(cv.queue_tracks_list))}.'
    add_new_list_item(queue_number, cv.queue_widget_dic['queue_list_widget']['list_widget'], True)
    add_new_list_item(title, cv.queue_widget_dic['name_list_widget']['list_widget'])
    add_new_list_item(cv.active_pl_title, cv.queue_widget_dic['playlist_list_widget']['list_widget'], True)
    add_new_list_item(duration, cv.queue_widget_dic['duration_list_widget']['list_widget'], True)


def queue_tab_add_track_from_search_tab(playlist, track_index, title):
    ''' 
        On the Queue & Search window / Search tab / search result 
        a track added to the queue --> track`s information
        populating on the Queue tab / queue list:
        Order Number | Track title | Playlist | Duration
    '''
    playlist_title = cv.playlist_widget_dic[playlist]['line_edit'].text()
    duration = cv.playlist_widget_dic[playlist]['duration_list_widget'].item(track_index).text()
    queue_number = f'{str(len(cv.queue_tracks_list))}.'
    add_new_list_item(queue_number, cv.queue_widget_dic['queue_list_widget']['list_widget'], True)
    add_new_list_item(title, cv.queue_widget_dic['name_list_widget']['list_widget'])
    add_new_list_item(playlist_title, cv.queue_widget_dic['playlist_list_widget']['list_widget'], True)
    add_new_list_item(duration, cv.queue_widget_dic['duration_list_widget']['list_widget'], True)


def queue_window_remove_track(current_queue_index):
    '''
        Remove de-queued track from the
        Queue & Search window / Queue tab / queue list
    
        +1: Queue playlist first row, titles of the columns:
        Order Number | Track title | Playlist | Duration
    '''
    current_window_queue_index = current_queue_index + 1    
    for item in cv.queue_widget_dic:
        cv.queue_widget_dic[item]['list_widget'].takeItem(current_window_queue_index)
    
    queue_list_widget = cv.queue_widget_dic['queue_list_widget']['list_widget']
    for index in range(1, queue_list_widget.count()):
        queue_number = f'{index}.'
        queue_list_widget.item(index).setText(queue_number)


def queue_add_remove_track():
    ''' queue_tracking_title - unique value pair/list to track the queued records
        queue_tracking_title = [current playlist, current row/track index] = [playlist_3, 6]
        queue_playlists_list = [queue_tracking_title 1, queue_tracking_title 2, ...]

        queue_playlists_list - collecting all the playlist where at least one track is queued
        queue_playlists_list = [playlist_5, playlist_2, ..]

        add record to queue -> queue_tracking_title generated -> added to the queue_playlists_list
                            -> current playlist added to the queue_playlists_list
                            -> queue list widget text/order number update
                            -> list widgets style update
    '''
    if cv.active_pl_name.currentItem():    # to avoid action on playlist where no track is selected
            
        cv.queue_tracking_title = [cv.active_db_table, cv.current_track_index]
        
        # STABDARD -> QUEUED TRACK
        if not cv.queue_tracking_title in cv.queue_tracks_list:

            cv.queue_tracks_list.append(cv.queue_tracking_title)
            cv.queue_playlists_list.append(cv.active_db_table)

            queue_order_number = f'[{len(cv.queue_tracks_list)}]'
            cv.active_pl_queue.item(cv.current_track_index).setText(queue_order_number)
            
            # AVOID UPDATING CURRENTLY PLAYING TRACK STYLE - ONLY QUEUE NUMBER UPDATE
            if cv.queue_tracking_title != [cv.playing_db_table, cv.playing_pl_last_track_index]:
                update_queued_track_style(cv.current_track_index)
            
            queue_window_add_track()
                   
        # QUEUED TRACK -> STANDARD
        else:
            current_queue_index = cv.queue_tracks_list.index(cv.queue_tracking_title)
            queue_window_remove_track(current_queue_index)
            cv.queue_tracks_list.remove(cv.queue_tracking_title)
            cv.queue_playlists_list.remove(cv.active_db_table)
            cv.active_pl_queue.item(cv.current_track_index).setText('')
            update_queued_tracks_order_number()

            if cv.current_track_index != cv.playing_pl_last_track_index:        
                update_dequeued_track_style(cv.current_track_index)
        
        search_result_queue_number_update()


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

def update_queued_tracks_order_number(clear_queue = False):
    for index, item in enumerate(cv.queue_tracks_list):
        playlist = item[0]
        track_index = item[1]
        queue_list_widget = cv.playlist_widget_dic[playlist]['queue_list_widget']
        if clear_queue:
            queue_new_order_number = ''
        else:
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
        # COLLECTING QUEUED TRACKS AFFACTED BY THE CLEAR
        queue_tracks_list_item_to_remove = []
        for tracking_title in cv.queue_tracks_list:   # tracking_title = [playlist_3, 6]
            
            playlist = tracking_title[0]

            if cv.active_db_table == playlist:
                queue_tracks_list_item_to_remove.append(tracking_title)

        # QUEUE TAB UPDATE
        for tracking_title in queue_tracks_list_item_to_remove:

            playlist = tracking_title[0]

            current_queue_index = cv.queue_tracks_list.index(tracking_title)
            queue_window_remove_track(current_queue_index)

            cv.queue_tracks_list.remove(tracking_title)
            cv.queue_playlists_list.remove(playlist)



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

    cv.track_change_on_main_playlist_new_search_needed = True


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


def search_result_queue_number_update():
    '''
    Paylists - queue/dequeue track --> Update the queue numbers in the Search tab
    - cv.queue_tracks_list = [[playlist_3, 4], [playlist_4, 2], ..]
    - playing a queued track: [2] 
        -> queue number update -> [2] to ''
        -> update the rest of the queue numbers: [1], . , <-[3], <-[4], ..
    
    Why seperate the queue, dequeue number update as below?
    - Dequeue: do not need to iterate through all the search results
    - At least the dequeue part is efficient
    '''
    def search_result_queued_tracks_index_list():
        queued_tracks_index_list = []
        for index in range(0, cv.search_queue_list_widget.count()):
            if cv.search_queue_list_widget.item(index).text() != '':
                queued_tracks_index_list.append(index)
        return queued_tracks_index_list
    
    if cv.search_result_dic:
        cv.search_result_queued_tracks_index_list = search_result_queued_tracks_index_list()
        index_for_remove_queue_number = cv.search_result_queued_tracks_index_list
        
        # DEQUEUE
        if len(cv.queue_tracks_list) < len(cv.search_result_queued_tracks_index_list):

            
            for tracking_title in cv.queue_tracks_list:

                for search_result_index in cv.search_result_queued_tracks_index_list:

                    playlist = cv.search_result_dic[search_result_index]['playlist']
                    track_index = cv.search_result_dic[search_result_index]['track_index']

                    if tracking_title == [playlist, track_index]:
                            
                            queue_number = f'[{cv.queue_tracks_list.index(tracking_title) + 1}]'
                            cv.search_queue_list_widget.item(search_result_index).setText(queue_number)
                            index_for_remove_queue_number.remove(search_result_index)
            
            if index_for_remove_queue_number:
                cv.search_queue_list_widget.item(index_for_remove_queue_number[0]).setText('')
                cv.search_result_queued_tracks_index_list.remove(index_for_remove_queue_number[0])
        
        # QUEUE
        else:
            cv.search_result_queued_tracks_index_list = []

            for tracking_title in cv.queue_tracks_list:

                for search_result_index in cv.search_result_dic:

                    playlist = cv.search_result_dic[search_result_index]['playlist']
                    track_index = cv.search_result_dic[search_result_index]['track_index']
                    
                    if tracking_title == [playlist, track_index]: 
                        queue_number = f'[{cv.queue_tracks_list.index(tracking_title) + 1}]'
                        cv.search_queue_list_widget.item(search_result_index).setText(queue_number)
                        cv.search_result_queued_tracks_index_list.append(search_result_index)



def clear_queue_update_all_occurrences():
    if cv.queue_tracks_list:
        # SEARCH TAB
        if cv.search_result_dic:
            for index in cv.search_result_dic:
                cv.search_queue_list_widget.item(index).setText('')
        cv.search_result_queued_tracks_index_list.clear()
        
        # QUEUE TAB
        for item in cv.queue_widget_dic:
            title = cv.queue_widget_dic[item]['list_widget_title']
            list_widget = cv.queue_widget_dic[item]['list_widget']
            list_widget.clear()
            add_queue_window_list_widgets_header(title, list_widget)
        
        # PLAYLISTS
        for track_title in cv.queue_tracks_list:
            playlist = track_title[0]
            track_index = track_title[1]
            update_dequeued_track_style_from_queue_window(playlist, track_index)

        update_queued_tracks_order_number(clear_queue = True)
        cv.queue_tracks_list.clear()
        cv.queue_playlists_list.clear()

def update_window_size_vars_from_saved_values():
    cv.window_width = settings['general_settings']['window_width']
    cv.window_height = settings['general_settings']['window_height']
    cv.window_alt_width = settings['general_settings']['window_alt_width']
    cv.window_alt_height = settings['general_settings']['window_alt_height']
    cv.window_second_alt_width = settings['general_settings']['window_second_alt_width']
    cv.window_second_alt_height = settings['general_settings']['window_second_alt_height']