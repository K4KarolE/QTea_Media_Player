
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem, QPushButton, QMainWindow
from PyQt6.QtWidgets import QSlider, QFrame, QTabWidget, QLabel, QScrollBar
from PyQt6.QtCore import QUrl, Qt, QEvent
from PyQt6.QtGui import QMovie, QIcon, QFont

# from PyQt6.QtWidgets import QLineEdit
# from PyQt6.QtCore import QSize, QTimer, QTime

import os
import sys
import random
import sqlite3

from src import Path
from src import AVPlayer, Data
from src import TrackDuration
from src import save_json
from src import PATH_JSON_SETTINGS, settings



def active_utility():
    cv.active_db_table = cv.paylist_list[cv.active_tab] # playlist_1, playlist_2, ..
    cv.last_track_index = settings[cv.active_db_table]['last_track_index']
    cv.active_playlist = cv.paylist_widget_dic[cv.active_db_table]['name_list_widget']  # widget
    cv.active_pl_duration = cv.paylist_widget_dic[cv.active_db_table]['duration_list_widget']   # widget


def save_last_track_index():
    cv.last_track_index = cv.active_playlist.currentRow()
    settings[cv.active_db_table]['last_track_index'] = cv.last_track_index
    save_json(settings, PATH_JSON_SETTINGS)


def add_record_db(duration, path):
    cur.execute("INSERT INTO {0}(duration, path) VALUES (?, ?)".format(cv.active_db_table), (duration, str(path)))
    connection.commit()


def remove_record_db(list_row_id):
    cur.execute("DELETE FROM {0} WHERE row_id = ?".format(cv.active_db_table), (list_row_id,))
    cur.execute("UPDATE {0} SET row_id = row_id - 1 WHERE row_id > ?".format(cv.active_db_table), (list_row_id,) )
    connection.commit()


def get_row_id_db(path):
    return cur.execute("SELECT row_id FROM {0} WHERE path = ?".format(cv.active_db_table), (str(path),)).fetchall()[-1][0] 
    # [-1][0]: adding same track multiple times --> row_id: picked the latest's one


def get_path_db():
    return cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(cv.active_db_table),
                        (cv.active_playlist.currentRow() + 1,)).fetchall()[0][2]

def get_duration_db():
    # active_playlist = tabs_playlist.currentWidget()
    return int(cur.execute("SELECT * FROM {0} WHERE row_id = ?".format(cv.active_db_table),
                           (cv.active_playlist.currentRow() + 1,)).fetchall()[0][1])

def generate_duration_to_display(raw_duration):

    try:
        # SECONDS
        str_seconds = str(int(int(raw_duration)/1000%60))
        if str_seconds == '0':
            seconds = '00'
        elif len(str_seconds) == 1:
            seconds = f'0{str_seconds}'
        else:
            seconds = str_seconds[0:2]
        
        # MINUTES
        int_minutes = int(int(raw_duration)/60/1000)
        if int_minutes == 60:
            minutes = '01'
        elif int_minutes in range(10,60):
            minutes = str(int_minutes)
        elif int_minutes in range(0,10):
            minutes = f'0{str(int_minutes)}'
        else:
            minutes = str(int_minutes%60)

        # HOURS
        if int_minutes > 60:
            str_hours = str(int((int_minutes - int_minutes%60)/60))
            duration = f'{str_hours}:{minutes}:{seconds}'
        else:
            duration = f'{minutes}:{seconds}'
    except:
        duration = 'ERROR'

    return duration


def generate_track_list_detail(db_track_record):
    # [0]:row, [1]:duration, [2]:path
    track_name = f'{db_track_record[0]}. {Path(db_track_record[2]).stem}'
    duration = generate_duration_to_display(db_track_record[1])
    return track_name, duration


def add_record_grouped_actions(track_path):

    track_name = Path(track_path).stem
    # DURATION
    mt_player_duration.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    raw_duration = mt_player_duration.player.duration()
    duration = generate_duration_to_display(raw_duration)
    # DB
    add_record_db(raw_duration, track_path)
    # TRACK NAME
    row_id = get_row_id_db(track_path)
    track_name = f'{row_id}. {track_name}'
    
    add_new_list_item(track_name, cv.active_playlist, 'left')
    add_new_list_item(duration, cv.active_pl_duration, 'right')


def add_new_list_item(new_item, list_widget, alignment):
    
    list_item = QListWidgetItem(new_item, list_widget)
    list_item.setFont(inactive_track_font_style)

    if alignment == 'left':
        list_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
    else:
        list_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)


