'''
TERMINOLOGY
-----------
Apart from the Window Settings TABS (src / window_settings.py)
the TABS has been referred as paylists, playlist_all, playlist_index, ..

Playing playlist = playlist where the current track is in the playing or paused state
                     / playlist where the last track was played
Active playlist = playlist which is currently selected / displayed
'''

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QSplitter,
    QVBoxLayout
    )

from src import (
    cv,
    br,
    inactive_track_font_style,
    AVPlayer,
    MyButtons,
    MyIcon,
    MyImage,
    MyPlaylists,
    MyQueueWindow,
    MySettingsWindow,
    MySlider,
    MyVolumeSlider,
    MyWindow,
    PlaysFunc,
    TrackDuration,
    logger_basic
    )




logger_basic('App start')
app = QApplication(sys.argv)

br.icon = MyIcon()
br.window = MyWindow()
br.av_player = AVPlayer()
br.av_player_duration = TrackDuration()   
br.play_slider = MySlider()
br.image_logo = MyImage('logo.png', 200)
br.play_funcs = PlaysFunc()

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
    return int(PLIST_BUTTONS_X_BASE + (PLIST_BUTTONS_WIDTH + 6) * num)


''' BUTTON PLAYLIST - ADD TRACK '''
br.button_add_track = MyButtons(
    'AT',
    'Add Track'
    )
