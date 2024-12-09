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
        
    def run_right(self):
        pass
    
    def run_left(self):
        pass

    def jump(self):
        pass

        self.score = 0
        self.selected_character = None

        self.obstacles = py.sprite.Group()
        self.obstacle_timer = 0
        self.obstacle_spawn_time = 90  # frames between obstacle spawns
        self.obstacle_image = "Game Images/Backgrounds&Objects/boxes.gif"

class GameState(Enum):
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    RUNNING = "running"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"

class Game:
    def __init__(self, screen_width, screen_height):
        py.init()
        # Create and name screen
        self.screen = py.display.set_mode((screen_width, screen_height), py.RESIZABLE)
        py.display.set_caption("Wizard Run")

        # Game Variables
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
        
        # Load images (placeholder functions)
        self.draw_world()

    def draw_world(self):
        # Character select assets
        self.character_image = {
            'wizard': None,
            'knight': None,
            'dark_knight': None
        }
        
        self.backgrounds = {
        'menu': "Game Images/Test Screens/loading.gif",
        'fields': "Game Images/Backgrounds&Objects/Game_Background_Extended.jpg",
        'forest': "Game Images/Backgrounds&Objects/FOREST.jpg",
        'transition': "Game Images/Backgrounds&Objects/transition.png"
        }
        
        self.screen.fill((0, 0, 0))
        if self.game_state == GameState.MENU:
            bg = py.image.load(self.backgrounds['menu'])
            self.screen.blit(bg, (0, 0))
            
        elif self.game_state == GameState.CHARACTER_SELECT:
            bg = py.image.load("Game Images/Test Screens/CharacterSelect.jpg")
            self.screen.blit(bg, (0, 0))

        elif self.game_state == GameState.RUNNING:
            bg = py.image.load(self.backgrounds['fields'])
            bg_height = self.screen.get_height()
            bg_width = int(bg.get_width() * (bg_height / bg.get_height()))
            bg = py.transform.scale(bg, (bg_width, bg_height))
            
            scroll_speed = 3
            self.scroll_x = (self.scroll_x + scroll_speed) % bg_width

            self.screen.blit(bg, (-self.scroll_x, 0))
            self.screen.blit(bg, (bg_width - self.scroll_x, 0))

            # Check for boss fight transition
            if self.score >= 1000 and not self.transition_done:
                self.play_transition(self.backgrounds['transition'], 'boss')

        elif self.game_state == GameState.BOSS_FIGHT:
            #if self.score >= 2000 and not self.transition_done:
            #    self.play_transition(self.backgrounds['transition'], 'running')

            bg = py.image.load(self.backgrounds['forest'])
            bg = py.transform.scale(bg, self.screen.get_size())
            self.screen.blit(bg, (0, 0))

        elif self.game_state == GameState.GAME_OVER:
            bg = py.transform.scale(py.image.load("Game Images/Backgrounds&Objects/GameOverOverlay3.png"), self.screen.get_size())
            bg = py.transform.scale(bg, self.screen.get_size())
            self.screen.blit(bg, (0, 0))

    def draw_transition(self, image):
        transition_image = py.image.load(self.backgrounds['transition'])
        transition_image = py.transform.scale(transition_image, self.screen.get_size())
        transition_speed = 20  # Pixels per frame for quick scroll
        transition_x = 0

        while transition_x < self.screen.get_width():
        # Draw the running background behind the transition image
            self.draw_scrolling_background(self.backgrounds['fields'], 3)

            # Draw the transition image scrolling across
            self.screen.blit(transition_image, (-transition_x, 0))
            self.screen.blit(transition_image, (self.screen.get_width() - transition_x, 0))

            py.display.flip()
            self.clock.tick(60)  # Ensure consistent frame rate

            # Update the transition position
            transition_x += transition_speed

        # Once the transition image covers the screen, switch to the boss fight background
        boss_bg = py.transform.scale(py.image.load(self.backgrounds['forest']), self.screen.get_size())
        self.screen.blit(boss_bg, (0, 0))
        py.display.flip()
        py.time.delay(5000)  # Optional brief pause before continuing

        # After the transition, update the game state to continue the boss fight
        self.game_state = GameState.BOSS_FIGHT

    def play_transition(self, image_path, next_mode):
        """Plays the transition animation and switches game modes."""
        transition_img = py.image.load(image_path)
        transition_height = self.screen.get_height()
        transition_width = int(transition_img.get_width() * (transition_height / transition_img.get_height()))
        transition_img = py.transform.scale(transition_img, (transition_width, transition_height))

        transition_speed = 10
        transition_x = -transition_width  # Start off-screen to the left

        while transition_x < 0:
            self.screen.fill((0, 0, 0))
            self.screen.blit(transition_img, (transition_x, 0))
            py.display.flip()
            transition_x += transition_speed
            self.clock.tick(20)

        # Transition is complete, update game state
        self.transition_done = True
        if next_mode == 'boss':
            self.game_state = GameState.BOSS_FIGHT
            self.score = 1000  # Reset score for this phase
        elif next_mode == 'running':
            self.game_state = GameState.RUNNING
            self.score = 2000  # Reset score for the next cycle

        

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
            if event.key == py.K_F11 or (event.key == py.K_f and py.key.get_mods() & py.KMOD_ALT) or event.key == py.K_ESCAPE:
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
        #self.score += 1
        
        #
        #if self.score >= 1000:
        #    self.game_state = GameState.BOSS_FIGHT
        self.obstacles.update()
        self.obstacles.draw(self.screen)
        py.display.flip()
        return True

    def boss_fight_state(self):
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
            self.draw_world()
            self.clock.tick(60)
            running = self.states[self.game_state]()
        
        py.quit()

if __name__ == "__main__":
    Screen_Width = 960
    Screen_Height = 540

    game = Game(Screen_Width, Screen_Height)
    game.run_game()