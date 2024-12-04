# Alden Thacker
# CPTR-215 Final Project - Wizard Run Game
# 11/07/2024 - started framework
# 11/12/2024 - cont
# test
# References
# https://www.py.org/docs/
# https://www.py.org/docs/ref/event.html

# Sprites and Groups
# https://www.pygame.org/docs/ref/sprite.html
# https://www.youtube.com/watch?v=4TfZjhw0J-8
# http://www.codingwithruss.com/pygame/sprite-class-and-sprite-groups-explained/

# Collisions
# https://www.youtube.com/watch?v=BHr9jxKithk
# http://www.codingwithruss.com/pygame/top-3-collision-types-in-pygame/


import pygame as py
from enum import Enum
import random
import sys

class CharacterOptions(Enum):
    Wizard = 'Game Images/Characters/wizard_running_R.gif'
    Knight = 'Game Images/Characters/knight_running_R.gif'
    Dark_Knight = 'Game Images/Characters/Dark-Knight_running_R.gif'



class Character(py.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        self.image = 0 # FIX THIS!!!!!


class GameState:
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    RUNNING = "running"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"
    VICTORY = "victory"

class Game:
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((800, 600))
        py.display.set_caption("Wizard Run")
        self.clock = py.time.Clock()
        self.game_state = GameState.MENU
        self.score = 0
        self.selected_character = None
        
        # Game states
        self.states = {
            GameState.MENU: self.menu_state,
            GameState.CHARACTER_SELECT: self.character_select_state,
            GameState.RUNNING: self.running_state,
            GameState.BOSS_FIGHT: self.boss_fight_state,
            GameState.GAME_OVER: self.game_over_state,
            GameState.VICTORY: self.victory_state
        }
        
        # Load assets (placeholder functions)
        self.load_images()
        self.load_sounds()
        
    def load_images(self):
        # Menu assets
        self.menu_bg = None  # Load menu background
        self.start_button = None  # Load start button
        
        # Character select assets
        self.character_portraits = {
            'wizard': None,  # Load wizard image
            'knight': None,  # Load knight image
            'dark_knight': None  # Load dark knight image
        }
        
        # Game assets
        self.backgrounds = {
            'fields': None,  # Load scrolling field background
            'forest': None,  # Load forest background for boss fight
        }
        
        # Character sprites and animations would be loaded here
        
    def load_sounds(self):
        # Load game sounds (jump, hit, music, etc.)
        pass

    def menu_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.MOUSEBUTTONDOWN:
                # Check if start button clicked
                self.game_state = GameState.CHARACTER_SELECT
        
        # Draw menu screen
        # self.screen.blit(self.menu_bg, (0, 0))
        # Draw start button
        py.display.flip()
        return True

    def character_select_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.MOUSEBUTTONDOWN:
                # Check which character was selected
                # self.selected_character = selected
                self.game_state = GameState.RUNNING
        
        # Draw character selection screen
        py.display.flip()
        return True

    def running_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    # Handle jump
                    pass
        
        # Update score
        self.score += 1
        
        # Check for boss fight transition
        if self.score >= 1000:  # Adjust threshold as needed
            self.game_state = GameState.BOSS_FIGHT
        
        # Update background scroll
        # Update character animation
        # Update obstacles
        # Check collisions
        # Draw everything
        py.display.flip()
        return True

    def boss_fight_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.KEYDOWN:
                # Handle combat controls
                pass
        
        # Update boss fight mechanics
        # Check win/lose conditions
        py.display.flip()
        return True

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            running = self.states[self.game_state]()
        
        py.quit()

if __name__ == "__main__":
    game = Game()
    game.run()