br.button_add_track.setGeometry(button_x_pos(0), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
br.button_add_track.clicked.connect(br.button_add_track.button_add_track_clicked)


''' BUTTON PLAYLIST - ADD DIRECTORY '''
br.button_add_dir = MyButtons(
    'AD',
    'Add Directory',
    )
br.button_add_dir.setGeometry(button_x_pos(1)-PLIST_BUTTONS_X_DIFF, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
br.button_add_dir.clicked.connect(lambda: br.button_add_dir.button_add_dir_clicked())   # logger decorator on func. -> lambda needed


''' BUTTON PLAYLIST - REMOVE TRACK '''
br.button_remove_track = MyButtons(
    'RT',
    'Remove track'
    )
br.button_remove_track.setGeometry(button_x_pos(2), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
br.button_remove_track.clicked.connect(br.button_remove_track.button_remove_single_track)


''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
br.button_remove_all_track = MyButtons(
    'CP',
    'Clear Playlist'
    )
br.button_remove_all_track.setGeometry(button_x_pos(3)-PLIST_BUTTONS_X_DIFF, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
br.button_remove_all_track.clicked.connect(br.button_remove_all_track.button_remove_all_track)


''' BUTTON PLAYLIST - QUEUE '''
br.button_queue = MyButtons(
    'Q',
    'Queue and Search window',
    br.icon.queue
    )
br.button_queue.setGeometry(button_x_pos(4.3), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
br.button_queue.clicked.connect(lambda: br.window_queue.show())
br.button_queue.set_style_settings_button()
br.button_queue.setIconSize(QSize(15, 15))



''' BUTTON PLAYLIST - SETTINGS '''
br.button_settings = MyButtons(
    'SE',
    'Settings window',
    br.icon.settings
    )
br.button_settings.setGeometry(button_x_pos(5.3)-PLIST_BUTTONS_X_DIFF - 6, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
br.button_settings.clicked.connect(lambda: br.button_settings.button_settings_clicked())
br.button_settings.set_style_settings_button()


''' 
    PLAYLIST BUTTONS LIST
    used to add widgets to the layout
    apart from button_queue and button_settings:
    buttons style applied in the LAYOUTS section
'''
playlist_buttons_list = [
    br.button_add_track,
    br.button_add_dir,
    br.button_remove_track,
    br.button_remove_all_track,
    br.button_queue,
    br.button_settings
                    ]




'''
####################
    PLAY SECTION
####################
'''
PLAY_BUTTONS_WIDTH = 32
PLAY_BUTTONS_HEIGHT = 32

def play_buttons_x_pos(num):
    return int((PLAY_BUTTONS_WIDTH) * num)


''' 
BUTTON PLAY SECTION - PLAY/PAUSE
The button`s icon update at startup is declared after
the playlists creation (playlists_all = MyPlaylists(..))
'''
br.button_play_pause = MyButtons(
    'PLAY/PAUSE',
    'Start/stop playing',
    br.icon.start,
    )
br.button_play_pause.clicked.connect(br.button_play_pause.button_play_pause_clicked)
br.button_play_pause.setGeometry(0, 0, PLAY_BUTTONS_WIDTH+4, PLAY_BUTTONS_HEIGHT+4)
br.button_play_pause.setIconSize(QSize(cv.icon_size + 5, cv.icon_size + 5))


''' BUTTON PLAY SECTION - STOP '''
br.button_stop = MyButtons(
    'Stop',
    'Stop playing',
    br.icon.stop
    )
br.button_stop.setGeometry(play_buttons_x_pos(1.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
br.button_stop.clicked.connect(br.button_stop.button_stop_clicked)
br.button_stop.setIconSize(QSize(cv.icon_size, cv.icon_size))


''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
br.button_prev_track = MyButtons(
    'Prev',
    'Previous track',
    br.icon.previous
    )
br.button_prev_track.setGeometry(play_buttons_x_pos(2.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
br.button_prev_track.clicked.connect(br.button_prev_track.button_prev_track_clicked)


''' BUTTON PLAY SECTION - NEXT TRACK '''
br.button_next_track = MyButtons(
    'Next',
    'Next track',
    br.icon.next
    )
br.button_next_track.setGeometry(play_buttons_x_pos(3.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
br.button_next_track.clicked.connect(br.button_next_track.button_next_track_clicked)


''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
br.button_toggle_repeat_pl = MyButtons(
    'Tog Rep PL',
    'Toggle Repeat Playlist',
    br.icon.repeat
    )
br.button_toggle_repeat_pl.setGeometry(play_buttons_x_pos(5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
br.button_toggle_repeat_pl.clicked.connect(br.button_toggle_repeat_pl.button_toggle_repeat_pl_clicked)

if cv.repeat_playlist == 2:
    br.button_toggle_repeat_pl.setFlat(1)
elif cv.repeat_playlist == 0:
    br.button_toggle_repeat_pl.setFlat(1)
    br.button_toggle_repeat_pl.setIcon(br.icon.repeat_single)


''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
br.button_toggle_shuffle_pl = MyButtons(
    'Shuffle PL',
    'Toggle Shuffle Playlist',
    br.icon.shuffle
    )
br.button_toggle_shuffle_pl.setGeometry(play_buttons_x_pos(6), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
br.button_toggle_shuffle_pl.clicked.connect(br.button_toggle_shuffle_pl.button_toggle_shuffle_pl_clicked)
if cv.shuffle_playlist_on:
    br.button_toggle_shuffle_pl.setFlat(1)


''' BUTTON PLAY SECTION - TOGGLE PLAYLIST '''
br.button_toggle_playlist = MyButtons(
    'Shuffle PL',
    'Toggle Show Playlists',
    br.icon.toggle_playlist
    )
br.button_toggle_playlist.setGeometry(play_buttons_x_pos(7), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
br.button_toggle_playlist.clicked.connect(br.button_toggle_playlist.button_toggle_playlist_clicked)


''' BUTTON PLAY SECTION - TOGGLE VIDEO '''
br.button_toggle_video = MyButtons(
    'Shuffle PL',
    'Toggle Show Video Window',
    br.icon.toggle_video
    )
br.button_toggle_video.setGeometry(play_buttons_x_pos(8), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
br.button_toggle_video.clicked.connect(br.button_toggle_video.button_toggle_video_clicked)


''' BUTTON PLAY SECTION - DURATION INFO '''
def button_duration_info_clicked():
    ''' 01:22 / 03:43 <--> -02:21 / 03:43 ''',
    if cv.track_full_duration_to_display:
        if cv.is_duration_to_display_straight:
            cv.is_duration_to_display_straight = False
            br.button_duration_info.setText(cv.duration_to_display_back)
        else:
            cv.is_duration_to_display_straight = True
            br.button_duration_info.setText(cv.duration_to_display_straight)
        
        br.button_duration_info.adjustSize()

br.button_duration_info = MyButtons(
    '00:00 / 00:00',
    'Click to switch',
    )
br.button_duration_info.move(play_buttons_x_pos(9.5), 0)
br.button_duration_info.clicked.connect(button_duration_info_clicked)
br.button_duration_info.set_style_duration_info_button()


''' 
    PLAY BUTTONS LIST
    used to add widgets to the layout
    the speaker/mute button is not
    part of the list
'''
play_buttons_list = [
    br.button_play_pause,
    br.button_stop,
    br.button_prev_track,
    br.button_next_track,
    br.button_toggle_repeat_pl,
    br.button_toggle_shuffle_pl,
    br.button_toggle_playlist,
    br.button_toggle_video,
    br.button_duration_info
]



''' BUTTON PLAY SECTION - SPEAKER/MUTE '''
br.button_speaker = MyButtons(
    'Speaker',
    'Toggle Mute',
    icon = br.icon.speaker
    )
br.button_speaker.setFlat(1)
br.button_speaker.clicked.connect(br.button_speaker.button_speaker_clicked)
if cv.is_speaker_muted:
    br.button_speaker.setIcon(br.icon.speaker_muted)
    br.av_player.audio_output.setVolume(0)


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


layout_base = QVBoxLayout(br.window)
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
br.layout_vert_left_qframe = QFrame()
br.layout_vert_left_qframe.setLayout(layout_vert_left)

''' TOP RIGHT - PLAYLIST / BUTTONS / DURATION '''
layout_vert_right = QVBoxLayout() # here layout type is not relevant
layout_vert_right.setContentsMargins(5, 0, 4, 0)
br.layout_vert_right_qframe = QFrame()
br.layout_vert_right_qframe.setLayout(layout_vert_right)
br.layout_vert_right_qframe.setMinimumWidth(cv.window_min_width-200)


splitter_left_right.addWidget(br.layout_vert_left_qframe)
splitter_left_right.addWidget(br.layout_vert_right_qframe)
splitter_left_right.setStretchFactor(0, 3)
splitter_left_right.setStretchFactor(1, 1)



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
layout_vert_left.addWidget(br.av_player.video_output)
br.av_player.video_output.hide()
layout_vert_left.addWidget(br.image_logo)


''' TOP RIGHT '''
# BUTTONS
playlist_buttons_list_wrapper = QFrame()
playlist_buttons_list_wrapper.setFixedSize(250, PLIST_BUTTONS_HEIGHT+5)

for button in playlist_buttons_list:
    button.setParent(playlist_buttons_list_wrapper)
    if button not in [br.button_settings, br.button_queue]:
        button.set_style_playlist_buttons()

layout_under_playlist_buttons.addWidget(playlist_buttons_list_wrapper)

# DURATION
br.duration_sum_widg = QPushButton('DURATION')
br.duration_sum_widg.setDisabled(1)
br.duration_sum_widg.setFont(inactive_track_font_style)
layout_under_playlist_duration.addWidget(br.duration_sum_widg)


''' PAYLISTS '''
br.playlists_all = MyPlaylists()
layout_playlist.addWidget(br.playlists_all)


''' WINDOW - QUEUE & SEARCH / SETTINGS '''
br.window_queue = MyQueueWindow()
br.window_settings = MySettingsWindow()


# PLAY BUTTON ICON UPDATE
if cv.play_at_startup and cv.active_pl_tracks_count > 0:
    br.button_play_pause.setIcon(br.icon.pause)


''' BOTTOM '''
# SLIDER
layout_bottom_slider.addWidget(br.play_slider)

# LAYOUT BUTTONS / VOLUME
layout_bottom_buttons = QVBoxLayout()
layout_bottom_volume = QHBoxLayout()
layout_bottom_volume.setAlignment(Qt.AlignmentFlag.AlignTop)

layout_bottom_wrapper.addLayout(layout_bottom_buttons, 80)
layout_bottom_wrapper.addLayout(layout_bottom_volume, 20)

# WIDGETS
# SPEAKER/MUTE BUTTON CREATED EARLIER
volume_slider = MyVolumeSlider()


# BUTTONS WRAPPER
play_buttons_list_wrapper= QFrame()
play_buttons_list_wrapper.setFixedHeight(50)
for button in play_buttons_list:
    button.setParent(play_buttons_list_wrapper)

layout_bottom_buttons.addWidget(play_buttons_list_wrapper)
layout_bottom_volume.addWidget(br.button_speaker, alignment=Qt.AlignmentFlag.AlignRight)
layout_bottom_volume.addWidget(volume_slider)


br.window.show()
logger_basic('Window displayed')

sys.exit(app.exec())