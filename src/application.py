from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QApplication


from .class_data import cv
from .class_bridge import br

'''
To avoid system theme >> qt app theme
https://doc.qt.io/qt-6/qguiapplication.html#setDesktopSettingsAware
'''
QApplication.setDesktopSettingsAware(False)




class MyApp(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.installEventFilter(self)
        self.app_moved_while_fullscreen_mode = False


    def eventFilter(self, source, event):
        """ 
            Used to track the app`s repositioning
            >> double clicking on the video
            >> full screen on the current display
            more: src / av_player
        """      
        starting_pos, end_pos = 0, 0

        if event.type() == QEvent.Type.NonClientAreaMouseButtonPress:
            starting_pos = br.window.pos().x()

            """ Scenario:
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
     