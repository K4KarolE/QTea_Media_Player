"""
Resizing the window:
> Reposition the widgets
> Resize the widgets to max fulfillment in the row
> Tried first with the QGridLayout, does not felt right
"""


from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt6.QtCore import Qt, QTimer
import sys

QApplication.setDesktopSettingsAware(False) # avoid OS auto coloring


class Data:
    window_width = 600
    window_height = 400
    thumbnail_width, thumbnail_height = 100, 100
    thumbnail_new_width = thumbnail_width
    thumbnail_pos_gap = 1
    pos_base_x = 5
    pos_base_y = 5
    thumbnail_widget_dic = {}


class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(cv.window_width, cv.window_height)
        self.setMinimumWidth(cv.thumbnail_width + cv.pos_base_x * 2)
        self.setWindowTitle("Thumbnails")
        self.timer = QTimer()
        self.timer.timeout.connect(lambda : self.timer_action())

    def timer_action(self):
        # Timer: For avoiding multiple trigger from resizeEvent
        thumbnails_resize_and_move_to_pos()
        self.timer.stop()

    def resizeEvent(self, a0):
        if cv.window_width != self.width():
            cv.window_width = self.width()
            self.timer.start(500)
        return super().resizeEvent(a0)



class ThumbnailWidget(QWidget):
    def __init__(self, widget_bg_color):
        super().__init__()
        self.setParent(window)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color:{widget_bg_color};")
        self.setMinimumWidth(cv.thumbnail_width)

    def mousePressEvent(self, a0):
        print("Clicked")
        self.setStyleSheet(f"background-color: pink;")

    def mouseDoubleClickEvent(self, a0):
        print("Double clicked")



cv = Data()
app = MyApp()
window = MyWindow()


bg_colors = 'blue red orange purple pink yellow'.split()
for index, bg_color in enumerate(bg_colors):
    cv.thumbnail_widget_dic[index] = ThumbnailWidget(bg_color)



def thumbnails_resize_and_move_to_pos():
    thumbnail_counter = 0
    thumbnail_pos_y = cv.pos_base_y
    generate_thumbnail_new_width()

    for thumbnail_index in cv.thumbnail_widget_dic:
        thumbnail_pos_x = cv.pos_base_x + thumbnail_counter * (cv.thumbnail_new_width + cv.thumbnail_pos_gap)
        # PLACE THUMBNAIL TO A NEW ROW IF NECESSARY
        if thumbnail_pos_x > cv.window_width - cv.thumbnail_width - cv.pos_base_x:
            thumbnail_counter = 0
            thumbnail_pos_x = cv.pos_base_x + thumbnail_counter * (cv.thumbnail_new_width + cv.thumbnail_pos_gap)
            thumbnail_pos_y += cv.thumbnail_height + cv.thumbnail_pos_gap
        cv.thumbnail_widget_dic[thumbnail_index].move(thumbnail_pos_x, thumbnail_pos_y)
        cv.thumbnail_widget_dic[thumbnail_index].resize(cv.thumbnail_new_width, cv.thumbnail_height)
        thumbnail_counter += 1


def generate_thumbnail_new_width():
    available_space =  cv.window_width - 2 * cv.pos_base_x + cv.thumbnail_pos_gap
    thumbnail_and_gap =  cv.thumbnail_width + cv.thumbnail_pos_gap
    thumbnails_in_row_possible = int(available_space / thumbnail_and_gap)
    thumbnail_count = len(cv.thumbnail_widget_dic)
    if thumbnails_in_row_possible >= thumbnail_count:
        thumbnail_width_diff = int((available_space - thumbnail_count * thumbnail_and_gap) / thumbnail_count)
    else:
        thumbnail_width_diff = int((available_space - thumbnails_in_row_possible * thumbnail_and_gap) / thumbnails_in_row_possible)
    cv.thumbnail_new_width = cv.thumbnail_width + thumbnail_width_diff


thumbnails_resize_and_move_to_pos()

window.show()
sys.exit(app.exec())