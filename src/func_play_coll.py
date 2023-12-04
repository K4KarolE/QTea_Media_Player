
from PyQt6.QtCore import QUrl

import random

from .func_coll import (
    save_last_track_index,
    get_path_db,
    get_duration_db,
    Path,
    cv, # data
    inactive_track_font_style,  
    active_track_font_style
    )


class PlaysFunc():
    def __init__(self, window, av_player, play_slider, image_logo):
        self.window = window
        self.av_player = av_player
        self.av_player.player.mediaStatusChanged.connect(self.auto_play_next_track)
        self.play_slider = play_slider
        self.image_logo = image_logo

    def play_track(self):
        try:  
            # FONT STYLE - PREV/NEW TRACK
            if self.av_player.played_row != None:

                try:
                    cv.active_pl_name.item(cv.last_track_index).setFont(inactive_track_font_style)
                    cv.active_pl_duration.item(cv.last_track_index).setFont(inactive_track_font_style)
                except:
                    print(f'ERROR in row: {cv.last_track_index}\n\n')

                cv.last_track_index = self.av_player.played_row

            cv.active_pl_name.currentItem().setFont(active_track_font_style)
            cv.active_pl_duration.currentItem().setFont(active_track_font_style)
            save_last_track_index()
            # PATH / DURATION / SLIDER
            track_path = get_path_db()
            track_duration = get_duration_db()
            self.play_slider.setMaximum(track_duration)
            # PLAYER
            ''' 
                Why showing the pre vid last frame
                in a vid-audio-vid sequence? 
                
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
            
            # COUNTER
            self.av_player.played_row = cv.active_pl_name.currentRow()
            # WINDOW TITLE
            self.window.setWindowTitle(f'{Path(track_path).stem} - QTea media player')

        except:
            self.play_next_track()


    def play_next_track(self):
        # SHUFFLE
        if cv.shuffle_playlist_on and cv.active_pl_name.count() > 1:
            next_track_index = random.randint(0, cv.active_pl_name.count()-1)
            while next_track_index == cv.active_pl_name.currentRow():
                next_track_index = random.randint(0, cv.active_pl_name.count()-1)
            cv.active_pl_name.setCurrentRow(next_track_index)
            self.play_track()
        # MORE TRACKS IN THE PLAYLIST - NO REPEAT PL
        elif (cv.active_pl_name.count() != cv.active_pl_name.currentRow() + 1 and 
              cv.repeat_playlist == 1):
            cv.active_pl_name.setCurrentRow(self.av_player.played_row + 1)
            self.play_track()
        # PLAYING THE LAST TRACK - REPEAT PL     
        elif (cv.active_pl_name.count() == cv.active_pl_name.currentRow() + 1 and
            cv.repeat_playlist == 2):
                cv.active_pl_name.setCurrentRow(0)
                self.play_track()
        # PLAYING THE LAST TRACK - REPEAT SINGLE TRACK    
        elif cv.repeat_playlist == 0:
            self.av_player.player.setPosition(0)
            self.av_player.player.play()
        # CURRENT TRACK BACK TO START         
        else:
            self.av_player.player.setPosition(0)


    def auto_play_next_track(self):
        if self.av_player.base_played:   # avoiding the dummy song played when the class created
            if self.av_player.player.mediaStatus() == self.av_player.player.MediaStatus.EndOfMedia:

                self.play_next_track()
        else:
            self.av_player.base_played = True    
           