################## IMPORTED LIBRARIES #################

# Standard library imports
from datetime import datetime

# Third party imports
import pygame

# Local imports
from svgCreator import render_svg
from windowManager import *




################## CONSTANTS & SETTINGS #################

# More detailed output, listens to 'Neuer Tab', no vector image
debug = True

# Abbreviations for programs
abbreviations = {'lol': 'League of Legends (TM) Client'}

# Settings for display
SCALING_FACTOR = 0.5
monitorSize = getMonitorResolution()

# Colors used in the display and vector graphic
COLOR_BACKGROUND = (0, 0, 0)
COLOR_LINE = (100, 200, 255, 0.3)



################## FUNCTIONS #################

# Used for debug-ouput
def _log (*args):
    if debug:
        print ('\t[DEBUG]', *args)


# Checks if coordinates are in range
def inbound(pos):
    if pos[0] < 0 or pos[1] < 0:
        return False
    return True


# Draws a scaled version of what's happening
def drawLine(start, end):
    startScaled = (int(start[0] * SCALING_FACTOR), int(start[1] * SCALING_FACTOR))
    endScaled = (int(end[0] * SCALING_FACTOR), int(end[1] * SCALING_FACTOR))
    pygame.draw.line(screen, COLOR_LINE, startScaled, endScaled)


def initialize(screen):
    pygame.init()
    screen.fill(COLOR_BACKGROUND)
    pygame.display.set_caption('Mouse Tracer')
    # Avoids redundant out-of-bounds checks later on
    coordinates.insert(0, getMousePos())
    coordinates.insert(0, getMousePos())


def generateTitle(title):
    date = str(datetime.now())[:-10].replace(':', '.')
    fileName = 'mouseTrace[' + date + '] - ' + title.strip()
    return fileName   


def checkInput(title):
    if title in abbreviations:
        return abbreviations[title]
    return title


################# BEGINNING OF THE PROGRAM #################

# Check for debug-mode
_log ()
_log ('############################')
_log ('#####              #########')
_log ('#####  DEBUG-MODE  #########')
_log ('#####              #########')
_log ('############################\n')

# Get name of the program
title = checkInput(input('Please input the desired program: '))
    
# Output some infos
print ('\nWaiting for "' + title + '" to start...')


# Wait for program to start...
while not isWindowOpen(title):
    pass


# Initialize stuff
coordinates = []
printSwitch = True
screenWidth  = int(monitorSize[0] * SCALING_FACTOR)
screenHeight = int(monitorSize[1] * SCALING_FACTOR)
screen = pygame.display.set_mode((screenWidth, screenHeight))
initialize(screen)


# Start logging mouse movements
print ('\n"' + title + '" has started, now logging mouse movements...')
while isWindowOpen(title):

    # Make sure window keeps responding
    pygame.event.get()

    # Check if user is in the desired program and log movements
    topWindow = getActiveWindow()
    if title in topWindow:
        pos = getMousePos()
        if not printSwitch:
            printSwitch = True
            print ('\nHere we are again:D')
            print ('Continuing logging coordinates...\n')
        if coordinates[0] != pos and inbound(pos) and pos != (960, 600):
                _log ('Current position: ', pos)
                coordinates.insert(0, pos)
    else:
        if printSwitch:
            printSwitch = False
            _log ('Active window: ' + topWindow)
            _log ('Timestamp: ' + str(datetime.now()) +'')
            print ('\n"' + title + '" is open, but not active.')
            print ('Stop logging coordinates...\n')

    # Update display
    drawLine(coordinates[0], coordinates[1])
    pygame.display.update()


# Game is over, save image as vector
print ('\n"' + title + '" has terminated!')
fileName = generateTitle(title)
render_svg(fileName, monitorSize, COLOR_BACKGROUND, COLOR_LINE, coordinates, 1)


# Cleanup
pygame.quit()
