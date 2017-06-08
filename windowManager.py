import ctypes
import win32gui

# List of active windows composed of HWND and name
openWindows = []

# System stuff
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

# FUNCTIONS
def isWindowOpen(title):
    """Checks if a window titled 'title' is open"""
    openWindows = getOpenWindows()
    for window in openWindows:
        if title in window[1]:
            return True
    return False


def _foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        openWindows.append((hwnd, buff.value))
    return True


def getOpenWindows():
    """Returns a list of all windows open"""
    del openWindows[:]
    EnumWindows(EnumWindowsProc(_foreach_window), 0)
    for window in openWindows:
        if len(window[1]) < 2:
            openWindows.remove(window)
    return openWindows


def getActiveWindow():
    """Returns the name of the currently active window"""
    activeWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return activeWindow


def getMonitorResolution():
    user = ctypes.windll.user32
    monitorWidth = user.GetSystemMetrics(0)
    monitorHeight = user.GetSystemMetrics(1)
    return (monitorWidth, monitorHeight)


def getMousePos():
    pt = win32gui.GetCursorPos()
    return pt
