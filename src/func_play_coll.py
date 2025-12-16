from pathlib import Path
import random

from PyQt6.QtCore import QUrl

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    active_track_font_style,
    disable_minimal_interface,
    generate_duration_to_display,
    get_all_from_db,
    inactive_track_font_style,
    list_item_style_update,
    queue_window_remove_track,
    save_playing_playlist_and_playing_last_track_index,
    search_result_queue_number_update,
    update_playing_playlist_vars_and_widgets,
    update_queued_track_style,
    update_queued_tracks_order_number,
    update_raw_current_duration_db
    )
from .func_thumbnail import update_thumbnail_style_at_play_track
from .logger import logger_check


class PlaysFunc:
    def __init__(self):
        self.track_path = ""

    def play_track(self, playing_track_index=None):
        # PyQt playing the first audio_track of the video by default
        #  -> reset our variable when playing new track
        cv.audio_track_played = 0

        # If the "Start from the latest point" is enabled:
        # Saving the current duration in every 5 second
        # -> reset our assist variable when playing new track   
        cv.counter_for_duration = 0

        update_playing_playlist_vars_and_widgets()
        
        # playing_track_index --> cv.playing_track_index
        self.generate_playing_track_index(playing_track_index)

        # TO MAKE SURE UN-PLAYED TRACK`S THUMBNAIL VIEW STYLE IS CORRECT
        # SCENARIO: app started >> non-playing playlist is active + one of the row is selected
        # >> switch to thumbnail view >> only the selected thumbnail style is in use
        cv.playlist_widget_dic[cv.playing_db_table]['played_thumbnail_style_update_needed'] = True
        
        ''' QUEUE MANAGEMENT '''
        cv.queue_tracking_title = [cv.playing_db_table, cv.playing_track_index]
        if cv.queue_tracking_title in cv.queue_tracks_list:
            current_queue_index = cv.queue_tracks_list.index(cv.queue_tracking_title)
            queue_window_remove_track(current_queue_index)

            cv.queue_tracks_list.remove(cv.queue_tracking_title)
            cv.queue_playlists_list.remove(cv.playing_db_table)
            cv.playing_pl_queue.item(cv.playing_track_index).setText('')
            update_queued_tracks_order_number()
            # THUMBNAIL VIEW
            thumbnail_widgets_dic = cv.playlist_widget_dic[cv.playing_db_table]['thumbnail_widgets_dic']
            if thumbnail_widgets_dic:
                thumbnail_widgets_dic[cv.playing_track_index]['widget'].is_queued = False
                thumbnail_widgets_dic[cv.playing_track_index]['widget'].set_queue_number(None)


        ''' PLAY '''
        ''' SCENARIOS TO AVOID:
            1, last, played track in the playlist removed
                -> next startup: start the 1st track in the playlist
            2, playing track, clear playlist, restart app
                -> next startup: empty playlist displayed, no autoplay
        '''
        if 0 <= cv.playing_pl_last_track_index < cv.playing_pl_tracks_count:

            # PLAYING TRACK ADDED TO THE QUEUE - VALUATION
            if not [cv.playing_db_table, cv.playing_pl_last_track_index] in cv.queue_tracks_list:
                self.update_previous_track_style()
                self.update_new_track_style()
            else:
                update_queued_track_style(cv.playing_pl_last_track_index)

            update_thumbnail_style_at_play_track()
            cv.playing_pl_last_track_index = cv.playing_track_index
            if cv.active_db_table == cv.playing_db_table:
                cv.active_pl_last_track_index = cv.playing_track_index
            save_playing_playlist_and_playing_last_track_index()

        else:
            if cv.playing_pl_tracks_count: # last played track index > playlist amount
                cv.playing_pl_last_track_index = 0
                save_playing_playlist_and_playing_last_track_index()
                self.play_track()
            else:   # empty playlist
                return

        if cv.shuffle_playlist_on:
            self.add_to_shuffle_played_list()

        # PATH / DURATION / SLIDER
        cv.track_full_duration, cv.track_current_duration, self.track_path = get_all_from_db(cv.playing_track_index, cv.playing_db_table)
        cv.track_full_duration_to_display = generate_duration_to_display(cv.track_full_duration)
        br.play_slider.setMaximum(cv.track_full_duration)
        
        # PLAYER
        br.av_player.stopped = False
        br.av_player.player.setSource(QUrl.fromLocalFile(str(Path(self.track_path))))


    def play_track_second_part(self):
        """ Media was set as source in the previous "play_track" function which triggers
            the src / av_player / mediaStatusChanged signal calling this function
            Otherwise the Audio and Subtitles tracks amount generated
            before the media is loaded >> zero >> not able to switch Audio or
            Subtitles via hotkeys
        """
        # FILE REMOVED / RENAMED
        if br.av_player.player.mediaStatus() == br.av_player.player.MediaStatus.InvalidMedia:
            br.play_slider.setEnabled(False)
            br.image_logo.show()
            br.av_player.video_output.hide()
            self.update_window_title(self.track_path, False)
            return
        else:
            br.play_slider.setEnabled(True)
            self.update_window_title(self.track_path, True)
        
        # VIDEO AREA / LOGO DISPLAY
        if self.track_path.split('.')[-1] in cv.AUDIO_FILES:     # music_title.mp3 -> mp3
            br.image_logo.show()
            br.av_player.video_output.hide()
        else:
            br.image_logo.hide()
            br.av_player.video_output.show()
        
        # AUDIO / SUBTITLE TRACKS
        cv.audio_tracks_amount = len(br.av_player.player.audioTracks())
        cv.subtitle_tracks_amount = len(br.av_player.player.subtitleTracks())
        
        # PLAY
        self.audio_tracks_use_default()
        br.av_player.player.play()

        # DISPLAY TRACK TITLE ON VIDEO
        if br.av_player.video_output.isVisible():
            br.av_player.text_display_on_video(2000, cv.track_title)
        
        # SCROLL TO PLAYING TRACK
        # STANDARD PLAYLIST
        item = cv.playing_pl_name.item(cv.playing_track_index)
        cv.playing_pl_name.scrollToItem(item)
        # THUMBNAIL PLAYLIST
        cv.playlist_widget_dic[cv.playing_db_table]['thumbnail_window'].scroll_to_current_item_playing_pl()

        # SCREEN SAVER SETTINGS UPDATE
        br.av_player.screen_saver_on_off()

        # UPDATING THE QUEUE NUMBERS IN THE SEARCH TAB / RESULTS LIST
        search_result_queue_number_update()


    def add_to_shuffle_played_list(self):
        '''
        "Shuffle playlist" is ON:
        The currently playing tracks added to the "shuffle_played_tracks_list"
        which is used when the "Play previous" button/hotkey is triggered
        "Shuffle playlist" is OFF: the previous track played in playlist
        '''
        if (not cv.is_play_prev_track_clicked and
                cv.playing_track_index not in cv.shuffle_played_tracks_list):
            cv.shuffle_played_tracks_list.append(cv.playing_track_index)
            if len(cv.shuffle_played_tracks_list) > cv.shuffle_played_tracks_list_size:
                cv.shuffle_played_tracks_list.pop(0)
        else:
            if cv.shuffle_played_tracks_list:
                cv.shuffle_played_tracks_list.pop(-1)


    def update_window_title(self, track_path, no_error):
        cv.track_title = Path(track_path).stem
        cv.currently_playing_track_info_in_window_title = f'{cv.playing_pl_title}  |  {cv.track_title}'
        if no_error:
            br.window.setWindowTitle(f'{cv.currently_playing_track_info_in_window_title} - QTea Media Player')
            br.window_queue_and_search.setWindowTitle(cv.currently_playing_track_info_in_window_title)
        else:
            base_window_title = f'### ERROR ### |  {cv.currently_playing_track_info_in_window_title}'
            br.window.setWindowTitle(f'{base_window_title} - QTea Media Player')
            br.window_queue_and_search.setWindowTitle(base_window_title)


    def play_next_track(self):
        if not cv.playing_pl_name:
            # Scenario: app started without autoplay + play next button clicked
            cv.playing_pl_name = cv.active_pl_name

        if cv.queue_tracks_list:
            # IF: THE CURRENTLY PLAYING TRACK ADDED TO THE QUEUE AS 1ST ONE
            # cv.queue_tracks_list = [[playlist_3, 5],[playlist_2, 3]..]
            if cv.queue_tracks_list[0] == [cv.playing_db_table, cv.playing_track_index]:
                br.av_player.player.setPosition(0)
                self.play_track(cv.queue_tracks_list[0][1]) # call the function with argument -> queue will be updated
            else:
                cv.playing_playlist_index = cv.playlist_list.index(cv.queue_tracks_list[0][0])
                update_playing_playlist_vars_and_widgets()
                self.play_track(cv.queue_tracks_list[0][1])

        elif cv.playing_pl_name.count() > 0:

            cv.playing_pl_tracks_count = cv.playing_pl_name.count()

            # SHUFFLE
            if cv.shuffle_playlist_on and cv.playing_pl_tracks_count > 1:
                # Selecting a new track which was not played
                # the last "cv.shuffle_played_tracks_list_size" times
                if cv.playing_pl_tracks_count > cv.shuffle_played_tracks_list_size:
                    random_choice_list = [x for x in range(0, cv.playing_pl_tracks_count) if x not in cv.shuffle_played_tracks_list]
                else:
                    random_choice_list = [x for x in range(0, cv.playing_pl_tracks_count) if x != cv.playing_track_index]
                next_track_index = random.choice(random_choice_list)
                cv.playing_track_index = next_track_index
                self.play_track(next_track_index)
            # REPEAT SINGLE TRACK - NO BUTTON CLICK    
            elif (cv.repeat_playlist == 0 and 
                br.av_player.player.mediaStatus() == br.av_player.player.MediaStatus.EndOfMedia):
                    cv.track_current_duration = 0
                    br.av_player.player.setPosition(0)
                    br.av_player.player.play()
            # MORE TRACKS IN THE PLAYLIST - BUTTON CLICK
            elif (cv.playing_pl_tracks_count != cv.playing_track_index + 1 and 
                cv.repeat_playlist in [0,1,2]):
                cv.playing_track_index += 1
                self.play_track(cv.playing_track_index)
            # REPEAT PLAYLIST    
            elif (cv.playing_pl_tracks_count == cv.playing_track_index + 1 and
                cv.repeat_playlist == 2):
                    cv.playing_track_index = 0
                    self.play_track(cv.playing_track_index)
            # SET THE CURRENT TRACK BACK TO STARTING POINT
            # LAST VIDEO TRACK IN PLAYLIST AND REPEAT INACTIVE
            # -> HIDE BLACK SCREEN & DISPLAY LOGO         
            elif (cv.playing_pl_tracks_count == cv.playing_track_index + 1 and
                br.av_player.player.mediaStatus() == br.av_player.player.MediaStatus.EndOfMedia):
                    disable_minimal_interface()
                    br.av_player.stopped = True
                    br.av_player.player.setPosition(0)
                    br.av_player.video_output.hide()
                    br.image_logo.show()
                    br.button_play_pause.setIcon(br.icon.start)
                    br.button_duration_info.disable_and_set_to_zero()


    @logger_check
    def auto_play_next_track(self):
        """
        AT STARTUP:
        - The function first triggered once the base is played (src/av_player)
        - On every playlist the last/previously played row will be selected (src/playlists.py)
        - The last playing playlist will be set active/displayed (src/playlists.py)
        - If 'Play at startup' active (Settings / General), track will be played automatically
        """
        # END OF THE MEDIA >> PLAY NEXT TRACK
        if br.av_player.base_played_end_of_media_signal_ignored:
            # if br.av_player.player.mediaStatus() == br.av_player.player.MediaStatus.EndOfMedia:
                # To play from the start at next time playing the same track
                # Not from (full duration - 5 sec) position
                if cv.continue_playback and not cv.adding_records_at_moment:
                    update_raw_current_duration_db(0, cv.playing_track_index)
                self.play_next_track()
        else:
            br.av_player.base_played_end_of_media_signal_ignored = True


    def audio_tracks_play_next_one(self):
        if cv.audio_tracks_amount:
            cv.audio_track_played = (cv.audio_track_played + 1) % cv.audio_tracks_amount
            br.av_player.player.setActiveAudioTrack(cv.audio_track_played)
            # Display the current audio track title on the screen
            audio_track = br.av_player.player.audioTracks()[cv.audio_track_played]
            audio_track_title = br.av_player.generate_audio_track_title(audio_track)
            br.av_player.text_display_on_video(1000, audio_track_title)
        else:
            br.av_player.text_display_on_video(1000, "Video has one audio track only")


    def audio_tracks_use_default(self):
        # Some video`s default audiotrack is not the 1st one >>
        # make sure the 1st one playing when cv.default_audio_track = 1
        if cv.audio_tracks_amount > 1 and 1 <= cv.default_audio_track <= cv.audio_tracks_amount:
            br.av_player.player.setActiveAudioTrack(cv.default_audio_track - 1)
            cv.audio_track_played = cv.default_audio_track - 1
    

    def subtitle_tracks_play_next_one(self):
        if cv.subtitle_tracks_amount:
            sub_list = [n for n in range(cv.subtitle_tracks_amount)]
            sub_list.append(-1) # -1: disable subtitle
            cv.subtitle_track_played = sub_list[cv.subtitle_track_played + 1]
            br.av_player.player.setActiveSubtitleTrack(cv.subtitle_track_played)
            # Display the current subtitle name on the screen
            if cv.subtitle_track_played == -1:
                subtitle_track_title = 'Disable'
            else:
                subtitle_track = br.av_player.player.subtitleTracks()[cv.subtitle_track_played]
                subtitle_track_title = br.av_player.generate_subtitle_track_title(subtitle_track)
        else:
            subtitle_track_title = 'No subtitles'
        br.av_player.text_display_on_video(1000, subtitle_track_title)


    def audio_output_device_use_next_one(self):
        device_list = br.av_player.media_devices.audioOutputs()
        current_device = br.av_player.audio_output.device()
        current_device_index = device_list.index(current_device)
        next_device_index = (current_device_index + 1) % len(device_list)
        next_device = device_list[next_device_index]
        br.av_player.audio_output.setDevice(next_device)
        br.av_player.text_display_on_video(1000, next_device.description())


    def generate_playing_track_index(self, playing_track_index):
        ''' 
        SCENARIO A - playing_track_index == None:
        - Double-click on a track in a playlist
        - Autoplay at startup

        SCENARIO B - playing_track_index == row number:
        - Play next/prev buttons
        '''
        if playing_track_index == None: # Scenario - A
            cv.playing_playlist_index = cv.active_playlist_index
            update_playing_playlist_vars_and_widgets()

            if cv.playing_pl_tracks_count > 0:
                if cv.playing_pl_name.currentRow() > -1: # When row selected
                    cv.playing_track_index = cv.playing_pl_name.currentRow()
                else:
                    cv.playing_track_index = 0
            else:   # empty playlist
                return

        else:   # Scenario - B
            cv.playing_track_index = playing_track_index


    def update_previous_track_style(self):
        list_item_style_update(
            cv.playing_pl_name.item(cv.playing_pl_last_track_index),
            inactive_track_font_style,
            'black',
            'white'
        )

        list_item_style_update(
            cv.playing_pl_queue.item(cv.playing_pl_last_track_index),
            inactive_track_font_style,
            'black',
            'white'
        )

        list_item_style_update(
            cv.playing_pl_duration.item(cv.playing_pl_last_track_index),
            inactive_track_font_style,
            'black',
            'white'
        )
    

    def update_new_track_style(self):
        list_item_style_update(
            cv.playing_pl_name.item(cv.playing_track_index), 
            active_track_font_style,
            'white',
            '#287DCC'
            )
                
        list_item_style_update(
            cv.playing_pl_queue.item(cv.playing_track_index), 
            active_track_font_style,
            'white',
            '#287DCC'
            )

        list_item_style_update(
            cv.playing_pl_duration.item(cv.playing_track_index),
            active_track_font_style,
            'white',
            '#287DCC'
            )