# Alden Thacker
# CPTR-215 Final Project - Wizard Run Game
# 11/07/2024 - started framework
# 11/12/2024 - cont
# 12/02/2024 - 

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
from threading import Thread


class ScoreManager:
    pass

class CharacterOptions(Enum):
    Wizard = 'Game Images/Characters/wizard_running_R.gif'
    Knight = 'Game Images/Characters/knight_running_R.gif'
    Dark_Knight = 'Game Images/Characters/Dark-Knight_running_R.gif'

class Obstace(py.sprite.Sprite):
    pass

class Character(py.sprite.Sprite):
    # Sprite Sheet to animate Characters

    def __init__(self, character):
        py.sprite.Sprite.__init__(self)
        self.image = 0 # FIX THIS!!!!!

    def run_right(self):
        pass
    
    def run_left(self):
        pass

    def jump(self):
        pass

class GameState(Enum):
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    RUNNING = "running"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"

class Game:
    def __init__(self):
        # Initialize pygames
        py.init()
        # Create and name screen
        self.screen = py.display.set_mode((960, 540), py.RESIZABLE)
        py.display.set_caption("Wizard Run")

        self.clock = py.time.Clock()
        self.game_state = GameState.MENU
        self.score = 0
        self.selected_character = None
        self.is_fullscreen = False
        
        # Game states
        self.states = {
            GameState.MENU: self.menu_state,
            GameState.CHARACTER_SELECT: self.character_select_state,
            GameState.RUNNING: self.running_state,
            GameState.BOSS_FIGHT: self.boss_fight_state,
            GameState.GAME_OVER: self.game_over_state,
        }
        
        # Load images (placeholder functions)
        self.load_images()


    def load_images(self):
        # Menu assets
        self.menu_bg = None  # Load menu background
        self.start_button = None  # Load start button
        
        # Character select assets
        self.character_image = {
            'wizard': None,  # Load wizard image
            'knight': None,  # Load knight image
            'dark_knight': None  # Load dark knight image
        }
        
        # Game assets
        self.backgrounds = {
            'fields': None,  # Load scrolling field background
            'forest': None,  # Load forest background for boss fight
        }

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            # Store the current window size before going fullscreen
            self.windowed_size = self.screen.get_size()
            # Switch to fullscreen
            self.screen = py.display.set_mode((0, 0), py.FULLSCREEN)
        else:
            # Return to windowed mode with previous size
            self.screen = py.display.set_mode(self.windowed_size, py.RESIZABLE)

    def handle_global_events(self, event):
        # Global event handling that applies to all game states
        if event.type == py.KEYDOWN:
            if event.key == py.K_F11 or (event.key == py.K_f and py.key.get_mods() & py.KMOD_ALT):
                # Toggle fullscreen with F11 or Alt+F
                self.toggle_fullscreen()
            
            # Navigation shortcuts (delete later)
            if event.key == py.K_1:
                self.game_state = GameState.MENU
            if event.key == py.K_2:
                self.game_state = GameState.CHARACTER_SELECT
            if event.key == py.K_3:
                self.game_state = GameState.RUNNING
            if event.key == py.K_4:
                self.game_state = GameState.BOSS_FIGHT
            if event.key == py.K_5:
                self.game_state = GameState.GAME_OVER

    def menu_state(self):
        self.screen.fill((0, 0, 0))
        bg = py.image.load("Game Images/Test Screens/loading.gif")
        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            
            # Handle global events first
            self.handle_global_events(event)

            if event.type == py.MOUSEBUTTONDOWN:
                # Check if start button clicked
                self.game_state = GameState.CHARACTER_SELECT
        
        py.display.flip()
        return True

    def character_select_state(self):
        self.screen.fill((0, 0, 0))
        bg = py.image.load("Game Images/Test Screens/CharacterSelect.jpg")
        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            
            # Handle global events first
            self.handle_global_events(event)

            if event.type == py.MOUSEBUTTONDOWN:
                # Check which character was selected
                # self.selected_character = selected
                self.game_state = GameState.RUNNING
        
        py.display.flip()
        return True

    def running_state(self):
        self.screen.fill((0, 0, 0))
        bg = py.image.load("Game Images/Test Screens/RunningState.jpg")
        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            
            # Handle global events first
            self.handle_global_events(event)

            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    # Handle jump
                    pass
        
        # Update score
        self.score += 1
        
        # Check for boss fight transition
        if self.score >= 1000:  # Adjust threshold as needed
            self.game_state = GameState.BOSS_FIGHT
        
        py.display.flip()
        return True

    def boss_fight_state(self):
        self.screen.fill((0, 0, 0))
        bg = py.transform.scale(py.image.load("Game Images/Backgrounds&Objects/BossFightBackground.jpg"), self.screen.get_size())
        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            
            # Handle global events first
            self.handle_global_events(event)

            if event.type == py.KEYDOWN:
                # Handle combat controls
                pass
        
        py.display.flip()
        return True

    def game_over_state(self):
        bg = py.transform.scale(py.image.load("Game Images/Backgrounds&Objects/GameOverOverlay3.png"), self.screen.get_size())
        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            # Handle global events first
            self.handle_global_events(event)
        
        py.display.flip()
        return True

    def run_game(self):
        running = True
        while running:
            self.clock.tick(60)
            running = self.states[self.game_state]()
        
        py.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()