from PyQt6.QtWidgets import QLabel, QLineEdit, QScrollArea, QWidget

from .class_data import cv, settings, save_json
from .func_coll import inactive_track_font_style
from .message_box import MyMessageBoxError
from .window_settings_common import CommonTabValues



class HotkeysTab(CommonTabValues):
    def __init__(self):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.inner_window = QWidget()
        self.last_widget_pos_y = 0

        WIDGET_HOTKEY_POS_X = self.WIDGETS_POS_X
        widget_hotkey_pos_y = self.WIDGETS_POS_Y
        HOTKEY_LABEL_LINE_EDIT_POS_X_DIFF = 180
        LINE_BREAK_AFTER_LIST_HOTK = [
            'big_jump_forward',
            'display_track_info_on_video',
            'audio_output_device_rotate',
            'subtitle_tracks_rotate',
            'next_track',
            'window_size_toggle',
            'playlist_select_next_pl',
            'remove_black_bars_around_video',]
        LINE_BREAK_SIZE_HOTK = 20
        LINE_BREAK_SEPERATOR_HOTK = "\n " + "_" * 35

        for hotkey_dic_key, hotkey_dic_value in cv.hotkey_settings_dic.items():

            item_text, item_value = self.get_dic_values_before_widget_creation(hotkey_dic_value)

            ''' LABEL '''
            # Adding seperator to the line break
            # In the Settings window it looks like there is a separator below the field title
            # The field title and the separator are one QLabel object
            item_text_original = item_text
            if hotkey_dic_key in LINE_BREAK_AFTER_LIST_HOTK:
                item_text += LINE_BREAK_SEPERATOR_HOTK

            item_label = QLabel(self.inner_window, text=item_text)
            item_label.setFont(inactive_track_font_style)
            item_label.move(WIDGET_HOTKEY_POS_X, widget_hotkey_pos_y)

            ''' LINE EDIT '''
            hotkey_dic_value['line_edit_widget'] = QLineEdit(self.inner_window)
            line_edit_widget = hotkey_dic_value['line_edit_widget']

            line_edit_widget.setText(item_value)
            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(self.LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_HOTKEY_POS_X + HOTKEY_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_hotkey_pos_y,
                120,
                self.LINE_EDIT_HIGHT
                )

            # Adding extra space after a multi line QLabel field title like:
            # "Automatically clear playlist
            #  when it is removed"            #
            lines_amount = item_text_original.count('\n') + 1  # line break in too long text - multiple lines
            if lines_amount != 1:
                multi_line_compensation = lines_amount * 12
            else:
                multi_line_compensation = 0

            widget_hotkey_pos_y += int(self.WIDGETS_NEXT_LINE_POS_Y_DIFF + multi_line_compensation)

            # To make gap between different sections, item: 'always_on_top', 'continue_playback'
            if hotkey_dic_key in LINE_BREAK_AFTER_LIST_HOTK:
                widget_hotkey_pos_y += LINE_BREAK_SIZE_HOTK

        self.last_widget_pos_y = widget_hotkey_pos_y + self.EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y



    def hotkey_fields_validation(self, pass_validation = True):
        """ EXPRESSION CHECK """
        line_edit_text_all_values = []

        for hotkey_dic_key, hotkey_dic_value in cv.hotkey_settings_dic.items():

            item_text, item_value, line_edit_text = self.get_dic_values_after_widget_creation(hotkey_dic_value)

            if "|" in line_edit_text:   # multiple hotkeys for the same action
                for line_edit_text in line_edit_text.split("|"):
                    line_edit_text = line_edit_text.strip()
                    line_edit_text_all_values.append(line_edit_text)
            else:
                line_edit_text_all_values.append(line_edit_text)

            search_result = cv.search_regex.search(line_edit_text.title())
            if not search_result:
                item_text = item_text.replace('\n', ' ')
                MyMessageBoxError('HOTKEYS TAB', f'The "{item_text}" value is not valid.\n\n' +
                "Acceptable hotkey format examples:\n" +
                "`M`, `m`, `Ctrl`, `ctRL`, `M+Ctrl`, `Ctrl++`, `Ctrl+-`," +
                "`M+Ctrl+Space`, `Shift+Left`, `M | P`, `M+Ctrl | P`")
                pass_validation = False


        ''' DUPLICATE CHECK '''
        if pass_validation:
            for index, item in enumerate(line_edit_text_all_values):
                for index_2, item_2 in enumerate(line_edit_text_all_values[(index+1):]):
                    if item == item_2 and item != '':
                        MyMessageBoxError('HOTKEYS TAB', f'The "{item}" hotkey value used more than once.')
                        pass_validation = False

        return pass_validation


    def hotkeys_fields_to_save(self, to_save = False):
        for hotkey_dic_key, hotkey_dic_value in cv.hotkey_settings_dic.items():

            item_text, item_value, line_edit_text = self.get_dic_values_after_widget_creation(hotkey_dic_value)

            if item_value != line_edit_text:
                settings['hotkey_settings'][hotkey_dic_key] = line_edit_text
                cv.hotkey_settings_dic[hotkey_dic_key]['value'] = line_edit_text
                to_save = True
        if to_save:
            save_json()