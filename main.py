
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
    )
from PyQt6.QtCore import QUrl, Qt, QEvent, QSize
from PyQt6.QtGui import QIcon, QFont

import sys

from src import cv, settings, PATH_JSON_SETTINGS
from src import Path
from src import AVPlayer, TrackDuration, MySlider, MyTabs
from src import MyButtons, PlaysFunc, MyImage
from src import save_json



''' APP '''
class MyApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
        self.installEventFilter(self) 

    def eventFilter(self, source, event):
        to_save_settings = False
        # PAUSE/PLAY - IF PLAYER IS NOT FULL SCREEN
        # IF FULL SCREEN: SET UP IN 'AVPlayer class'
        if event.type() == QEvent.Type.KeyRelease:
            # PAUSE
            if event.key() == Qt.Key.Key_Space:
                pass
                # TODO button_play_pause_clicked()
            # VOLUME
            elif event.key() == Qt.Key.Key_Plus:
                new_volume = round(av_player.audio_output.volume() + 0.01, 4)
                av_player.audio_output.setVolume(new_volume)
                to_save_settings = True
            elif event.key() == Qt.Key.Key_Minus:
                new_volume = round(av_player.audio_output.volume() - 0.01, 4)
                av_player.audio_output.setVolume(new_volume)
                to_save_settings = True
            # JUMP - SMALL
            elif event.key() == Qt.Key.Key_Left:
                av_player.player.setPosition(av_player.player.position() - 600)
            elif event.key() == Qt.Key.Key_Right:
                av_player.player.setPosition(av_player.player.position() + 600)
        if to_save_settings:
            settings['volume'] = new_volume
            save_json(settings, PATH_JSON_SETTINGS)
        return super().eventFilter(source, event)
    

''' APP '''
app = MyApp()

''' WINDOW '''
WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 750
window = QWidget()
window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.setMinimumSize(400, 400)
window.setWindowIcon(QIcon(str(Path(Path(__file__).parent, 'skins/window_icon.png'))))
window.setWindowTitle("QTea media player")


''' PLAYER '''
av_player = AVPlayer(volume=cv.volume)

""" 
    av_player_duration
    -------------------
    only used for duration calculation -->
    able to add new track(s) without interrupting 
    the playing (av_player)
"""
av_player_duration = TrackDuration()   


''' 
#######################
        WINDOWS              
#######################
'''
# FOR BUTTONS: ADD TRACK, REMOVE TRACK, ..
under_playlist_window = QFrame()
under_playlist_window.setMinimumSize(400, 30)

# FOR BUTTONS: PLAY/STOP, PAUSE, ..
under_play_slider_window = QFrame()
under_play_slider_window.setFixedHeight(50)
under_play_slider_window.setMinimumSize(400, 50)

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
# but_func = ButtonsFunc(av_player, av_player_duration, play_funcs)

''' 
    PLAYLIST SECTION
'''
PLIST_BUTTONS_WIDTH = 32
PLIST_BUTTONS_HEIGHT = 30
PLIST_BUTTONS_X_DIFF = 4    # FOR SELECTING ADD AND REMOVE BUTTONS

def button_x_pos(num):
    return (PLIST_BUTTONS_WIDTH + 5) * num


''' BUTTON PLAYLIST - ADD TRACK '''
button_add_track = MyButtons(
    under_playlist_window,
    'AT',
    'Add Track',
    av_player,
    av_player_duration,
    )
