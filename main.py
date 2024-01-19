
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QSplitter
    )
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut


from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl, QEvent, Qt
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget

import sys
import ctypes
from src import Path

from src import cv, inactive_track_font_style
from src import MySlider, MyVolumeSlider, MySettingsWindow 
from src import MyButtons, PlaysFunc, MyImage, MyTabs
from src import update_and_save_volume_slider_value, generate_duration_to_display
from src import update_raw_current_duration_db



"""
PLAY EMPTY SOUND WORKAROUND
at least one music file need to be played from start to finish
before be able to switch tracks without crashing
--> class instance creation = dummy "song" played
"""
class AVPlayer(QWidget):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        # VIDEO
        self.video_output = QVideoWidget()
        self.video_output.installEventFilter(self)
        self.player.setVideoOutput(self.video_output)
        # AUDIO
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        # BASE PLAY
        self.player.setSource(QUrl.fromLocalFile('skins/base.mp3'))
        self.player.play()
        # SETTINGS
        self.base_played = False    # 1st auto_play_next_track() run --> base_played = True
        self.audio_output.setVolume(cv.volume)
        self.paused = False
        self.playlist_visible = True
        self.video_area_visible = True

    
    ''' FOR FULL SCREEN MODE '''
    def eventFilter(self, source, event):

        if source == self.video_output and event.type() == QEvent.Type.MouseButtonDblClick:
            self.full_screen_toggle()

        if event.type() == QEvent.Type.KeyRelease:

            # EXIT FULL SCREEN
            if event.key() == Qt.Key.Key_Escape:
                self.video_output.setFullScreen(0)
                
        return super().eventFilter(source, event)


    def full_screen_toggle(self):
        if self.video_output.isVisible():
            if self.video_output.isFullScreen():
                self.video_output.setFullScreen(0)
            else:
                self.video_output.setFullScreen(1)


    # SCREEN SAVER SETTINGS UPDATE
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



""" 
    Only used for duration calculation -->
    Adding small amount of new record/track:
        Able to add new tracks without interrupting the current playing
    Adding big amount of new record/track:
        Video frame lagging while the new tracks are loading
        No interruption in the sound
"""
class TrackDuration(QWidget):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()


''' 
    APP

    LEARNED:
    No eventFilter on the app(QApplication)
    otherwise: keyRelease --> multiple trigger

'''
app = QApplication(sys.argv)


