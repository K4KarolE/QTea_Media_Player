"""
Standard / built-in icons
Cheers: https://stackoverflow.com/q/11643221
"""

from PyQt6.QtWidgets import (QApplication, QGridLayout, QPushButton, QStyle, QWidget)

QApplication.setDesktopSettingsAware(False) # avoid OS auto coloring

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        icons = [
            'SP_ArrowBack',
            'SP_ArrowDown',
            'SP_ArrowForward',
            'SP_ArrowLeft',
            'SP_ArrowRight',
            'SP_ArrowUp',
            'SP_BrowserReload',
            'SP_BrowserStop',
            'SP_CommandLink',
            'SP_ComputerIcon',
            'SP_DesktopIcon',
            'SP_DialogAbortButton',
            'SP_DialogApplyButton',
            'SP_DialogCancelButton',
            'SP_DialogCloseButton',
            'SP_DialogDiscardButton',
            'SP_DialogHelpButton',
            'SP_DialogIgnoreButton',
            'SP_DialogNoButton',
            'SP_DialogNoToAllButton',
            'SP_DialogOkButton',
            'SP_DialogOpenButton',
            'SP_DialogResetButton',
            'SP_DialogRetryButton',
            'SP_DialogSaveAllButton',
            'SP_DialogSaveButton',
            'SP_DialogYesButton',
            'SP_DialogYesToAllButton',
            'SP_DirClosedIcon',
            'SP_DirHomeIcon',
            'SP_DirIcon',
            'SP_DirLinkIcon',
            'SP_DirLinkOpenIcon',
            'SP_DirOpenIcon',
            'SP_DockWidgetCloseButton',
            'SP_DriveCDIcon',
            'SP_DriveDVDIcon',
            'SP_DriveFDIcon',
            'SP_DriveHDIcon',
            'SP_DriveNetIcon',
            'SP_FileDialogBack',
            'SP_FileDialogContentsView',
            'SP_FileDialogDetailedView',
            'SP_FileDialogEnd',
            'SP_FileDialogInfoView',
            'SP_FileDialogListView',
            'SP_FileDialogNewFolder',
            'SP_FileDialogStart',
            'SP_FileDialogToParent',
            'SP_FileIcon',
            'SP_FileLinkIcon',
            'SP_LineEditClearButton',
            'SP_MediaPause',
            'SP_MediaPlay',
            'SP_MediaSeekBackward',
            'SP_MediaSeekForward',
            'SP_MediaSkipBackward',
            'SP_MediaSkipForward',
            'SP_MediaStop',
            'SP_MediaVolume',
            'SP_MediaVolumeMuted',
            'SP_MessageBoxCritical',
            'SP_MessageBoxInformation',
            'SP_MessageBoxQuestion',
            'SP_MessageBoxWarning',
            'SP_RestoreDefaultsButton',
            'SP_TitleBarCloseButton',
            'SP_TitleBarContextHelpButton',
            'SP_TitleBarMaxButton',
            'SP_TitleBarMenuButton',
            'SP_TitleBarMinButton',
            'SP_TitleBarNormalButton',
            'SP_TitleBarShadeButton',
            'SP_TitleBarUnshadeButton',
            'SP_ToolBarHorizontalExtensionButton',
            'SP_ToolBarVerticalExtensionButton',
            'SP_TrashIcon',
            'SP_VistaShield'
        ]

        layout = QGridLayout()

        for n, name in enumerate(icons):
            btn = QPushButton(name)
            pixmapi = getattr(QStyle.StandardPixmap, name)
            icon = self.style().standardIcon(pixmapi)
            btn.setIcon(icon)
            layout.addWidget(btn, int(n / 4), n % 4)

        self.setLayout(layout)

app = QApplication([])
w = Window()
w.show()
app.exec()