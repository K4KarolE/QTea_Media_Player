import sys
import pytest
from src.message_box import *
from src.application import logger_sum, QApplication
from src.icons import MyIcon
from src.class_bridge import br


@pytest.fixture
def test_instance():
    """ logger_sum() declares a variable, which will be used
        in the @logger_runtime MyIcon()
    """
    logger_sum('App started')
    return QApplication(sys.argv), MyIcon()


def test_my_message_box_error(test_instance):
    app, br.icon = test_instance
    mmb_error = MyMessageBoxError('Test title', 'Test error message')
    assert mmb_error.windowTitle() == 'ERROR - Test title'
    assert mmb_error.text() ==  'Test error message' + ' ' * 8


def test_my_message_box_warning(test_instance):
    app, br.icon = test_instance
    mmb_warning = MyMessageBoxWarning()
    assert mmb_warning.windowTitle() == 'Warning - Queued track'
    assert mmb_warning.text() ==  ('There is a queued track in the playlist!  ' +
            'It will be removed from the queue list.\n\n' +
            'Do you want to clear the playlist?')


def test_my_message_box_confirmation_request(test_instance):
    app, br.icon = test_instance
    mmb_conf_req = MyMessageBoxConfReq('test_question', lambda: print('Test function'))
    assert mmb_conf_req.windowTitle() == 'Confirmation needed'


def test_my_message_box_confirmation(test_instance):
    app, br.icon = test_instance
    mmb_conf = MyMessageBoxConfirmation('Test title', 'Test confirmation message')
    assert mmb_conf.windowTitle() == 'Test title'
    assert mmb_conf.text() == 'Test confirmation message'
