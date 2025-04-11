from pathlib import Path

from .class_data import cv
from .func_coll import cur as sql_cursor
from .thumbnail_widget import ThumbnailWidget


def get_all_playlist_path_from_db():
    result_all = sql_cursor.execute("SELECT * FROM {0}".format(cv.active_db_table)).fetchall()
    duration_list = [duration[1] for duration in result_all]
    path_list = [path[3] for path in result_all]
    return path_list, duration_list


def generate_thumbnail_dic():
    path_list, duration_list = get_all_playlist_path_from_db()
    if path_list:
        for index, path in enumerate(path_list):
            file_name = Path(path).name
            cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'][index] = {}
            cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'][index]["widget"] = ThumbnailWidget(file_name, index)
            cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'][index]["file_name"] = file_name
            cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'][index]["file_path"] = path
            cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'][index]["duration"] = duration_list[index]


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


def update_window_widgets_size(last_thumbnail_pos_y):
    window_widgets_height = last_thumbnail_pos_y + cv.thumbnail_height + cv.thumbnail_pos_base_y
    thumbnail_widgets_window = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window'].widgets_window
    thumbnail_widgets_window.resize(cv.thumbnail_main_window_width, window_widgets_height)


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


def thumbnail_grouped_action():
    generate_thumbnail_dic()
    thumbnail_widget_resize_and_move_to_pos()