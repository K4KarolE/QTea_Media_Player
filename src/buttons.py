from PyQt6.QtWidgets import QFileDialog, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont


from .class_bridge import br
from .class_data import save_json, cv, settings
from .func_coll import (
    generate_duration_to_display,
    remove_track_from_playlist,
    remove_queued_tracks_after_playlist_clear,
    save_speaker_muted_value,
    cur, # db
    connection, # db
    )
from .func_thumbnail import thumbnail_grouped_action
from .logger import logger_runtime
from .message_box import MyMessageBoxWarning



class MyButtons(QPushButton):
    def __init__(
            self,
            title,
            tooltip,
            icon = None):
        super().__init__()
        self.setText(title)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setToolTipDuration(2000)
        self.setFont(QFont('Times', 9, 600))
        self._window_min_width_no_vid = 650
        self._window_min_height_no_vid = 180
        if icon:
            self.setIcon(icon)
            self.setText(None)
            self.setIconSize(QSize(cv.icon_size, cv.icon_size))



    '''
    ########################
        PLAYLIST SECTION
    ########################
    '''
    ''' BUTTON PLAYLIST - ADD TRACK '''
    def button_add_track_clicked(self):
        ''' BUTTON - MUSIC '''
        dialog_add_track = QFileDialog()
        dialog_add_track.setWindowTitle("Select a media file")
        dialog_add_track.setNameFilters(cv.FILE_TYPES_LIST)
        dialog_add_track.exec()
        if dialog_add_track.result():
            br.window.thread_add_media.source = dialog_add_track.selectedFiles()[0]
            br.window.thread_add_media.start()


    ''' BUTTON PLAYLIST - ADD DIRECTORY '''
    @logger_runtime
    def button_add_dir_clicked(self):
        dialog_add_dir = QFileDialog()
        dialog_add_dir.setWindowTitle("Select a directory")
        dialog_add_dir.setFileMode(QFileDialog.FileMode.Directory)
        dialog_add_dir.exec()
        if dialog_add_dir.result():
            br.window.thread_add_media.source = dialog_add_dir.selectedFiles()[0]
            br.window.thread_add_media.start()





    ''' BUTTON PLAYLIST - REMOVE SINGLE TRACK '''
    def button_remove_single_track(self):
        if cv.active_pl_name.currentRow() > -1:
            remove_track_from_playlist()


    ''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
    def button_remove_all_track(self):
        
        def clear_playlist():
            # QUEUE
            remove_queued_tracks_after_playlist_clear()
            # DB
            cur.execute("DELETE FROM {0}".format(cv.active_db_table))
            connection.commit()
            # PLAYLIST
            cv.active_pl_name.clear()
            cv.active_pl_queue.clear()
            cv.active_pl_duration.clear()
            # FOR SEARCH WINDOW
            cv.track_change_on_main_playlist_new_search_needed = True

        ''' Queued track in the playlist '''
        if cv.active_db_table in cv.queue_playlists_list:
            if MyMessageBoxWarning().clicked_continue():
                clear_playlist()
        else:
            clear_playlist()
        
        cv.playlist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = 0
        cv.active_pl_sum_duration = 0
        br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))
        

    ''' BUTTON PLAYLIST - SETTINGS BUTTON / WINDOW '''
    def button_settings_clicked(self):
        br.window_settings.show()


    ''' BUTTON PLAYLIST - SET STYLE '''
    def set_style_playlist_buttons(self):
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.2 #F0F0F0, stop: 0.8 #F0F0F0, stop: 1 #C2C2C2);"
                            "color: grey;"   # font
                            "border: 1px solid grey;"
                            "border-radius: 4px;"
                            "margin: 3 px;" # 3 px != 3px
                            "}"
                        "QPushButton::pressed"
                            "{"
                            "background-color : #C2C2C2;"
                            "}"
                        )
    

    ''' BUTTON PLAYLIST - SETTINGS - SET STYLE '''
    def set_style_settings_button(self):
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.2 #F0F0F0, stop: 0.8 #F0F0F0, stop: 1 #C2C2C2);"
                            "color: grey;"   
                            "border: 1px solid grey;"
                            "border-radius: 4px;"
                            "margin: 3px;" # 3 px != 3px, diff. pre. style sheet
                            "}"
                        "QPushButton::pressed"
                            "{"
                            "background-color : #C2C2C2;"
                            "}"
                        )

    ''' BUTTON PLAYLIST - THUMBNAIL '''
    def button_thumbnail_clicked(self):
        if cv.playlist_widget_dic[cv.active_db_table]['name_list_widget'].isVisible():
            cv.playlist_widget_dic[cv.active_db_table]['name_list_widget'].hide()
            cv.playlist_widget_dic[cv.active_db_table]['queue_list_widget'].hide()
            cv.playlist_widget_dic[cv.active_db_table]['duration_list_widget'].hide()
            cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window'].show()
            thumbnail_grouped_action()
        else:
            cv.playlist_widget_dic[cv.active_db_table]['name_list_widget'].show()
            cv.playlist_widget_dic[cv.active_db_table]['queue_list_widget'].show()
            cv.playlist_widget_dic[cv.active_db_table]['duration_list_widget'].show()
            cv.playlist_widget_dic[cv.active_db_table]['thumbnail_window'].hide()


    

    ''' BUTTON PLAYLIST - DURATION INFO - SET STYLE '''
    def set_style_duration_info_button(self):
        self.setFont(QFont('Times', 14, 600))
        self.setFlat(True)
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "color: grey;"   
                            "}"
                        )
    



    ''' 
    #####################
        PLAY SECTION    
    #####################
    '''
    ''' BUTTON PLAY SECTION - PLAY / PAUSE '''
    def button_play_pause_clicked(self):
        if br.av_player.player.isPlaying():
            br.av_player.player.pause()
            if cv.os_linux: # workaround info in the readme
                cv.player_paused_position = br.av_player.player.position()
            br.av_player.paused = True
            self.setIcon(br.icon.start)
            br.av_player.screen_saver_on()
        elif br.av_player.paused:
            if cv.os_linux:
                br.av_player.player.setPosition(cv.player_paused_position)
            br.av_player.player.play()
            br.av_player.paused = False
            self.setIcon(br.icon.pause)
            br.av_player.screen_saver_on_off()
        elif not br.av_player.player.isPlaying() and not br.av_player.paused:
            br.play_funcs.play_track()
            if br.av_player.player.isPlaying(): # ignoring empty playlist
                self.setIcon(br.icon.pause)
        
    
    # TRIGGERED BY THE DOUBLE-CLICK IN THE PLAYLIST
    def button_play_pause_via_list(self):
        self.setIcon(br.icon.pause)
        br.play_funcs.play_track()
    

    ''' BUTTON PLAY SECTION - STOP '''
    def button_stop_clicked(self):
        br.av_player.player.stop()
        br.av_player.paused = False
        br.button_play_pause.setIcon(br.icon.start)
        br.av_player.screen_saver_on()
        if br.av_player.video_output.isVisible():
            br.image_logo.show()
            br.av_player.video_output.hide()


    ''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
    def button_prev_track_clicked(self):
        if cv.playing_track_index is None:
            cv.playing_track_index = cv.playing_pl_name.currentRow()

        if cv.playing_pl_tracks_count > 0:
            cv.is_play_prev_track_clicked = True
            # TRACK IN SHUFFLE LIST
            if cv.shuffle_playlist_on and len(cv.shuffle_played_tracks_list) > 1:
                self.play_shuffle_played_list_track()
            # STANDARD PREV TRACK / THE LAST TRACK IN PLAYLIST
            elif cv.playing_track_index != 0:
                cv.playing_track_index -= 1
                if cv.playing_pl_tracks_count - 1 > cv.playing_track_index:
                    br.play_funcs.play_track(cv.playing_track_index)
                else:
                    cv.playing_track_index = cv.playing_pl_tracks_count - 1
                    br.play_funcs.play_track(cv.playing_track_index)
            cv.is_play_prev_track_clicked = False

    def play_shuffle_played_list_track(self):
        cv.playing_track_index = cv.shuffle_played_tracks_list[-2]
        if cv.playing_pl_tracks_count > cv.playing_track_index + 1:
            br.play_funcs.play_track(cv.playing_track_index)



    ''' BUTTON PLAY SECTION - NEXT TRACK '''
    def button_next_track_clicked(self):
        br.play_funcs.play_next_track()
    

    ''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
    def button_toggle_repeat_pl_clicked(self):
        cv.repeat_playlist =  (cv.repeat_playlist + 1) % 3
        
        # NO REPEAT
        if cv.repeat_playlist == 1:
            self.setFlat(False)
            self.setIcon(br.icon.repeat)
            br.av_player.text_display_on_video(1500, 'Repeat: OFF') 
        # REPEAT PLAYLIST
        elif cv.repeat_playlist == 2:
            self.setFlat(True)
            br.av_player.text_display_on_video(1500, 'Repeat: Playlist') 
        # REPEAT SINGLE TRACK
        else:
            self.setIcon(br.icon.repeat_single)
            br.av_player.text_display_on_video(1500, 'Repeat: Single track') 
        
        settings['repeat_playlist'] = cv.repeat_playlist
        save_json()
    

    ''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
    def button_toggle_shuffle_pl_clicked(self):
        if cv.shuffle_playlist_on:
            cv.shuffle_playlist_on = False
            self.setFlat(False)
            br.av_player.text_display_on_video(1500, 'Shuffle: OFF')
            cv.shuffle_played_tracks_list.clear()
        else:
            cv.shuffle_playlist_on = True
            self.setFlat(True)
            br.av_player.text_display_on_video(1500, 'Shuffle: ON') 
        
        settings['shuffle_playlist_on'] = cv.shuffle_playlist_on
        save_json()
    

    ''' BUTTON PLAY SECTION - TOGGLE SHOW/HIDE PLAYLIST '''
    def button_toggle_playlist_clicked(self):
        if br.av_player.playlist_visible and br.av_player.video_area_visible:
            br.layout_vert_right_qframe.hide()
            br.av_player.playlist_visible = False
            br.button_toggle_video.setDisabled(True)
        else:
            br.layout_vert_right_qframe.show()
            br.av_player.playlist_visible = True
            br.button_toggle_video.setDisabled(False)


    ''' BUTTON PLAY SECTION - TOGGLE SHOW/HIDE VIDEO '''
    def button_toggle_video_clicked(self):
        if br.av_player.playlist_visible and br.av_player.video_area_visible:
            br.layout_vert_left_qframe.hide()
            br.av_player.video_area_visible = False
            br.window.resize(int(cv.window_width/3), br.window.geometry().height())
            br.window.setMinimumSize(self._window_min_width_no_vid, self._window_min_height_no_vid)
            br.button_toggle_playlist.setDisabled(True)
        else:
            br.window.resize(cv.window_width, br.window.geometry().height())
            br.window.setMinimumSize(cv.window_min_width, cv.window_min_height)
            br.layout_vert_left_qframe.show()
            br.av_player.video_area_visible = True
            br.button_toggle_playlist.setDisabled(False)


    ''' BUTTON PLAY SECTION - SPEAKER/MUTE '''
    def button_speaker_clicked(self):
        if cv.is_speaker_muted:
            cv.is_speaker_muted = False
            br.button_speaker.setIcon(br.icon.speaker)
            br.av_player.audio_output.setVolume(cv.volume)
            br.av_player.text_display_on_video(1500, 'Muted: OFF') 
        else:
            cv.is_speaker_muted = True
            br.button_speaker.setIcon(br.icon.speaker_muted)
            br.av_player.audio_output.setVolume(0)
            br.av_player.text_display_on_video(1500, 'Muted: ON') 
        save_speaker_muted_value()

    # USED WHEN CHANGING VOLUME WHILE MUTED
    # WITHOUT THE SPEAKER BUTTON - SLIDER, HOTKEYS
    def button_speaker_update(self):
        if cv.is_speaker_muted:
            cv.is_speaker_muted = False
            br.button_speaker.setIcon(br.icon.speaker)