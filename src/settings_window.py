''' 
    Settings window displayed once the settings button
    (cog icon) clicked under the playlists section
'''

from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QTabWidget
    )

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

from pathlib import Path

from .cons_and_vars import cv, settings, PATH_JSON_SETTINGS
from .cons_and_vars import save_json
from .func_coll import inactive_track_font_style
from .message_box import MyMessageBoxError


class MySettingsWindow(QWidget):
    
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
        self.setWindowIcon(QIcon(str(Path(Path().resolve(), 'skins', cv.skin_selected, 'settings.png'))))
        self.setWindowTitle("Settings")


        '''
        ############
            TABS         
        ############
        ''' 
        TABS_POS_X = 10
        TABS_POS_Y = 10

        tabs = QTabWidget(self)
        tabs.setFont(QFont('Times', 10, 500))
        tabs.resize(WINDOW_WIDTH-TABS_POS_X*2, WINDOW_HEIGHT-TABS_POS_Y*6) 
        tabs.move(TABS_POS_X+2, TABS_POS_Y+2)
        tabs.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            "background: #287DCC;" 
                            "color: white;"   # font
                            "}"
                        )

        tab_playlist = QWidget() 
        tab_general = QWidget()
        tab_hotkey = QWidget()

        tabs.addTab(tab_playlist, 'Playlists')
        tabs.addTab(tab_general, 'General')
        tabs.addTab(tab_hotkey, 'Hotkeys')

        LINE_EDIT_TEXT_ALIGNMENT = (Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        LINE_EDIT_HIGHT = 20
        WIDGETS_POS_X=45
        WIDGETS_POS_Y=20
        WIDGETS_NEXT_LINE_POS_Y_DIFF = 25


        def get_dic_values_before_widget_creation(dictionary, item):
            item_text = dictionary[item]['text']
            item_value = dictionary[item]['value']
            return item_text, item_value

        def get_dic_values_after_widget_creation(dictionary, item):
            item_text = dictionary[item]['text']
            item_value = dictionary[item]['value']
            line_edit_text = dictionary[item]['line_edit_widget'].text()
            line_edit_text = line_edit_text.strip().title()
            return item_text, item_value, line_edit_text
        

        
        '''
        ######################
            TAB - HOTKEYS          
        ######################
        '''
        WIDGET_HOTKEY_POS_X = WIDGETS_POS_X
        widget_hotkey_pos_y = WIDGETS_POS_Y
        HOTKEY_LABEL_LINE_EDIT_POS_X_DIFF = 180

        for item in cv.hotkey_settings_dic:

            item_text, item_value = get_dic_values_before_widget_creation(cv.hotkey_settings_dic, item)

            ''' LABEL '''
            item_label = QLabel(tab_hotkey, text=item_text)
            item_label.setFont(inactive_track_font_style)
            item_label.move(WIDGET_HOTKEY_POS_X, widget_hotkey_pos_y)

            ''' LINE EDIT '''
            cv.hotkey_settings_dic[item]['line_edit_widget'] = QLineEdit(tab_hotkey)
            line_edit_widget = cv.hotkey_settings_dic[item]['line_edit_widget']

            line_edit_widget.setText(item_value)
            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_HOTKEY_POS_X + HOTKEY_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_hotkey_pos_y,
                120,
                LINE_EDIT_HIGHT
                )

            widget_hotkey_pos_y += WIDGETS_NEXT_LINE_POS_Y_DIFF


        def hotkey_fields_validation(pass_validation = True):
            
            ''' EXPRESSION CHECK '''
            line_edit_text_all_values = []

            for item in cv.hotkey_settings_dic:

                item_text, item_value, line_edit_text = get_dic_values_after_widget_creation(cv.hotkey_settings_dic, item)

                line_edit_text_all_values.append(line_edit_text)

                search_result = cv.search_regex.search(line_edit_text.title())
                if not search_result:
                    MyMessageBoxError('HOTKEYS TAB', f'The "{item_text}" value is not valid!')
                    pass_validation = False

             
            ''' DUPLICATE CHECK '''
            if pass_validation:
                for index, item in enumerate(line_edit_text_all_values):
                    for index_2, item_2 in enumerate(line_edit_text_all_values[(index+1):]):
                        if item == item_2:
                            MyMessageBoxError('HOTKEYS TAB', f'The "{item}" hotkey value used more than once!')
                            pass_validation = False

            return pass_validation 
        

        def hotkeys_fields_to_save(to_save = False):
            
            for item in cv.hotkey_settings_dic:

                item_text, item_value, line_edit_text = get_dic_values_after_widget_creation(cv.hotkey_settings_dic, item)

                if item_value != line_edit_text:
                    settings['hotkey_settings'][item] = line_edit_text
                    to_save = True
                    
            if to_save:
                save_json(settings, PATH_JSON_SETTINGS)


        
        '''
        ######################
            TAB - GENEREAL          
        ######################
        '''
        WIDGET_GENERAL_POS_X = WIDGETS_POS_X
        widget_general_pos_y = WIDGETS_POS_Y
        GENERAL_LABEL_LINE_EDIT_POS_X_DIFF = 170

        for item in cv.general_settings_dic:

            item_text, item_value = get_dic_values_before_widget_creation(cv.general_settings_dic, item)

            ''' LABEL '''
            item_label = QLabel(tab_general, text=item_text)
            item_label.setFont(inactive_track_font_style)
            item_label.move(WIDGET_GENERAL_POS_X, widget_general_pos_y)

            ''' LINE EDIT '''
            cv.general_settings_dic[item]['line_edit_widget'] = QLineEdit(tab_general)
            line_edit_widget = cv.general_settings_dic[item]['line_edit_widget']
            
            # JUMP VALUES
            if 'jump' in item_text:
                line_edit_widget.setText(str(int(item_value/1000)))
            # OTHER VALUES    
            else:
                line_edit_widget.setText(str(item_value))

            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_GENERAL_POS_X + GENERAL_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_general_pos_y,
                100,
                LINE_EDIT_HIGHT
                )

            widget_general_pos_y += WIDGETS_NEXT_LINE_POS_Y_DIFF
        

        def general_fields_validation(pass_validation = True):

            MAX_WINDOW_SIZE_XY = 4500

            # screen values can be bigger than the display size - no over-reaching
            for item in cv.general_settings_dic:

                item_text, item_value, line_edit_text = get_dic_values_after_widget_creation(cv.general_settings_dic, item)

                if item_text in cv.gen_sett_boolean_text_list:
                    if line_edit_text not in ['True', 'False']:
                        MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be "True" or "False"!')
                        pass_validation = False
                
                elif item_text in cv.gen_sett_window_width_text_list:
                    if (not line_edit_text.isdecimal() or 
                        int(line_edit_text) < cv.window_min_width or
                        int(line_edit_text) > MAX_WINDOW_SIZE_XY):
                            MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be an integer: {cv.window_min_width}=< X <={MAX_WINDOW_SIZE_XY}')
                            pass_validation = False
                
                elif item_text in cv.gen_sett_window_height_text_list:
                    if (not line_edit_text.isdecimal() or
                        int(line_edit_text) < cv.window_min_height or
                        int(line_edit_text) > MAX_WINDOW_SIZE_XY):
                            MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be an integer: {cv.window_min_width}=< X <={MAX_WINDOW_SIZE_XY}')
                            pass_validation = False
                else:
                    if not line_edit_text.isdecimal():
                        MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be a positive integer!')
                        pass_validation = False

            return pass_validation
        

        def general_fields_to_save(to_save = False):
            for item in cv.general_settings_dic:

                item_text, item_value, line_edit_text = get_dic_values_after_widget_creation(cv.general_settings_dic, item)

                if item_text in cv.gen_sett_jump_text_list:
                    if item_value != int(line_edit_text)*1000:
                        settings['general_settings'][item] = int(line_edit_text)*1000
                        to_save = True
   
                elif item_text in cv.gen_sett_boolean_text_list:
                    if item_value != line_edit_text:
                        settings['general_settings'][item] = line_edit_text
                        to_save = True
   
                else:
                    if item_value != int(line_edit_text):
                        settings['general_settings'][item] = int(line_edit_text)
                        to_save = True

            if to_save:
                save_json(settings, PATH_JSON_SETTINGS)
            


        ''' TAB - PLAYLISTS '''
        ''' VALUE SAVING IN button_save_clicked()'''
        WIDGET_PL_POS_X = WIDGETS_POS_X
        widget_pl_pos_y = WIDGETS_POS_Y
        PL_LABEL_LINE_EDIT_POS_X_DIFF = 100
        number_counter = 1

        # AT GENERAL AND HOTKEYS TAB THE LOWEST DIC. KAY-VALUE PAIR WERE ITERATED
        # AT PLAYLIST IT IS THE TOP / PLAYLIST TITLES
        for pl in cv.paylist_widget_dic:

            ''' LABEL '''
            number = QLabel(tab_playlist, text=f'Playlist #{number_counter}')
            number.setFont(inactive_track_font_style)
            
            if number_counter >= 10:
                number.move(WIDGET_PL_POS_X, widget_pl_pos_y)
            else:
                number.move(WIDGET_PL_POS_X, widget_pl_pos_y)

            ''' LINE EDIT '''
            cv.paylist_widget_dic[pl]['line_edit'] = QLineEdit(tab_playlist)
            line_edit_widget = cv.paylist_widget_dic[pl]['line_edit']

            line_edit_widget.setText(settings[pl]['tab_title'])
            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_PL_POS_X + PL_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_pl_pos_y,
                170,
                LINE_EDIT_HIGHT
                )

            number_counter += 1
            widget_pl_pos_y += WIDGETS_NEXT_LINE_POS_Y_DIFF

        

        '''
        ####################
            BUTTON - SAVE      
        ####################
        '''
        BUTTON_SAVE_WIDTH = 50
        BUTTON_SAVE_HIGHT = 25
        BUTTON_SAVE_POS_X = WINDOW_WIDTH - TABS_POS_X - BUTTON_SAVE_WIDTH
        BUTTON_SAVE_POS_Y = WINDOW_HEIGHT - TABS_POS_Y - BUTTON_SAVE_HIGHT

        def is_at_least_one_playlist_title_kept():
            pl_list_with_title = []
            for pl in cv.paylist_widget_dic:
                playlist_title = cv.paylist_widget_dic[pl]['line_edit'].text().strip()
                if len(playlist_title) != 0:
                    pl_list_with_title.append(pl)
            if len(pl_list_with_title) == 0:
                MyMessageBoxError('PAYLISTS TAB', 'At least one playlist title needed!')
            return pl_list_with_title

    
        def button_save_clicked(to_save = False):
                
            pl_list_with_title = is_at_least_one_playlist_title_kept()
            
            if pl_list_with_title and general_fields_validation() and hotkey_fields_validation():
                
                ''' GENERAL TAB FIELDS '''
                hotkeys_fields_to_save()

                ''' GENERAL TAB FIELDS '''
                general_fields_to_save()


                ''' PAYLISTS TAB FIELDS '''
                for pl in cv.paylist_widget_dic:
                    playlist_title = cv.paylist_widget_dic[pl]['line_edit'].text().strip()
                    
                    if playlist_title != settings[pl]['tab_title']:
                        settings[pl]['tab_title'] = playlist_title
                        to_save = True

                ''' 
                    If the last used tab/playlist removed 
                    at next start the new last tab will active / displayed
                '''
                if  len(settings[cv.paylist_list[cv.active_tab]]['tab_title']) == 0:
                    cv.active_tab = settings[pl_list_with_title[-1]]['tab_index']
                    settings['last_used_tab'] = cv.active_tab

                if to_save:
                    save_json(settings, PATH_JSON_SETTINGS)
            
                self.hide()


        button_save = QPushButton(self, text='SAVE')
        button_save.setGeometry(BUTTON_SAVE_POS_X, BUTTON_SAVE_POS_Y, BUTTON_SAVE_WIDTH, BUTTON_SAVE_HIGHT)    
        button_save.clicked.connect(button_save_clicked)
