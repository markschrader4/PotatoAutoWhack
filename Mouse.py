import win32api as api, win32con as con, time

class Mouse:
    """Mouse manipulation using win32api and win32con"""
    def click(x, y):
        api.SetCursorPos((x, y))
        api.mouse_event(con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        api.mouse_event(con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        
    #UNFINISHED
    def clickandmove(x1, y1, x2, y2):
        t = int((x2 + x1) / 2)
        e = int((y2 + y1) / 2)
        api.SetCursorPos((x1,y1))
        api.mouse_event(api.MOUSEEVENTF_LEFTDOWN,x1,y1,0,0)
        time.sleep(1)
        api.SetCursorPos((t,e))
        time.sleep(1)
        api.mouse_event(api.MOUSEEVENTF_LEFTUP,x2,y2,0,0)
    
    def rightclick(x, y):
        api.SetCursorPos((x,y))
        api.mouse_event(api.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        api.mouse_event(api.MOUSEEVENTF_RIGHTUP,x,y,0,0)

    def move(x, y):
        api.SetCursorPos((x,y))