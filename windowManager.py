import ctypes

#list of active windows composed of HWND and name
activeWindows = []

#system stuff
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

#FUNCTIONS
def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        activeWindows.append((hwnd, buff.value))
    return True

def getActiveWindows():
    del activeWindows[:]
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    for window in activeWindows:
        if len(window[1]) < 2:
            activeWindows.remove(window)
    return activeWindows
