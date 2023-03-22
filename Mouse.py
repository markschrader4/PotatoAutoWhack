from win32api import SetCursorPos, mouse_event, GetCursorPos
from win32con import MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
from time import sleep


class Mouse:
    """Mouse manipulation using win32api and win32con"""
    def click(x, y):
        """Moves mouse to position on screen and left clicks"""
        SetCursorPos((x, y))
        mouse_event(MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        
    #UNFINISHED
    def clickandmove(x1, y1, x2, y2):
        """Moves mouse to position on screen, holds left click,
        moves to a second position on screen, and releases"""
        t = int((x2 + x1) / 2)
        e = int((y2 + y1) / 2)
        SetCursorPos((x1,y1))
        mouse_event(MOUSEEVENTF_LEFTDOWN,x1,y1,0,0)
        sleep(1)
        SetCursorPos((t,e))
        sleep(1)
        mouse_event(MOUSEEVENTF_LEFTUP,x2,y2,0,0)
    
    def rightclick(x, y):
        """"Moves mouse to a position on screen and right clicks"""
        SetCursorPos((x,y))
        mouse_event(MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        mouse_event(MOUSEEVENTF_RIGHTUP,x,y,0,0)

    def move(x, y):
        """"Moves mouse to a position on screen"""
        SetCursorPos((x,y))
        
    def getmousepos():
        """Returns current mouse pos (x, y)"""
        return GetCursorPos()