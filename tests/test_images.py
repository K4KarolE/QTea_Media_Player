import sys
import pytest
from src.application import logger_sum, QApplication
from src.images import *


def test_images():
    """ logger_sum() declares a variable,
        which will be used in the @logger_runtime in MyImage
    """
    logger_sum('App started')
    app = QApplication(sys.argv)

    test_instance = MyImage('logo.png', 50)
    assert test_instance.width() != 0
    assert test_instance.alignment() == 132 # AlignCenter


def test_fail():
    app = QApplication(sys.argv)
    with pytest.raises(Exception):
        test_instance_invalid = MyImage('no_image.png', 60)
        assert test_instance_invalid.width() == 60