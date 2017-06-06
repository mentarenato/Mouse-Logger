import win32gui
import pygame
import ctypes
import os
import svgCreator
import time

from datetime import datetime
from win32gui import GetWindowText, GetForegroundWindow
from pygame.locals import *
from svgCreator import render_svg


#settings for recording
title = 'League of Legends (TM) Client'
debug = False
if debug:
    title = 'Chrome'

#settings for display
SCALING_FACTOR = 0.5
user = ctypes.windll.user32
monitorWidth = user.GetSystemMetrics(0)
monitorHeight = user.GetSystemMetrics(1)
screenWidth = int(monitorWidth * SCALING_FACTOR)
screenHeight = int(monitorHeight * SCALING_FACTOR)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-screenWidth, 35)

#system stuff
activeWindows = []
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible


#colors used in the display
COLOR_BACKGROUND = (0, 0, 0)
COLOR_LINE = (100, 200, 255, 0.1)


#FUNCTIONS
def getActiveWindows():
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    for window in activeWindows:
        if len(window[1]) == 0:
            activeWindows.remove(window)

def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        activeWindows.append((hwnd, buff.value))
    return True

    
def getMousePos():
    pt = win32gui.GetCursorPos()
    return pt


def log(*args):
    if debug:
        print (*args)


def drawLine(start, end):
    startScaled = (int(start[0] * SCALING_FACTOR), int(start[1] * SCALING_FACTOR))
    endScaled = (int(end[0] * SCALING_FACTOR), int(end[1] * SCALING_FACTOR))
    pygame.draw.line(screen, COLOR_LINE, startScaled, endScaled)


def inbound(pos):
    if pos[0] < 0 or pos[0] > monitorWidth:
        return False
    if pos[1] < 0 or pos[1] > monitorHeight:
        return False
    return True


def logActiveWindows():
    log ('\n\nThere are ' + str(len(activeWindows)) + ' windows active:')
    for window in activeWindows:
        log (window)


def initialize(screen):
    pygame.init()
    screen.fill(COLOR_BACKGROUND)
    pygame.display.set_caption('Mouse Tracer')
    while len(coordinates) < 2:
        pos = getMousePos()
        coordinates.insert(0, pos)


def generateTitle(title):
    date = str(datetime.now())[:-10].replace(':', '.')
    fileName = 'mouseTrace[' + date + '] - ' + title.strip()
    return fileName


def wantedWindowActive():
    for window in activeWindows:
        if title in window[1]:
            return True
    return False


################# BEGINNING OF THE PROGRAM #################

#output some infos
        
print('Starting the capture for ', title)
log('Monitor Resolution: ', (monitorWidth, monitorHeight))
log('Background color: ', COLOR_BACKGROUND)
log('Line color: ', COLOR_LINE)

#initialize variables
coordinates = []
windowChange = False
logActiveWindows()
topWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())

#wait for program to start...
print ('\nWaiting for "' + title + '" to start...')
while not title in topWindow:
    topWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())


#initialize graphics
screen = pygame.display.set_mode((screenWidth, screenHeight))
initialize(screen)


#start logging mouse movements
print ('\nGame has started, now logging mouse movements...')
getActiveWindows()
while wantedWindowActive():

    #make sure window keeps responding
    pygame.event.get()

    #make sure we're still in the wanted window
    activeWindows = []
    getActiveWindows()
    topWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if title in topWindow:
        if windowChange:
            windowChange = False
            log('\nWelcome back\n')
        
        #Log movements
        pos = getMousePos()
        if coordinates[0] != pos and inbound(pos):
            log ('Current position: ', pos)
            coordinates.insert(0, pos)
    else:
        if not windowChange:
            log ('\nActive window has changed. Currently active windows:')
            logActiveWindows()
            windowChange = True

    #Update display
    drawLine(coordinates[0], coordinates[1])
    pygame.display.update()



#game is over, save image as vector
fileName = generateTitle(title)
print ('\nGame is over!')
logActiveWindows()
print ('\nCreating SVG-image...')
render_svg(fileName, (monitorWidth, monitorHeight), COLOR_BACKGROUND, COLOR_LINE, coordinates)
render_svg(fileName + ' (fullRender)', (monitorWidth, monitorHeight), (0, 0, 0), (255, 255, 255, 1), coordinates)
print (fileName + '.svg successfully created!')
print ('\nByeBye:)')
pygame.quit()
