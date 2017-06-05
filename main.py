import win32gui
import pygame
import ctypes
import os

from win32gui import GetWindowText, GetForegroundWindow
from pygame.locals import *


#settings for recording
title = "Discord"
debug = True


#settings for display
SCALING_FACTOR = 0.5
user = ctypes.windll.user32
monitorWidth = user.GetSystemMetrics(0)
monitorHeight = user.GetSystemMetrics(1)
screenWidth = int(monitorWidth * SCALING_FACTOR)
screenHeight = int(monitorHeight * SCALING_FACTOR)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-screenWidth, 35)


#colors used in the display
COLOR_BACKGROUND = (0, 0, 0)
COLOR_LINE = (100, 100, 100, 255)


#FUNCTIONS
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

        

################# BEGINNING OF THE PROGRAM #################

#initialize variables
coordinates = []
activeWindow = GetWindowText(GetForegroundWindow())

#wait for league to start...
log ("\nWaiting for the game to start...")
while title not in activeWindow:
    activeWindow = GetWindowText(GetForegroundWindow())


#initialize graphics
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
screen.fill(COLOR_BACKGROUND)
pygame.display.set_caption(title + " - Game mouse logger")


#add first movements to list
while len(coordinates) < 2:
    pos = getMousePos()
    coordinates.insert(0, pos)


#start logging mouse movements
log ("\nGame has started, now logging mouse movements...")
while title in activeWindow:

    #make sure window keeps responding
    pygame.event.get()
    
    #Check if we're still in-game
    activeWindow = GetWindowText(GetForegroundWindow())
    
    #Log movements
    pos = getMousePos()
    log("Current position: ", pos)
    if coordinates[0] != pos and inbound(pos):
        coordinates.insert(0, pos)

    #Update display
    drawLine(coordinates[0], coordinates[1])
    pygame.display.update()
        


#game is over, save image as vector
log ("\nGame is over!")
pygame.quit()