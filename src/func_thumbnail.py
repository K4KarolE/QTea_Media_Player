from datetime import timedelta
from pathlib import Path
from time import time
import glob
import os

from .class_bridge import br
from .class_data import (
    cv,
    PATH_THUMBNAILS,
    thumbnail_history,
    save_thumbnail_history_json
    )
from .func_coll import cur as sql_cursor
from .thumbnail_widget import ThumbnailWidget
from .message_box import (
    MyMessageBoxConfirmation,
    MyMessageBoxConfReq,
    MyMessageBoxError
    )

current_time = int(time())

# THUMBNAIL PL
def get_all_playlist_path_from_db():
    result_all = sql_cursor.execute("SELECT * FROM {0}".format(cv.thumbnail_db_table)).fetchall()
    duration_list = [duration[1] for duration in result_all]
    path_list = [path[3] for path in result_all]
    return path_list, duration_list

# THUMBNAIL PL
def generate_thumbnail_dic():
    path_list, duration_list = get_all_playlist_path_from_db()
    if path_list:
        for index, path in enumerate(path_list):
            file_name = Path(path).name
            cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index] = {}
            cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index]["widget"] = ThumbnailWidget(file_name, index)
            cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index]["file_name"] = file_name
            cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index]["file_path"] = path
            cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index]["duration"] = duration_list[index]

        # Used to validate if a new thumbnail generation needed
        thumbnail_window_validation = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window_validation']
        thumbnail_window_validation['tracks_count'] = cv.active_pl_tracks_count
        thumbnail_window_validation['duration_sum'] = cv.active_pl_sum_duration
        thumbnail_window_validation['thumbnail_img_size'] = cv.thumbnail_img_size
        thumbnail_window_validation['thumbnail_generation_completed'] = False


        cv.thumbnail_widget_dic = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic']
        if cv.thumbnail_last_played_track_index_is_valid:
            cv.thumbnail_widget_last_played = cv.thumbnail_widget_dic[cv.thumbnail_last_played_track_index]['widget']
        if cv.thumbnail_last_selected_track_index_is_valid:
            cv.thumbnail_widget_last_selected = cv.thumbnail_widget_dic[cv.thumbnail_last_selected_track_index]['widget']

# BOTH PL
def thumbnail_widget_resize_and_move_to_pos():
    thumbnail_widget_dic = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic']
    if thumbnail_widget_dic:
        thumbnail_counter = 0
        thumbnail_pos_y = cv.thumbnail_pos_base_y
        generate_thumbnail_widget_new_width()

        for thumbnail_index in thumbnail_widget_dic:
            thumbnail_pos_x = cv.thumbnail_pos_base_x + thumbnail_counter * (cv.thumbnail_new_width + cv.thumbnail_pos_gap)
            # PLACE THUMBNAIL TO A NEW ROW IF NECESSARY
            if thumbnail_pos_x > cv.thumbnail_main_window_width - cv.thumbnail_width - cv.thumbnail_pos_base_x:
                thumbnail_counter = 0
                thumbnail_pos_x = cv.thumbnail_pos_base_x + thumbnail_counter * (cv.thumbnail_new_width + cv.thumbnail_pos_gap)
                thumbnail_pos_y += cv.thumbnail_height + cv.thumbnail_pos_gap
            thumbnail_widget_dic[thumbnail_index]["widget"].move(thumbnail_pos_x, thumbnail_pos_y)
            thumbnail_widget_dic[thumbnail_index]["widget"].resize(cv.thumbnail_new_width, cv.thumbnail_height)
            thumbnail_counter += 1

        update_window_widgets_size(thumbnail_pos_y)

# BOTH PL
def update_window_widgets_size(last_thumbnail_pos_y):
    window_widgets_height = last_thumbnail_pos_y + cv.thumbnail_height + cv.thumbnail_pos_base_y
    thumbnail_widgets_window = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window'].widgets_window
    thumbnail_widgets_window.resize(cv.thumbnail_main_window_width, window_widgets_height)

