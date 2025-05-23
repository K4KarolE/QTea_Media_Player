"""
    ThumbnailMainWindow(QScrollArea) << WidgetsWindow(QWidget) - Window holding the thumbnail widgets
    Used in the src / playlists / playlists_creation()
 """


from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QWidget,
    QScrollArea,
    QScrollBar
    )

from .class_bridge import br
from .class_data import cv
from .func_thumbnail import thumbnail_widget_resize_and_move_to_pos, save_thumbnail_history_json
from .thread_thumbnail import ThreadThumbnail


class ThumbnailMainWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        # setMinimumWidth declared in ui_create / ''' TOP RIGHT - PLAYLIST / BUTTONS / DURATION ''' section
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
        self.setStyleSheet("QScrollArea"
                           "{"
                           "background: white;"
                           "}"
                           )
        self.create_widgets_window()


    def create_widgets_window(self):
        self.widgets_window = WidgetsWindow()  # holding all the thumbnail widgets
        self.widgets_window.resize(self.width(), self.height())
        self.setWidget(self.widgets_window)


    def timer_action(self):
        # Timer: For avoiding multiple trigger from resizeEvent
        if self.isVisible():
            thumbnail_widget_resize_and_move_to_pos()
            self.setMinimumWidth(cv.thumbnail_width + cv.thumbnail_pos_base_x * 2 + cv.scroll_bar_size)
        self.timer.stop()

    def resizeEvent(self, a0):
        if cv.thumbnail_main_window_width != self.width():
            cv.thumbnail_main_window_width = self.width()
            cv.thumbnail_main_window_height = self.height()
            self.timer.start(500)
        return super().resizeEvent(a0)

    def scroll_to_current_item_active_pl(self):
        if cv.current_track_index != -1:
            thumbnail_widget = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic'][cv.current_track_index]['widget']
            self.scroll_bar_ver.setValue(thumbnail_widget.y() - cv.thumbnail_height)

    def scroll_to_current_item_playing_pl(self):
        thumbnail_widget_dic = cv.playlist_widget_dic[cv.playing_db_table]['thumbnail_widgets_dic']
        if thumbnail_widget_dic:
            thumbnail_widget = thumbnail_widget_dic[cv.playing_track_index]['widget']
            min_pos = self.scroll_bar_ver.value()
            max_pos = self.scroll_bar_ver.value() + br.playlists_all.height() - cv.thumbnail_height
            if not thumbnail_widget.y() in range(min_pos, max_pos):
                self.scroll_bar_ver.setValue(thumbnail_widget.y() - cv.thumbnail_height)



class WidgetsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(cv.window_width, cv.window_height)
        self.thread_thumbnails_update = ThreadThumbnail()
        self.thread_thumbnails_update.result_ready.connect(self.thumbnail_img_ready)
        self.setStyleSheet("QWidget"
                           "{"
                           "background: white;"
                           "}"
                           )

    def thumbnail_img_ready(self, index: int, result: str):
        thumbnail_widget = cv.playlist_widget_dic[cv.thumbnail_db_table]['thumbnail_widgets_dic'][index]["widget"]
        if result == "audio":
            thumbnail_widget.update_to_default_audio_img()
            thumbnail_widget.thumbnail_type = "audio"
        elif result == "failed":
            thumbnail_widget.update_to_default_video_img()
            thumbnail_widget.thumbnail_type = "video_failed"
        else:
            thumbnail_widget.update_img(result)
            thumbnail_widget.thumbnail_type = "video_completed" # not in use, yet

        if index > 0 and index % 20 == 0:
            save_thumbnail_history_json()