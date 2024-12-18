'''
Prevent the screen saver - Windows

Cheers mate!
https://stackoverflow.com/questions/63076389/python-prevent-the-screen-saver
'''
import ctypes

#this will prevent the screen saver or sleep.
ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  

#set the setting back to normal
ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)