''' WINDOW '''
# WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 500
# WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT = 650, 250
WINDOW_MIN_WIDTH_NO_VID, WINDOW_MIN_HEIGHT_NO_VID = 650, 180

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()

        hotkeys_action_dic = {
        'small_jump_backward': self.small_jump_back_action,
        'small_jump_forward': self.small_jump_forward_action,
        'medium_jump_backward': self.medium_jump_back_action,
        'medium_jump_forward': self.medium_jump_forward_action,
        'big_jump_backward': self.big_jump_back_action,
        'big_jump_forward': self.big_jump_forward_action,
        'volume_mute': self.volume_mute_action,
        'volume_up': self.volume_up_action,
        'volume_down': self.volume_down_action,
        'audio_tracks_rotate': self.audio_tracks_rotate_action,
        'subtitle_tracks_rotate': self.subtitle_tracks_rotate_action,
        'play_pause': self.play_pause_action,
        'previous_track': self.play_prev_track_action,
        'next_track': self.play_next_track_action,
        'repeat_track_playlist_toggle': self.repeat_track_playlist_toggle_action,
        'shuffle_playlist_toggle': self.shuffle_playlist_toggle_action,
        'full_screen_toggle': self.full_screen_toggle_action,
        'playlist_toggle': self.playlist_toggle_action,
        'window_size_toggle': self.window_size_toggle_action,
        }

        for index, hotkey in enumerate(cv.hotkeys_list):
            hotkey_value = cv.hotkey_settings_dic[hotkey]['value']
            hotkey = QShortcut(QKeySequence(hotkey_value), self)
            hotkey.setContext(Qt.ShortcutContext.ApplicationShortcut)
            hotkey.activated.connect(hotkeys_action_dic[cv.hotkeys_list[index]])
    
   
    def small_jump_back_action(self):
        av_player.player.setPosition(av_player.player.position() - cv.small_jump)

    def small_jump_forward_action(self):
        av_player.player.setPosition(av_player.player.position() + cv.small_jump)

    def medium_jump_back_action(self):
        av_player.player.setPosition(av_player.player.position() - cv.medium_jump)

    def medium_jump_forward_action(self):
        av_player.player.setPosition(av_player.player.position() + cv.medium_jump)

    def big_jump_back_action(self):
        av_player.player.setPosition(av_player.player.position() - cv.big_jump)

    def big_jump_forward_action(self):
        av_player.player.setPosition(av_player.player.position() + cv.big_jump)

    def play_pause_action(self):
        button_play_pause.button_play_pause_clicked()

    def play_prev_track_action(self):
        button_prev_track.button_prev_track_clicked()
    
    def play_next_track_action(self):
        button_next_track.button_next_track_clicked()

    def volume_mute_action(self):
        button_speaker_clicked()

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
        av_player.audio_output.setVolume(new_volume)
        button_speaker_update()
        update_and_save_volume_slider_value(new_volume, volume_slider)

    def audio_tracks_rotate_action(self):
        play_funcs.audio_tracks_play_next_one()
    
    def subtitle_tracks_rotate_action(self):
        play_funcs.subtitle_tracks_play_next_one()
    
    def full_screen_toggle_action(self):
        av_player.full_screen_toggle()

    def repeat_track_playlist_toggle_action(self):
        button_toggle_repeat_pl.button_toggle_repeat_pl_clicked()

    def shuffle_playlist_toggle_action(self):
        button_toggle_shuffle_pl.button_toggle_shuffle_pl_clicked()
    
    def playlist_toggle_action(self):
        button_toggle_playlist_clicked()

    def window_size_toggle_action(self):
        button_toggle_playlist_clicked()
        if cv.window_size_normal:
            cv.window_size_normal = False
            self.resize(cv.window_alt_width, cv.window_alt_height)
        else:
            cv.window_size_normal = True
            self.resize(cv.window_width, cv.window_height)



window = MyWindow()

window.resize(cv.window_width, cv.window_height)
window.setMinimumSize(cv.window_min_width, cv.window_min_height)
window.setWindowIcon(QIcon(str(Path(Path(__file__).parent, 'skins/window_icon.png'))))
window.setWindowTitle("QTea media player")
if cv.always_on_top == 'True':
    window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

''' WINDOW SETTINGS '''
window_settings = MySettingsWindow()

''' PLAYER '''
av_player = AVPlayer()

def update_duration_info():

    if av_player.base_played:

        track_current_duration = av_player.player.position()

        # SAVING THE CURRENT DURATION EVERY 5 SEC
        if cv.continue_playback == 'True' and ((track_current_duration - cv.counter_for_duration) / 5000) >= 1:
            update_raw_current_duration_db(track_current_duration, cv.playing_track_index)
            cv.counter_for_duration = track_current_duration

        # DURATION TO DISPLAY
        cv.duration_to_display_straight = f'{generate_duration_to_display(track_current_duration)} / {cv.track_full_duration_to_display}'
        cv.duration_to_display_back = f'-{generate_duration_to_display(cv.track_full_duration - track_current_duration)} / {cv.track_full_duration_to_display}'

        if cv.is_duration_to_display_straight:
            button_duration_info.setText(cv.duration_to_display_straight)
        else:
            button_duration_info.setText(cv.duration_to_display_back)

        button_duration_info.adjustSize()
    
        # cv.prev_track_current_duration = track_current_duration

av_player.player.positionChanged.connect(update_duration_info)


""" 
    Only used for duration calculation
    more info @ class definition (main.py)
"""
av_player_duration = TrackDuration()   



''' 
########################################
        SLIDER / LOGO / PLAY FUNCS                        
########################################
'''
play_slider = MySlider(av_player)

image_logo = MyImage('logo.png', 200)

play_funcs = PlaysFunc(window, av_player, play_slider, image_logo, cv.playing_track_index)

''' 
#######################
        BUTTONS              
#######################
'''

