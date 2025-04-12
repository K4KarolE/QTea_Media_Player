from datetime import timedelta
from pathlib import Path
from time import time
import glob
import os

from .class_data import (
    cv,
    PATH_THUMBNAILS,
    thumbnail_history,
    save_thumbnail_history_json
    )
from .func_coll import cur as sql_cursor
from .thumbnail_widget import ThumbnailWidget

current_time = int(time())

def get_all_playlist_path_from_db():
    result_all = sql_cursor.execute("SELECT * FROM {0}".format(cv.thumbnail_db_table)).fetchall()
    duration_list = [duration[1] for duration in result_all]
    path_list = [path[3] for path in result_all]
    return path_list, duration_list


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


def thumbnail_widget_resize_and_move_to_pos():
    thumbnail_widget_dic = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic']
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


def update_window_widgets_size(last_thumbnail_pos_y):
    window_widgets_height = last_thumbnail_pos_y + cv.thumbnail_height + cv.thumbnail_pos_base_y
    thumbnail_widgets_window = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window'].widgets_window
    thumbnail_widgets_window.resize(cv.thumbnail_main_window_width, window_widgets_height)


def generate_thumbnail_widget_new_width():
    available_space = cv.thumbnail_main_window_width - cv.scroll_bar_size - 2 * cv.thumbnail_pos_base_x + cv.thumbnail_pos_gap
    thumbnail_and_gap = cv.thumbnail_width + cv.thumbnail_pos_gap
    thumbnails_in_row_possible = int(available_space / thumbnail_and_gap)
    thumbnail_count = len(cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'])
    if thumbnails_in_row_possible >= thumbnail_count:
        thumbnail_width_diff = int((available_space - thumbnail_count * thumbnail_and_gap) / thumbnail_count)
    else:
        if thumbnails_in_row_possible:
            thumbnail_width_diff = int((available_space - thumbnails_in_row_possible * thumbnail_and_gap) / thumbnails_in_row_possible)
        else:
            thumbnail_width_diff = 0
    cv.thumbnail_new_width = cv.thumbnail_width + thumbnail_width_diff


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


def thumbnail_grouped_action():
    if is_new_thumbnail_generation_needed():
        remove_previous_and_create_new_thumbnail_widgets_window()
        generate_thumbnail_dic()
        thumbnail_widget_resize_and_move_to_pos()
        widgets_window = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_window'].widgets_window
        widgets_window.thread_thumbnails_update.start()


def is_new_thumbnail_generation_needed():
    thumbnail_window_validation = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window_validation']
    if (thumbnail_window_validation['tracks_count'] != cv.active_pl_tracks_count or
        thumbnail_window_validation['duration_sum'] != cv.active_pl_sum_duration or
        thumbnail_window_validation['thumbnail_img_size'] != cv.thumbnail_img_size
        ):
        cv.thumbnail_db_table = cv.active_db_table
        return True
    else: return False


def remove_previous_and_create_new_thumbnail_widgets_window():
    cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window'].widgets_window.deleteLater()
    cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'] = {}
    cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window_validation'] = {}
    cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window'].create_widgets_window()


def remove_all_thumbnails_and_history():
    files = glob.glob(f'{PATH_THUMBNAILS}/*')
    for file in files:
        if Path(file).suffix != '.json':
            os.remove(file)

    thumbnail_history["failed"] = {}
    thumbnail_history["completed"] = {}
    save_thumbnail_history_json()


