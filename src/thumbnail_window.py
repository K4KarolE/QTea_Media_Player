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
from .func_thumbnail import (
    is_new_thumbnail_generation_necessary,
    is_track_index_inside_playlist,
    thumbnail_widget_resize_and_move_to_pos,
)
from .thread_thumbnail import ThreadThumbnail


class ThumbnailMainWindow(QScrollArea):
    def __init__(self, playlist):
        super().__init__()
        # setMinimumWidth declared in ui_create / ''' TOP RIGHT - PLAYLIST / BUTTONS / DURATION ''' section
        self.playlist = playlist
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
        self.widgets_window = None


    def create_widgets_window(self):
        """
        Widgets Window creation triggered by the Thumbnail view button
        button_thumbnail_clicked() / start_thumbnail_thread_grouped_action() /
        create_new_thumbnail_widgets_window()
        """
        self.widgets_window = WidgetsWindow(self.playlist)  # holding all the thumbnail widgets
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
        if (not is_new_thumbnail_generation_necessary(cv.active_db_table) and
                is_track_index_inside_playlist('active_pl', cv.current_track_index)):
            thumbnail_widget_dic = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic']
            thumbnail_widget = thumbnail_widget_dic[cv.current_track_index]['widget']
            self.scroll_bar_ver.setValue(thumbnail_widget.y() - cv.thumbnail_height)

    def scroll_to_current_item_playing_pl(self):
        """
        Scenario: playing next track on the playing playlist with thumbnail view
        while another playlist is active / in use >> go back to the playing playlist
        and the current playing track / thumbnail will be visible
        Can be really useful when the "Shuffle" play mode is on
        """
        if (not is_new_thumbnail_generation_necessary(cv.playing_db_table) and
                is_track_index_inside_playlist('playing_pl', cv.playing_track_index)):
            thumbnail_widget_dic = cv.playlist_widget_dic[cv.playing_db_table]['thumbnail_widgets_dic']
            thumbnail_widget = thumbnail_widget_dic[cv.playing_track_index]['widget']
            min_pos = self.scroll_bar_ver.value()
            max_pos = self.scroll_bar_ver.value() + br.playlists_all.height() - cv.thumbnail_height
            if not thumbnail_widget.y() in range(min_pos, max_pos):
                self.scroll_bar_ver.setValue(thumbnail_widget.y() - cv.thumbnail_height)



class WidgetsWindow(QWidget):
    def __init__(self, playlist):
        super().__init__()
        self.playlist = playlist
        self.resize(cv.window_width, cv.window_height)
        self.thread_thumbnails_update = ThreadThumbnail(self.playlist)
        self.thread_thumbnails_update.result_ready.connect(self.thumbnail_img_ready)
        self.setStyleSheet("QWidget"
                           "{"
                           "background: white;"
                           "}"
                           )

    def thumbnail_img_ready(self, index: int, result: str):
        """ Update the thumbnail widget with the generated image and the appropriate thumbnail style """
        if thumbnail_widget_dic := cv.playlist_widget_dic[self.playlist]['thumbnail_widgets_dic'].get(index):
            thumbnail_widget = thumbnail_widget_dic["widget"]
            if result == "audio":
                thumbnail_widget.update_to_default_audio_img()
                thumbnail_widget.thumbnail_type = "audio"
            elif result == "failed":
                thumbnail_widget.update_to_default_video_img()
                thumbnail_widget.thumbnail_type = "video_failed"
            else:
                thumbnail_widget.update_img(result)
                thumbnail_widget.thumbnail_type = "video_completed" # not in use, yet

            """ Updating playing and selected track style, thumbnail image
                The "failed" and "audio" validations are in the
                thumbnail_widget.set_ functions
            """
            # QUEUED
            if [self.playlist, index] in cv.queue_tracks_list:
                thumbnail_widget.set_queued_track_thumbnail_style()
                thumbnail_widget.is_queued = True
                queue_number = cv.queue_tracks_list.index([self.playlist, index]) + 1
                thumbnail_widget.set_queue_number(queue_number)

            # PLAYED
            if index == cv.thumbnail_last_played_track_index and index != cv.thumbnail_last_selected_track_index:
                if cv.playlist_widget_dic[cv.active_db_table]['played_thumbnail_style_update_needed']:
                    thumbnail_widget.set_playing_thumbnail_style()
                    thumbnail_widget.set_playing_thumbnail_img()

            # SELECTED
            if index == cv.thumbnail_last_selected_track_index:
                thumbnail_widget.set_selected_thumbnail_style()
                thumbnail_widget.set_default_thumbnail_img()
