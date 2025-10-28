from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication, QWidget

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    add_media_grouped_actions,
    disable_minimal_interface,
    queue_add_remove_track,
    toggle_minimal_interface,
    update_and_save_volume_slider_value,
    update_window_size_vars_from_saved_values
    )
from .func_thumbnail import (
    auto_thumbnails_removal_after_app_closure,
    switch_to_standard_active_playlist_from_thumbnail_pl
    )
from .thread_add_media import ThreadAddMedia



class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(cv.window_width, cv.window_height)
        self.setMinimumSize(cv.window_min_width, cv.window_min_height)
        self.setWindowIcon(br.icon.window_icon)
        self.setWindowTitle("QTea Media Player")
        self.setAcceptDrops(True)  # for the external file, dictionary drag&drop
        if cv.always_on_top:
            self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.hotkeys_creation()
        self.move_window_to_middle()
        self.thread_add_media = ThreadAddMedia()
        self.thread_add_media.result_ready.connect(self.add_track_to_playlist_via_thread)


    def add_track_to_playlist_via_thread(self, track_path, raw_duration):
        add_media_grouped_actions(track_path, raw_duration)


    def hotkeys_creation(self):
        hotkeys_action_dic = {
        'small_jump_backward': lambda:self.jump_action(cv.small_jump, 'backward'),
        'small_jump_forward': lambda: self.jump_action(cv.small_jump, 'forward'),
        'medium_jump_backward': lambda:self.jump_action(cv.medium_jump, 'backward'),
        'medium_jump_forward': lambda:self.jump_action(cv.medium_jump, 'forward'),
        'big_jump_backward':  lambda:self.jump_action(cv.big_jump, 'backward'),
        'big_jump_forward':  lambda:self.jump_action(cv.big_jump, 'forward'),
        'display_track_info_on_video': lambda: br.av_player.text_display_on_video(
                2000,
                f'{cv.track_title}\n'
                f'{cv.playing_track_index + 1} / {cv.playing_pl_name.count()}\n'
                f'{self.get_current_duration_info()}'),
        'volume_mute': lambda: br.button_speaker.button_speaker_clicked(),
        'volume_up': self.volume_up_action,
        'volume_down': self.volume_down_action,
        'audio_tracks_rotate': lambda: br.play_funcs.audio_tracks_play_next_one(),
        'subtitle_tracks_rotate': lambda: br.play_funcs.subtitle_tracks_play_next_one(),
        'play_pause': lambda: br.button_play_pause.button_play_pause_clicked(),
        'play': lambda: br.play_funcs.play_track(), # play_pause vs. play: info in readme
        'stop': lambda: br.button_stop.button_stop_clicked(),
        'previous_track': lambda: br.button_prev_track.button_prev_track_clicked(),
        'next_track': lambda: br.button_next_track.button_next_track_clicked(),
        'repeat_track_playlist_toggle': lambda: br.button_toggle_repeat_pl.button_toggle_repeat_pl_clicked(),
        'shuffle_playlist_toggle': lambda: br.button_toggle_shuffle_pl.button_toggle_shuffle_pl_clicked(),
        'full_screen_toggle': lambda: br.av_player.full_screen_onoff_toggle(),
        'playlist_toggle': lambda: br.button_toggle_playlist.button_toggle_playlist_clicked(),
        'video_toggle': lambda: br.button_toggle_video.button_toggle_video_clicked(),
        'window_size_toggle': self.window_size_toggle_action,
        'playlist_add_track': lambda: br.button_add_track.button_add_track_clicked(),
        'playlist_add_directory': lambda: br.button_add_dir.button_add_dir_clicked(),
        'playlist_remove_track': lambda: br.button_remove_track.button_remove_single_track(),
        'playlist_remove_all_track': lambda: br.button_remove_all_track.button_remove_all_track(),
        'playlist_select_prev_pl': self.playlist_select_prev_pl_action,
        'playlist_select_next_pl': self.playlist_select_next_pl_action,
        'queue_toggle': lambda: queue_add_remove_track(),
        'queue_window': lambda: br.window_queue_and_search.show_queue_tab(),
        'search_window': lambda: br.window_queue_and_search.show_search_tab(),
        'minimal_interface_toggle': lambda: toggle_minimal_interface()
        }

        for index, hotkey in enumerate(cv.hotkeys_list):
            hotkey_value_raw = cv.hotkey_settings_dic[hotkey]['value']
            if "|" in hotkey_value_raw: # multiple hotkeys for the same action
                for hotkey_value in hotkey_value_raw.split("|"):
                    hotkey_value = hotkey_value.strip()
                    self.hotkey_allocation(hotkeys_action_dic, hotkey_value, index)
            else: self.hotkey_allocation(hotkeys_action_dic, hotkey_value_raw, index)

        self.add_escape_key_for_disable_minimal_interface()


    def hotkey_allocation(self, hotkeys_action_dic, hotkey_value, index):
        if hotkey_value != 'Enter':
            hotkey = QShortcut(QKeySequence(hotkey_value), self)
            hotkey.setContext(Qt.ShortcutContext.ApplicationShortcut)
            hotkey.activated.connect(hotkeys_action_dic[cv.hotkeys_list[index]])
        else:
            ''' Make sure both enter keys(standard and return(numpad)) are in sync
                and the enter hotkey as "start track" only works in the main window
                -> be able to use it in the search window
            '''
            hotkey = QShortcut(QKeySequence(hotkey_value), self)
            hotkey.setContext(Qt.ShortcutContext.WindowShortcut)
            hotkey.activated.connect(hotkeys_action_dic[cv.hotkeys_list[index]])
            # Return
            hotkey = QShortcut(QKeySequence('Return'), self)
            hotkey.setContext(Qt.ShortcutContext.WindowShortcut)
            hotkey.activated.connect(hotkeys_action_dic[cv.hotkeys_list[index]])


    def add_escape_key_for_disable_minimal_interface(self):
        """ To avoid: Video played with minimal interface,
            next track, audio only, played automatically
            >> minimal interface mode is still on
            >> there is no control available
        """
        hotkey = QShortcut(QKeySequence('Escape'), self)
        hotkey.setContext(Qt.ShortcutContext.WindowShortcut)
        hotkey.activated.connect(disable_minimal_interface)


    def closeEvent(self, a0):
        auto_thumbnails_removal_after_app_closure()

    '''
        DRAG/DROP FILES, FOLDERS ON THE PLAYLISTS

        The list widget items internal movement(drag/drop) defined in src / playlist.py
        Could not use the below event management in the
        src / list_widget_playlist.py / list widget class creation
        because the internal and external drag/drop actions interfered

        Thank you Jie Jenn:
        https://youtu.be/KVEIW2htw0A?si=9XDIMz_2OfIjSRFQ
    '''
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            switch_to_standard_active_playlist_from_thumbnail_pl()
            br.window.thread_add_media.source = event.mimeData().urls()
            br.window.thread_add_media.start()


    def get_current_duration_info(self):
        """ Example: 54%  -  11:11 / 20:25 """
        return (f'{int(br.av_player.player.position() / cv.track_full_duration * 100)}%'
                f'  -  {cv.duration_to_display_straight}')

    def jump_action(self, jump_size: int, direction: str):
        if direction == 'backward':
            new_pos = br.av_player.player.position() + jump_size * -1
        else:
            new_pos = br.av_player.player.position() + jump_size
        br.av_player.player.setPosition(new_pos)
        br.av_player.text_display_on_video(1000, self.get_current_duration_info()),


    ''' 
        VOLUME CHANGE CAN BE TRIGGERED BY:
        - Shortcut key
        - Volume slider
        - Scroll wheel over video screen when available
        >> which will update the volume slider
        >> which will update the volume
        --------------------------------------

        TO DISPLAY THE VOLUME CHANGE ON THE VIDEO SCREEN:
        When volume in (0< <100): 
            src/sliders/MyVolumeSlider/update_volume()
    
        When volume is already 0 or 100 and user tries
        to go beyond, below:
            volume_up_action() / volume_down_action()
    '''
    def volume_up_action(self):
        if cv.volume < 1:
            cv.volume = cv.volume + 0.05
            if cv.volume > 1:
                cv.volume = 1
            self.volume_update()
        elif cv.volume == 1:
            br.av_player.text_display_on_video(1000, "Volume:  100%")


    def volume_down_action(self):
        if cv.volume > 0:
            cv.volume = cv.volume - 0.05
            if cv.volume < 0:
                cv.volume = 0
            self.volume_update()
        elif cv.volume == 0:
            br.av_player.text_display_on_video(1000, "Volume:  0%")


    def volume_update(self):
        new_volume = round(cv.volume, 4)
        br.av_player.audio_output.setVolume(new_volume)
        br.button_speaker.button_speaker_update()
        update_and_save_volume_slider_value(new_volume)


    def generate_window_middle_position(self):
        current_screen = QApplication.screenAt(self.pos())
        screen_rect = current_screen.availableGeometry()
        pos_x = screen_rect.x() + int((screen_rect.width() - self.width()) / 2)
        pos_y = screen_rect.y() + int((screen_rect.height() - self.height()) / 2)
        return screen_rect, pos_x, pos_y


    def move_window_to_middle(self):
        _, pos_x, pos_y, = self.generate_window_middle_position()
        self.move(pos_x, pos_y)


    def move_window_to_middle_alt_size_repositioning_enabled(self):
        if cv.window_alt_size_repositioning:
            self.move_window_to_middle()


    def toggle_playlist_no_minimal_interface(self):
        if not cv.minimal_interface_enabled:
            br.button_toggle_playlist.button_toggle_playlist_clicked()


    def window_size_toggle_action(self):
        # RETURN FROM FULL SCREEN
        if br.av_player.video_output.isFullScreen():
            br.av_player.full_screen_onoff_toggle()
            return

        cv.window_size_toggle_counter =  (cv.window_size_toggle_counter + 1) % 3
        update_window_size_vars_from_saved_values()
        screen_rect, _, _  = self.generate_window_middle_position()
        TASKBAR_HEIGHT = 30

        # 1ST - GREATER THAN MEDIUM SIZE WINDOW WITHOUT PLAYLIST
        if cv.window_size_toggle_counter == 1:
            self.toggle_playlist_no_minimal_interface()
            self.resize(cv.window_alt_width, cv.window_alt_height)
            self.move_window_to_middle_alt_size_repositioning_enabled()
            br.av_player.resize_window_minimal_interface_enabled()
        # 2ND - SMALL WINDOW IN THE RIGHT-BOTTOM CORNER, NO PLAYLIST
        elif cv.window_size_toggle_counter == 2:
            self.resize(cv.window_second_alt_width, cv.window_second_alt_height)
            br.av_player.resize_window_minimal_interface_enabled()
            if cv.window_alt_size_repositioning:
                pos_x_corner = screen_rect.x() + screen_rect.width() - self.width()
                pos_y_corner = screen_rect.y() + screen_rect.height() - self.height() - TASKBAR_HEIGHT
                self.move(pos_x_corner, pos_y_corner)
        # BACK TO STANDARD - MEDIUM SIZE WINDOW WITH PLAYLIST
        else:
            self.toggle_playlist_no_minimal_interface()
            self.resize(cv.window_width, cv.window_height)
            self.move_window_to_middle_alt_size_repositioning_enabled()
            br.av_player.resize_window_minimal_interface_enabled()


    def playlist_select_prev_pl_action(self):
        current_index = br.playlists_all.currentIndex()
        index_counter = -1
        next_playlist_index = current_index + index_counter

        while next_playlist_index in cv.playlists_without_title_to_hide_index_list and next_playlist_index > 0:
            index_counter -=1
            next_playlist_index = current_index + index_counter

        if next_playlist_index >= 0 and next_playlist_index not in cv.playlists_without_title_to_hide_index_list:
            br.playlists_all.setCurrentIndex(next_playlist_index)



    def playlist_select_next_pl_action(self):
        current_index = br.playlists_all.currentIndex()
        last_playlist_index = cv.playlists_amount-1
        index_counter = 1
        next_playlist_index = current_index + index_counter

        while next_playlist_index in cv.playlists_without_title_to_hide_index_list and next_playlist_index < last_playlist_index:
            index_counter +=1
            next_playlist_index = current_index + index_counter

        if next_playlist_index <= last_playlist_index and next_playlist_index not in cv.playlists_without_title_to_hide_index_list:
            br.playlists_all.setCurrentIndex(next_playlist_index)