# BOTH PL
def generate_thumbnail_widget_new_width():
    available_space = cv.thumbnail_main_window_width - cv.scroll_bar_size - 2 * cv.thumbnail_pos_base_x + cv.thumbnail_pos_gap
    thumbnail_and_gap = cv.thumbnail_width + cv.thumbnail_pos_gap
    thumbnails_in_row_possible = int(available_space / thumbnail_and_gap)
    thumbnail_count = len(cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'])
    if thumbnails_in_row_possible >= thumbnail_count:
        thumbnail_width_diff = int((available_space - thumbnail_count * thumbnail_and_gap) / thumbnail_count)
    else:
        if thumbnails_in_row_possible:
            thumbnail_width_diff = int((available_space - thumbnails_in_row_possible * thumbnail_and_gap) / thumbnails_in_row_possible)
        else:
            thumbnail_width_diff = 0
    cv.thumbnail_new_width = cv.thumbnail_width + thumbnail_width_diff

# THUMBNAIL PL
def create_thumbnails_and_update_widgets(index):
    """ Triggered / used via thread
    ffmpeg: https://ffmpeg.org/ffmpeg.html
    -vf: video filter
    -n: skip existing files
    -loglevel error: only error messages displayed
    -frames:v number (output): Set the number of video frames to output.
    -ss position: when used as an input option (before -i), seeks in this input file to position.
    """
    vid_scale = f"-vf scale={cv.thumbnail_img_size}:{cv.thumbnail_img_size}:force_original_aspect_ratio=decrease"
    file_path = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index]["file_path"]
    # AUDIO
    if Path(file_path).suffix in ['.mp3', '.flac']:
        result = "audio"
    # VIDEO
    else:
        vid_duration = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index]["duration"]
        thumbnail_img_name = f'{cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index]["file_name"]}.{vid_duration}.{cv.thumbnail_img_size}.jpg'
        result = Path(PATH_THUMBNAILS, thumbnail_img_name)

        if thumbnail_img_name in thumbnail_history["completed"] or thumbnail_img_name in thumbnail_history["failed"]:
            if Path(result).is_file():
                thumbnail_history["completed"][thumbnail_img_name] = current_time
            else:
                thumbnail_history["failed"][thumbnail_img_name] = current_time
                result = "failed"
        else:
            at_seconds = get_time_frame_taken_from(vid_duration)
            target_path = Path(PATH_THUMBNAILS, thumbnail_img_name)
            ffmpeg_action = f'ffmpeg -n -loglevel error -ss {at_seconds} -i "{file_path}" {vid_scale} -frames:v 1 "{target_path}"'
            os.system(ffmpeg_action)
            if Path(result).is_file():
                thumbnail_history["completed"][thumbnail_img_name] = current_time
            else:
                thumbnail_history["failed"][thumbnail_img_name] = current_time
                result = "failed"
    return str(result)

# NONE
def get_time_frame_taken_from(vid_duration):
    if vid_duration:
        vid_duration = int(int(vid_duration)/1000)
        if 600 < vid_duration:
            at_seconds_raw = 140
        elif 30 < vid_duration <= 600:
            at_seconds_raw = 60
        else:
            at_seconds_raw = int(vid_duration/2)
    else:
        at_seconds_raw = 0
    return timedelta(seconds=at_seconds_raw)

# THUMBNAIL PL
def start_thumbnail_thread_grouped_action():
    if is_new_thumbnail_generation_needed():
        stop_another_playlist_thumbnail_thread()
        update_thumbnail_support_vars_before_thumbnail_thread()
        remove_thumbnail_widgets_window_and_thumbnail_dic()
        create_new_thumbnail_widgets_window()
        generate_thumbnail_dic()
        thumbnail_widget_resize_and_move_to_pos()
        # THREAD
        widgets_window = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window'].widgets_window
        widgets_window.thread_thumbnails_update.start()
        # THUMBNAIL STYLE
        update_thumbnail_style_after_thumbnail_generation()

# THUMBNAIL PL
def update_thumbnail_support_vars_before_thumbnail_thread():
    """ Once the thumbnail generation triggered,
        snapshot the crucial vars to make sure
        switching playlist is not causing any issue
        while the thumb. gen. is still in progress
    """
    cv.thumbnail_db_table = cv.active_db_table
    cv.thumbnail_pl_tracks_count = cv.active_pl_name.count()

    cv.thumbnail_last_played_track_index = cv.active_pl_last_track_index
    cv.thumbnail_last_played_track_index_is_valid = -1 < cv.thumbnail_last_played_track_index <=cv.thumbnail_pl_tracks_count-1

    cv.thumbnail_last_selected_track_index = cv.active_pl_name.currentRow()
    cv.thumbnail_last_selected_track_index_is_valid = -1 < cv.thumbnail_last_selected_track_index <=cv.thumbnail_pl_tracks_count-1

# ACTIVE PL
def update_thumbnail_support_vars_before_playlist_clear():
    """ When the playlist clear actioned the row change signal triggered
        earlier before the "cv.active_pl_name.count()" get the 0 value >>
        values have to be set manually >>
        avoid style update on deleted thumbnails
    """
    cv.active_pl_tracks_count = 0
    cv.current_track_index = -1
    cv.active_pl_last_track_index = -1
    cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'] = {}

