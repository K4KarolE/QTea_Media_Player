'''
    Used to measure the time of 
    - application launch: main.py
    - add directory: src / buttons.py / button_add_dir_clicked()
    
    LEARNED:
    The function with the @logger_runtime decorator need to be called with lambda:
        - button_add_dir.clicked.connect(lambda: button_add_dir.button_add_dir_clicked())
        -   @logger_runtime
            def button_add_dir_clicked(self):...
        - otherwise:
        TypeError: MyButtons.button_add_dir_clicked() takes 1 positional argument but 2 were given
'''

import logging
from time import perf_counter, time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="log_file.log",
                    format='%(asctime)s %(message)s',
                    filemode='w') # w/a

""" PlaysFunc and Data class creations' time so small
    >> gave back invalid values >> not measurable
    >> no logging added
"""

def logger_runtime(func):
    """ To check the class creation, function running time """
    def func_wrapper(*args, **kwargs):
        timer_start = perf_counter()
        func_actioned = func(*args, **kwargs)
        timer_stop = perf_counter()
        diff_raw = timer_stop-timer_start
        if diff_raw >= 0.1:
            marker = ' *' * 10
        else: marker = ''
        logger.info(f'{func.__name__}: {str(timer_stop-timer_start)[:7]}{marker}')

        time_diff = str(time() - logger.app_started)[0:5]
        logger.info(f'{func.__name__} - sum: {time_diff}\n')

        return func_actioned
    return func_wrapper


def logger_check(func):
    """ To check when a function is called """
    def func_wrapper(*args, **kwargs):
        func_actioned = func(*args, **kwargs)
        logger.info(f'{func.__name__}')
        return func_actioned
    return func_wrapper


def logger_sum(msg):
    """ No logging for src / window_settings / MySettingsWindow at startup
        It is created once the Settings button clicked
    """
    if msg == 'App started':
        logger.app_started = time()
        logger.info(msg)

    elif 'sum' in msg:
        time_diff = str(time() - logger.app_started)[0:5]
        msg = f'{msg}: {time_diff}'
        logger.info(msg)

    else: logger.info(msg)