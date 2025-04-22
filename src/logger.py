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


def logger_runtime(func):

    def func_wrapper(*args, **kwargs):
        logger.info(f'START: {func.__name__}')
        timer_start = perf_counter()
        func_actioned = func(*args, **kwargs)
        timer_stop = perf_counter()
        logger.info(f'{func.__name__} - runtime: {str(timer_stop-timer_start)[:4]}')
        return func_actioned
    return func_wrapper


def logger_basic(msg):
    logger.info(msg)
    if msg == 'App started':
        logger.app_started = time()
    elif msg == 'Window displayed':
        time_diff = str(time() - logger.app_started)[0:5]
        msg = f'Launch time: {time_diff}'
        logger.info(msg)
        