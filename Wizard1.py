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


'''
  Video that we were working from (Stopped at 16:31)
  https://www.youtube.com/watch?v=ZV8TNrwqG1Y
'''

import pygame as py
import random
from enum import Enum




class GameState(Enum):
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    RUNNING = "running"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"

class Character(py.sprite.Sprite):
    def __init__(self, character_image = "Game Images/Characters/knight_running_R.gif"):
        py.sprite.Sprite.__init__(self)
        self.player_X = 50
        self.player_Y = 450
        self.Y_change = 0
        self.gravity = 1
        self.character_image = character_image


class Game_Images():
    pass

class Game():
    def __init__(self, screen_width, screen_height):
        py.init()
        # Create and name screen
        self.screen = py.display.set_mode((screen_width, screen_height), py.RESIZABLE,)
        py.display.set_caption("Wizard Run")
        font = py.font.Font('freesansbold.ttf',14)
        # Game Variables
        self.score = 0

        self.bg_scroll_x = 0
        self.ground_scroll_x = 0

        self.scroll_speed = 3
        self.clock = py.time.Clock()
        self.game_state = GameState.MENU
        self.score = 0
        self.selected_character = None
        self.is_fullscreen = False

        self.character = Character()

        # Game states
        self.states = {
            GameState.MENU: self.menu_state,
            GameState.CHARACTER_SELECT: self.character_select_state,
            GameState.RUNNING: self.running_state,
            GameState.BOSS_FIGHT: self.boss_fight_state,
            GameState.GAME_OVER: self.game_over_state,
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

    def draw_background(self):
        '''
        '''

        if self.game_state == GameState.RUNNING:
            #Load Background
            bg = py.image.load("Game Images/Backgrounds&Objects/Game_Background_Extended.jpg")
            bg_height = self.screen.get_height()
            bg_width = int(bg.get_width() * (bg_height / bg.get_height()))
            bg = py.transform.scale(bg, (bg_width, bg_height))
            
            scroll_speed = 3
            self.bg_scroll_x = (self.bg_scroll_x + scroll_speed) % bg_width
            self.screen.blit(bg, (-self.bg_scroll_x, 0))
            self.screen.blit(bg, (bg_width - self.bg_scroll_x, 0))

            self.draw_ground()

    def draw_ground(self):
        # Load scrolling Ground
        ground = py.image.load("Game Images/Backgrounds&Objects/ground.png").convert_alpha()
        
        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Calculate new dimensions for ground image
        scalling_factor = 1.5

        scaled_width = (screen_width * scalling_factor)
        scaled_height = (int(ground.get_height() * (screen_width / ground.get_width())) * scalling_factor)

        # Scale the ground image to fit the screen
        ground = py.transform.scale(ground, (scaled_width, scaled_height))

        # Update scroll position
        scroll_speed = 3
        self.ground_scroll_x = (self.ground_scroll_x + scroll_speed) % scaled_width

        # Blit the ground image twice
        self.screen.blit(ground, (-self.ground_scroll_x, screen_height - scaled_height))
        self.screen.blit(ground, (scaled_width - self.ground_scroll_x, screen_height - scaled_height))


    def draw_character(self):
        #self.character = py.image.load(self.character.character_image)
        #self.screen.blit(self.character, (0, 0))
        py.draw.rect(self.screen, (255, 0, 0), [self.character.player_X, self.character.player_Y, 20, 20])

    def jump(self, y_change):
        if self.character.Y_change > 0 or self.character.player_Y < 200:
            self.character.player_Y -= y_change

    def menu_state(self):
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        self.screen.fill((0, 0, 0))  # Black screen for the menu
        return True

    def character_select_state(self):
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        self.screen.fill((100, 100, 200))  # Blueish screen for character select
        return True

    def running_state(self):
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        self.screen.fill((0, 255, 0))  # Green screen for running state
        return True

    def boss_fight_state(self):
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        self.screen.fill((255, 0, 0))  # Red screen for boss fight
        return True

    def game_over_state(self):
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        self.screen.fill((50, 50, 50))  # Gray screen for game over
        return True


    def handle_global_events(self, event):
        # Global event handling that applies to all game states
        if event.type == py.KEYDOWN:
            if event.key == py.K_F11 or (event.key == py.K_f and py.key.get_mods() & py.KMOD_ALT) or event.key == py.K_ESCAPE:
                # Toggle fullscreen with F11 or Alt+F
                self.toggle_fullscreen()
            
            if event.key == py.KEYDOWN:
                if event.key == py.K_SPACE and self.character.Y_change == 0:
                    self.character.Y_change = 18
                    
                    if self.character.player_Y < 450:
                        self.character.player_Y -= self.character.Y_change
                        self.character.Y_change -= self.character.gravity

                    if self.character.player_Y > 450:
                        self.character.player_Y = 450

                    if self.character.player_Y == 200 and self.character.Y_change < 0:
                        self.character.Y_change = 0


                


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


    def run_game(self):
        running = True
        while running:
            self.draw_background()
            self.draw_character()
            py.display.flip()
            self.clock.tick(60)
            running = self.states[self.game_state]()
            
        py.quit()




if __name__ == '__main__':
    Screen_Width = 960
    Screen_Height = 540
    
    game = Game(Screen_Width, Screen_Height)
    game.run_game()
