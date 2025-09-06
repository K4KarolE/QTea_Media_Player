from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QMenu,
    QVBoxLayout,
    QWidget
    )

from .class_data import cv
from .class_bridge import br
from .func_coll import (
    active_track_font_style,
    inactive_track_font_style,
    clear_queue_update_all_occurrences,
    open_track_folder_via_context_menu,
    play_track_with_default_player_via_context_menu,
    queue_add_remove_track,
    remove_track_from_playlist
    )
from .message_box import MyMessageBoxError


class ThumbnailWidget(QWidget):
    def __init__(self, file_name, index):
        super().__init__()
        self.index = index
        self.is_selected = False
        self.is_playing = False
        self.is_queued = False
        self.thumbnail_type = None
        self.setParent(cv.playlist_widget_dic[cv.thumbnail_db_table]["thumbnail_window"].widgets_window)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumWidth(cv.thumbnail_width)
        self.installEventFilter(self)
        self.layout = QVBoxLayout()
        # IMAGE
        self.label_image = QLabel()
        self.label_image.setPixmap(br.icon.thumbnail_default)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # TITLE
        label_text = f'{index + 1}.{file_name}'
        self.text = QLabel(label_text)
        self.text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        # QUEUE NUMBER
        self.queue_number = QLabel('#')
        self.queue_number.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.layout.addWidget(self.queue_number, 1)
        self.layout.addWidget(self.label_image, 95)
        self.layout.addWidget(self.text, 2)
        self.setLayout(self.layout)
        self.set_default_thumbnail_style()
        self.context_menu_dic = {
            'Play / Pause': {'icon': br.icon.start},
            'Queue / Dequeue': {'icon': br.icon.queue_blue},
            'Clear queue': {'icon': br.icon.clear_queue},
            'Remove': {'icon': br.icon.remove},
            'Open item`s folder': {'icon': br.icon.folder},
            'Play track with default player': {'icon': br.icon.start_with_default_player}
        }
        self.show()


    def eventFilter(self, source, event):
        """ ContextMenu triggered by the right click
            on the thumbnail widget
        """
        if event.type() == QEvent.Type.ContextMenu:
            menu = QMenu()
            for menu_title, menu_icon in self.context_menu_dic.items():
                icon = menu_icon['icon']
                menu.addAction(QAction(icon, menu_title, self))
            menu.triggered[QAction].connect(self.context_menu_clicked)
            menu.exec(event.globalPos())
        return super().eventFilter(source, event)


    def context_menu_clicked(self, q):
        # PLAY
        if q.text() == list(self.context_menu_dic)[0]:
            try:
                if self.index == cv.playing_track_index:
                    br.button_play_pause.button_play_pause_clicked()
                else:
                    br.button_play_pause.button_play_pause_via_list()
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                )

        # QUEUE
        elif q.text() == list(self.context_menu_dic)[1]:
            queue_add_remove_track()


        # CLEAR QUEUE
        elif q.text() == list(self.context_menu_dic)[2]:
            try:
                clear_queue_update_all_occurrences()
            except:
                MyMessageBoxError('Error', 'Sorry, something went wrong.')

        # REMOVE TRACK
        elif q.text() == list(self.context_menu_dic)[3]:
            try:
                if self.index == cv.playing_track_index:
                    cv.playlist_widget_dic[cv.active_db_table]['played_thumbnail_style_update_needed'] = False
                remove_track_from_playlist()
                self.deleteLater()
                self.remove_thumbnail_track_grouped()
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                )

        # FOLDER
        elif q.text() == list(self.context_menu_dic)[4]:
            try:
                open_track_folder_via_context_menu(self.index, cv.active_db_table)
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                )

        # PLAY TRACK WITH DEFAULT PLAYER
        elif q.text() == list(self.context_menu_dic)[5]:
            try:
                play_track_with_default_player_via_context_menu(self.index, cv.active_db_table)
            except:
                MyMessageBoxError(
                    'Not able to play the file',
                    'The file or the file`s home folder has been renamed / removed.  '
                )

    def remove_thumbnail_track_grouped(self):
        thumbnail_widgets_dic = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic']
        for index in range(self.index, cv.active_pl_tracks_count):
            # Get and set the title from the standard playlist
            new_title = cv.active_pl_name.item(index).text()
            thumbnail_widgets_dic[index + 1]['widget'].index = index
            thumbnail_widgets_dic[index + 1]['widget'].text.setText(new_title)
            # Renaming the keys of the dict. - moving down the elements
            # to make sure there are no gaps in the dict. keys
            thumbnail_widgets_dic[index] = thumbnail_widgets_dic.pop(index + 1)
        cv.thumbnail_widget_resize_and_move_to_pos_func_holder()

    def mousePressEvent(self, a0):
        """ Thumbnail playlist change (new widget selected / double-clicked) >>
            standard playlist change >> thumbnail playlist style update
            via src / func_thumbnail / update_thumbnail_style_at_row_change
        """
        cv.active_pl_name.setCurrentRow(self.index)

    def mouseDoubleClickEvent(self, a0):
        """ mousePressEvent() / setCurrentRow() + mouseDoubleClickEvent()
            >> using the standard playlist to play the track via thumbnail
        """
        br.button_play_pause.button_play_pause_via_list()

    def update_img(self, img_file_path):
        self.label_image.setPixmap(QPixmap(img_file_path))

    def update_to_default_video_img(self):
        self.label_image.setPixmap(br.icon.thumbnail_default_video)

    def update_to_playing_video_img(self):
        self.label_image.setPixmap(br.icon.thumbnail_playing_video)

    def update_to_default_audio_img(self):
        self.label_image.setPixmap(br.icon.thumbnail_default_audio)

    def update_to_playing_audio_img(self):
        self.label_image.setPixmap(br.icon.thumbnail_playing_audio)


    def set_default_thumbnail_style(self):
        self.is_selected = False
        self.is_playing = False
        self.is_queued = False
        self.set_default_thumbnail_img()
        self.setStyleSheet(
            "background-color: white;"
            "border: 1px solid grey;"
            "border-radius: 2px;"
        )
        self.label_image.setStyleSheet("border: None;")
        self.set_text_style(self.text, 'inactive', 'black')
        self.set_text_style(self.queue_number, 'inactive', 'black')


    def set_selected_thumbnail_style(self):
        self.is_selected = True
        self.set_default_thumbnail_img()
        self.setStyleSheet(
            "background-color: #CCE8FF;"
            "border: 1px solid grey;"
            "border-radius: 2px;"
        )
        self.set_text_style(self.text, 'inactive', 'black')
        self.set_text_style(self.queue_number, 'inactive', 'black')


    def set_queued_track_thumbnail_style(self):
        self.is_queued = True
        self.setStyleSheet("background-color: #2b2b2b;")
        self.set_text_style(self.text, 'active', 'white')
        self.set_text_style(self.queue_number, 'active', 'white')

    def set_queue_number(self, queue_number = None):
        if queue_number:
            self.queue_number.setText(f'[ {queue_number} ]')
        else:
            self.queue_number.setText('#')


    def set_playing_thumbnail_style(self):
        self.is_playing = True
        self.set_playing_thumbnail_img()
        self.setStyleSheet(
            "background-color: #287DCC;"
            "border: 2px solid grey;"
            "border-radius: 2px;"
        )
        self.set_text_style(self.text, 'active', 'white')
        self.set_text_style(self.queue_number, 'active', 'white')


    def set_text_style(self, widget, font_style: str, font_color: str):
        if font_style == 'active':
            widget.setFont(active_track_font_style)
        else:
            widget.setFont(inactive_track_font_style)
        widget.setStyleSheet(
            "border: None;"
            f"color: {font_color};"
        )


    def set_default_thumbnail_img(self):
        if self.thumbnail_type == "audio":
            self.update_to_default_audio_img()
        elif self.thumbnail_type == "video_failed":
            self.update_to_default_video_img()

    def set_playing_thumbnail_img(self):
        if self.thumbnail_type == "audio":
            self.update_to_playing_audio_img()
        elif self.thumbnail_type == "video_failed":
            self.update_to_playing_video_img()