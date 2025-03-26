"""
> Get the list of the specific playlist files from sql db
    > The track order is the same as in the app/playlist
> Generate thumbnail widgets with standard dummy icon
> Generate thumbnail images if needed
> Update the thumbnail widgets with the thumbnail images
Note:
    > the used playlist should have video tracks added to ("playlist_n")
"""

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QScrollBar
    )

import sqlite3
import sys
import subprocess
import os
from pathlib import Path
from datetime import timedelta
from json import dump, load
from time import time

playlist_n = "playlist_0"   # playlist_0 - playlist_29
path_project = Path().resolve().parent.parent.parent
path_thumbnails = str(Path(path_project, 'thumbnails'))
current_time = int(time())
path_thumbnail_history = Path(path_thumbnails, '_thumbnail_history.json')


class Data:
    thumbnail_img_size = 300
    window_width = 1200
    window_height = 900
    widg_and_img_diff = 0
    thumbnail_width = thumbnail_img_size + widg_and_img_diff
    thumbnail_height = thumbnail_img_size + widg_and_img_diff
    thumbnail_new_width = thumbnail_width
    thumbnail_pos_gap = 1
    pos_base_x = 5
    pos_base_y = 5
    thumbnail_widget_dic = {}
    scroll_bar_size = 10


QApplication.setDesktopSettingsAware(False) # avoid OS auto coloring

class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)


class MainWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.resize(cv.window_width, cv.window_height)
        self.setMinimumWidth(cv.thumbnail_width + cv.pos_base_x * 2 + cv.scroll_bar_size)
        self.setWindowTitle("Thumbnails")
        self.timer = QTimer()
        self.timer.timeout.connect(lambda : self.timer_action())
        self.scroll_bar_ver = QScrollBar()
        self.scroll_bar_ver.setStyleSheet(
            "QScrollBar::vertical"
            "{"
            f"width: {cv.scroll_bar_size}px;"
            "}"
            )
        self.setVerticalScrollBar(self.scroll_bar_ver)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


    def timer_action(self):
        # Timer: For avoiding multiple trigger from resizeEvent
        thumbnail_widget_resize_and_move_to_pos()
        self.timer.stop()

    def resizeEvent(self, a0):
        if cv.window_width != self.width():
            cv.window_width = self.width()
            cv.window_height = self.height()
            self.timer.start(500)
        return super().resizeEvent(a0)


class WidgetsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(cv.window_width, cv.window_height)


class ThumbnailWidget(QWidget):
    def __init__(self, file_name, index):
        super().__init__()
        self.index = index
        self.setParent(window_widgets)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumWidth(cv.thumbnail_width)
        self.setStyleSheet(
            f"background-color: white;"
            "border: 1px solid grey;"
            "border-radius: 2px;"
            )
        self.layout = QVBoxLayout()
        self.label_image = QLabel()
        self.label_image_pixmap = QPixmap('../../../skins/default/window_icon.png').scaledToWidth(30, Qt.TransformationMode.SmoothTransformation)
        self.label_image.setPixmap(self.label_image_pixmap)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
            )
        label_text = f'{index + 1}.{file_name}'
        self.text = QLabel(label_text)
        self.text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.text.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
            "font: arial 11px;"
            "color: black;"  # text color
            # will be used after import from src/func_coll:
            # inactive_track_font_style.pointSize()
            # inactive_track_font_style.family()
            )
        self.layout.addWidget(self.label_image, 95)
        self.layout.addWidget(self.text, 5)
        self.setLayout(self.layout)

    def mousePressEvent(self, a0):
        self.setStyleSheet(f"background-color: light grey;")

    def mouseDoubleClickEvent(self, a0):
        file_dir_path = cv.thumbnail_widget_dic[self.index]["vid_path"]
        if sys.platform == 'linux':
            subprocess.Popen(["xdg-open", file_dir_path])
        else:
            subprocess.Popen(["explorer", file_dir_path])

    def update_img(self, file_path):
        self.label_image_pixmap = QPixmap(file_path)
        self.label_image.setPixmap(self.label_image_pixmap)



def open_thumbnail_history_json():
    with open(path_thumbnail_history) as f:
        json_dic = load(f)
    return json_dic

def save_thumbnail_history_json():
    with open(path_thumbnail_history, 'w') as f:
        dump(thumbnail_history, f, indent=2)
    return

thumbnail_history = open_thumbnail_history_json()


def get_all_playlist_path_from_db(playlist_n):
    connection = sqlite3.connect('../../../playlist.db')
    sql_cursor = connection.cursor()
    result_all = sql_cursor.execute("SELECT * FROM {0}".format(playlist_n)).fetchall()
    duration_list = [duration[1] for duration in result_all]
    path_list = [path[3] for path in result_all]
    connection.close()
    return path_list, duration_list


def generate_thumbnail_dic(playlist_n):
    path_list, duration_list = get_all_playlist_path_from_db(playlist_n)
    if path_list:
        for index, path in enumerate(path_list):
            file_name = Path(path).name
            cv.thumbnail_widget_dic[index] = {}
            cv.thumbnail_widget_dic[index]["widget"] = ThumbnailWidget(file_name, index)
            cv.thumbnail_widget_dic[index]["vid_name"] = file_name
            cv.thumbnail_widget_dic[index]["vid_path"] = path
            cv.thumbnail_widget_dic[index]["duration"] = duration_list[index]


