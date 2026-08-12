"""
SETTINGS WINDOW displayed once the settings button
(cog icon) clicked under the playlists section

TERMINOLOGY
In the rest of the files the TABS(Playlists) has been referred as playlists, playlist_all, playlist_index, ..
In this file the TAB terminology is kept for the SETTINGS WINDOW tabs
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QPushButton,
    QScrollBar,
    QTabWidget,
    QWidget
    )

from .class_bridge import br
from .class_data import (
    cv,
    settings,
    save_json
    )
from .class_skins import sk
from .func_coll import (
    inactive_track_font_style,
    move_window_to_middle_of_current_screen,
    open_log_file,
    update_playing_playlist_vars_and_widgets
    )
from .func_thumbnail import (
    msg_box_wrapper_for_remove_all_thumbnails_and_clear_history,
    switch_all_pl_to_standard_from_thumbnails_view
    )
from .logger import logger_check

from .window_settings_tab_general import GeneralTab
from .window_settings_tab_hotkeys import HotkeysTab
from .window_settings_tab_playlists import PlaylistsTab
from .window_settings_tab_skins import SkinsTab



@logger_check
class MySettingsWindow(QWidget):
    """ It is created once the Settings button clicked """
    def __init__(self):
        super().__init__()

        '''
        ##############
            WINDOW          
        ##############
        '''
        WINDOW_WIDTH, WINDOW_HEIGHT = 400, 630
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.setFixedWidth(WINDOW_WIDTH)
        self.setFixedHeight(WINDOW_HEIGHT)
        self.setWindowIcon(br.icon.settings)
        self.setWindowTitle("Settings")
        self.setStyleSheet(f"background: {sk.window};")


        '''
        ############
            TABS         
        ############
        '''
        TABS_POS_X, TABS_POS_Y  = 12, 12

        tabs = QTabWidget(self)
        tabs.setFont(QFont('Verdana', 10, 500))
        tabs.resize(WINDOW_WIDTH-TABS_POS_X*2, int(WINDOW_HEIGHT-TABS_POS_Y*5.5))
        tabs.move(TABS_POS_X, TABS_POS_Y)
        tabs.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            f"background-color: {sk.tab_playlist_selected_bg};" 
                            f"color: {sk.tab_playlist_selected_font};"   # font
                            f"border: 2px solid {sk.tab_playlist_selected_border};"
                            "border-radius: 5px;"
                            "padding: 6px"
                            "}"
                        "QTabBar::tab:!selected"
                            "{"
                            f"background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1,"
                            f"stop: 0 {sk.tab_playlist_bg_1},"
                            f"stop: 0.4 {sk.tab_playlist_bg_2},"
                            f"stop: 0.8 {sk.tab_playlist_bg_3},"
                            f"stop: 1 {sk.tab_playlist_bg_4});"
                            f"color: {sk.tab_playlist_font};"   # font
                            f"border: 2px solid {sk.tab_playlist_border};"
                            "border-radius: 6px;"
                            "padding: 6px"
                            "}"
                        "QTabWidget::pane"
                            "{" 
                            "position: absolute;"
                            "top: 0.3em;"
                            "}"
                        )

        self.LINE_EDIT_TEXT_ALIGNMENT = (Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.LINE_EDIT_HIGHT = 20
        self.WIDGETS_POS_X = 25
        self.WIDGETS_POS_Y = 20
        self.WIDGETS_NEXT_LINE_POS_Y_DIFF = 25



        """ TAB - HOTKEYS """
        tab_hotkey = HotkeysTab()

        """ TAB - GENERAL """
        tab_general = GeneralTab()

        """ TAB - PLAYLIST """
        tab_playlist = PlaylistsTab()

        """ TAB - SKINS """
        tab_skins = SkinsTab()


        """ 
        #####################
            TABS COMPILING     
        #####################
        
        WIDGETS_WINDOW and SCROLL_AREA background color is the same
        --> if WIDGETS_WINDOW size < SCROLL_AREA --> still looks like one window
        """
        def set_widgets_window_style(widgets_window):
            widgets_window.setStyleSheet(
                            "QWidget"
                                "{"
                                f"background-color: {sk.window_settings_inner_window};"
                                "}"
                            "QLineEdit"
                                "{"
                                f"border: 1px solid {sk.window_settings_line_edit_border};"
                                f"background-color: {sk.window_settings_line_edit};"
                                f"color: {sk.window_settings_line_edit_text};" # text
                                "}"
                                )


        def set_scroll_area_style(scroll_area):
            scroll_area.setStyleSheet(
                                "QScrollArea"
                                    "{"
                                    f"border: 1px solid {sk.window_settings_inner_window_border};"
                                    "border-radius: 2px;"
                                    "}"
                                )


        def set_scroll_bar_style(scroll_bar):
            scroll_bar.setStyleSheet(
                                    "QScrollBar::vertical"
                                        "{"
                                        f"background: {sk.window_settings_scrollbar};"
                                        "width: 10px;"
                                        "}"
                                    "QScrollBar::horizontal"
                                        "{"
                                        "width: 0px;"
                                        "}"
                                    )

        tabs_dic = {
            'Playlists': {
                'text': 'Playlists',
                'scroll_area': tab_playlist.scroll_area,
                'scroll_bar_ver': '',
                'scroll_bar_hor': '',
                'widgets_window': tab_playlist.inner_window,
                'widgets_window_height': tab_playlist.last_widget_pos_y
            },
            'General': {
                'text': 'General',
                'scroll_area': tab_general.scroll_area,
                'scroll_bar_ver': '',
                'scroll_bar_hor': '',
                'widgets_window': tab_general.inner_window,
                'widgets_window_height': tab_general.last_widget_pos_y
            },
            'Hotkeys': {
                'text': 'Hotkeys',
                'scroll_area': tab_hotkey.scroll_area,
                'scroll_bar_ver': '',
                'scroll_bar_hor': '',
                'widgets_window': tab_hotkey.inner_window,
                'widgets_window_height': tab_hotkey.last_widget_pos_y
            },
            'Skins': {
                'text': 'Skins',
                'scroll_area': tab_skins.scroll_area,
                'scroll_bar_ver': '',
                'scroll_bar_hor': '',
                'widgets_window': tab_skins.inner_window,
                'widgets_window_height': tab_skins.last_widget_pos_y
            }
        }


        '''
        WIDGET RESIZE 
            - If widget size > tab size -> scroll bar visible
            - resize(WINDOW_WIDTH-50,.. -> no horizontal scroll bar
            - widget amount -> vertical scroll bar visible / invisible
            - more info: docs / learning / set_scrollbar_to_tab_widget.py 
        '''
        for tab in tabs_dic:
            tabs_dic[tab]['widgets_window'].resize(WINDOW_WIDTH, tabs_dic[tab]['widgets_window_height'])
            set_widgets_window_style(tabs_dic[tab]['widgets_window'])

            tabs_dic[tab]['scroll_bar_ver'] = QScrollBar()
            set_scroll_bar_style(tabs_dic[tab]['scroll_bar_ver'])
            tabs_dic[tab]['scroll_bar_hor'] = QScrollBar()
            set_scroll_bar_style(tabs_dic[tab]['scroll_bar_hor'])

            tabs_dic[tab]['scroll_area'].setVerticalScrollBar(tabs_dic[tab]['scroll_bar_ver'])
            tabs_dic[tab]['scroll_area'].setHorizontalScrollBar(tabs_dic[tab]['scroll_bar_hor'])
            set_scroll_area_style(tabs_dic[tab]['scroll_area'])

            tabs_dic[tab]['scroll_area'].setWidget(tabs_dic[tab]['widgets_window'])
            tabs.addTab(tabs_dic[tab]['scroll_area'], tabs_dic[tab]['text'])

        """
        UNDER TABS SECTION
        Combo box + button
        """
        def set_widgets_style(widget):
            widget.setStyleSheet("QPushButton"
                                   "{"
                                   f"background-color: {sk.window_settings_button};"
                                   f"border: 1px solid {sk.row_playing};"
                                   "border-radius: 4px;"
                                   "}"
                                "QPushButton::pressed"
                                    "{"
                                    f"background-color: {sk.window_settings_button_pressed_bg};"
                                    "}"
                                "QComboBox"
                                     "{"
                                    f"border: 1px solid {sk.row_playing};"
                                    "border-radius: 2px;"
                                     f"background: {sk.row_inactive};"
                                     f"color: {sk.row_inactive_text};"
                                     "}"
                                "QComboBox::item:selected"
                                     "{"
                                     f"background: {sk.row_playing};"
                                     f"color: {sk.row_playing_text};"
                                     "}"
                                   )

        def save_action():
            pl_list_with_title = tab_playlist.playlist_fields_validation_at_least_one_playlist()

            if (pl_list_with_title and
                tab_playlist.playlist_fields_validation_playing_playlist() and
                tab_playlist.playlist_fields_validation_queued_track() and
                tab_general.general_fields_validation() and
                tab_hotkey.hotkey_fields_validation()):

                ''' GENERAL TAB FIELDS '''
                tab_hotkey.hotkeys_fields_to_save()

                ''' GENERAL TAB FIELDS '''
                tab_general.general_fields_to_save()

                ''' PLAYLISTS TAB FIELDS '''
                switch_all_pl_to_standard_from_thumbnails_view()
                tab_playlist.playlists_fields_to_save()

                ''' SKINS TAB FIELDS '''
                tab_skins.skins_fields_to_save()


                ''' 
                    - Playing playlist removed (media played + stopped + playlist removed)
                        >> to make sure the next "Play" will be actioned on the new active / displayed playlist
                    - Playing playlist removed (media played + stopped + playlist removed) + app closed
                        >> app starts with the new first non-hidden playlist
                    - Active playlist removed 
                        >> automatically switching to another playlist tab 
                        >> the new "active_playlist_index" (json: last_used_playlist) value being saved automatically
                '''
                # PLAYING PLAYLIST
                if  len(settings['playlists'][cv.playlist_list[cv.playing_playlist_index]]['playlist_title']) == 0:
                    cv.playing_playlist_index = settings['playlists'][pl_list_with_title[0]]['playlist_index']
                    settings['playing_playlist'] = cv.playing_playlist_index
                    update_playing_playlist_vars_and_widgets()
                    save_json()

                self.hide()


        """ ACTION BUTTON """
        def action_button_clicked():
            combo_box_selected = action_combo_box.currentText()
            action_combo_box_dir[combo_box_selected]()

        BUTTON_ACTION_WIDTH = 50
        BUTTON_ACTION_HIGHT = 25
        BUTTON_ACTION_POS_X = WINDOW_WIDTH - TABS_POS_X - BUTTON_ACTION_WIDTH
        BUTTON_ACTION_POS_Y = WINDOW_HEIGHT - TABS_POS_Y - BUTTON_ACTION_HIGHT

        button_action = QPushButton(self, text='<<<')
        button_action.setGeometry(
            BUTTON_ACTION_POS_X,
            BUTTON_ACTION_POS_Y,
            BUTTON_ACTION_WIDTH,
            BUTTON_ACTION_HIGHT)
        button_action.clicked.connect(lambda: action_button_clicked())
        set_widgets_style(button_action)



        """ ACTION COMBO BOX """
        ACTION_COMBO_WIDTH = 140
        ACTION_COMBO_HEIGHT = BUTTON_ACTION_HIGHT
        ACTION_COMBO_POS_X = BUTTON_ACTION_POS_X - ACTION_COMBO_WIDTH - 5
        ACTION_COMBO_POS_Y = BUTTON_ACTION_POS_Y

        action_combo_box_dir = {
            'Save': save_action,
            'Purge thumbnails': msg_box_wrapper_for_remove_all_thumbnails_and_clear_history,
            'Open log file': open_log_file
        }
        action_combo_box_item_list = list(action_combo_box_dir)
        action_combo_box_item_list.sort()

        action_combo_box = QComboBox(self)
        action_combo_box.setFont(inactive_track_font_style)
        action_combo_box.addItems(action_combo_box_item_list)
        action_combo_box.setCurrentIndex(action_combo_box_item_list.index('Save'))
        action_combo_box.setEditable(True)
        action_combo_box.lineEdit().setAlignment(Qt.AlignmentFlag.AlignRight)
        action_combo_box.lineEdit().setReadOnly(True)
        set_widgets_style(action_combo_box)
        action_combo_box.setGeometry(
            ACTION_COMBO_POS_X,
            ACTION_COMBO_POS_Y,
            ACTION_COMBO_WIDTH,
            ACTION_COMBO_HEIGHT
        )


    def reposition_window_to_middle(self):
        """ Used in "br.window_settings.reposition_window_to_middle()" """
        move_window_to_middle_of_current_screen(self)