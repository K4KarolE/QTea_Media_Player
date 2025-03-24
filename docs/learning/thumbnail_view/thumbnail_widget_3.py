"""
> Get the list of the specific playlist files from sql db
    > The track order is the same as in the app/playlist
> Generate thumbnail widgets with standard dummy icon
> Once double-clicked one of the thumbnails
    > Generate thumbnail images if needed
    > Update the thumbnail widgets with the thumbnail images
Note:
    > the used playlist should have video tracks added to ("playlist_n")
    > "path_thumbnails" should be existed/edited
"""

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

import sqlite3
import sys
import os
from pathlib import Path
from datetime import timedelta

playlist_n = "playlist_0"   # playlist_0 - playlist_29
path_thumbnails = '/BlackSweat/_DEV/test_vids/thumbnails'

class Data:
    window_width = 600
    window_height = 400
    thumbnail_img_size = 500
    widg_and_img_diff = 50
    thumbnail_width = thumbnail_img_size + widg_and_img_diff
    thumbnail_height = thumbnail_img_size + widg_and_img_diff
    thumbnail_new_width = thumbnail_width
    thumbnail_pos_gap = 1
    pos_base_x = 5
    pos_base_y = 5
    thumbnail_widget_dic = {}
    at_seconds_raw = 60 # time at the frame img will be taken from


QApplication.setDesktopSettingsAware(False) # avoid OS auto coloring

class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(cv.window_width, cv.window_height)
        self.setMinimumWidth(cv.thumbnail_width + cv.pos_base_x * 2)
        self.setWindowTitle("Thumbnails")
        self.timer = QTimer()
        self.timer.timeout.connect(lambda : self.timer_action())

    def timer_action(self):
        # Timer: For avoiding multiple trigger from resizeEvent
        thumbnail_widget_resize_and_move_to_pos()
        self.timer.stop()

    def resizeEvent(self, a0):
        if cv.window_width != self.width():
            cv.window_width = self.width()
            self.timer.start(500)
        return super().resizeEvent(a0)



class ThumbnailWidget(QWidget):
    def __init__(self, file_name):
        super().__init__()
        self.setParent(window)
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
        self.label_image_pixmap = QPixmap('../../../skins/default/window_icon.png')
        self.label_image.setPixmap(self.label_image_pixmap)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
            )
        self.text = QLabel(file_name)
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
        print("Clicked")
        self.setStyleSheet(f"background-color: pink;")

    def mouseDoubleClickEvent(self, a0):
        print("Double clicked")
        create_thumbnails_update_widgets()

    def update_img(self, file_path):
        self.label_image_pixmap = QPixmap(file_path)
        self.label_image.setPixmap(self.label_image_pixmap)



def get_all_playlist_path_from_db(playlist_n):
    connection = sqlite3.connect('/BlackSweat/_DEV/Python/QTea_Media_Player/playlist.db')
    sql_cursor = connection.cursor()
    result_list= [path[0] for path in sql_cursor.execute("SELECT path FROM {0}".format(playlist_n))]
    connection.close()
    return result_list


def generate_thumbnail_dic(playlist_n):
    path_list = get_all_playlist_path_from_db(playlist_n)
    if path_list:
        for index, path in enumerate(path_list):
            file_name = Path(path).name
            cv.thumbnail_widget_dic[index] = {}
            cv.thumbnail_widget_dic[index]["widget"] = ThumbnailWidget(file_name)
            cv.thumbnail_widget_dic[index]["vid_name"] = file_name
            cv.thumbnail_widget_dic[index]["vid_path"] = path


def create_thumbnails_update_widgets():
    if cv.thumbnail_widget_dic:
        for index in cv.thumbnail_widget_dic:
            thumbnail_img_name = f'{cv.thumbnail_widget_dic[index]["vid_name"]}.{cv.thumbnail_img_size}.jpg'
            thumbnail_img_path = Path(path_thumbnails, thumbnail_img_name)
            vid_path = cv.thumbnail_widget_dic[index]["vid_path"]
            if Path(thumbnail_img_path).is_file():
                cv.thumbnail_widget_dic[index]["widget"].update_img(str(thumbnail_img_path))
            else:
                at_seconds = timedelta(seconds=cv.at_seconds_raw)
                target_path = Path(path_thumbnails, thumbnail_img_name)
                ffmpeg_action = f'ffmpeg -ss {at_seconds} -i "{vid_path}" -vf "scale={cv.thumbnail_img_size}:{cv.thumbnail_img_size}:force_original_aspect_ratio=decrease" -vframes 1 "{target_path}"'
                os.system(ffmpeg_action)
                if Path(thumbnail_img_path).is_file():
                    cv.thumbnail_widget_dic[index]["widget"].update_img(str(thumbnail_img_path))


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


def generate_thumbnail_widget_new_width():
    available_space = cv.window_width - 2 * cv.pos_base_x + cv.thumbnail_pos_gap
    thumbnail_and_gap = cv.thumbnail_width + cv.thumbnail_pos_gap
    thumbnails_in_row_possible = int(available_space / thumbnail_and_gap)
    thumbnail_count = len(cv.thumbnail_widget_dic)
    if thumbnails_in_row_possible >= thumbnail_count:
        thumbnail_width_diff = int((available_space - thumbnail_count * thumbnail_and_gap) / thumbnail_count)
    else:
        thumbnail_width_diff = int((available_space - thumbnails_in_row_possible * thumbnail_and_gap) / thumbnails_in_row_possible)
    cv.thumbnail_new_width = cv.thumbnail_width + thumbnail_width_diff


cv = Data()
app = MyApp()
window = MyWindow()

generate_thumbnail_dic(playlist_n)
thumbnail_widget_resize_and_move_to_pos()

window.show()
sys.exit(app.exec())