def create_thumbnails_and_update_widgets():
    if cv.thumbnail_widget_dic:
        for index in cv.thumbnail_widget_dic:
            vid_path = cv.thumbnail_widget_dic[index]["vid_path"]
            vid_duration = cv.thumbnail_widget_dic[index]["duration"]
            thumbnail_img_name = f'{cv.thumbnail_widget_dic[index]["vid_name"]}.{vid_duration}.{cv.thumbnail_img_size}.jpg'
            thumbnail_img_path = Path(path_thumbnails, thumbnail_img_name)
            if thumbnail_img_name in thumbnail_history["completed"] or thumbnail_img_name in thumbnail_history["failed"]:
                if Path(thumbnail_img_path).is_file():
                    cv.thumbnail_widget_dic[index]["widget"].update_img(str(thumbnail_img_path))
                    thumbnail_history["completed"][thumbnail_img_name] = current_time
                else:
                    thumbnail_history["failed"][thumbnail_img_name] = current_time
            else:
                at_seconds = get_time_frame_taken_from(vid_duration)
                target_path = Path(path_thumbnails, thumbnail_img_name)
                ffmpeg_action = f'ffmpeg -ss {at_seconds} -i "{vid_path}" -vf "scale={cv.thumbnail_img_size}:{cv.thumbnail_img_size}:force_original_aspect_ratio=decrease" -vframes 1 "{target_path}"'
                os.system(ffmpeg_action)
                if Path(thumbnail_img_path).is_file():
                    cv.thumbnail_widget_dic[index]["widget"].update_img(str(thumbnail_img_path))
                    thumbnail_history["completed"][thumbnail_img_name] = current_time
                else:
                    thumbnail_history["failed"][thumbnail_img_name] = current_time
        save_thumbnail_history_json()


def get_time_frame_taken_from(vid_duration):
    if vid_duration:
        vid_duration = int(int(vid_duration)/1000)
        if 600 < vid_duration:
            at_seconds_raw = 120
        elif 30 < vid_duration <= 600:
            at_seconds_raw = 60
        else:
            at_seconds_raw = int(vid_duration/2)
    else:
        at_seconds_raw = 0
    return timedelta(seconds=at_seconds_raw)


def thumbnail_widget_resize_and_move_to_pos():
    if cv.thumbnail_widget_dic:
        thumbnail_counter = 0
        thumbnail_pos_y = cv.pos_base_y
        generate_thumbnail_widget_new_width()

        for thumbnail_index in cv.thumbnail_widget_dic:
            thumbnail_pos_x = cv.pos_base_x + thumbnail_counter * (cv.thumbnail_new_width + cv.thumbnail_pos_gap)
            # PLACE THUMBNAIL TO A NEW ROW IF NECESSARY
            if thumbnail_pos_x > cv.window_width - cv.thumbnail_width - cv.pos_base_x:
                thumbnail_counter = 0
                thumbnail_pos_x = cv.pos_base_x + thumbnail_counter * (cv.thumbnail_new_width + cv.thumbnail_pos_gap)
                thumbnail_pos_y += cv.thumbnail_height + cv.thumbnail_pos_gap
            cv.thumbnail_widget_dic[thumbnail_index]["widget"].move(thumbnail_pos_x, thumbnail_pos_y)
            cv.thumbnail_widget_dic[thumbnail_index]["widget"].resize(cv.thumbnail_new_width, cv.thumbnail_height)
            thumbnail_counter += 1

        update_window_widgets_size(thumbnail_pos_y)


def update_window_widgets_size(last_thumbnail_pos_y):
    window_widgets_height = last_thumbnail_pos_y + cv.thumbnail_height + cv.pos_base_y
    window_widgets.resize(cv.window_width, window_widgets_height)


def generate_thumbnail_widget_new_width():
    available_space = cv.window_width - cv.scroll_bar_size - 2 * cv.pos_base_x + cv.thumbnail_pos_gap
    thumbnail_and_gap = cv.thumbnail_width + cv.thumbnail_pos_gap
    thumbnails_in_row_possible = int(available_space / thumbnail_and_gap)
    thumbnail_count = len(cv.thumbnail_widget_dic)
    if thumbnails_in_row_possible >= thumbnail_count:
        thumbnail_width_diff = int((available_space - thumbnail_count * thumbnail_and_gap) / thumbnail_count)
    else:
        if thumbnails_in_row_possible:
            thumbnail_width_diff = int((available_space - thumbnails_in_row_possible * thumbnail_and_gap) / thumbnails_in_row_possible)
        else:
            thumbnail_width_diff = 0
    cv.thumbnail_new_width = cv.thumbnail_width + thumbnail_width_diff


cv = Data()
app = MyApp()
window_main = MainWindow()
window_widgets = WidgetsWindow()
window_main.setWidget(window_widgets)

generate_thumbnail_dic(playlist_n)
thumbnail_widget_resize_and_move_to_pos()
create_thumbnails_and_update_widgets()

window_main.show()
sys.exit(app.exec())