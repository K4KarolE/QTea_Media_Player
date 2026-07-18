""" AVPlayer and TrackDuration classes """

from PyQt6.QtMultimedia import (
    QAudioOutput,
    QMediaDevices,
    QMediaMetaData,
    QMediaPlayer
    )
from PyQt6.QtCore import QUrl, QEvent, Qt, QTimer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtGui import QAction

import ctypes
import os
import sys


from .class_bridge import br
from .class_data import cv
from .func_coll import (
    generate_duration_to_display,
    play_track_with_default_player_via_context_menu,
    toggle_minimal_interface,
    update_raw_current_duration_db
    )
from .logger import logger, logger_runtime, logger_sum
from .message_box import MyMessageBoxError

"""
PLAY EMPTY SOUND WORKAROUND (self.base_played)
At least one media file needs to be played from start to
finish before be able to switch tracks without crashing:
    - Once the app is running >> "src / application / applicationStateChanged signal
        >> application_state_changed_action() / br.av_player.set_base_track_as_source() 
        >> the dummy "song" loaded, played (<1s, no sound)
    - After the 1st dummy track played, no error while switching media

The same issue, another workaround in Jarod Mica's GitHub/PySide6 repo:
https://github.com/JarodMica/audiobook_maker/blob/5790f7eeb2eaa4b2ccd92ba497ba75f61ba9ab64/src/view.py#L1685

From the above repo:
def release_media_player_resources(self):
    # Reinitialize the media player to release any file handles
    # This way is NECESSARY to prevent the gui from freezing (for some unknown reason)
    self.media_player = QMediaPlayer()
    self.audio_output = QAudioOutput()
    self.media_player.setAudioOutput(self.audio_output)
    self.media_player.mediaStatusChanged.connect(self.on_audio_finished)
"""
@logger_runtime
class AVPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.media_devices = QMediaDevices()
        # VIDEO
        self.video_output = QVideoWidget()
            # Window flag:
            # To make sure on Linux / full screen mode:
            # the app is not visible, just the full-screened video
        self.video_output.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.video_output.installEventFilter(self)
        self.player.setVideoOutput(self.video_output)
        self.timer = QTimer()   # used to display volume, track title on video
        # AUDIO
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(cv.volume)
        # BASE PLAY - more info in above
        self.base_played = False
        self.base_played_end_of_media_signal_ignored = False
        self.media_status_loaded_media_signal_counter: int = 1 # playing track >> setSource(track path) >> LoadedMedia signal fires twice
        # SIGNALS (more signals below)
        self.media_devices.audioOutputsChanged.connect(lambda: self.set_audio_output())
        self.player.positionChanged.connect(self.update_duration_info)
        self.player.mediaStatusChanged.connect(lambda: self.media_status_changed_action())
        # SETTINGS
        self.paused = False
        self.is_end_of_media = False
        self.playlist_visible = True
        self.video_area_visible = True
        self.vid_width = None
        self.vid_height = None
        # SCREEN UPDATE HANDLING
        self.primary_screen_changed = False
        br.app.primaryScreenChanged.connect(lambda: self.screen_primary_changed())
        br.app.screenRemoved.connect(lambda: self.screen_back_to_default())
        # CONTEXT MENU
        self.audio_track_menu_title = f'Audio Track  ({cv.audio_tracks_rotate})'
        self.audio_device_menu_title = f'Audio Device  ({cv.audio_output_device_rotate})'
        self.subtitle_track_menu_title = f'Subtitle  ({cv.subtitle_tracks_rotate})'
        self.full_screen_menu_title = f'Full Screen ({cv.full_screen_toggle})'
        # CONTEXT MENU
        # The "Play/Pause" context menu ('Temp_play_pause_title' in the dic.) title and icon are generated in the
        # "eventFilter()" below, depend on the current track's playing state
        self.context_menu_dic = {
            'Temp_play_pause_title': {'icon': None},
            'Stop': {'icon': br.icon.stop},
            'Previous': {'icon': br.icon.previous},
            'Next': {'icon': br.icon.next},
            f'Mute - Toggle  ({cv.volume_mute})':{'icon': br.icon.speaker},
            f'Alter - Toggle  ({cv.window_size_toggle})': {'icon': br.icon.alter},
            'Play track with default player': {'icon': br.icon.start_with_default_player},
            f'Minimal Interface - Toggle  ({cv.minimal_interface_toggle})': {'icon': br.icon.minimal_interface},
            f'{self.audio_track_menu_title}': {
                'icon': None,
                'menu_sub': '',
                'audio_tracks': []
            },
            f'{self.audio_device_menu_title}': {
                'icon': None,
                'menu_sub': '',
                'audio_devices': []
            },
            f'{self.subtitle_track_menu_title}': {
                'icon': None,
                'menu_sub': '',
                'subtitle_tracks': []
            },
            f'{self.full_screen_menu_title}': {
                'icon': None,
                'menu_sub': '',
                'screens': [],
                'screens_pos_x': []
            },
            'Quit': {'icon': br.icon.quit},
        }
    @logger_runtime
    def set_base_track_as_source(self):
        """ More information above the class """
        self.player.setSource(QUrl.fromLocalFile('skins/base.mp3'))


    def is_playing_or_paused(self):
        return self.player.isPlaying() or self.paused


    def is_current_pl_playing_pl_with_playing_or_paused_state(self):
        return cv.active_db_table == cv.playing_db_table and self.is_playing_or_paused()


    def set_audio_output(self):
        """
        Triggered when the audio output device has changed
        example: speaker >> headset
        """
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(cv.volume)


    def eventFilter(self, source, event):
        """
        To compile the context menu
        Displayed once right-clicked on the active video area (video in playing or paused state)
        """
        if source == self.video_output:
            if event.type() == QEvent.Type.ContextMenu:

                menu = QMenu()

                # MENU ITEMS
                for menu_title, menu_icon in self.context_menu_dic.items():
                    if menu_title == 'Temp_play_pause_title':
                        if self.paused:
                            icon = br.icon.start
                            menu_title = 'Play'
                        else:
                            icon = br.icon.pause
                            menu_title = 'Pause'
                        menu.addAction(QAction(icon, menu_title, self))
                    else:
                        icon = menu_icon['icon']
                        if icon:
                            menu.addAction(QAction(icon, menu_title, self))
                        else:
                            self.context_menu_dic[menu_title]['menu_sub'] = menu.addMenu(menu_title)
                        # SEPARATOR
                        if menu_title.split()[0] in ['Next', 'Minimal', 'Full']:
                            menu.addSeparator()


                # AUDIO TRACKS
                counter = 0
                for audio_track in self.player.audioTracks():

                    audio_track_title = self.generate_audio_track_title(audio_track)
                    if not audio_track_title:
                        audio_track_title = f"Track {counter + 1} - No information"
                    else:
                        audio_track_title = f"Track {counter + 1} - {audio_track_title}"

                    if cv.audio_track_played == counter:
                        qaction_to_add = QAction(br.icon.selected, audio_track_title, self)
                    else:
                        qaction_to_add = QAction(audio_track_title, self)
                    self.context_menu_dic[self.audio_track_menu_title]['menu_sub'].addAction(qaction_to_add)
                    self.context_menu_dic[self.audio_track_menu_title]['audio_tracks'].append(audio_track_title)
                    counter += 1


                # AUDIO DEVICES
                counter = 0
                for audio_device in self.media_devices.audioOutputs():

                    audio_device_title = audio_device.description()
                    # "if audio_device.isDefault()" - not suitable when PC output != QTea output
                    # always the PC device will be marked as selected in the context menu
                    if audio_device == self.audio_output.device():
                        qaction_to_add = QAction(br.icon.selected, audio_device_title, self)
                    else:
                        qaction_to_add = QAction(audio_device_title, self)
                    self.context_menu_dic[self.audio_device_menu_title]['menu_sub'].addAction(qaction_to_add)
                    self.context_menu_dic[self.audio_device_menu_title]['audio_devices'].append(audio_device_title)
                    counter += 1


                # SUBTITLE TRACKS
                if self.player.activeSubtitleTrack() == -1:
                    qaction_to_add = QAction(br.icon.selected, 'Disable', self)
                else:
                    qaction_to_add = QAction('Disable', self)
                self.context_menu_dic[self.subtitle_track_menu_title]['menu_sub'].addAction(qaction_to_add)

                for sub_track in self.player.subtitleTracks():
                    subtitle_track_title = self.generate_subtitle_track_title(sub_track)

                    if self.player.activeSubtitleTrack() == self.player.subtitleTracks().index(sub_track):
                        qaction_to_add = QAction(br.icon.selected, subtitle_track_title, self)
                    else:
                        qaction_to_add = QAction(subtitle_track_title, self)

                    self.context_menu_dic[self.subtitle_track_menu_title]['menu_sub'].addAction(qaction_to_add)
                    self.context_menu_dic[self.subtitle_track_menu_title]['subtitle_tracks'].append(subtitle_track_title)


                # SCREENS
                counter = 0
                for screen in br.app.screens():
                    screen_width = screen.availableSize().width()
                    screen_height = screen.availableSize().height()
                    screen_title = f'#{counter + 1} display - {screen_width} x {screen_height}'

                    if counter == cv.screen_index_for_fullscreen:
                        qaction_to_add = QAction(br.icon.selected, screen_title, self)
                    else:
                        qaction_to_add = QAction(screen_title, self)
                    self.context_menu_dic[self.full_screen_menu_title]['menu_sub'].addAction(qaction_to_add)
                    self.context_menu_dic[self.full_screen_menu_title]['screens'].append(screen_title)

                    screen_pos_x = screen.availableGeometry().x()
                    self.context_menu_dic[self.full_screen_menu_title]['screens_pos_x'].append(screen_pos_x)

                    counter +=1


                menu.triggered[QAction].connect(self.context_menu_clicked)
                menu.exec(event.globalPos())


            # FULL SCREEN TOGGLE 
            elif event.type() == QEvent.Type.MouseButtonDblClick:
                self.full_screen_onoff_toggle()

            # VOLUME UPDATE
            elif event.type() == QEvent.Type.Wheel:
                if event.angleDelta().y() > 0:
                    br.window.volume_up_action()
                else:
                    br.window.volume_down_action()

        # EXIT FULL SCREEN
        if event.type() == QEvent.Type.KeyRelease:
            if event.key() == Qt.Key.Key_Escape:
                if not self.video_area_visible:
                    br.button_toggle_video.button_toggle_video_clicked()
                self.video_output.setFullScreen(False)
                self.video_output.move(0, 0)
                self.video_output.setCursor(Qt.CursorShape.ArrowCursor)
                br.image_logo.hide()    # scenario: video fullscreen was on the additional display
                cv.screen_index_for_fullscreen = -1

        return super().eventFilter(source, event)



    def context_menu_clicked(self, q):
        """
        Context menu displayed once right-clicked on the active video area (video in playing or paused state)

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
        audio_tracks_list = self.context_menu_dic[self.audio_track_menu_title]['audio_tracks']
        audio_devices_list = self.context_menu_dic[self.audio_device_menu_title]['audio_devices']
        subtitle_tracks_list = self.context_menu_dic[self.subtitle_track_menu_title]['subtitle_tracks']
        screens_list = self.context_menu_dic[self.full_screen_menu_title]['screens']

        if q.text() in ['Play', 'Pause']:
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

        elif q.text() == list(self.context_menu_dic)[6]:
            try:
                play_track_with_default_player_via_context_menu(cv.playing_track_index, cv.playing_db_table)
            except:
                MyMessageBoxError(
                    'Not able to play the file',
                    'The file or the file`s home folder has been renamed / removed.  '
                )

        elif q.text() == list(self.context_menu_dic)[7]:
            toggle_minimal_interface()

        elif q.text() in audio_tracks_list:
            br.av_player.text_display_on_video(1000, q.text())
            self.player.setActiveAudioTrack(audio_tracks_list.index(q.text()))
            cv.audio_track_played = audio_tracks_list.index(q.text())
            audio_tracks_list.clear()

        elif q.text() in audio_devices_list:
            br.av_player.text_display_on_video(1000, q.text())
            audio_device_index = audio_devices_list.index(q.text())
            selected_device = self.media_devices.audioOutputs()[audio_device_index]
            self.audio_output.setDevice(selected_device)
            audio_devices_list.clear()

        elif q.text() in subtitle_tracks_list or q.text() == 'Disable':
            br.av_player.text_display_on_video(1000, q.text())
            if q.text() in subtitle_tracks_list:
                subtitle_track_index = subtitle_tracks_list.index(q.text())
            else:
                subtitle_track_index = -1   # -1: disable subtitle

            self.player.setActiveSubtitleTrack(subtitle_track_index)
            cv.subtitle_track_played = subtitle_track_index
            subtitle_tracks_list.clear()

        elif q.text() in screens_list:
            screen_selected = screens_list.index(q.text())
            if cv.screen_index_for_fullscreen != screen_selected:
                cv.screen_index_for_fullscreen = screen_selected
                screen_pos_x = self.context_menu_dic[self.full_screen_menu_title]['screens_pos_x'][screen_selected]
                if cv.os_linux:
                    app_pos_x = br.window.pos().x()
                else:
                    app_pos_x = 0
                cv.screen_pos_x_for_fullscreen_via_menu = screen_pos_x - app_pos_x
            screens_list.clear()
            self.full_screen_to_screen_toggle()

        elif q.text() == list(self.context_menu_dic)[12]:
            sys.exit()


    def generate_subtitle_track_title(self, sub_track):
        """
        QMediaMetaData --> Subtitle track info
        Examples:
            Hungarian - forced[sub]
            Hungarian - [sub]
            English - [sub]
            English - SDH[sub]
        """
        title = sub_track.stringValue(sub_track.Key.Title)
        subtitle_language = sub_track.stringValue(sub_track.Key.Language)

        if title:
            subtitle_track_title = f'{subtitle_language} - {title} [sub]'
        else:
            subtitle_track_title = f'{subtitle_language} - [sub]'
        return subtitle_track_title


    def generate_audio_track_title(self, audio_track):
        """
        QMediaMetaData --> Audio track info
        Examples:
            Hungarian - AC3 5.1 @ 448 kbps
            English - DTS 5.1 @ 1510 kbps
        """
        title = audio_track.stringValue(audio_track.Key.Title)
        audio_language = audio_track.stringValue(audio_track.Key.Language)

        if title:
            audio_track_title = f'{audio_language} - {title}'
        else:
            audio_track_title = audio_language
        return audio_track_title


    def full_screen_onoff_toggle(self):
        """ 
        Used when double-clicked on the video area
        1st "if" scenario:
            - full screen on another display
            - video area hidden in the app
        >> video area needs to be shown before moving back the video output
        br.image_logo.hide(): fullscreen video was on the additional display
        """
        if not self.video_area_visible:
            br.button_toggle_video.button_toggle_video_clicked()
        if self.video_output.isFullScreen():
            self.video_output.setFullScreen(False)
            self.video_output.move(0, 0)
            self.video_output.setCursor(Qt.CursorShape.ArrowCursor)
            cv.screen_index_for_fullscreen = -1
            br.image_logo.hide()
        else:
            self.video_output.move(cv.screen_pos_x_for_fullscreen, 5) # 2nd value !=0 all good
            self.video_output.setFullScreen(True)
            self.video_output.setCursor(Qt.CursorShape.BlankCursor)


    def full_screen_to_screen_toggle(self):
        """
        Used in the right-clicked on the
        video area / Full Screen / available screen(s)
        br.image_logo.show(): fullscreen video on the additional display
        """
        self.video_output.setFullScreen(False)
        self.video_output.move(cv.screen_pos_x_for_fullscreen_via_menu, 5) # 2nd value !=0 all good
        self.video_output.setFullScreen(True)
        br.image_logo.show()


    """
    Covering screen updates like:
    1: app on primary screen, full screen video on secondary screen
        >> secondary screen removed
    2: app on primary screen, full screen video on secondary screen
        >> primary screen removed
    """
    def screen_primary_changed(self):
        """ Triggered by the primaryScreenChanged signal """
        if not cv.os_linux:
            br.av_player = AVPlayer()
        self.primary_screen_changed = True

    def screen_back_to_default(self):
        """
        Triggered by the screenRemoved signal
        br.image_logo.show(): fullscreen video was on the additional display
        """
        if not self.primary_screen_changed:
            if self.video_output.isVisible():
                if self.video_output.isFullScreen():
                    self.video_output.setFullScreen(0)
                    self.video_output.move(0, 0)
                    self.video_output.setCursor(Qt.CursorShape.ArrowCursor)
                    br.image_logo.hide()
                    cv.screen_index_for_fullscreen = -1
        else:
            self.primary_screen_changed = False


    def text_display_on_video(self, time, text):
        """
        To display text as a subtitle
        Muted, Repeat, Shuffle: src / buttons.py
        Volume: src / sliders.py / MyVolumeSlider class / update_volume()
        Track title: src / func_play_coll.py / PlaysFunc class / play_track()
        """
        if cv.subtitle_tracks_amount: self.player.setActiveSubtitleTrack(-1)
        self.video_output.videoSink().setSubtitleText(text)
        self.timer.start(time)
        self.timer.timeout.connect(lambda: self.text_display_on_video_time_out_action())

    def text_display_on_video_time_out_action(self):
        self.video_output.videoSink().setSubtitleText(None)
        if cv.subtitle_tracks_amount: self.player.setActiveSubtitleTrack(cv.subtitle_track_played)



    # SCREEN SAVER SETTINGS UPDATE USED IN:
    # src / func_play_coll.py / play_track()
    # src / buttons / button_play_pause_clicked()
    # main / button_stop_clicked()    
    def screen_saver_on_off(self):
        # SCREEN SAVER OFF
        if self.video_output.isVisible() and self.player.isPlaying():
            self.set_screen_saver_off()
        # SCREEN SAVER ON
        else:
            self.set_screen_saver_on()

    def set_screen_saver_on(self):
        # LINUX
        if cv.screen_saver_idle_delay_default_value:
            try:
                os.system(
                    f'gsettings set org.{cv.desktop_env_for_screen_saver}.desktop.session idle-delay'
                    f' {cv.screen_saver_idle_delay_default_value}')

            except:
                logger.info('ERROR - Not able to set back the screensaver.')
        # WINDOWS
        else:
            try:
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
            except:
                logger.info('ERROR - Not able to set back the screensaver.')


    def set_screen_saver_off(self):
        # LINUX
        if cv.screen_saver_idle_delay_default_value:
            try:
                os.system(f'gsettings set org.{cv.desktop_env_for_screen_saver}.desktop.session idle-delay 0')
            except:
                logger.info('ERROR - Not able to disable the screensaver.')
        # WINDOWS
        else:
            try:
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
            except:
                logger.info('ERROR - Not able to disable the screensaver.')


    def update_duration_info(self):
        if self.base_played_end_of_media_signal_ignored:
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


    def generate_video_resolution_from_meta_data(self):
        """ The "self.player.hasVideo()" validation placed before this function is called """
        vid_res_string = self.player.metaData().stringValue(QMediaMetaData.Key.Resolution)
        vid_res_list = vid_res_string.split('x')
        if len(vid_res_list) == 2:
            self.vid_width = int(vid_res_list[0].strip())
            self.vid_height = int(vid_res_list[1].strip())
        else:
            self.vid_width, self.vid_height = None, None


    def resize_window_to_video_resolution(self):
        # cv.window_size_toggle_counter == 2: small, right-bottom corner mode
        if cv.window_auto_resize_to_video_resolution and cv.window_size_toggle_counter != 2:
            if self.vid_width and self.vid_height:
                if cv.minimal_interface_enabled:
                    br.window.resize(self.vid_width, self.vid_height)
                else:
                    # 100: height of the bottom part of the player:
                    # duration slider, volume section, control buttons
                    br.window.resize(self.vid_width, self.vid_height + 100)


    def resize_window_minimal_interface_enabled(self):
        """
        Avoiding black bars around the video area
        in the Minimal Interface mode via height
        adjusted to the window width
        In use in every "window size toggle" position
        """
        if cv.minimal_interface_enabled:
            self.resize_window_height_to_match_video_res_ratio()


    def resize_window_height_to_match_video_res_ratio(self):
        """
        Avoiding black bars around the video area
        in the Minimal Interface mode by default and
        in non Min.Int. mode via hotkey only
        """
        if cv.minimal_interface_enabled:
            player_bottom_section_height = 0
        else:
            player_bottom_section_height = 100  # duration slider, control buttons, volume section

        if self.vid_width and self.vid_height:
            resolution_ratio = self.vid_width / self.vid_height
            new_vid_height = int(br.window.width() / resolution_ratio)
            br.window.resize(br.window.width(), new_vid_height + player_bottom_section_height)


    def is_media_status_loaded(self):
        if self.player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            if self.media_status_loaded_media_signal_counter % 2 == 0:
                self.media_status_loaded_media_signal_counter += 1
                return True
            else:
                self.media_status_loaded_media_signal_counter += 1
                return False
        return False


    def is_media_status_end_of_media(self):
        return self.player.mediaStatus() == QMediaPlayer.MediaStatus.EndOfMedia


    def play_base_and_play_at_startup(self):
        if self.player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.play()
            self.base_played = True
            logger_sum('Base has been played - App is running - sum')
            if cv.play_at_startup:
                cv.ignore_loaded_media_signal = True
                logger_sum("play_base_and_play_at_startup() - before .player.stop()")
                # avoid unresponsive app at startup
                # hectic behaviour - not able replicate the frozen app at startup
                self.player.stop()
                logger_sum("play_base_and_play_at_startup() - after .player.stop()")
                self.base_played_end_of_media_signal_ignored = True
                if cv.active_pl_tracks_count:
                    logger_sum('Last media starts playing')
                    br.play_funcs.play_track()
            # Playlists creation in 3 rounds - more info in the "src / playlists"
            br.playlists_all.playlists_second_and_third_round_content_creation()


    def is_loaded_media_validation_passed(self):
        """
        cv.ignore_loaded_media_signal condition to avoid unnecessary "Media status: Loaded media" signal

        Some reason this condition can not be moved outside to the media_status_changed_action() function,
        otherwise when a repeat single track is on + one replay + play another media >> player loaded but not playing

        Mor info in media_status_changed_action() below
        """
        if self.base_played and self.is_media_status_loaded():
            if not cv.ignore_loaded_media_signal:
                return True
            else:
                cv.ignore_loaded_media_signal = False
                return False
        return False


    def is_end_of_media_validation_passed(self):
        """
        cv.ignore_loaded_media_signal condition to avoid unnecessary "Media status: Loaded media" signal

        Some reason this condition can not be moved outside to the media_status_changed_action() function,
        otherwise when a repeat single track is on + one replay + play another media >> player loaded but not playing

        Mor info in media_status_changed_action() below
        """
        if self.base_played and self.is_media_status_end_of_media():
            if not cv.ignore_loaded_media_signal:
                return True
            else:
                cv.ignore_loaded_media_signal = False
                return False
        return False


    def media_status_changed_action(self):
        """
        Where this function takes place in the play media chain:
        Start playing a track >> src / func_play_coll / PlaysFunc / play_track()
        >> br.av_player.player.setSource
        >> mediaStatusChanged signal >> MEDIA_STATUS_CHANGED_ACTION()
        ||>> PlaysFunc / play_track_second_part() includes:
            - InvalidMedia handling
            - Audio and Subtitle tracks amount creation
            - Play
            - etc.
        ||>> or PlaysFunc / play_decider() >> play_next_track()


        cv.ignore_loaded_media_signal
        As condition it is inside is_loaded_media_validation_passed() and is_end_of_media_validation_passed()
        to avoid the below scenarios where unnecessary loaded media signal is triggered:
        - playing + pause + playing again + jump via hotkey or slider click
        - or playing media stopped
        - at the end of media
        PyQt 6.11 issue / was not in PyQt 6.5.3
        """
        if self.is_loaded_media_validation_passed():
            logger_sum("Media status: Loaded media")
            # DURATION
            if cv.track_current_duration > 0 and cv.continue_playback:
                br.av_player.player.setPosition(cv.track_current_duration)
            # DURATION INFO - BUTTON
            br.button_duration_info.setEnabled(True)
            # WINDOW RESIZE
            if self.player.hasVideo():
                self.generate_video_resolution_from_meta_data()
                self.resize_window_to_video_resolution()
            else:
                self.vid_width, self.vid_height = None, None
            br.play_funcs.play_track_second_part()

        elif self.is_end_of_media_validation_passed():
            """
            self.player.stop():
            PyQt 6.11 workaround to be able to play the next track / was not needed in PyQt 6.5.3
            
            self.is_end_of_media - more info in src / func_play_coll / play_next_track()
            """
            logger_sum("Media status: End of media")
            self.player.stop()
            self.is_end_of_media = True
            br.play_funcs.play_decider()

        elif not self.base_played:
            self.play_base_and_play_at_startup()



@logger_runtime
class TrackDuration(QWidget):
    """ The class used for duration calculation only """
    def __init__(self, playlist):
        super().__init__()
        self.playlist = playlist
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(lambda: self.media_status_changed_action_duration())

    def media_status_changed_action_duration(self):
        """
        Media is loaded > duration is ready to be generated
        in the src / thread_add_media

        Invalid media status triggers once for adding multiple media at the same time
        and triggers twice for adding single media
        It is handled in the "src / thread_add_media / return_thread_generated_values"
        """
        if self.player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            cv.playlist_widget_dic[self.playlist]['add_media_thread'].return_thread_generated_values()
        elif self.player.mediaStatus() == QMediaPlayer.MediaStatus.InvalidMedia:
            cv.playlist_widget_dic[self.playlist ]['add_media_thread'].return_thread_generated_values(invalid_media = True)