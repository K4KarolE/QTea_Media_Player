
from PyQt6.QtCore import QUrl

import random
from pathlib import Path

from .cons_and_vars import cv
from .func_coll import (
    save_playing_playlist_and_playing_last_track_index,
    list_item_style_update,
    generate_duration_to_display,
    update_playing_playlist_vars_and_widgets,
    update_active_playlist_vars_and_widgets,
    get_all_from_db,
    update_raw_current_duration_db,
    update_queued_tracks_order_number,
    update_queued_track_style,
    queue_window_remove_track,
    inactive_track_font_style,  
    active_track_font_style
    )

import time

class PlaysFunc():

    def __init__(self, window, av_player, play_slider, image_logo, playing_track_index):
        self.window = window
        self.av_player = av_player
        self.av_player.player.mediaStatusChanged.connect(self.auto_play_next_track)
        self.play_slider = play_slider
        self.image_logo = image_logo
        self.playing_track_index = playing_track_index
    

    def play_track(self, playing_track_index=None):

        cv.counter_for_duration = 0  # for iterate: saving the current duration
        update_active_playlist_vars_and_widgets()
        
        self.get_playing_track_index(playing_track_index)
        
        ''' QUEUE MANAGEMENT '''
        cv.queue_tracking_title = [cv.playing_db_table, cv.playing_track_index]
        if cv.queue_tracking_title in cv.queue_tracks_list:
            current_queue_index = cv.queue_tracks_list.index(cv.queue_tracking_title)
            queue_window_remove_track(current_queue_index)
            
            cv.queue_tracks_list.remove(cv.queue_tracking_title)
            cv.queue_playlists_list.remove(cv.playing_db_table)
            cv.playing_pl_queue.item(cv.playing_track_index).setText('')
            update_queued_tracks_order_number()


        ''' PLAY '''
        try:
            ''' AVOID SCENARIO:
                1, last, played track in the playlist removed
                2, another track started in the same playlist
                3, failing last played track style update
            '''
            if cv.playing_pl_last_track_index < cv.playing_pl_tracks_count:
                
                # PLAYING TRACK ADDED TO THE QUEUE VALUATION
                if not [cv.playing_db_table, cv.playing_pl_last_track_index] in cv.queue_tracks_list:
                    self.update_previous_track_style()
                else:
                    update_queued_track_style(cv.playing_pl_last_track_index)
                
            self.update_new_track_style()
             
            
            cv.playing_pl_last_track_index = cv.playing_track_index
            save_playing_playlist_and_playing_last_track_index()
            
            # PATH / DURATION / SLIDER
            cv.track_full_duration, cv.track_current_duration, track_path = get_all_from_db(cv.playing_track_index, cv.playing_db_table)
            cv.track_full_duration_to_display = generate_duration_to_display(cv.track_full_duration)
            self.play_slider.setMaximum(cv.track_full_duration)
            
            # WINDOW TITLE
            cv.currently_playing_track_info_in_window_title = f'{cv.playing_pl_title}  |  {Path(track_path).stem}'
            self.window.setWindowTitle(f'{cv.currently_playing_track_info_in_window_title} - QTea media player')

            # PLAYER
            ''' 
                Why showing the previous vid's last frame in the
                play vid -- play just audio / stop video -- play vid sequence? 
                
                Tried:
                    - stop player before hiding
                    - hide / show - setSource diff. variation
                    - no video_output.hide() --> no problem
            '''
            if track_path[-4:] in cv.AUDIO_FILES:
                self.image_logo.show()
                self.av_player.video_output.hide()
            else:
                self.image_logo.hide()
                self.av_player.video_output.show()
        
            self.av_player.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))

            # FILE REMOVED / RENAMED
            if self.av_player.player.mediaStatus() == self.av_player.player.MediaStatus.InvalidMedia:
                self.play_next_track()
           
            # PLAY FROM LAST POINT
            if cv.track_current_duration > 0 and cv.continue_playback == 'True':
                self.av_player.player.setPosition(cv.track_current_duration)
            
            # PLAY
            self.av_player.player.play()
            
            # AUDIO / SUBTITLE TRACKS
            cv.audio_tracks_amount = len(self.av_player.player.audioTracks())
            cv.subtitle_tracks_amount = len(self.av_player.player.subtitleTracks())
            

            # SCROLL TO PLAYING TRACK IF IT WOULD BE
            # OUT OF THE VISIBLE WINDOW/LIST
            cv.playing_pl_name.scrollToItem(cv.playing_pl_name.item(cv.playing_track_index))

            # SCREEN SAVER SETTINGS UPDATE
            self.av_player.screen_saver_on_off()

        except:
            print('ERROR - play_track()\n')
            # self.play_next_track()


    def play_next_track(self):

        if cv.queue_tracks_list:
            
            # IF: THE CURRENTLY PLAYING TRACK ADDED TO THE QUEUE AS 1ST ONE
            # cv.queue_tracks_list = [[playlist_3, 5],[playlist_2, 3]..]
            if cv.queue_tracks_list[0] == [cv.playing_db_table, cv.playing_track_index]:
                self.av_player.player.setPosition(0)
                self.play_track(cv.queue_tracks_list[0][1]) # call the function with argument -> queue will be updated
            else:
                cv.playing_playlist_index = cv.paylist_list.index(cv.queue_tracks_list[0][0])
                update_playing_playlist_vars_and_widgets()
                self.play_track(cv.queue_tracks_list[0][1])

        elif cv.playing_pl_name.count() > 0:

            cv.playing_pl_tracks_count = cv.playing_pl_name.count()

            # SHUFFLE
            if cv.shuffle_playlist_on and cv.playing_pl_tracks_count > 1:
                next_track_index = list(range(0, cv.playing_pl_tracks_count))
                next_track_index.pop(cv.playing_track_index)
                next_track_index = random.choice(next_track_index)
                cv.playing_track_index = next_track_index
                self.play_track(next_track_index)
            # REPEAT SINGLE TRACK - NO BUTTON CLICK    
            elif (cv.repeat_playlist == 0 and 
                self.av_player.player.mediaStatus() == self.av_player.player.MediaStatus.EndOfMedia):
                    self.av_player.player.setPosition(0)
                    self.av_player.player.play()
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
            # CURRENT TRACK BACK TO START         
            else:
                self.av_player.player.setPosition(0)


    
    def auto_play_next_track(self):

        ''' AT STARTUP:
            - It first triggered once the based is played (main / AVPlayer())
            --> cv.played_at_startup_counter needed
            - On every playlist the last/previously played row will be selected (src/playlists.py) 
            - The last playing playist will be set active/displayed (src/playlists.py)
            - If 'Play at startup' active (Settings / General), track will be played automatically
        '''

        if not cv.played_at_startup_counter:
            cv.active_playlist_index = cv.playing_playlist_index

        if self.av_player.base_played:   # avoiding the dummy song played when the class created
            if self.av_player.player.mediaStatus() == self.av_player.player.MediaStatus.EndOfMedia:
                # To play from the start at next time playing the same track
                # Not from (duration - 5 sec) position
                if cv.continue_playback == 'True' and not cv.adding_records_at_moment:
                    update_raw_current_duration_db(0, cv.playing_track_index)
                self.play_next_track()
        else:
            self.av_player.base_played = True

            if cv.play_at_startup == 'True' and not cv.played_at_startup_counter:
                time.sleep(0.1) # otherwise media loading error occurs / not mediastatus problem
                self.play_track()

        cv.played_at_startup_counter = True


    def audio_tracks_play_next_one(self):
        if cv.audio_tracks_amount:
            cv.audio_track_played = (cv.audio_track_played + 1) % cv.audio_tracks_amount
            self.av_player.player.setActiveAudioTrack(cv.audio_track_played)
    

    def subtitle_tracks_play_next_one(self):
        if cv.subtitle_tracks_amount:
            sub_list = [n for n in range(cv.subtitle_tracks_amount)]
            sub_list.append(-1) # -1: disable subtitle
            cv.subtitle_track_played = sub_list[cv.subtitle_track_played + 1]
            self.av_player.player.setActiveSubtitleTrack(cv.subtitle_track_played)
    

    def get_playing_track_index(self, playing_track_index):
        ''' SCENARIO A - playing_track_index == None:
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
           