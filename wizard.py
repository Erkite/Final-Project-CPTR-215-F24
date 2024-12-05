# Alden Thacker
# CPTR-215 Final Project - Wizard Run Game
# 11/07/2024 - started framework
# 11/12/2024 - cont

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

class Obstacle(py.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = py.image.load(image_path).convert_alpha()
        # this scales the image to an appropriate size - adjust these numbers as needed Alden
        self.image = py.transform.scale(self.image, (50, 50))  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed  # move left
        if self.rect.right < 0:  # if off screen
            self.kill()

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
        self.screen = py.display.set_mode((800, 600))
        py.display.set_caption("Wizard Run")

        self.clock = py.time.Clock()
        self.game_state = GameState.MENU
        self.score = 0
        self.selected_character = None
        
        self.obstacles = py.sprite.Group()
        self.obstacle_timer = 0
        self.obstacle_spawn_time = 90  # frames between obstacle spawns

        self.obstacle_image = "Game Images/Backgrounds&Objects/boxes.gif"


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
        #self.load_sounds()
        
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
        
        # Character sprites and animations would be loaded here
    '''    
    def load_sounds(self):
        # Load game sounds (jump, hit, music, etc.)
        pass
    ''' 

    # Define all GameStates

    def menu_state(self):
        bg = py.image.load("Game Images/Test Screens/loading.gif")
        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.MOUSEBUTTONDOWN:
                # Check if start button clicked
                self.game_state = GameState.CHARACTER_SELECT
            # TEST EVENT TO CHANGE SCREENS
            if event.type == py.KEYDOWN:
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
        
        # Draw menu screen
        # self.screen.blit(self.menu_bg, (0, 0))
        # Draw start button
        py.display.flip()
        return True

    def character_select_state(self):
        bg = py.image.load("Game Images/Test Screens/CharacterSelect.jpg")
        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.MOUSEBUTTONDOWN:
                # Check which character was selected
                # self.selected_character = selected
                self.game_state = GameState.RUNNING
            # TEST EVENT TO CHANGE SCREENS
            if event.type == py.KEYDOWN:
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
        
        # Draw character selection screen
        py.display.flip()
        return True

    def running_state(self):
        bg = py.image.load("Game Images/Test Screens/RunningState.jpg")

        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.KEYDOWN:
                    pass

        # Debug obstacle creation
        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_spawn_time:
            new_obstacle = Obstacle(800, 450, self.obstacle_image)  # Adjust y position
            self.obstacles.add(new_obstacle)

            self.obstacle_timer = 0

        # update score
        self.score += 1

        # check for boss fight transition
        if self.score >= 1000:
            self.game_state = GameState.BOSS_FIGHT

        # update obstacles
        self.obstacles.update()
        self.obstacles.draw(self.screen)

        py.display.flip()
        return True


    def boss_fight_state(self):
        bg = py.image.load("Game Images/Test Screens/BossFightState.jpg")
        self.screen.blit(bg, (0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.KEYDOWN:
                # Handle combat controls
                pass
            # TEST EVENT TO CHANGE SCREENS
            if event.type == py.KEYDOWN:
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
        
        # Update boss fight mechanics
        # Check win/lose conditions
        py.display.flip()
        return True
    

    def game_over_state(self):
        bg = py.image.load("Game Images/Test Screens/GameOverState.jpg")
        self.screen.blit(bg, (0, 0))
        # TEST EVENT TO CHANGE SCREENS
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            if event.type == py.KEYDOWN:
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