''' DATA '''
cv = Data()


''' PLAYLIST DB '''
connection = sqlite3.connect('playlist.db')
cur = connection.cursor()


''' STYLE '''
inactive_track_font_style = QFont('Times', 11, 500)
active_track_font_style = QFont('Times', 11, 600)


''' APP '''
WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 750

app = QApplication(sys.argv)
window = QWidget()
window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.setMinimumSize(400, 400)
window.setWindowIcon(QIcon(str(Path(Path(__file__).parent, 'skins/window_icon.png'))))
window.setWindowTitle("QTea media player")


''' PLAYER '''
mt_player = AVPlayer()
""" 
    mt_player_duration
    -------------------
    only used for duration calculation -->
    able to add new track(s) without interrupting 
    the playing (mt_player)
"""
mt_player_duration = TrackDuration()   


''' 
#######################
        WINDOWS              
#######################
'''
# FOR BUTTONS: ADD TRACK, REMOVE TRACK, ..
under_playlist_window = QMainWindow()
under_playlist_window.setMinimumSize(400, 30)

# FOR BUTTONS: PLAY/STOP, PAUSE, ..
under_play_slider_window = QMainWindow()
under_play_slider_window.setFixedHeight(50)
under_play_slider_window.setMinimumSize(400, 50)


''' 
#######################
        BUTTONS              
#######################
'''
MEDIA_FILES = "Media files (*.mp3 *.wav *.flac *.midi *.aac *.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
AUDIO_FILES = "Audio files (*.mp3 *.wav *.flac *.midi *.aac)"
VIDEO_FILES = "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
FILE_TYPES_LIST = [MEDIA_FILES, AUDIO_FILES, VIDEO_FILES, 'All Files']

''' 
    PLAYLIST SECTION
'''
PLIST_BUTTONS_WIDTH = 32
PLIST_BUTTONS_HEIGHT = 30
PLIST_BUTTONS_X_DIFF = 4    # FOR SELECTING ADD AND REMOVE BUTTONS

def button_x_pos(num):
    return (PLIST_BUTTONS_WIDTH + 5) * num

''' BUTTON PLAYLIST - ADD TRACK '''
def button_add_track_clicked():
    dialog_add_track = QFileDialog()
    dialog_add_track.setWindowTitle("Select a media file")
    dialog_add_track.setNameFilters(FILE_TYPES_LIST)
    dialog_add_track.exec()
    if dialog_add_track.result():
        add_record_grouped_actions(dialog_add_track.selectedFiles()[0])

