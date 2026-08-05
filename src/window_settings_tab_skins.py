from pathlib import Path
import os

from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
    )

from .class_data import cv, settings, save_json
from .class_skins import sk
from .func_coll import inactive_track_font_style
from .window_settings_common import CommonTabValues


class SkinsTab(CommonTabValues):
    def __init__(self):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.inner_window = QWidget()
        self.skins_dir = Path(Path().resolve(), 'skins')
        self.skins_jsons_dir = Path(Path().resolve(), 'skins', 'jsons')
        self.skins_list = self.gen_available_skins_list()
        self.skins_with_icons_list  = self.gen_skins_with_icons_list()
        self.logo_imgs_dir = self.gen_available_logo_imgs_dir()
        self.img_sizes_list = [str(n) for n in range(200, 420, 20)]

        WIDGET_POS_X = self.WIDGETS_POS_X
        widget_pos_y = self.WIDGETS_POS_Y
        COMBO_BOX_WIDGET_LENGTH = 300
        INFO_WIDGET_LENGTH = 300
        INFO_WIDGET_HIGHT = 30
        WIDGET_HIGHT = 25
        GAP = 15
        number_counter = 1

        info_widget = QPushButton('Restart needed for the changes take place')
        info_widget.setEnabled(False)

        # SKINS
        self.skins_combo_box = QComboBox()
        self.skins_combo_box.addItems(self.skins_list)
        self.skins_combo_box.setCurrentIndex(self.skins_list.index(cv.skin_selected))

        # ICONS
        self.skin_icons_combo_box = QComboBox()
        self.skin_icons_combo_box.addItems(self.skins_with_icons_list)
        self.skin_icons_combo_box.setCurrentIndex(self.skins_with_icons_list.index(cv.skin_icons))

        # LOGO
        self.logo_imgs_combo_box = QComboBox()
        self.logo_imgs_combo_box.addItems(self.logo_imgs_dir.keys())
        img_rep = f'{cv.skin_logo_path_list[0]} - {cv.skin_logo_path_list[1]}'
        if img_rep in self.logo_imgs_dir.keys():
            self.logo_imgs_combo_box.setCurrentIndex(list(self.logo_imgs_dir.keys()).index(img_rep))

        # LOGO SIZE
        self.img_size_combo_box = QComboBox()
        self.img_size_combo_box.addItems(self.img_sizes_list)
        self.img_size_combo_box.setCurrentIndex(self.img_sizes_list.index(cv.skin_logo_img_size))

        skins_tab_widgets_dic = {
            'info_widget': info_widget,
            'skins_combo_box_label': QLabel("Skins"),
            'skins_combo_box': self.skins_combo_box,
            'skin_icons_combo_box_label': QLabel("Icons"),
            'skin_icons_combo_box': self.skin_icons_combo_box,
            'images_combo_box_label': QLabel("Logo Images"),
            'images_combo_box': self.logo_imgs_combo_box,
            'img_size_combo_box_label': QLabel("Logo Image Size"),
            'img_size_combo_box': self.img_size_combo_box
            }

        for key in skins_tab_widgets_dic:
            widget = skins_tab_widgets_dic[key]
            widget.setParent(self.inner_window)
            widget.setFont(inactive_track_font_style)
            self.set_widgets_style(widget)
            widget.setGeometry(
                WIDGET_POS_X,
                widget_pos_y,
                COMBO_BOX_WIDGET_LENGTH,
                WIDGET_HIGHT
                )

            info_widget.resize(INFO_WIDGET_LENGTH, INFO_WIDGET_HIGHT)

            if key in ['info_widget', 'skins_combo_box','skin_icons_combo_box', 'images_combo_box']:
                widget_pos_y += (self.WIDGETS_NEXT_LINE_POS_Y_DIFF + GAP)
                if key == 'info_widget': widget_pos_y += 15
            else:
                widget_pos_y += self.WIDGETS_NEXT_LINE_POS_Y_DIFF
            number_counter += 1

        self.last_widget_pos_y = widget_pos_y + self.EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y
        # to make sure the background covers the whole inner window
        if self.last_widget_pos_y < 525: self.last_widget_pos_y = 525


    def gen_available_skins_list(self):
        skins_list = [p.name for p in self.skins_dir.iterdir() if p.is_dir()]
        skins_list.sort()
        skins_list.remove("jsons")
        # Checking relevant JSON exists
        unavailable_skins = []
        for skin in skins_list:
            if skin != 'system':
                file_name = f'{skin}.json'
                file_path = Path(self.skins_jsons_dir, file_name)
                if not Path(file_path).is_file():
                    unavailable_skins.append(skin)
        if unavailable_skins:
            for un_skin in unavailable_skins:
                skins_list.remove(un_skin)
        return skins_list


    def gen_skins_with_icons_list(self):
        skins_with_icons_list = []
        for skin in self.skins_list:
            start_icon_path = f'skins/{skin}/start.png'
            if Path(start_icon_path).is_file():
                skins_with_icons_list.append(skin)
        skins_with_icons_list.sort()
        return skins_with_icons_list


    def gen_available_logo_imgs_dir(self):
        logo_imgs_dir = {}
        for skin in self.skins_list:
            images_dir = Path(self.skins_dir, skin, 'images')
            for _, _, file_names in os.walk(images_dir):
                for file in file_names:
                    if file.split('.')[-1] in ['png', 'jpg', 'jpeg']:
                        logo_imgs_dir[f'{skin} - {file}'] = str(Path(images_dir, file))
        return logo_imgs_dir


    def skins_fields_to_save(self):
        settings['skin_selected'] = self.skins_combo_box.currentText()
        img_path_list = self.logo_imgs_combo_box.currentText().split('-')
        settings['skin_logo_path_list'] = [n.strip() for n in img_path_list]
        settings['skin_logo_img_size'] = self.img_size_combo_box.currentText()
        save_json()


    def set_widgets_style(self, widget):
        widget.setStyleSheet(
                        "QPushButton"
                            "{"
                            f"color: {sk.row_inactive_text};"
                            "}"
                        "QComboBox"
                            "{"
                            f"background: {sk.row_inactive};"
                            f"color: {sk.row_inactive_text};"
                            "}"
                        "QComboBox::item:selected"
                            "{"
                            f"background: {sk.row_playing};"
                            f"color: {sk.row_playing_text};"
                        "}"
                        )