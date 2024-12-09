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
    pass

class Game_Images():
    pass

class Game():
    def __init__(self, screen_width, screen_height):
        py.init()
        # Create and name screen
        self.screen = py.display.set_mode((screen_width, screen_height), py.RESIZABLE)
        py.display.set_caption("Wizard Run")
        font = py.font.Font('freesansbold.ttf',14)
        # Game Variables
        self.score = 0
        self.scroll_x = 0
        self.scroll_speed = 3
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

    def draw_world(self):
        ground = py.image.load("Game Images/Backgrounds&Objects/ground.png").convert()
        ground = py.transform.scale(ground, ((ground.get_width() * self.screen.get_width()), (ground.get_height() * self.screen.get_height())))
        self.screen.blit(ground, (0, 0))





    def menu_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
        self.screen.fill((0, 0, 0))  # Black screen for the menu
        return True

    def character_select_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
        self.screen.fill((100, 100, 200))  # Blueish screen for character select
        return True

    def running_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
        self.screen.fill((0, 255, 0))  # Green screen for running state
        return True

    def boss_fight_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
        self.screen.fill((255, 0, 0))  # Red screen for boss fight
        return True

    def game_over_state(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
        self.screen.fill((50, 50, 50))  # Gray screen for game over
        return True

        
    def run_game(self):
        running = True
        while running:
            self.draw_world()
            py.display.flip()
            self.clock.tick(60)
            running = self.states[self.game_state]()
            
        
        py.quit()




if __name__ == '__main__':
    Screen_Width = 960
    Screen_Height = 540
    
    game = Game(Screen_Width, Screen_Height)
    game.run_game()