button_add_track = QPushButton(under_playlist_window, text='AT')
button_add_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_track.setToolTip('Add track')
button_add_track.setToolTipDuration(2000)
button_add_track.setFont(QFont('Times', 10, 600))
button_add_track.setGeometry(5, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_add_track.clicked.connect(button_add_track_clicked)


''' BUTTON PLAYLIST - ADD DIRECTORY '''
def button_add_dir_clicked():
    track_path_list = []
    error_path_list = []
    dialog_add_dir = QFileDialog()
    dialog_add_dir.setWindowTitle("Select a directory")
    dialog_add_dir.setFileMode(QFileDialog.FileMode.Directory)
    dialog_add_dir.exec()
    if dialog_add_dir.result():
        for dir_path, dir_names, file_names in os.walk(dialog_add_dir.selectedFiles()[0]):
            for file in file_names:
                if file[-4:] in MEDIA_FILES:
                    track_path_list.append(Path(dir_path, file))
        if len(track_path_list) > 0:
            for track_path in track_path_list:
                try:
                    add_record_grouped_actions(track_path)
                except:
                    error_path_list.append(track_path)
            if error_path_list:
                for item in error_path_list:
                    print(f'ERROR - {item}')

button_add_dir = QPushButton(under_playlist_window, text='AD')
button_add_dir.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_dir.setToolTip('Add directory')
button_add_dir.setToolTipDuration(2000)
button_add_dir.setFont(QFont('Times', 10, 600))
button_add_dir.setGeometry(button_x_pos(1)-PLIST_BUTTONS_X_DIFF, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_add_dir.clicked.connect(button_add_dir_clicked)



''' BUTTON PLAYLIST - REMOVE TRACK '''
def button_remove_track_clicked():
    # LAST TRACK INDEX
    if  cv.active_playlist.currentRow() < cv.last_track_index:
        cv.last_track_index = cv.last_track_index - 1
        settings[cv.active_db_table]['last_track_index'] = cv.last_track_index
        save_json(settings, PATH_JSON_SETTINGS)
    # DB
    row_id_db = cv.active_playlist.currentRow() + 1
    remove_record_db(row_id_db)
    # PLAYLIST
    cv.active_playlist.takeItem(cv.active_playlist.currentRow())
    cv.active_pl_duration.takeItem(cv.active_playlist.currentRow())
    rename_playlist(row_id_db)



def rename_playlist(row_id_db):
    cur.execute("SELECT * FROM {0} WHERE row_id >= ?".format(cv.active_db_table), (row_id_db,))
    playlist = cur.fetchall()
    for item in playlist:
        list_name, duration = generate_track_list_detail(item)
        cv.active_playlist.item(row_id_db-1).setText(list_name)
        row_id_db +=1

button_remove_track = QPushButton(under_playlist_window, text='RT')
button_remove_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_track.setToolTip('Remove track')
button_remove_track.setToolTipDuration(2000)
button_remove_track.setFont(QFont('Times', 10, 600))
button_remove_track.setGeometry(button_x_pos(2), 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_remove_track.clicked.connect(button_remove_track_clicked)

''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
def button_remove_all_track_clicked():
    # DB
    cur.execute("DELETE FROM {0}".format(cv.active_db_table))
    connection.commit()
    # PLAYLIST
    cv.active_playlist.clear()
    cv.active_pl_duration.clear()

button_remove_all_track = QPushButton(under_playlist_window, text='CP')
button_remove_all_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_all_track.setToolTip('Clear Playlist')
button_remove_all_track.setToolTipDuration(2000)
button_remove_all_track.setFont(QFont('Times', 10, 600))
button_remove_all_track.setGeometry(button_x_pos(3)-PLIST_BUTTONS_X_DIFF, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_remove_all_track.clicked.connect(button_remove_all_track_clicked)


''' 
    PLAY SECTION
'''
PLAY_BUTTONS_WIDTH = 60
PLAY_BUTTONS_HEIGHT = 30

def play_buttons_x_pos(num):
    return (PLAY_BUTTONS_WIDTH + 3) * num


''' BUTTON PLAY SECTION - PLAY / PAUSE '''
def button_play_pause_clicked():

    if mt_player.played_row == None:
        cv.active_playlist.setCurrentRow(0)
        play_track()
    elif mt_player.player.isPlaying():
        mt_player.player.pause()
        mt_player.paused = True
    elif mt_player.paused:
        mt_player.player.play()
        mt_player.paused = False
    elif not mt_player.player.isPlaying() and not mt_player.paused:
        play_track()

button_play_pause = QPushButton(under_play_slider_window, text='PLAY/PAUSE')
button_play_pause.setCursor(Qt.CursorShape.PointingHandCursor)
button_play_pause.setFont(QFont('Times', 10, 600))
button_play_pause.clicked.connect(button_play_pause_clicked)


''' BUTTON PLAY SECTION - STOP '''
def button_stop_clicked():
    mt_player.player.stop()
    mt_player.paused = False
 
button_stop = QPushButton(under_play_slider_window, text='Stop')
button_stop.setCursor(Qt.CursorShape.PointingHandCursor)
button_stop.setFont(QFont('Times', 10, 600))
button_stop.setGeometry(play_buttons_x_pos(2), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_stop.clicked.connect(button_stop_clicked)


''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
def button_prev_track_clicked():
    if cv.active_playlist.count() > 0 and mt_player.played_row != None:

        if cv.shuffle_playlist_on:
            cv.active_playlist.setCurrentRow(cv.last_track_index)
        elif cv.active_playlist.currentRow() != 0:
            cv.active_playlist.setCurrentRow(mt_player.played_row - 1)
        else:
            cv.active_playlist.setCurrentRow(cv.active_playlist.count() - 1)
        play_track()

button_prev_track = QPushButton(under_play_slider_window, text='Prev')
button_prev_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_prev_track.setFont(QFont('Times', 10, 600))
button_prev_track.setGeometry(play_buttons_x_pos(3), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_prev_track.clicked.connect(button_prev_track_clicked)


''' BUTTON PLAY SECTION - NEXT TRACK '''
def button_next_track_clicked():
    if cv.active_playlist.count() > 0 and mt_player.played_row != None:
        play_next_track()

button_next_track = QPushButton(under_play_slider_window, text='Next')
button_next_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_next_track.setFont(QFont('Times', 10, 600))
button_next_track.setGeometry(play_buttons_x_pos(4), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_next_track.clicked.connect(button_next_track_clicked)


''' BUTTON PLAY SECTION - TOGGLE PLAYLIST '''
def button_toggle_playlist_clicked():

    if mt_player.playlist_visible and mt_player.video_area_visible:
        layout_vert_right_qframe.hide()
        layout_vert_middle_qframe.hide()
        mt_player.playlist_visible = False
        button_toggle_video.setDisabled(1)
    else:
        layout_vert_right_qframe.show()
        layout_vert_middle_qframe.show()
        mt_player.playlist_visible = True
        button_toggle_video.setDisabled(0)    
    
button_toggle_playlist = QPushButton(under_play_slider_window, text='Tog PL')
button_toggle_playlist.setCursor(Qt.CursorShape.PointingHandCursor)
button_toggle_playlist.setFont(QFont('Times', 10, 600))
button_toggle_playlist.setGeometry(play_buttons_x_pos(5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_playlist.clicked.connect(button_toggle_playlist_clicked)


''' BUTTON PLAY SECTION - TOGGLE VIDEO '''
def button_toggle_video_clicked():
    
    if mt_player.playlist_visible and mt_player.video_area_visible:
        layout_vert_left_qframe.hide()
        mt_player.video_area_visible = False
        window.resize(int(WINDOW_WIDTH/3), window.geometry().height())
        button_toggle_playlist.setDisabled(1)
    else:
        window.resize(WINDOW_WIDTH, window.geometry().height())
        layout_vert_left_qframe.show()
        mt_player.video_area_visible = True
        button_toggle_playlist.setDisabled(0)
    
button_toggle_video = QPushButton(under_play_slider_window, text='Tog Vid')
button_toggle_video.setCursor(Qt.CursorShape.PointingHandCursor)
button_toggle_video.setFont(QFont('Times', 10, 600))
button_toggle_video.setGeometry(play_buttons_x_pos(6), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_video.clicked.connect(button_toggle_video_clicked)


''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
def button_toggle_repeat_pl_clicked():
    if cv.repeat_playlist_on:
        cv.repeat_playlist_on = False
        button_toggle_repeat_pl.setFlat(0)
    else:
        cv.repeat_playlist_on = True
        button_toggle_repeat_pl.setFlat(1)
    
    settings['repeat_playlist_on'] = cv.repeat_playlist_on
    save_json(settings, PATH_JSON_SETTINGS)
    
button_toggle_repeat_pl = QPushButton(under_play_slider_window, text='Tog Rep')
button_toggle_repeat_pl.setCursor(Qt.CursorShape.PointingHandCursor)
button_toggle_repeat_pl.setFont(QFont('Times', 10, 600))
button_toggle_repeat_pl.setGeometry(play_buttons_x_pos(7), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_repeat_pl.clicked.connect(button_toggle_repeat_pl_clicked)


''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
def button_toggle_shuffle_pl_clicked():
    if cv.shuffle_playlist_on:
        cv.shuffle_playlist_on = False
        button_toggle_shuffle_pl.setFlat(0)
    else:
        cv.shuffle_playlist_on = True
        button_toggle_shuffle_pl.setFlat(1)
    
    settings['shuffle_playlist_on'] = cv.shuffle_playlist_on
    save_json(settings, PATH_JSON_SETTINGS)
    
button_toggle_shuffle_pl = QPushButton(under_play_slider_window, text='Shu Rep')
button_toggle_shuffle_pl.setCursor(Qt.CursorShape.PointingHandCursor)
button_toggle_shuffle_pl.setFont(QFont('Times', 10, 600))
button_toggle_shuffle_pl.setGeometry(play_buttons_x_pos(8), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_shuffle_pl.clicked.connect(button_toggle_shuffle_pl_clicked)


''' LIST ACTIONS '''
def play_track():
    
    try:  
        # FONT STYLE - PREV/NEW TRACK
        if mt_player.played_row != None and mt_player.played_row < cv.active_playlist.count():

            try:
                cv.active_playlist.item(cv.last_track_index).setFont(inactive_track_font_style)
            except:
                print(f'ERROR in row: {cv.last_track_index}\n\n')

            cv.last_track_index = mt_player.played_row

        cv.active_playlist.currentItem().setFont(active_track_font_style)
        save_last_track_index()
        # PATH / DURATION / SLIDER
        track_path = get_path_db()
        track_duration = get_duration_db()
        play_slider.setMaximum(track_duration)
        # PLAYER
        mt_player.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
        # TODO mt_player.audio_output.setVolume(0.5)
        mt_player.player.play()
        # COUNTER
        mt_player.played_row = cv.active_playlist.currentRow()
        # WINDOW TITLE
        window.setWindowTitle(f'{Path(track_path).stem} - QTea media player')

    except:
        play_next_track()


def play_next_track():
    # SHUFFLE
    if cv.shuffle_playlist_on and cv.active_playlist.count() > 1:
        next_track_index = random.randint(0, cv.active_playlist.count()-1)
        while next_track_index == cv.active_playlist.currentRow():
            next_track_index = random.randint(0, cv.active_playlist.count()-1)
        cv.active_playlist.setCurrentRow(next_track_index)
        play_track()
    # MORE TRACKS IN THE PLAYLIST
    elif cv.active_playlist.count() != cv.active_playlist.currentRow() + 1:
        cv.active_playlist.setCurrentRow(mt_player.played_row + 1)
        play_track()
    # PLAYING THE LAST TRACK    
    elif (cv.active_playlist.count() == cv.active_playlist.currentRow() + 1 and
        cv.repeat_playlist_on):
            cv.active_playlist.setCurrentRow(0)
            play_track()
    # CURRENT TRACK BACK TO START         
    else:
        mt_player.player.setPosition(0)


def auto_play_next_track():
    if mt_player.base_played:   # avoiding the dummy song played when the class created
        if mt_player.player.mediaStatus() == mt_player.player.MediaStatus.EndOfMedia:

            play_next_track()
    else:
        mt_player.base_played = True    
mt_player.player.mediaStatusChanged.connect(auto_play_next_track)




''' 
######################
        SLIDER                          
######################
'''

play_slider = QSlider()
# wihout the groove's bg color --> 
# not able to change the handle's size
play_slider.setStyleSheet(
                        "QSlider::groove"
                            "{"
                            "background: #C2C2C2;"
                            "height: 10px;"
                            "border-radius: 4px;"
                            "}"

                        "QSlider::handle"
                            "{"
                            "border: 1px solid grey;"
                            "border-radius: 8px;"
                            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C2C2C2, stop:1 #E8E8E8);"
                            "width: 15px;"
                            "margin: -3 px;  /* expand outside the groove */"
                            "}"

                        "QSlider::sub-page"
                            "{"
                            "background: #287DCC;"
                            "}"
                        )
                            
play_slider.setOrientation(Qt.Orientation.Horizontal)

play_slider.setCursor(Qt.CursorShape.PointingHandCursor)

def player_set_position():
    if mt_player.base_played and mt_player.player.isPlaying():
        mt_player.player.setPosition(play_slider.value())

play_slider.sliderReleased.connect(player_set_position)


def play_slider_set_value():
    if mt_player.base_played and not play_slider.isSliderDown():
        play_slider.setValue(mt_player.player.position())

mt_player.player.positionChanged.connect(play_slider_set_value)


''' 
######################
        LAYOUTS                          
######################

LEARNED:
1,              
do not mix widgets and layouts in a layout
hiding the widget --> layout disapears too
2,
layout add to QFrame --> hiding QFrame hides the layout


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
# TO AVOID THE tabs_playlist.currentChanged.connect(active_tab) SIGNAL
# TRIGGERED WHEN TAB ADDED TO tabs_playlist
tabs_created_at_first_run = False

def active_tab():
    if tabs_created_at_first_run:
        cv.active_tab = tabs_playlist.currentIndex()
        settings['last_used_tab'] = cv.active_tab
        save_json(settings, PATH_JSON_SETTINGS)
        active_utility()    # set the current lists(name, duration)

tabs_playlist = QTabWidget()
tabs_playlist.setFont(QFont('Times', 10, 500))
tabs_playlist.currentChanged.connect(active_tab)

'''
    CREATING FRAME, LAYOUT, LIST WIDGETS 
    LOADING TRACKS
'''
def name_list_to_duration_row_selection():
    cv.active_pl_duration.setCurrentRow(cv.active_playlist.currentRow())
    cv.active_pl_duration.setStyleSheet(
                        "QListWidget::item:selected"
                            "{"
                            "background: #CCE8FF;"
                            "}"
                        )

def duration_list_to_name_row_selection():
    cv.active_playlist.setCurrentRow(cv.active_pl_duration.currentRow())
    cv.active_playlist.setStyleSheet(
                        "QListWidget::item:selected"
                            "{"
                            "background: #CCE8FF;"
                            "}"
                        )

for pl in cv.paylist_widget_dic:
    if settings[pl]['tab_index'] != None:
        
        scroll_bar_name_ver = QScrollBar()
        scroll_bar_name_hor = QScrollBar()
        scroll_bar_duration_ver = QScrollBar()
        scroll_bar_duration_hor = QScrollBar()

        scroll_bar_name_ver.valueChanged.connect(scroll_bar_duration_ver.setValue)
        scroll_bar_duration_ver.valueChanged.connect(scroll_bar_name_ver.setValue)

        scroll_bar_name_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 0px;"
                            "}"
                        )
        scroll_bar_name_hor.setStyleSheet(
                        "QScrollBar::horizontal"
                            "{"
                            "height: 0px;"
                            "}"
                        )
        
        scroll_bar_duration_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 10px;"
                            "}"               
                        )
        
        scroll_bar_duration_hor.setStyleSheet(
                        "QScrollBar::horizontal"
                            "{"
                            "height: 0px;"
                            "}"
                        )
    
        cv.paylist_widget_dic[pl]['name_list_widget'] = QListWidget()
        cv.paylist_widget_dic[pl]['name_list_widget'].setVerticalScrollBar(scroll_bar_name_ver)
        cv.paylist_widget_dic[pl]['name_list_widget'].setHorizontalScrollBar(scroll_bar_name_hor)
        # cv.paylist_widget_dic[pl]['name_list_widget'].setAlternatingRowColors(True)
        cv.paylist_widget_dic[pl]['name_list_widget'].currentItemChanged.connect(name_list_to_duration_row_selection)

        cv.paylist_widget_dic[pl]['duration_list_widget'] = QListWidget()
        cv.paylist_widget_dic[pl]['duration_list_widget'].setVerticalScrollBar(scroll_bar_duration_ver)
        cv.paylist_widget_dic[pl]['duration_list_widget'].setHorizontalScrollBar(scroll_bar_duration_hor)
        # cv.paylist_widget_dic[pl]['duration_list_widget'].setAlternatingRowColors(True)
        cv.paylist_widget_dic[pl]['duration_list_widget'].setFixedWidth(70)
        cv.paylist_widget_dic[pl]['duration_list_widget'].currentItemChanged.connect(duration_list_to_name_row_selection)

        name_list_widget = cv.paylist_widget_dic[pl]['name_list_widget']
        name_list_widget.itemDoubleClicked.connect(play_track)
        duration_list_widget = cv.paylist_widget_dic[pl]['duration_list_widget']
        tab_title = settings[pl]['tab_title']
        

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(name_list_widget, 90)
        layout.addWidget(duration_list_widget, 10)

        frame = QFrame()
        frame.setStyleSheet(
                        "QFrame"
                            "{"
                            "border: 0px;"
                            "}"
                        )
        frame.setLayout(layout)

        tabs_playlist.addTab(frame, tab_title)

        ''' PLAYLIST DB --> LIST WIDGET '''
        cur.execute("SELECT * FROM {0}".format(pl))
        playlist = cur.fetchall()
        for item in playlist:
            track_name, duration = generate_track_list_detail(item)
            add_new_list_item(track_name, name_list_widget, 'left')
            add_new_list_item(duration, duration_list_widget, 'right')

    tabs_created_at_first_run = True 


# LOAD ACTIVE NAME and DURATION LIST WIDGETS
active_utility()
# SET THE LAST USED TAB ACTIVE
tabs_playlist.setCurrentIndex(cv.active_tab)
# SET LAST PLAYED TRACK
cv.active_playlist.setCurrentRow(cv.last_track_index)


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

''' TOP MIDDLE '''
layout_vert_middle_qframe = QFrame()


layout_hor_top.addWidget(layout_vert_left_qframe, 65)
layout_hor_top.addWidget(layout_vert_middle_qframe, 0)
layout_hor_top.addWidget(layout_vert_right_qframe, 35)


''' ADDING WIDGETS TO LAYOUTS '''
layout_vert_left.addWidget(mt_player.video_output)
layout_vert_right.addWidget(tabs_playlist, 95)
layout_vert_right.addWidget(under_playlist_window, 5)
layout_ver_bottom.addWidget(play_slider)
layout_ver_bottom.addWidget(under_play_slider_window)

# TODO: layout_hor.setStretch(0, 10)


window.show()

sys.exit(app.exec())