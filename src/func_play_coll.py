
from PyQt6.QtCore import QUrl

import random
from pathlib import Path

from .cons_and_vars import cv
from .func_coll import (
    save_playing_tab_and_playing_last_track_index,
    list_item_style_update,
    generate_duration_to_display,
    update_playing_tab_vars_and_widgets,
    update_active_tab_vars_and_widgets,
    get_all_from_db,
    update_raw_current_duration_db,
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
        update_active_tab_vars_and_widgets()
        
        '''
            SCENARIO A - playing_track_index == None:
            - Double-click on a track in a playlist
            - Autoplay at startup

            SCENARIO B - playing_track_index = row number:
            - Play next/prev buttons
        '''
        if playing_track_index == None: # Scenario - A
            cv.playing_tab = cv.active_tab
            update_playing_tab_vars_and_widgets()

            if cv.playing_pl_tracks_count > 0:
                if cv.playing_pl_name.currentRow() > -1: # When row selected
                    cv.playing_track_index = cv.playing_pl_name.currentRow()
                else:
                    cv.playing_track_index = 0
            else:   # empry playlist
                return

        else:   # Scenario - B
            cv.playing_track_index = playing_track_index

        try:
            ''' AVOID SCENARIO:
                1, last, played track in the playlist removed
                2, another track started in the same playlist
                3, failing last played track style update
            '''
            if cv.playing_pl_last_track_index < cv.playing_pl_tracks_count:
                
                ''' PREVIOUS TRACK STYLE'''
                list_item_style_update(
                    cv.playing_pl_name.item(cv.playing_pl_last_track_index),
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
             
            cv.playing_pl_last_track_index = cv.playing_track_index
            save_playing_tab_and_playing_last_track_index()
          
      
            ''' NEW TRACK STYLE'''
            list_item_style_update(
                cv.playing_pl_name.item(cv.playing_track_index), 
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

            
            # PATH / DURATION / SLIDER
            cv.track_full_duration, cv.track_current_duration, track_path = get_all_from_db(cv.playing_track_index, cv.playing_db_table)
            cv.track_full_duration_to_display = generate_duration_to_display(cv.track_full_duration)
            self.play_slider.setMaximum(cv.track_full_duration)
            

            # PLAYER
            ''' 
                Why showing the previous vid's last frame in the
                play vid - play just audio - play vid(prev. vid's frame here) sequence? 
                
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
            
            # WINDOW TITLE
            self.window.setWindowTitle(f'{cv.playing_pl_title} | {Path(track_path).stem} - QTea media player')

            # SCROLL TO PLAYING TRACK IF IT WOULD BE
            # OUT OF THE VISIBLE WINDOW/LIST
            cv.playing_pl_name.scrollToItem(cv.playing_pl_name.item(cv.playing_track_index))

            # SCREEN SAVER SETTINGS UPDATE
            self.av_player.screen_saver_on_off()

        except:
            print('ERROR - play_track()\n')


    def play_next_track(self):

        if cv.playing_pl_tracks_count > 0:

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


    '''
        AT STARTUP
        - It first triggered once the based is played (main / AVPlayer())
          --> cv.played_at_startup_counter needed
        - On every tab/playlist the last played row will be selected (src/tabs.py) 
        - The last playing tab/playist will be set active/displayed (src/tabs.py)
        - If 'Play at startup' active (Settings / General), track will be played automatically (below)
    '''
    def auto_play_next_track(self):

        if not cv.played_at_startup_counter:
            cv.active_tab = cv.playing_tab

        if self.av_player.base_played:   # avoiding the dummy song played when the class created
            if self.av_player.player.mediaStatus() == self.av_player.player.MediaStatus.EndOfMedia:
                # To play from the start at next time playing the same track
                # Not from (duration - 5 sec) position
                if cv.continue_playback == 'True':
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
           