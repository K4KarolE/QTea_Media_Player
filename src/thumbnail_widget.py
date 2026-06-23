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
    clear_queue_update_for_current_playlist,
    open_track_folder_via_context_menu,
    play_track_with_default_player_via_context_menu,
    queue_add_remove_track,
    remove_track_from_playlist
    )
from .message_box import MyMessageBoxError


class ThumbnailWidget(QWidget):
    """
    A thumbnail widget represents one media (video, audio)
    It contains a square frame, an image, the title of the media and the queue number placeholder (or the number)
    Audio: thumbnail widget contains the default audio icon which not related to the audio file
    Video: thumbnail widget contains an image generated from the video if possible, if not, it holds the default
    video icon
    """
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
        self.text.setToolTip(label_text)
        self.text.setCursor(Qt.CursorShape.PointingHandCursor)
        # QUEUE NUMBER
        self.queue_number = QLabel('#')
        self.queue_number.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.layout.addWidget(self.queue_number, 1)
        self.layout.addWidget(self.label_image, 95)
        self.layout.addWidget(self.text, 2)
        self.setLayout(self.layout)
        self.set_default_thumbnail_style()
        # CONTEXT MENU
        # The "Play/Pause", and "Queue/Dequeue" titles and icons are generated in the "eventFilter()" below depend on
        # is the current track in the playing state or is the current track already queued
        self.context_menu_dic = {
            'Temp_play_pause_title': {'icon': None},
            'Temp_queue_dequeue_title': {'icon': None},
            'Clear queue': {'icon': br.icon.clear_queue},
            'Clear queue for this playlist only': {'icon': br.icon.clear_queue_current_playlist},
            'Remove': {'icon': br.icon.remove},
            'Open item`s folder': {'icon': br.icon.folder},
            'Play track with default player': {'icon': br.icon.start_with_default_player}
        }
        self.show()


    def is_current_track_playing(self):
        return (cv.active_db_table == cv.playing_db_table and
                cv.current_track_index == cv.playing_track_index and
                br.av_player.player.isPlaying())


    def eventFilter(self, source, event):
        """
        To compile the context menu, displayed once right-clicked on a thumbnail widget
        """
        if event.type() == QEvent.Type.ContextMenu:
            menu = QMenu()
            for menu_title, menu_icon in self.context_menu_dic.items():
                # Play / Pause
                if menu_title == 'Temp_play_pause_title':
                    if self.is_current_track_playing():
                        menu_title = 'Pause'
                        icon = br.icon.pause
                    else:
                        menu_title = 'Play'
                        icon = br.icon.start
                # Queue / Dequeue
                elif menu_title == 'Temp_queue_dequeue_title':
                    if self.is_queued:
                        menu_title = 'Dequeue'
                        icon = br.icon.de_queue
                    else:
                        menu_title = 'Queue'
                        icon = br.icon.queue_blue
                else:
                    icon = menu_icon['icon']
                menu.addAction(QAction(icon, menu_title, self))

            # Disable "Clear queue" when there is no queued track at all
            if not cv.queue_playlists_list:
                menu.actions()[2].setEnabled(False)

            # Disable "Clear queue for this playlist only"
            # when there is no queued track in the current playlist
            if cv.active_db_table not in cv.queue_playlists_list:
                menu.actions()[3].setEnabled(False)

            menu.triggered[QAction].connect(self.context_menu_clicked)
            menu.exec(event.globalPos())
        return super().eventFilter(source, event)


    def context_menu_clicked(self, q):
        """
        Context menu displayed once right-clicked on a thumbnail widget

        Why not to use "match-case" statement instead of "if/elif q.text() == list(self.context_menu_dic)[1]":
        The match-case statement does not allow indexing, instead of simple value comparisons.

        ERROR:
        match q.text()
            case list(self.context_menu_dic)[1]:    # [1] >> issue
                to_do

        WORKING, but losing the "match-case" syntax simplicity:
        match q.text()
            case x if x == list(self.context_menu_dic)[1]:      # x if x ==
                to_do
        """
        # PLAY
        if q.text() in ['Play', 'Pause']:
            try:
                # Switch between "Playing" and "Pause" states
                if cv.active_db_table == cv.playing_db_table and self.index == cv.playing_track_index:
                    br.button_play_pause.button_play_pause_clicked()
                # Start playing an inactive track
                else:
                    br.button_play_pause.button_play_pause_via_list()
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                )

        # QUEUE
        elif q.text() in ['Queue', 'Dequeue']:
            queue_add_remove_track()


        # CLEAR QUEUE
        elif q.text() == list(self.context_menu_dic)[2]:
            try:
                clear_queue_update_all_occurrences()
            except:
                MyMessageBoxError('Error', 'Sorry, something went wrong.')


        # CLEAR QUEUE FOR THE CURRENT PLAYLIST ONLY
        elif q.text() == list(self.context_menu_dic)[3]:
            try:
                clear_queue_update_for_current_playlist()
            except:
                MyMessageBoxError('Error', 'Sorry, something went wrong.')


        # REMOVE TRACK
        elif q.text() == list(self.context_menu_dic)[4]:
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
        elif q.text() == list(self.context_menu_dic)[5]:
            try:
                open_track_folder_via_context_menu(self.index, cv.active_db_table)
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                )

        # PLAY TRACK WITH DEFAULT PLAYER
        elif q.text() == list(self.context_menu_dic)[6]:
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
        """
        Thumbnail playlist change (new widget selected / double-clicked) >>
        standard playlist change >> thumbnail playlist style update
        via src / func_thumbnail / update_thumbnail_style_at_row_change
        """
        cv.active_pl_name.setCurrentRow(self.index)

    def mouseDoubleClickEvent(self, a0):
        """
        mousePressEvent() / setCurrentRow() + mouseDoubleClickEvent()
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

    def update_to_playing_default_img(self):
        """
        Till the thumbnail image is ready
        More info below at "set_playing_thumbnail_img()"
        """
        self.label_image.setPixmap(br.icon.thumbnail_backup)


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
        self.is_selected = False
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
        """
        Last option: thumbnail generation is still running and the thumbnail image
        is not created yet for the thumbnail widget which got double-clicked (track started playing)
        >> dummy icon set as thumbnail till the image is ready
        """
        if self.thumbnail_type == "audio":
            self.update_to_playing_audio_img()
        elif self.thumbnail_type == "video_failed":
            self.update_to_playing_video_img()
        elif not self.thumbnail_type:
            self.update_to_playing_default_img()