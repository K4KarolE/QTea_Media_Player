''' AVPlayer and TrackDuration classes creation '''

from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl, QEvent, Qt, QTimer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtGui import QAction

import ctypes

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    update_raw_current_duration_db,
    generate_duration_to_display
    )


'''
The .av_player.player.mediaStatusChanged signal to
autoplay next track is declared in src / func_play_coll.py


PLAY EMPTY SOUND WORKAROUND
- At least one file needs to be played from start to finish
before be able to switch tracks without crashing:
    - At the AVPlayer class instance creation, dummy "song" loaded, played (<1s, no sound)
    - After the 1st dummy track played, no error while switching media
Tried to fix/test:
    - Created an "empty" script to exclude possible errors on my side(like: docs/learning), same behaviour
    - Checked online sources and GitHub repos, but the class creation steps look the same
'''
class AVPlayer(QWidget):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        # VIDEO
        self.video_output = QVideoWidget()
        self.video_output.installEventFilter(self)
        self.player.setVideoOutput(self.video_output)
        self.timer = QTimer()   # used to display volume, track title on video
        # AUDIO
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        # BASE PLAY
        self.player.setSource(QUrl.fromLocalFile('skins/base.mp3'))
        self.player.play()
        # SIGNALS
        self.player.positionChanged.connect(self.update_duration_info)
        # SETTINGS
        self.base_played = False    # 1st auto_play_next_track() run --> base_played = True
        self.audio_output.setVolume(cv.volume)
        self.paused = False
        self.playlist_visible = True
        self.video_area_visible = True
        self.context_menu_dic = { 
            'Play / Pause': {'icon': br.icon.start},
            'Stop': {'icon': br.icon.stop},
            'Previous':{'icon': br.icon.previous},
            'Next':{'icon': br.icon.next},
            'Mute - Toggle':{'icon': br.icon.speaker},
            'Alter - Toggle':{'icon': br.icon.alter},
            'Audio Track': {
                'icon': None,
                'menu_sub': '',
                'audio_tracks': [],
                },
            'Subtitle': {
                'icon': None,
                'menu_sub': '',
                'subtitle_tracks': [],
                }
            }    



    def eventFilter(self, source, event):

        if source == self.video_output:
            if event.type() == QEvent.Type.ContextMenu:
                
                menu = QMenu()

                # MENU ITEMS
                for menu_title, menu_icon in self.context_menu_dic.items():
                    icon = menu_icon['icon']
                    if icon:
                        menu.addAction(QAction(icon, menu_title, self))
                    else:
                        self.context_menu_dic[menu_title]['menu_sub'] = menu.addMenu(menu_title)


                # AUDIO TRACKS
                for audio_track in self.player.audioTracks():

                    audio_track_title = self.generate_audio_track_title(audio_track)
                    
                    if self.player.activeAudioTrack() == self.player.audioTracks().index(audio_track):
                        qaction_to_add = QAction(br.icon.selected, audio_track_title, self)
                    else:
                        qaction_to_add = QAction(audio_track_title, self)
                    self.context_menu_dic['Audio Track']['menu_sub'].addAction(qaction_to_add)
                    self.context_menu_dic['Audio Track']['audio_tracks'].append(audio_track_title)


                # SUBTITLE TRACKS
                if self.player.activeSubtitleTrack() == -1:
                    qaction_to_add = QAction(br.icon.selected, 'Disabled', self)
                else:
                    qaction_to_add = QAction('Disable', self)
                self.context_menu_dic['Subtitle']['menu_sub'].addAction(qaction_to_add)

                for sub_track in self.player.subtitleTracks():
                    subtitle_track_title = self.generate_subtitle_track_title(sub_track)

                    if self.player.activeSubtitleTrack() == self.player.subtitleTracks().index(sub_track):
                        qaction_to_add = QAction(br.icon.selected, subtitle_track_title, self)
                    else:
                        qaction_to_add = QAction(subtitle_track_title, self)
                        
                    self.context_menu_dic['Subtitle']['menu_sub'].addAction(qaction_to_add)
                    self.context_menu_dic['Subtitle']['subtitle_tracks'].append(subtitle_track_title)

                menu.triggered[QAction].connect(self.context_menu_clicked)
                menu.exec(event.globalPos())
      
            # FULL SCREEN TOGGLE 
            elif event.type() == QEvent.Type.MouseButtonDblClick:
                self.full_screen_toggle()
            
            # VOLUME UPDATE
            elif event.type() == QEvent.Type.Wheel:
                if event.angleDelta().y() > 0:
                    br.window.volume_up_action()
                else:
                    br.window.volume_down_action()

        # EXIT FULL SCREEN
        if event.type() == QEvent.Type.KeyRelease:
            if event.key() == Qt.Key.Key_Escape:
                self.video_output.setFullScreen(0)
                self.video_output.setCursor(Qt.CursorShape.ArrowCursor)
                
        return super().eventFilter(source, event)



    def context_menu_clicked(self, q):
        audio_tracks_list = self.context_menu_dic['Audio Track']['audio_tracks']
        subtitle_tracks_list = self.context_menu_dic['Subtitle']['subtitle_tracks']

        if q.text() == list(self.context_menu_dic)[0]:
            br.button_play_pause.button_play_pause_clicked()
        elif q.text() == list(self.context_menu_dic)[1]:
            br.button_stop.button_stop_clicked()
        elif q.text() == list(self.context_menu_dic)[2]:
            br.button_prev_track.button_prev_track_clicked()
        elif q.text() == list(self.context_menu_dic)[3]:
            br.button_next_track.button_next_track_clicked()
        elif q.text() == list(self.context_menu_dic)[4]:
            br.button_queue.button_speaker_clicked()
        elif q.text() == list(self.context_menu_dic)[5]:
            br.window.window_size_toggle_action()
        
        elif q.text() in audio_tracks_list:
            self.player.setActiveAudioTrack(audio_tracks_list.index(q.text()))
            cv.audio_track_played = audio_tracks_list.index(q.text())
            audio_tracks_list.clear()

        elif q.text() in subtitle_tracks_list or q.text() == 'Disable':
            if q.text() in subtitle_tracks_list:
                subtitle_track_index = subtitle_tracks_list.index(q.text())
            else:
                subtitle_track_index = -1   # -1: disable subtitle
    
            self.player.setActiveSubtitleTrack(subtitle_track_index)
            cv.subtitle_track_played = subtitle_track_index
            subtitle_tracks_list.clear()


    def generate_subtitle_track_title(self, sub_track):
        ''' QMediaMetaData --> Subtitle track info
            Examples:
                Hungarian - forced[sub]
                Hungarian - [sub]
                English - [sub]
                English - SDH[sub]
        '''
        title = sub_track.stringValue(sub_track.Key.Title)
        subtitle_language = sub_track.stringValue(sub_track.Key.Language)
        
        if title:
            subtitle_track_title = f'{subtitle_language} - {title} [sub]'
        else:
            subtitle_track_title = f'{subtitle_language} - [sub]'
        return subtitle_track_title


    def generate_audio_track_title(self, audio_track):
        ''' QMediaMetaData --> Audio track info
            Examples:
                Hungarian - AC3 5.1 @ 448 kbps
                English - DTS 5.1 @ 1510 kbps
        '''
        title = audio_track.stringValue(audio_track.Key.Title)
        audio_language = audio_track.stringValue(audio_track.Key.Language)
        
        if title:
            audio_track_title = f'{audio_language} - {title}'
        else:
            audio_track_title = audio_language
        return audio_track_title


    def full_screen_toggle(self):
        if self.video_output.isVisible():
            if self.video_output.isFullScreen():
                self.video_output.setFullScreen(0)
                self.video_output.setCursor(Qt.CursorShape.ArrowCursor)
            else:
                self.video_output.setFullScreen(1)
                self.video_output.setCursor(Qt.CursorShape.BlankCursor)
    

    def text_display_on_video(self, time, text):
        ''' 
            To display text as a subtitle
            Muted, Repeat, Shuffle: src / buttons.py
            Volume: src / sliders.py / MyVolumeSlider class / update_volume()
            Track title: src / func_play_coll.py / PlaysFunc class / play_track()
        '''
        self.video_output.videoSink().setSubtitleText(text)
        self.timer.start(time)
        self.timer.timeout.connect(lambda: self.video_output.videoSink().setSubtitleText(None))


    # SCREEN SAVER SETTINGS UPDATE USED IN:
    # src / func_play_coll.py / play_track()
    # src / buttons / button_play_pause_clicked()
    # main / button_stop_clicked()    
    def screen_saver_on_off(self):
        # SCREEN SAVER OFF
        if self.video_output.isVisible() and self.player.isPlaying():
            self.screen_saver_off()
        # SCREEN SAVER ON
        else:
            self.screen_saver_on()

    def screen_saver_on(self):
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
    
    def screen_saver_off(self):
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)


    def update_duration_info(self):
        if self.base_played:
            track_current_duration = self.player.position()

            # SAVING THE CURRENT DURATION EVERY 5 SEC
            if cv.continue_playback and (abs(track_current_duration - cv.counter_for_duration) / 5000) >= 1:
                update_raw_current_duration_db(track_current_duration, cv.playing_track_index)
                cv.counter_for_duration = track_current_duration

            # DURATION TO DISPLAY
            cv.duration_to_display_straight = f'{generate_duration_to_display(track_current_duration)} / {cv.track_full_duration_to_display}'
            cv.duration_to_display_back = f'-{generate_duration_to_display(cv.track_full_duration - track_current_duration)} / {cv.track_full_duration_to_display}'

            if cv.is_duration_to_display_straight:
                br.button_duration_info.setText(cv.duration_to_display_straight)
            else:
                br.button_duration_info.setText(cv.duration_to_display_back)

            br.button_duration_info.adjustSize()




""" 
Only used for duration calculation -->
Adding small amount of new record/track:
    Able to add new tracks without interrupting the current playing
Adding big amount of new record/track while playing video:
    VIDEO frame lagging while the new tracks are loading:
        - No / minimal interruption while loading 10 seasons of a TV show
        - It takes 8+ seconds while video catches up after loading 400+ music library
    No interruption in the sound of the currently playing video or if only audio media is playing

Message example when adding files:
...
qt.multimedia.ffmpeg.mediadataholder: AVStream duration -9223372036854775808 is invalid. Taking it from the metadata
qt.multimedia.ffmpeg.mediadataholder: AVStream duration -9223372036854775808 is invalid. Taking it from the metadata
[AVHWFramesContext @ 000001B939AE5AC0] Static surface pool size exceeded.
[h264 @ 000001B93D732280] get_buffer() failed
[h264 @ 000001B93D732280] thread_get_buffer() failed
[h264 @ 000001B93D732280] decode_slice_header error
[h264 @ 000001B93D732280] no frame!

    
LEARNED:
QWidget can not be created earlier than the app = QApplication(sys.argv)
"""
class TrackDuration(QWidget):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()