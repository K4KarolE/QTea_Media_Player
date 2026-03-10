import sys
import pytest
from src.application import *
from src.images import *


def test_images():
    """ logger_sum() declares a variable,
        which will be used in the @logger_runtime in MyApp()
    """
    logger_sum('App started')
    MyApp(sys.argv)

    test_instance = MyImage('logo.png', 50)
    assert test_instance.width() != 0
    assert test_instance.alignment() == 132 # AlignCenter


def test_fail():
    with pytest.raises(Exception):
        test_instance_invalid = MyImage('no_image.png', 60)
        assert test_instance_invalid.width() == 60