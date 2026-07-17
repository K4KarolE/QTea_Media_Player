import sys

from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QApplication

from .class_data import cv
from .class_bridge import br
from .logger import *

"""
To avoid system theme >> qt app theme
https://doc.qt.io/qt-6/qguiapplication.html#setDesktopSettingsAware

windll - myappid:
To get the packaged application taskbar icon from the window icon,
otherwise the taskbar icon is the default python group icon 

Taskbar Icons section in:
https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/
"""
if cv.os_linux:
    QApplication.setDesktopSettingsAware(False)
else:
    sys.argv += ['-platform', 'windows:darkmode=1']
    try:
        from ctypes import windll
        myappid = 'qtea-media-player'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        logger_check("ctypes import - Packaged app`s taskbar icon issue")



@logger_runtime
class MyApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
        self.installEventFilter(self)
        self.app_moved_while_fullscreen_mode = False
        self.applicationStateChanged.connect(lambda: self.application_state_changed_action())
        self.is_app_status_changed = False
        if not cv.os_linux:
            self.setStyle("Fusion")     # To avoid system theme >> qt app theme


    def application_state_changed_action(self):
        if not self.is_app_status_changed:
            br.av_player.set_base_track_as_source()
            self.is_app_status_changed = True


    def eventFilter(self, source, event):
        """ 
        Used to track the app`s repositioning
        >> double-clicking on the video
        >> full screen on the current display
        more: src / av_player
        """      
        starting_pos, end_pos = 0, 0

        if event.type() == QEvent.Type.NonClientAreaMouseButtonPress:
            starting_pos = br.window.pos().x()
            """ 
            Scenario:
            the app and the full screen video are on
            different display
            
            Moving the app >>
                > the video would move back to the
                app`s area automatically and disable
                full screen mode

            Solution:
                > hiding the video while moving the app
                > set full screen mode back once the
                mouse button released
            """
            if br.av_player.video_output.isFullScreen():
                br.av_player.video_output.hide()
                self.app_moved_while_fullscreen_mode = True
        
        if event.type() == QEvent.Type.NonClientAreaMouseButtonRelease:
            end_pos = br.window.pos().x()
            cv.screen_pos_x_for_fullscreen = end_pos - starting_pos

            if self.app_moved_while_fullscreen_mode:
                br.av_player.full_screen_to_screen_toggle()
                br.av_player.video_output.show()
                self.app_moved_while_fullscreen_mode = False

        return super().eventFilter(source, event)   