# ACTIVE PL
def switch_to_standard_active_playlist_from_thumbnail_pl():
    if not cv.active_pl_name.isVisible():
        br.button_thumbnail.button_thumbnail_clicked()

# THUMBNAIL PL
def update_thumbnail_style_after_thumbnail_generation():
    widget_dic = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic']
    if widget_dic:
        # PLAYED TRACK
        if -1 < cv.thumbnail_last_played_track_index <= cv.thumbnail_pl_tracks_count-1:
            widget_dic[cv.thumbnail_last_played_track_index]['widget'].set_playing_thumbnail_style()
        # SELECTED TRACK
        if -1 < cv.thumbnail_last_selected_track_index <= cv.thumbnail_pl_tracks_count-1:
            widget_dic[cv.thumbnail_last_selected_track_index]['widget'].set_selected_thumbnail_style()

# ACTIVE PL
def is_new_thumbnail_generation_needed():
    """ The "thumbnail_generation_completed" value will be set True
        after a full completion of the thumbnail gen. thread.
        After an interrupted/stopped thumbnail gen. thread,
        it is triggered again at the next "thumbnail button" activation
    """
    thumbnail_window_validation = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window_validation']
    if cv.active_pl_name.count() == 0:
        return False
    elif not cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic']:
        return True
    elif (thumbnail_window_validation['tracks_count'] != cv.active_pl_tracks_count or
          thumbnail_window_validation['duration_sum'] != cv.active_pl_sum_duration or
          thumbnail_window_validation['thumbnail_img_size'] != cv.thumbnail_img_size or
          not thumbnail_window_validation['thumbnail_generation_completed']):
        thumbnail_window_validation['thumbnail_generation_completed'] = False
        return True
    else: return False

# THUMBNAIL PL
def stop_thumbnail_thread():
    if cv.thumbnail_db_table:
        widgets_window = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window'].widgets_window
        if widgets_window.thread_thumbnails_update.isRunning():
            widgets_window.thread_thumbnails_update.terminate()
            save_thumbnail_history_json()

# THUMBNAIL PL
def stop_another_playlist_thumbnail_thread():
    if cv.thumbnail_db_table:
        widgets_window = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window'].widgets_window
        if widgets_window.thread_thumbnails_update.isRunning() and cv.thumbnail_db_table != cv.active_db_table:
            widgets_window.thread_thumbnails_update.terminate()
            save_thumbnail_history_json()

# THUMBNAIL PL
def remove_thumbnail_widgets_window_and_thumbnail_dic():
    if cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window']:
        cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window'].widgets_window.deleteLater()
        cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'] = {}

# THUMBNAIL PL
def create_new_thumbnail_widgets_window():
    cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window'].create_widgets_window()

# ACTIVE PL
def thumbnail_repositioning_after_playlist_change():
    """ To make sure the active playlist thumbnail view
        is following the current playlist size
        Scenario:
            thumbnail view is generated > active playlist change > playlist size change
            > switch back to the playlist with thumbnail view > thumbnails resize & repositioning
        Used: src / playlists / currentChanged signal
    """
    thumbnail_widgets_dic = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic']
    if thumbnail_widgets_dic:
        thumbnail_main_window = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window']
        thumbnail_widgets_window = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window'].widgets_window
        if thumbnail_main_window.width() != thumbnail_widgets_window.width():
            thumbnail_widget_resize_and_move_to_pos()

# ACTIVE PL
def update_thumbnail_view_button_style_after_playlist_change():
    if cv.is_ffmpeg_installed:
        if cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window'].isVisible():
            br.button_thumbnail.set_style_thumbnail_button_active()
        else:
            br.button_thumbnail.set_style_settings_button()

# PLAYING PL
def update_playing_and_previous_thumbnail_style():
    """ Updating thumbnail style after new track is started """
    thumbnail_widget_dic = cv.playlist_widget_dic[cv.playing_db_table]['thumbnail_widgets_dic']
    if thumbnail_widget_dic:
        thumbnail_widget_dic[cv.playing_track_index]['widget'].set_playing_thumbnail_style()
        thumbnail_widget_dic[cv.playing_pl_last_track_index]['widget'].set_default_thumbnail_style()

