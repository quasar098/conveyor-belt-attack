from pygame import Color
import platform
from win32api import EnumDisplayDevices, EnumDisplaySettings

# pygame stuff
WIDTH, HEIGHT = 1280, 720
FRAMERATE = 60  # change this to your monitor refresh rate if using windows, dont have a linux or mac to test it on
if platform.system() == "Windows":  # windows
    FRAMERATE = EnumDisplaySettings(EnumDisplayDevices().DeviceName, -1).DisplayFrequency
if platform.system() == "Linux":  # linux
    pass
if platform.system() == "Darwin":  # mac
    pass

# game colors
BG_COLOR = Color(255, 255, 255)  # white
PRIMARY_COLOR = Color(56, 78, 119)  # blue
PRIMARY_COLOR_2 = Color(24, 49, 79)  # darker blue
SECONDARY_COLOR = Color(230, 249, 175)  # yellow-green
ORANGE = Color(228, 148, 69)  # ...orange?

# standard colors
WHITE = Color(255, 255, 255)
BLACK = Color(7, 8, 9)

# block colors
TIER_COLORS = (
    Color(215, 217, 215),
    Color(0, 253, 220),
    Color(255, 86, 102),
    Color(241, 143, 1),
    Color(173, 246, 177),
    Color(200, 29, 37),
    Color(255, 153, 200),
    Color(252, 246, 189),
    Color(208, 244, 222),
    Color(169, 222, 249),
    Color(228, 193, 249),
    Color(255, 255, 255)
)

RECIPIES = {
    (1, 1): 2,
    (2, 2): 3,
    (2, 3): 4,
    (2, 4): 5,
    (4, 3): 6,
    (3, 6): 7,
    (7, 2): 8,
    (8, 3): 9,
    (9, 2): 10,
    (10, 2): 11,
    (11, 11): 12,
}
CRAFTINGS = {
    1: (1, 1, 2),
    2: (2, 2, 3),
    3: (2, 3, 4),
    4: (2, 4, 5),
    5: (3, 4, 6),
    6: (3, 6, 7),
    7: (2, 7, 8),
    8: (3, 8, 9),
    9: (2, 9, 10),
    10: (2, 10, 11),
    11: (11, 11, 12),
    12: (11, 11, 12)
}

# viewing_screen
MAIN_MENU = "main menu"
GAME = "game"
HIGH_SCORE = "high score"
HOW_TO_PLAY = "how to play"
