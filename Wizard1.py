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
    def __init__(self, character_image="Game Images/Characters/knight_running_R.gif"):
        super().__init__()
        self.player_X = 50
        self.player_Y = 345
        self.character_width = 150
        self.character_height = 150
        self.rect = py.Rect(self.player_X, self.player_Y, self.character_width, self.character_height)
        self.Y_change = 0
        self.gravity = 0.8
        self.character_image = character_image
        self.is_jumping = False
        self.jump_velocity = 15
        self.ground_level = 345
        self.X_change = 0
        self.move_speed = 5

    def update_rect(self):
        self.rect.topleft = (self.player_X, self.player_Y)


class Obstacle(py.sprite.Sprite):
    def __init__(self, x, y, image_path="Game Images/Backgrounds&Objects/rock.gif"):
        super().__init__()
        self.image = py.image.load(image_path).convert_alpha()
        self.image = py.transform.scale(self.image, (70, 70))  # obstacle size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5  # speed of obstacle

    def update(self):
        self.rect.x -= self.speed  # movement of obstacle going left
        if self.rect.right < 0:  # delete the obstacle when it's off the screen
            self.kill()

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

        self.obstacles = py.sprite.Group()
        self.obstacle_spawn_timer = 0

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
        scroll_speed = 5
        self.ground_scroll_x = (self.ground_scroll_x + scroll_speed) % scaled_width

        # Blit the ground image twice
        self.screen.blit(ground, (-self.ground_scroll_x, screen_height - scaled_height))
        self.screen.blit(ground, (scaled_width - self.ground_scroll_x, screen_height - scaled_height))


    def draw_character(self):
        if self.game_state == GameState.RUNNING or self.game_state == GameState.BOSS_FIGHT:
        
            character_image = py.image.load(self.character.character_image).convert_alpha()
            character_image = py.transform.scale(character_image, (150, 150))
            self.screen.blit(character_image, (self.character.player_X, self.character.player_Y))

    def menu_state(self):
        '''
        '''
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        bg = py.image.load("Game Images/Backgrounds&Objects/Start_Menu_Placeholder.jpg").convert_alpha()
        bg = py.transform.scale(bg, self.screen.get_size())
        self.screen.blit(bg, (0,0))
        return True

    def character_select_state(self):
        '''
        '''
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        self.screen.fill((100, 100, 200))  # Blueish screen for character select
        return True

    def running_state(self):
        '''
        '''
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        
        self.obstacle_spawn_timer += 1
        if self.obstacle_spawn_timer > random.randint(100, 300):  # spawn frequency
            y_position = self.screen.get_height() - 115  # based on ground height
            obstacle = Obstacle(self.screen.get_width(), y_position)
            self.obstacles.add(obstacle)
            self.obstacle_spawn_timer = 0

        return True

    def boss_fight_state(self):
        '''
        '''
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        bg = py.image.load("Game Images/Backgrounds&Objects/FOREST.jpg").convert_alpha()
        bg = py.transform.scale(bg, self.screen.get_size())
        self.screen.fill((0,0,0))
        self.screen.blit(bg, (0,0))
        return True

    def game_over_state(self):
        '''
        '''
        for event in py.event.get():
            self.handle_global_events(event)
            if event.type == py.QUIT:
                return False
        self.screen.fill((50, 50, 50))  # Gray screen for game over
        return True

    def handle_global_events(self, event):
        '''
        '''

        if self.game_state == GameState.MENU:
            if event.type == py.MOUSEBUTTONUP:
                mouse_x, mouse_y = py.mouse.get_pos()
                if 648 <= mouse_x <= 928 and 285 <= mouse_y <= 345:
                    self.game_state = GameState.RUNNING




        # Global event handling that applies to all game states
        if event.type == py.KEYDOWN:
            if event.key == py.K_F11 or (event.key == py.K_f and py.key.get_mods() & py.KMOD_ALT) or event.key == py.K_ESCAPE:
                # Toggle fullscreen with F11 or Alt+F
                self.toggle_fullscreen()
            
            # Handle Character Movement
            if event.key == py.K_SPACE and not self.character.is_jumping:
                self.character.is_jumping = True
                self.character.Y_change = self.character.jump_velocity

            elif event.key == py.K_d or event.key == py.K_RIGHT:
                self.character.X_change = self.character.move_speed

            elif event.key == py.K_a or event.key == py.K_LEFT:
                if self.game_state == GameState.RUNNING:
                    self.character.X_change = -self.character.move_speed * 1.5
                elif self.game_state == GameState.BOSS_FIGHT:
                    self.character.X_change = -self.character.move_speed

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
        
        if event.type == py.KEYUP:
            if event.key == py.K_d or event.key == py.K_RIGHT or event.key == py.K_a or event.key == py.K_LEFT:
                self.character.X_change = 0

    def update_character_position(self):
        if self.character.is_jumping:
            # Apply jump velocity
            self.character.player_Y -= self.character.Y_change
            
            # Apply gravity
            self.character.Y_change -= self.character.gravity
            
            # Check if character has returned to ground
            if self.character.player_Y >= self.character.ground_level:
                self.character.player_Y = self.character.ground_level
                self.character.Y_change = 0
                self.character.is_jumping = False

    def update_character_horizontal_position(self):
        if self.character.X_change == 0 and self.game_state == GameState.RUNNING:
            self.character.X_change = -5

        # Update horizontal position
        self.character.player_X += self.character.X_change
        
        # Get screen width
        screen_width = self.screen.get_width()
        character_width = 100  # Match the width in draw_character method
        
        # Prevent character from moving off screen
        if self.character.player_X < 0:
            self.character.player_X = 0
        
        if self.character.player_X > screen_width - character_width:
            self.character.player_X = screen_width - character_width

    def run_game(self):
        running = True
        while running:
            self.draw_background()
            self.draw_character()
            self.obstacles.update()
            self.obstacles.draw(self.screen)
            self.update_character_position()
            self.update_character_horizontal_position()
            self.character.update_rect()  # Update character rect for collision detection
            
            # Check for collisions
            if py.sprite.spritecollideany(self.character, self.obstacles):
                self.game_state = GameState.GAME_OVER
            
            py.display.flip()
            self.clock.tick(60)
            running = self.states[self.game_state]()
        
        py.quit()



if __name__ == '__main__':
    Screen_Width = 960
    Screen_Height = 540
    
    game = Game(Screen_Width, Screen_Height)
    game.run_game()