
from PyQt6.QtCore import QUrl

import random

from .cons_and_vars import cv

from .func_coll import (
    save_last_track_index,
    get_path_db,
    get_duration_db,
    list_item_style_update,
    generate_duration_to_display,
    Path,
    inactive_track_font_style,  
    active_track_font_style
    )


class PlaysFunc():

    def __init__(self, window, av_player, play_slider, image_logo, playing_track_index):
        self.window = window
        self.av_player = av_player
        self.av_player.player.mediaStatusChanged.connect(self.auto_play_next_track)
        self.play_slider = play_slider
        self.image_logo = image_logo
        self.playing_track_index = playing_track_index
    

    def play_track(self, playing_track_index=None):
        if playing_track_index == None:
            playing_track_index = cv.active_pl_name.currentRow()
            cv.playing_track_index = cv.active_pl_name.currentRow()

        try:  
           # FONT STYLE - PREV/NEW TRACK
            if cv.playing_track_index != None:

                try:
                    ''' PREVIOUS TRACK STYLE'''
                    list_item_style_update(
                        cv.active_pl_name.item(cv.last_track_index),
                        inactive_track_font_style,
                        'black',
                        'white'
                    )

                    list_item_style_update(
                        cv.active_pl_duration.item(cv.last_track_index),
                        inactive_track_font_style,
                        'black',
                        'white'
                    )

                except:
                    print(f'ERROR in row: {cv.last_track_index}\n\n')
             
            cv.last_track_index = cv.playing_track_index
          
      
            ''' NEW TRACK STYLE'''
            list_item_style_update(
                cv.active_pl_name.item(playing_track_index), 
                active_track_font_style,
                'white',
                '#287DCC'
                )

            list_item_style_update(
                cv.active_pl_duration.item(playing_track_index),
                active_track_font_style,
                'white',
                '#287DCC'
                )

            save_last_track_index()
            
            # PATH / DURATION / SLIDER
            track_path = get_path_db(playing_track_index)
            cv.track_full_duration = get_duration_db(playing_track_index)
            cv.track_full_duration_to_display = generate_duration_to_display(cv.track_full_duration)
            self.play_slider.setMaximum(cv.track_full_duration)
            # PLAYER
            ''' 
                Why showing the previous vid's last 
                frame in a vid-audio-vid(here) sequence? 
                
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
            self.av_player.player.play()
            
            # WINDOW TITLE
            self.window.setWindowTitle(f'{Path(track_path).stem} - QTea media player')

            # SCROLL TO PLAYING TRACK IF IT WOULD BE
            # OUT OF THE VISIBLE WINDOW/LIST
            cv.active_pl_name.scrollToItem(cv.active_pl_name.item(cv.playing_track_index))

            # SCREEN SAVER SETTINGS UPDATE
            self.av_player.screen_saver_on_off()

        except:
            print('ERROR - play_track')


    def play_next_track(self):

        if cv.playing_track_index == None:
            cv.playing_track_index = cv.active_pl_name.currentRow()
        # SHUFFLE
        elif cv.shuffle_playlist_on and cv.active_pl_name.count() > 1:
            next_track_index = list(range(0, cv.active_pl_name.count()))
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
        elif (cv.active_pl_name.count() != cv.playing_track_index + 1 and 
              cv.repeat_playlist in [0,1,2]):
            cv.playing_track_index += 1
            self.play_track(cv.playing_track_index)
        # REPEAT PLAYLIST    
        elif (cv.active_pl_name.count() == cv.playing_track_index + 1 and
            cv.repeat_playlist == 2):
                cv.playing_track_index = 0
                self.play_track(cv.playing_track_index)
        # CURRENT TRACK BACK TO START         
        else:
            self.av_player.player.setPosition(0)


    def auto_play_next_track(self):
        if self.av_player.base_played:   # avoiding the dummy song played when the class created
            if self.av_player.player.mediaStatus() == self.av_player.player.MediaStatus.EndOfMedia:
                self.play_next_track()
        else:
            self.av_player.base_played = True    
           