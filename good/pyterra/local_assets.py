from local_types import Image, Colors, Tiles
import numpy as np
PLAY_TEXT = 0;
QUIT_TEXT = 0;
BACKGROUND_WORLD = 0
PLAYER_SPRITE = 0

PLAY_TEXT_ARRAY = [
        [Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT], 
        [Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE], 
        [Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT], 
        [Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT], 
        [Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT], 
        [Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT], 
        [Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT]
        ]

QUIT_TEXT_ARRAY = [
        [Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT],
        [Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.WHITE, Colors.WHITE],
        [Colors.TRANSPARENT, Colors.WHITE, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.WHITE],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT]
        ]

BACKGROUND_WORLD_ARRAY = [
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.YELLOW, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.BLUE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.YELLOW, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.BLUE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.BLUE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.BLUE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.RED, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.BLUE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.RED, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.BLUE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.RED, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.BLUE, Colors.BLUE, Colors.BLUE, Colors.BLUE, Colors.BLUE, Colors.BLUE, Colors.BLUE, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.BLUE, Colors.BLUE, Colors.BLUE, Colors.BLUE, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT]
        ]


TILE_AIR = np.array([
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT]
        ])

TILE_STONE = np.array([
        [Colors.GREY, Colors.GREY, Colors.GREY, Colors.WHITE, Colors.GREY],
        [Colors.GREY, Colors.GREY, Colors.WHITE, Colors.GREY, Colors.GREY],
        [Colors.GREY, Colors.GREY, Colors.GREY, Colors.GREY, Colors.GREY],
        [Colors.GREY, Colors.GREY, Colors.GREY, Colors.GREY, Colors.GREY],
        [Colors.WHITE, Colors.GREY, Colors.GREY, Colors.WHITE, Colors.GREY]
        ])

TILE_GRASS = np.array([
        [Colors.GREEN, Colors.YELLOW, Colors.GREEN, Colors.GREEN, Colors.GREEN],
        [Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN],
        [Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN],
        [Colors.BROWN, Colors.GREEN, Colors.BROWN, Colors.BROWN, Colors.BROWN],
        [Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.BROWN]
        ])
tileMap = []

PLAYER_SPRITE_STILL_ARRAY = np.array([
        [Colors.YELLOW, Colors.YELLOW, Colors.GOLD, Colors.GOLD, Colors.GOLD],
        [Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.BLACK, Colors.GOLD],
        [Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.GOLD],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT]
        ])

PLAYER_SPRITE_RUN1_ARRAY = [
        [Colors.YELLOW, Colors.YELLOW, Colors.GOLD, Colors.GOLD, Colors.GOLD],
        [Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.BLACK, Colors.GOLD],
        [Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.GOLD],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.CYAN, Colors.CYAN, Colors.TRANSPARENT, Colors.TRANSPARENT]
        ]

PLAYER_SPRITE_RUN2_ARRAY = [
        [Colors.YELLOW, Colors.YELLOW, Colors.GOLD, Colors.GOLD, Colors.GOLD],
        [Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.BLACK, Colors.GOLD],
        [Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.GOLD, Colors.GOLD],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.BROWN, Colors.BROWN, Colors.BROWN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT],
        [Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT],
        [Colors.CYAN, Colors.TRANSPARENT, Colors.CYAN, Colors.TRANSPARENT, Colors.TRANSPARENT]
        ]

ITEM_PICKAXE = np.array([
        [Colors.BLACK, Colors.YELLOW, Colors.BLACK, Colors.BLACK, Colors.BLACK],
        [Colors.BLACK, Colors.BLACK, Colors.YELLOW, Colors.YELLOW, Colors.BLACK],
        [Colors.BLACK, Colors.BLACK, Colors.WHITE, Colors.YELLOW, Colors.BLACK],
        [Colors.BLACK, Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.YELLOW],
        [Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK]
        ])

itemMap = []

CURSOR = np.array([
        [Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.WHITE, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.WHITE],
        [Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT, Colors.TRANSPARENT],
        [Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE, Colors.TRANSPARENT, Colors.WHITE],
        ])

def loadAssets():
    global PLAY_TEXT
    global QUIT_TEXT
    global BACKGROUND_WORLD
    global PLAYER_SPRITE
    global tileMap
    global itemMap

    PLAY_TEXT = Image()
    PLAY_TEXT.addTexture(PLAY_TEXT_ARRAY, 27, 7)
    PLAY_TEXT.setTextureID(0)

    QUIT_TEXT = Image()
    QUIT_TEXT.addTexture(QUIT_TEXT_ARRAY, 16, 5)
    QUIT_TEXT.setTextureID(0)

    BACKGROUND_WORLD = Image()
    BACKGROUND_WORLD.addTexture(BACKGROUND_WORLD_ARRAY, 145, 10)
    BACKGROUND_WORLD.setTextureID(0)

    PLAYER_SPRITE = Image()
    PLAYER_SPRITE.addTexture(PLAYER_SPRITE_STILL_ARRAY, 5, 10)
    PLAYER_SPRITE.addTexture(PLAYER_SPRITE_RUN1_ARRAY, 5, 10)
    PLAYER_SPRITE.addTexture(PLAYER_SPRITE_RUN2_ARRAY, 5, 10)
    PLAYER_SPRITE.setTextureID(0)
    tileMap.append(TILE_AIR)
    tileMap.append(TILE_STONE)
    tileMap.append(TILE_GRASS)

    itemMap.append(ITEM_PICKAXE)