''' 
    PLAYLIST SECTION
'''
PLIST_BUTTONS_WIDTH = 32
PLIST_BUTTONS_HEIGHT = 30
PLIST_BUTTONS_X_DIFF = 4    # FOR SELECTING ADD AND REMOVE BUTTONS
PLIST_BUTTONS_X_BASE = 0
PLIST_BUTTONS_Y = 3

def button_x_pos(num):
    return PLIST_BUTTONS_X_BASE + (PLIST_BUTTONS_WIDTH + 6) * num

def update_duration_sum_widg():
    duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))


''' BUTTON PLAYLIST - ADD TRACK '''
def button_add_track_clicked():
    button_add_track.button_add_track_clicked()
    update_duration_sum_widg()

button_add_track = MyButtons(
    'AT',
    'Add Track',
    av_player,
    av_player_duration,
    )
button_add_track.setGeometry(button_x_pos(0), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_add_track.clicked.connect(button_add_track_clicked)


''' BUTTON PLAYLIST - ADD DIRECTORY '''
def button_add_dir_clicked():
    button_add_dir.button_add_dir_clicked()
    update_duration_sum_widg()

button_add_dir = MyButtons(
    'AD',
    'Add Directory',
    av_player,
    av_player_duration,
    )
button_add_dir.setGeometry(button_x_pos(1)-PLIST_BUTTONS_X_DIFF, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_add_dir.clicked.connect(button_add_dir_clicked)


''' BUTTON PLAYLIST - REMOVE TRACK '''
def button_remove_track_clicked():
    if cv.active_pl_name.currentRow() > -1:
        button_remove_track.button_remove_track_clicked()
        update_duration_sum_widg()

button_remove_track = MyButtons(
    'RT',
    'Remove track'
    )
button_remove_track.setGeometry(button_x_pos(2), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_remove_track.clicked.connect(button_remove_track_clicked)


''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
def button_remove_all_track_clicked():
    button_remove_all_track.button_remove_all_track_clicked()
    cv.paylist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = 0
    cv.active_pl_sum_duration = 0
    update_duration_sum_widg()

button_remove_all_track = MyButtons(
    'CP',
    'Clear Playlist'
    )
button_remove_all_track.setGeometry(button_x_pos(3)-PLIST_BUTTONS_X_DIFF, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_remove_all_track.clicked.connect(button_remove_all_track_clicked)


''' BUTTON PLAYLIST - SETTINGS '''
button_settings = QIcon(f'skins/{cv.skin_selected}/settings.png')

def button_settings_clicked():
    window_settings.show()

button_settings = MyButtons(
    'SE',
    'Settings',
    icon = button_settings
    )
button_settings.setGeometry(button_x_pos(4), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_settings.clicked.connect(button_settings_clicked)
button_settings.set_style_settings_button()


''' 
    PLAYLIST BUTTONS LIST
    used to add widgets to the layout
'''
playlist_buttons_list = [
    button_add_track,
    button_add_dir,
    button_remove_track,
    button_remove_all_track,
    button_settings
                    ]




'''
    PLAY SECTION
'''
PLAY_BUTTONS_WIDTH = 32
PLAY_BUTTONS_HEIGHT = 32

def play_buttons_x_pos(num):
    return int((PLAY_BUTTONS_WIDTH) * num)


''' BUTTON PLAY SECTION - PLAY / PAUSE '''
''' BUTTON - MUSIC '''
button_image_start = QIcon(f'skins/{cv.skin_selected}/start.png')
button_image_pause = QIcon(f'skins/{cv.skin_selected}/pause.png')
button_image_stop = QIcon(f'skins/{cv.skin_selected}/stop.png')
button_image_prev = QIcon(f'skins/{cv.skin_selected}/previous.png')
button_image_next = QIcon(f'skins/{cv.skin_selected}/next.png')
button_image_repeat = QIcon(f'skins/{cv.skin_selected}/repeat.png')
button_image_repeat_single = QIcon(f'skins/{cv.skin_selected}/repeat_single.png')
button_image_shuffle = QIcon(f'skins/{cv.skin_selected}/shuffle.png')


button_image_toggle_vid = QIcon(f'skins/{cv.skin_selected}/toggle_vid.png')
button_image_toggle_playlist = QIcon(f'skins/{cv.skin_selected}/toggle_playlist.png')



''' BUTTON PLAY SECTION - PLAY/PAUSE '''
button_play_pause = MyButtons(
    'PLAY/PAUSE',
    'Start/stop playing',
    av_player,
    av_player_duration,
    play_funcs,
    button_image_start,
    )
button_play_pause.clicked.connect(button_play_pause.button_play_pause_clicked)
button_play_pause.setGeometry(0, 0, PLAY_BUTTONS_WIDTH+4, PLAY_BUTTONS_HEIGHT+4)
button_play_pause.setIconSize(QSize(cv.icon_size + 5, cv.icon_size + 5))


''' BUTTON PLAY SECTION - STOP '''
def button_stop_clicked():
    av_player.player.stop()
    av_player.paused = False
    button_play_pause.setIcon(button_image_start)
    av_player.screen_saver_on()


button_stop = MyButtons(
    'Stop',
    'Stops playing',
    av_player,
    av_player_duration,
    play_funcs,
    button_image_stop
    )
button_stop.setGeometry(play_buttons_x_pos(1.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_stop.clicked.connect(button_stop_clicked)
button_stop.setIconSize(QSize(cv.icon_size, cv.icon_size))


''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
button_prev_track = MyButtons(
    'Prev',
    'Previous track',
    av_player,
    av_player_duration,
    play_funcs,
    button_image_prev
    )
button_prev_track.setGeometry(play_buttons_x_pos(2.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_prev_track.clicked.connect(button_prev_track.button_prev_track_clicked)


''' BUTTON PLAY SECTION - NEXT TRACK '''
button_next_track = MyButtons(
    'Next',
    'Next track',
    av_player,
    av_player_duration,
    play_funcs,
    button_image_next
    )
button_next_track.setGeometry(play_buttons_x_pos(3.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_next_track.clicked.connect(button_next_track.button_next_track_clicked)


''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
button_toggle_repeat_pl = MyButtons(
    'Tog Rep PL',
    'Toggle Repeat Playlist',
    icon = button_image_repeat
    )
button_toggle_repeat_pl.setGeometry(play_buttons_x_pos(5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_repeat_pl.clicked.connect(button_toggle_repeat_pl.button_toggle_repeat_pl_clicked)

if cv.repeat_playlist == 2:
    button_toggle_repeat_pl.setFlat(1)
elif cv.repeat_playlist == 0:
    button_toggle_repeat_pl.setFlat(1)
    button_toggle_repeat_pl.setIcon(button_image_repeat_single)


''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
button_toggle_shuffle_pl = MyButtons(
    'Shuffle PL',
    'Toggle Shuffle Playlist',
    icon = button_image_shuffle
    )
button_toggle_shuffle_pl.setGeometry(play_buttons_x_pos(6), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_shuffle_pl.clicked.connect(button_toggle_shuffle_pl.button_toggle_shuffle_pl_clicked)
if cv.shuffle_playlist_on:
    button_toggle_shuffle_pl.setFlat(1)


''' BUTTON PLAY SECTION - TOGGLE PLAYLIST '''
def button_toggle_playlist_clicked():

    if av_player.playlist_visible and av_player.video_area_visible:
        layout_vert_right_qframe.hide()
        av_player.playlist_visible = False
        button_toggle_video.setDisabled(1)
    else:
        layout_vert_right_qframe.show()
        av_player.playlist_visible = True
        button_toggle_video.setDisabled(0)    

button_toggle_playlist = MyButtons(
    'Shuffle PL',
    'Toggle Show Playlists',
    icon = button_image_toggle_playlist
    )
button_toggle_playlist.setGeometry(play_buttons_x_pos(7), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_playlist.clicked.connect(button_toggle_playlist_clicked)


''' BUTTON PLAY SECTION - TOGGLE VIDEO '''
def button_toggle_video_clicked():
    
    if av_player.playlist_visible and av_player.video_area_visible:
        layout_vert_left_qframe.hide()
        av_player.video_area_visible = False
        window.resize(int(cv.window_width/3), window.geometry().height())
        window.setMinimumSize(WINDOW_MIN_WIDTH_NO_VID, WINDOW_MIN_HEIGHT_NO_VID)
        button_toggle_playlist.setDisabled(1)
    else:
        window.resize(cv.window_width, window.geometry().height())
        window.setMinimumSize(cv.window_min_width, cv.window_min_height)
        layout_vert_left_qframe.show()
        av_player.video_area_visible = True
        button_toggle_playlist.setDisabled(0)

button_toggle_video = MyButtons(
    'Shuffle PL',
    'Toggle Show Video Window',
    icon = button_image_toggle_vid
    )
button_toggle_video.setGeometry(play_buttons_x_pos(8), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_video.clicked.connect(button_toggle_video_clicked)


''' BUTTON PLAY SECTION - DURATION INFO '''
def button_duration_info_clicked():
    if cv.track_full_duration_to_display:
        if cv.is_duration_to_display_straight:
            cv.is_duration_to_display_straight = False
            button_duration_info.setText(cv.duration_to_display_back)

        else:
            cv.is_duration_to_display_straight = True
            button_duration_info.setText(cv.duration_to_display_straight)
        
        button_duration_info.adjustSize()


button_duration_info = MyButtons(
    '00:00 / 00:00',
    'Click to switch',
    )
button_duration_info.move(play_buttons_x_pos(9.5), 0)
button_duration_info.clicked.connect(button_duration_info_clicked)
button_duration_info.set_style_duration_info_button()


''' 
    PLAY BUTTONS LIST
    without the speaker/mute button
    used to add widgets to the layout
'''
play_buttons_list = [
    button_play_pause,
    button_stop,
    button_prev_track,
    button_next_track,
    button_toggle_repeat_pl,
    button_toggle_shuffle_pl,
    button_toggle_playlist,
    button_toggle_video,
    button_duration_info
]



''' BUTTON PLAY SECTION - SPEAKER/MUTE '''
button_image_speaker = QIcon(f'skins/{cv.skin_selected}/speaker.png')
button_image_speaker_muted = QIcon(f'skins/{cv.skin_selected}/speaker_muted.png')


def button_speaker_clicked():

    if cv.is_speaker_muted:
        cv.is_speaker_muted = False
        button_speaker.setIcon(button_image_speaker)
        av_player.audio_output.setVolume(cv.volume)

    else:
        cv.is_speaker_muted = True
        button_speaker.setIcon(button_image_speaker_muted)
        av_player.audio_output.setVolume(0)


# USED WHEN CHANGING VOLUME WHILE MUTED
# WITHOUT THE SPEAKER BUTTON - SLIDER, HOTKEYS
def button_speaker_update():
    if cv.is_speaker_muted:
        cv.is_speaker_muted = False
        button_speaker.setIcon(button_image_speaker)


button_speaker = MyButtons(
    'Speaker',
    'Toggle Mute',
    icon = button_image_speaker
    )
button_speaker.setFlat(1)
button_speaker.clicked.connect(button_speaker_clicked)



''' 
######################
        LAYOUTS                          
######################

LEARNED:
1,              
    Do not mix widgets and layouts in a layout
    Hiding the widget --> layout disapears too
2,
    Layout add to QFrame --> hiding QFrame hides the layout
    Not able to hide Layout by itself
3,
    Alignment should be in the widget
    Not in the Layout -->
    Made the av_player.video_output invisible

GUIDE:

  BASE
    LEFT      RIGHT  
    -----------------
    |       ||       |
    |       || PLIST |  TOP
    |  VID  ||_______|  
    |_______||___|___|
    |________________|  BOTTOM
    |________|_______|  
'''


layout_base = QVBoxLayout(window)
layout_base.setContentsMargins(0, 0, 0, 0)

layout_hor_top = QHBoxLayout()
layout_hor_top.setSpacing(0)

layout_bottom_slider = QVBoxLayout()
layout_bottom_slider.setContentsMargins(9, 0, 9, 0)

layout_bottom_wrapper = QHBoxLayout()
layout_bottom_wrapper.setContentsMargins(9, 0, 9, 0)

layout_base.addLayout(layout_hor_top, 90)
layout_base.addLayout(layout_bottom_slider, 5)
layout_base.addLayout(layout_bottom_wrapper, 5)


''' SPLITTER - LEFT / RIGHT'''
splitter_left_right = QSplitter(Qt.Orientation.Horizontal)
layout_hor_top.addWidget(splitter_left_right)


''' TOP LEFT - VIDEO / QTEA LOGO '''
layout_vert_left = QVBoxLayout() # here layout type is not relevant
layout_vert_left.setContentsMargins(0, 0, 0, 0)
layout_vert_left_qframe = QFrame()
layout_vert_left_qframe.setLayout(layout_vert_left)

''' TOP RIGHT - PLAYLIST / BUTTONS / DURATION '''
layout_vert_right = QVBoxLayout() # here layout type is not relevant
layout_vert_right.setContentsMargins(5, 0, 4, 0)
layout_vert_right_qframe = QFrame()
layout_vert_right_qframe.setLayout(layout_vert_right)
layout_vert_right_qframe.setMinimumWidth(cv.window_min_width-200)


splitter_left_right.addWidget(layout_vert_left_qframe)
splitter_left_right.addWidget(layout_vert_right_qframe)
splitter_left_right.setStretchFactor( 0, 3)
splitter_left_right.setStretchFactor( 1, 1)



''' TOP RIGHT 
_____________
|           |
|   PLIST   |
|___________|
|_BU__|__DU_|

'''

# PLAYLIST
layout_playlist = QVBoxLayout()
layout_vert_right.addLayout(layout_playlist)

# UNDER PLAYLIST
layout_under_playlist_wrapper = QHBoxLayout()
layout_under_playlist_wrapper.setContentsMargins(5, 0, 18, 0)

layout_under_playlist_buttons = QHBoxLayout()

layout_under_playlist_duration = QVBoxLayout()
layout_under_playlist_duration.setAlignment(Qt.AlignmentFlag.AlignRight)

layout_under_playlist_wrapper.addLayout(layout_under_playlist_buttons)
layout_under_playlist_wrapper.addLayout(layout_under_playlist_duration)

layout_vert_right.addLayout(layout_under_playlist_wrapper)


''' ADDING WIDGETS'''
''' TOP LEFT '''
layout_vert_left.addWidget(av_player.video_output)
av_player.video_output.hide()
layout_vert_left.addWidget(image_logo)


''' TOP RIGHT '''
# BUTTONS
playlist_buttons_list_wrapper = QFrame()
playlist_buttons_list_wrapper.setFixedSize(250, PLIST_BUTTONS_HEIGHT+5)

for button in playlist_buttons_list:
    button.setParent(playlist_buttons_list_wrapper)
    if button != button_settings:
        button.set_style_playlist_buttons()


layout_under_playlist_buttons.addWidget(playlist_buttons_list_wrapper)

# DURATION
duration_sum_widg = QPushButton('DURATION')
duration_sum_widg.setDisabled(1)
duration_sum_widg.setFont(inactive_track_font_style)
layout_under_playlist_duration.addWidget(duration_sum_widg)

# TABS
tabs_playlist = MyTabs(button_play_pause.button_play_pause_via_list, duration_sum_widg)
layout_playlist.addWidget(tabs_playlist)


''' BOTTOM '''
# SLIDER
layout_bottom_slider.addWidget(play_slider)

# LAYOUT BUTTONS / VOLUME
layout_bottom_buttons = QVBoxLayout()
layout_bottom_volume = QHBoxLayout()
layout_bottom_volume.setAlignment(Qt.AlignmentFlag.AlignTop)

layout_bottom_wrapper.addLayout(layout_bottom_buttons, 80)
layout_bottom_wrapper.addLayout(layout_bottom_volume, 20)

# WIDGETS
# SPEAKER/MUTE BUTTON CREATED EARLIER
volume_slider = MyVolumeSlider(av_player, button_speaker_update)
volume_slider.setFixedSize(100,30)


# BUTTONS WRAPPER
play_buttons_list_wrapper= QFrame()
play_buttons_list_wrapper.setFixedHeight(50)
for button in play_buttons_list:
    button.setParent(play_buttons_list_wrapper)


layout_bottom_buttons.addWidget(play_buttons_list_wrapper)
layout_bottom_volume.addWidget(button_speaker, alignment=Qt.AlignmentFlag.AlignRight)
layout_bottom_volume.addWidget(volume_slider)


window.show()

sys.exit(app.exec())