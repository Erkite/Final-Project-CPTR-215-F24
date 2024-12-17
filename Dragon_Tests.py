'''
This file contains doctests for the core functionalities of the game, including the Character, Obstacle, and Game classes.
'''

import pygame as py
from Dragon_Run import Score, Character, Obstacle, Game, GameState

def test_character_initialization():
    """
    Test Character initialization.

    >>> char = Character("Knight")
    >>> char.character
    'Knight'
    >>> char.player_X, char.player_Y
    (50, 330)
    >>> char.is_jumping
    False
    >>> char.frame
    1
    """

def test_character_change_image():
    """
    Test the image path change logic for Character.

    >>> char = Character("Wizard")
    >>> char.change_image()
    'Game Images/Characters/Wizard_1_Right_Resting.png'
    >>> char.timer = 12
    >>> char.change_image()
    'Game Images/Characters/Wizard_2_Right_Resting.png'
    >>> char.character = 'Dark_Knight'
    >>> char.change_image()
    'Game Images/Characters/Dark_Knight_2_Right_Resting.png'
    """

def test_obstacle_initialization():
    """
    Test Obstacle initialization.

    >>> screen = py.display.set_mode((960, 540))
    >>> obstacle = Obstacle(300, 450)
    >>> obstacle.rect.x, obstacle.rect.y
    (300, 450)
    >>> obstacle.speed
    5
    >>> obstacle.width
    70
    """

def test_obstacle_update():
    """
    Test obstacle movement and removal.

    >>> obstacle = Obstacle(300, 450)
    >>> obstacle.update()
    >>> obstacle.rect.x
    295
    >>> obstacle.rect.x = -71  # Simulate moving off-screen
    >>> obstacle.update()
    """

def test_game_state_enum():
    """
    Test the GameState enum.

    >>> GameState.MENU.value
    'menu'
    >>> GameState.GAME_OVER.name
    'GAME_OVER'
    >>> GameState.RUNNING == GameState('running')
    True
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()