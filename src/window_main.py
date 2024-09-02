import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication, QWidget

from .class_bridge import br
from .class_data import cv
from .func_coll import(
    add_record_grouped_actions,
    generate_duration_to_display,
    queue_add_remove_track,
    save_db,
    update_and_save_volume_slider_value,
    update_window_size_vars_from_saved_values,
    walk_and_add_dir
    )



class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(cv.window_width, cv.window_height)
        self.setMinimumSize(cv.window_min_width, cv.window_min_height)
        self.setWindowIcon(br.icon.window_icon)
        self.setWindowTitle("QTea media player")
        self.setAcceptDrops(1)  # for the external file, dictionary drag&drop
        if cv.always_on_top:
            self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.hotkeys_creation()

    
    def hotkeys_creation(self):
        hotkeys_action_dic = {
        'small_jump_backward': lambda: br.av_player.player.setPosition(br.av_player.player.position() - cv.small_jump),
        'small_jump_forward': lambda: br.av_player.player.setPosition(br.av_player.player.position() + cv.small_jump),
        'medium_jump_backward': lambda: br.av_player.player.setPosition(br.av_player.player.position() - cv.medium_jump),
        'medium_jump_forward': lambda: br.av_player.player.setPosition(br.av_player.player.position() + cv.medium_jump),
        'big_jump_backward': lambda: br.av_player.player.setPosition(br.av_player.player.position() - cv.big_jump),
        'big_jump_forward': lambda: br.av_player.player.setPosition(br.av_player.player.position() + cv.big_jump),
        'display_track_title_on_video': lambda: br.av_player.text_display_on_video(2000, cv.track_title),
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
        'full_screen_toggle': lambda: br.av_player.full_screen_toggle(),
        'playlist_toggle': lambda: br.button_toggle_playlist.button_toggle_playlist_clicked(),
        'video_toggle': lambda: br.button_toggle_video.button_toggle_video_clicked(),
        'window_size_toggle': self.window_size_toggle_action, 
        'paylist_add_track': lambda: br.button_add_track.button_add_track_clicked(),
        'paylist_add_directory': lambda: br.button_add_dir.button_add_dir_clicked(),
        'paylist_remove_track': lambda: br.button_remove_track.button_remove_single_track(),
        'paylist_remove_all_track': lambda: br.button_remove_all_track.button_remove_all_track(),
        'paylist_select_prev_pl': self.paylist_select_prev_pl_action, 
        'paylist_select_next_pl': self.paylist_select_next_pl_action, 
        'queue_toggle': lambda: queue_add_remove_track() 
        }

        for index, hotkey in enumerate(cv.hotkeys_list):
            hotkey_value = cv.hotkey_settings_dic[hotkey]['value']
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
        file_path_list = []
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                path = str(url.toLocalFile())
                # FILES - COLLECTING PATH
                if os.path.isfile(path):
                    extension =  path.split('.')[-1]
                    if extension in cv.MEDIA_FILES:
                        file_path_list.append(path)    
                # DICTIONARY - ADD
                else:
                    walk_and_add_dir(path)
            # FILES - ADD
            for path in file_path_list:
                add_record_grouped_actions(path)
            save_db()

            br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))
            cv.active_pl_tracks_count = cv.active_pl_name.count()
 


    def volume_up_action(self):
        if cv.volume < 1:
            cv.volume = cv.volume + 0.05
            if cv.volume > 1:
                cv.volume = 1
            self.volume_update()
            
    
    def volume_down_action(self):
        if cv.volume > 0:
            cv.volume = cv.volume - 0.05
            if cv.volume < 0:
                cv.volume = 0
            self.volume_update()

    def volume_update(self):
        new_volume = round(cv.volume, 4)
        br.av_player.audio_output.setVolume(new_volume)
        br.button_speaker.button_speaker_update()
        update_and_save_volume_slider_value(new_volume)


    def window_size_toggle_action(self):
        cv.window_size_toggle_counter =  (cv.window_size_toggle_counter + 1) % 3
        update_window_size_vars_from_saved_values()

        SCREEN = QApplication.primaryScreen()
        SCREEN_RECT = SCREEN.availableGeometry()
        WIN_TASKBAR_HEIGHT = 30
        
        def move_window_to_middle():
            if cv.window_alt_size_repositioning:
                WINDOW_MAIN_POS_X = int((SCREEN_RECT.width() - self.width())/2)
                WINDOW_MAIN_POS_Y = int((SCREEN_RECT.height() - self.height())/2)
                self.move(WINDOW_MAIN_POS_X, WINDOW_MAIN_POS_Y)
        
        # 1ST - GREATER THAN MEDIUM SIZE WINDOW WITHOUT PLAYLIST
        if cv.window_size_toggle_counter == 1:
            br.button_toggle_playlist.button_toggle_playlist_clicked()
            self.resize(cv.window_alt_width, cv.window_alt_height)
            move_window_to_middle()
            
        # 2ND - SMALL WINDOW IN THE RIGHT-BOTTOM CORNER, NO PLAYLIST
        elif cv.window_size_toggle_counter == 2:
            self.resize(cv.window_second_alt_width, cv.window_second_alt_height)
            if cv.window_alt_size_repositioning:
                self.move(SCREEN_RECT.width() - self.width(), SCREEN_RECT.height() - self.height() - WIN_TASKBAR_HEIGHT)
        
        # BACK TO STANDARD - MEDIUM SIZE WINDOW WITH PLAYLIST
        else:
            br.button_toggle_playlist.button_toggle_playlist_clicked()
            self.resize(cv.window_width, cv.window_height)
            move_window_to_middle()
        


    def paylist_select_prev_pl_action(self):
        current_index = br.playlists_all.currentIndex()
        index_counter = -1
        next_playlist_index = current_index + index_counter

        while next_playlist_index in cv.paylists_without_title_to_hide_index_list and next_playlist_index > 0:
            index_counter -=1
            next_playlist_index = current_index + index_counter
        
        if next_playlist_index >= 0 and next_playlist_index not in cv.paylists_without_title_to_hide_index_list:
            br.playlists_all.setCurrentIndex(next_playlist_index)
        
        

    def paylist_select_next_pl_action(self):
        current_index = br.playlists_all.currentIndex()
        last_playlist_index = cv.playlist_amount-1
        index_counter = 1
        next_playlist_index = current_index + index_counter

        while next_playlist_index in cv.paylists_without_title_to_hide_index_list and next_playlist_index < last_playlist_index:
            index_counter +=1
            next_playlist_index = current_index + index_counter
        
        if next_playlist_index <= last_playlist_index and next_playlist_index not in cv.paylists_without_title_to_hide_index_list:
            br.playlists_all.setCurrentIndex(next_playlist_index)