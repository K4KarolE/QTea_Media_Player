from PyQt6.QtCore import Qt

class CommonTabValues:
    def __init__(self):
        self.LINE_EDIT_TEXT_ALIGNMENT = (Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.LINE_EDIT_HIGHT = 20
        self.WIDGETS_POS_X = 25
        self.WIDGETS_POS_Y = 20
        self.WIDGETS_NEXT_LINE_POS_Y_DIFF = 25
        self.EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y = 20

    def get_dic_values_before_widget_creation(self, dic_value):
        item_text = dic_value['text']
        item_value = dic_value['value']
        return item_text, item_value

    def get_dic_values_after_widget_creation(self, dic_value):
        item_text = dic_value['text']
        item_value = dic_value['value']
        line_edit_text = dic_value['line_edit_widget'].text()
        line_edit_text = line_edit_text.strip().title()
        return item_text, item_value, line_edit_text