# ACTIVE PL
def update_selected_and_played_and_previous_thumbnail_style():
    """ Updating thumbnail style after new track/row is selected
        Scenarios:
        - Standard playlist change >> thumbnail playlist style update
        - Thumbnail playlist change (new widget selected / double-clicked) >>
            standard playlist change >> thumbnail playlist style update
    """
    if not is_new_thumbnail_generation_needed():
        thumbnail_widget_dic = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic']
        # CURRENT
        thumbnail_widget_dic[cv.current_track_index]['widget'].set_selected_thumbnail_style()
        # PREVIOUS
        if -1 < cv.active_pl_last_selected_track_index <= cv.active_pl_tracks_count-1:
            thumbnail_widget_dic[cv.active_pl_last_selected_track_index]['widget'].set_default_thumbnail_style()
        # PLAYING
        if cv.playing_track_index <= cv.active_pl_tracks_count-1 and cv.playing_track_index != cv.current_track_index:
            thumbnail_widget_dic[cv.playing_track_index]['widget'].set_playing_thumbnail_style()
        update_last_selected_track_dic_and_vars()

# ACTIVE PL
def update_last_selected_track_dic_and_vars():
    cv.playlist_widget_dic[cv.active_db_table]['last_selected_track_index'] = cv.current_track_index
    cv.active_pl_last_selected_track_index = cv.current_track_index

# NONE
def remove_all_thumbnails_and_clear_history():
    stop_thumbnail_thread()
    switch_all_pl_to_standard_from_thumbnails_view(True)
    try:
        files = glob.glob(f'{PATH_THUMBNAILS}/*')
        for file in files:
            if Path(file).suffix != '.json':
                os.remove(file)
        thumbnail_history["failed"] = {}
        thumbnail_history["completed"] = {}
        save_thumbnail_history_json()
        MyMessageBoxConfirmation(
            'Thumbnails have been removed successfully.')
    except:
        MyMessageBoxError(
            'Settings Window',
            'Sorry, something went wrong.'
        )

# NONE
def msg_box_wrapper_for_remove_all_thumbnails_and_clear_history():
    MyMessageBoxConfReq(
        "Are you sure you want to delete all the thumbnails\n"
        "and clear the thumbnail history?",
        remove_all_thumbnails_and_clear_history,
        )

# NONE
def switch_all_pl_to_standard_from_thumbnails_view(triggered_via_purge_thumbnails_button = False):

    def switch_to_standard_pl(pl_name):
        if not cv.playlist_widget_dic[pl_name]['name_list_widget'].isVisible():
            cv.playlist_widget_dic[pl_name]['name_list_widget'].show()
            cv.playlist_widget_dic[pl_name]['queue_list_widget'].show()
            cv.playlist_widget_dic[pl_name]['duration_list_widget'].show()
            cv.playlist_widget_dic[pl_name]['thumbnail_window'].hide()

    switch_to_standard_active_playlist_from_thumbnail_pl() # to make sure thumbnail button is updated
    for pl_index, pl_name in enumerate(cv.playlist_widget_dic):
        # Triggered by settings window / Purge thumbnails button
        if triggered_via_purge_thumbnails_button:
            cv.playlist_widget_dic[pl_name]['thumbnail_window_validation']['thumbnail_generation_completed'] = False
            if pl_index not in cv.playlists_without_title_to_hide_index_list:
                switch_to_standard_pl(pl_name)
        # Triggered by settings window / Save button
        # To make sure all playlist will be hidden with the standard pl "visible"
        else:
            switch_to_standard_pl(pl_name)

#NONE
def auto_thumbnails_removal_after_app_closure():
    """ Auto thumbnail removal field validation in
        window_settings.py / general_fields_validation()
        cv.thumbnail_remove_older_than:
        0 - every day
        -1 = never
    """
    if cv.thumbnail_remove_older_than != -1:
        try:
            is_thumbnail_history_save_needed = False
            keep_for_days = cv.thumbnail_remove_older_than * 60*60*24
            remove_from_failed_list = []
            remove_from_completed_list = []

            # FAILED
            for img_name in thumbnail_history["failed"]:
                img_date = thumbnail_history["failed"][img_name]
                if img_date <= current_time - keep_for_days:
                    remove_from_failed_list.append(img_name)

            if remove_from_failed_list:
                for img_name in remove_from_failed_list:
                    thumbnail_history.pop(img_name)
                is_thumbnail_history_save_needed = True

            # COMPLETED
            for img_name in thumbnail_history["completed"]:
                img_date = thumbnail_history["completed"][img_name]
                if img_date <= current_time - keep_for_days:
                    remove_from_completed_list.append(img_name)

            if remove_from_completed_list:
                for img_name in remove_from_completed_list:
                    os.remove(Path(PATH_THUMBNAILS, img_name))
                    thumbnail_history["completed"].pop(img_name)
                is_thumbnail_history_save_needed = True

            if is_thumbnail_history_save_needed:
                save_thumbnail_history_json()

        except:
            MyMessageBoxError(
                'Thumbnail removal',
                'Sorry, something went wrong with the auto thumbnail removal.'
            )