button_add_track.setGeometry(0, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_add_track.clicked.connect(button_add_track.button_add_track_clicked)


''' BUTTON PLAYLIST - ADD DIRECTORY '''
button_add_dir = MyButtons(
    under_playlist_window,
    'AD',
    'Add Directory',
    av_player,
    av_player_duration,
    )
button_add_dir.setGeometry(button_x_pos(1)-PLIST_BUTTONS_X_DIFF, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_add_dir.clicked.connect(button_add_dir.button_add_dir_clicked)


''' BUTTON PLAYLIST - REMOVE TRACK '''
button_remove_track = MyButtons(
    under_playlist_window,
    'RT',
    'Remove track'
    )
button_remove_track.setGeometry(button_x_pos(2), 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_remove_track.clicked.connect(button_remove_track.button_remove_track_clicked)


''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
button_remove_all_track = MyButtons(
    under_playlist_window,
    'CP',
    'Clear Playlist'
    )
button_remove_all_track.setGeometry(button_x_pos(3)-PLIST_BUTTONS_X_DIFF, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_remove_all_track.clicked.connect(button_remove_all_track.button_remove_all_track_clicked)


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

button_play_pause = MyButtons(
    under_play_slider_window,
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

button_stop = MyButtons(
    under_play_slider_window,
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
    under_play_slider_window,
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
    under_play_slider_window,
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
    under_play_slider_window,
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
    under_play_slider_window,
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
    under_play_slider_window,
    'Shuffle PL',
    'Toggle Shuffle Playlist',
    icon = button_image_toggle_playlist
    )
button_toggle_playlist.setGeometry(play_buttons_x_pos(7), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_playlist.clicked.connect(button_toggle_playlist_clicked)


''' BUTTON PLAY SECTION - TOGGLE VIDEO '''
def button_toggle_video_clicked():
    
    if av_player.playlist_visible and av_player.video_area_visible:
        layout_vert_left_qframe.hide()
        av_player.video_area_visible = False
        window.resize(int(WINDOW_WIDTH/3), window.geometry().height())
        button_toggle_playlist.setDisabled(1)
    else:
        window.resize(WINDOW_WIDTH, window.geometry().height())
        layout_vert_left_qframe.show()
        av_player.video_area_visible = True
        button_toggle_playlist.setDisabled(0)

button_toggle_video = MyButtons(
    under_play_slider_window,
    'Shuffle PL',
    'Toggle Shuffle Playlist',
    icon = button_image_toggle_vid
    )
button_toggle_video.setGeometry(play_buttons_x_pos(8), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_video.clicked.connect(button_toggle_video_clicked)




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
    |_______||_______|
    |________________|  BOTTOM
    |________________|  
'''


layout_base = QVBoxLayout(window)
layout_base.setContentsMargins(0, 0, 0, 0)

layout_hor_top = QHBoxLayout()
layout_hor_top.setSpacing(0)
layout_ver_bottom = QVBoxLayout()
layout_ver_bottom.setContentsMargins(10, 0, 10, 0)

layout_base.addLayout(layout_hor_top, 90)
layout_base.addLayout(layout_ver_bottom, 10)


''' TABS - PLAYLIST '''
tabs_playlist = MyTabs(button_play_pause.button_play_pause_via_list)


''' TOP RIGHT '''
layout_vert_right = QVBoxLayout()
layout_vert_right.setContentsMargins(5, 0, 4, 0)
layout_vert_right_qframe = QFrame()
layout_vert_right_qframe.setLayout(layout_vert_right)

''' TOP LEFT '''
layout_vert_left = QVBoxLayout()
layout_vert_left.setContentsMargins(0, 0, 0, 0)
layout_vert_left_qframe = QFrame()
layout_vert_left_qframe.setLayout(layout_vert_left)


layout_hor_top.addWidget(layout_vert_left_qframe, 65)
layout_hor_top.addWidget(layout_vert_right_qframe, 35)



''' ADDING WIDGETS TO LAYOUTS '''
layout_vert_left.addWidget(av_player.video_output)
layout_vert_left.addWidget(image_logo)
layout_vert_right.addWidget(tabs_playlist, 95)
layout_vert_right.addWidget(under_playlist_window, 5)
layout_ver_bottom.addWidget(play_slider)
layout_ver_bottom.addWidget(under_play_slider_window)


av_player.video_output.hide()


# TODO: add/edit tabs, tabs_playlist.setTabVisible(2, 0)

window.show()

sys.exit(app.exec())