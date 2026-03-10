import sys
import pytest
from src.application import *
from src.icons import *

@pytest.fixture
def test_instance():
    """ logger_sum() declares a variable, which will be used
        in the @logger_runtime in MyApp() and MyIcon()
    """
    logger_sum('App started')
    MyApp(sys.argv)
    return MyIcon()


def test_icons(test_instance):
    """ QIcon:
            test_instance.***.availableSizes() >> [PyQt6.QtCore.QSize(96, 96)]
            or an empty list if the path is not correct
        QPixmap:
            test_instance.***.width() >> 50
            or 0 if the path is not correct
    """

    assert test_instance.remove.availableSizes() != []
    assert test_instance.window_icon.availableSizes() != []

    assert test_instance.start.availableSizes() != []
    assert test_instance.pause.availableSizes() != []
    assert test_instance.stop.availableSizes() != []
    assert test_instance.previous.availableSizes() != []
    assert test_instance.next.availableSizes() != []
    assert test_instance.repeat.availableSizes() != []
    assert test_instance.repeat_single.availableSizes() != []
    assert test_instance.shuffle.availableSizes() != []

    assert test_instance.toggle_video.availableSizes() != []
    assert test_instance.toggle_playlist.availableSizes() != []
    assert test_instance.settings.availableSizes() != []

    assert test_instance.thumbnail.availableSizes() != []

    # QPixmap
    assert test_instance.thumbnail_default.width() != 0
    assert test_instance.thumbnail_default_video.width() != 0
    assert test_instance.thumbnail_playing_video.width() != 0
    assert test_instance.thumbnail_default_audio.width() != 0
    assert test_instance.thumbnail_playing_audio.width() != 0


    assert test_instance.speaker.availableSizes() != []
    assert test_instance.queue.availableSizes() != []
    assert test_instance.queue_blue.availableSizes() != []
    assert test_instance.de_queue.availableSizes() != []
    assert test_instance.folder.availableSizes() != []
    assert test_instance.remove.availableSizes() != []
    assert test_instance.search.availableSizes() != []
    assert test_instance.clear_queue.availableSizes() != []
    assert test_instance.clear_multi_selection.availableSizes() != []

    assert test_instance.start_with_default_player.availableSizes() != []
    assert test_instance.minimal_interface.availableSizes() != []

    assert test_instance.alter.availableSizes() != []
    assert test_instance.selected.availableSizes() != []


def test_fail(test_instance):
    with pytest.raises(Exception):
        assert test_instance.no_image.availableSizes() != []