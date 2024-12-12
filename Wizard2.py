# Alden Thacker & Peyton Wall
# CPTR-215 Final Project - Wizard Run Game
# 11/07/2024 - started framework
# 11/12/2024 - cont
# 12/02/2024 - 

# References
# https://www.py.org/docs/
# https://www.py.org/docs/ref/event.html
# https://www.youtube.com/watch?v=ZV8TNrwqG1Y

# Sprites and Groups
# https://www.pygame.org/docs/ref/sprite.html
# https://www.youtube.com/watch?v=4TfZjhw0J-8
# http://www.codingwithruss.com/pygame/sprite-class-and-sprite-groups-explained/

# Collisions
# https://www.youtube.com/watch?v=BHr9jxKithk
# http://www.codingwithruss.com/pygame/top-3-collision-types-in-pygame/


from enum import Enum
import pygame as py
import random

class GameState(Enum):
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    RUNNING = "running"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"

class Character(py.sprite.Sprite):
    path = 'Game Images/Characters/{}_{}_{}_{}.png'
    def __init__(self, character = "Dark_Knight"):
        py.sprite.Sprite.__init__(self)
        self.timer = 0
        self.player_X = 50
        self.player_Y = 330
        self.Y_change = 0
        self.gravity = .85
        self.character = character
        self.is_jumping = False
        self.jump_velocity = 15
        self.ground_level = 330

        # Movement variables
        self.X_change = 0
        self.move_speed = 5

        # Character Attributes
        self.frame = 1
        self.facing = 'Right'
        self.state = 'Resting'
        

    def change_image(self):
        self.timer += 1

        if self.timer >= 12:
            self.timer = 0
            if self.frame == 1:
                self.frame = 2
            else:
                self.frame = 1

        return Character.path.format(self.character, self.frame, self.facing, self.state)

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

    def change_image(self):
        '''
        '''
        pass

class Game():
    def __init__(self):
    # Create and name screen and declare font
        py.init()
        self.screen = py.display.set_mode((960, 540))
        py.display.set_caption("Wizard Run")
        font = py.font.Font('freesansbold.ttf',14)

        self.cached_images = {
            'background': self._load_and_scale_image("Game Images/Backgrounds&Objects/Game_Background_Extended.jpg"),
            'forest': self._load_and_scale_image("Game Images/Backgrounds&Objects/FOREST.jpg"),
            'ground': self._load_and_scale_image("Game Images/Backgrounds&Objects/ground.png", True),
            'menu': self._load_and_scale_image("Game Images/Backgrounds&Objects/Start_Menu_Placeholder.jpg"),
            'transition': self._load_and_scale_image("Game Images/Backgrounds&Objects/transition.png", True)
        }
    # Call GameStates
        self.states = {
            GameState.MENU: self.menu_state,
            GameState.CHARACTER_SELECT: self.character_select_state,
            GameState.RUNNING: self.running_state,
            GameState.BOSS_FIGHT: self.boss_fight_state,
            GameState.GAME_OVER: self.game_over_state,
        }

    # Game Variables
        self.score = 0
        self.is_fullscreen = False
        self.clock = py.time.Clock()
        self.game_state = GameState.MENU
        self.needs_redraw = True

    # Initialize Character
        self.character = Character()

    # Initialize Obstacles
        self.obstacles = py.sprite.Group()
        self.obstacle_spawn_timer = 0

    # Scroll Variables
        # Transition Scroll Variables
        self.transition = False
        self.transition_scroll_x = 0

        # Background Scroll Variable
        self.bg_scroll_x = 0

        # Ground Scroll Variable
        self.ground_scroll_x = 0


    def get_direction(self):
        pass

    def _load_and_scale_image(self, path, use_alpha=False):
        """Helper method to load and scale images efficiently"""
        if use_alpha:
            img = py.image.load(path).convert_alpha()
        else:
            img = py.image.load(path).convert()
        return py.transform.scale(img, self.screen.get_size())
    
    def handle_global_events(self):
        ''' 
        Handles Quit and Resizing (Turned Off) functionality, as well as event queue for all
        keypress and mouseclick events.
        '''
        # Turned Off
        '''
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            # Store the current window size before going fullscreen
            self.windowed_size = self.screen.get_size()
            # Switch to fullscreen
            self.screen = py.display.set_mode((0, 0), py.FULLSCREEN)
        else:
            # Return to windowed mode with previous size
            self.screen = py.display.set_mode(self.windowed_size, py.RESIZABLE)
        '''
        
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
                return

            if self.game_state == GameState.MENU:
                if event.type == py.MOUSEBUTTONUP:
                    mouse_x, mouse_y = py.mouse.get_pos()
                    if 648 <= mouse_x <= 928 and 285 <= mouse_y <= 345:
                        self.transition = True
                
            if event.type == py.KEYDOWN:

                # Navigation shortcuts (delete later)
                keys = py.key.get_pressed()
                if keys[py.K_1]:
                    self.game_state = GameState.MENU
                elif keys[py.K_2]:
                    self.game_state = GameState.CHARACTER_SELECT
                elif keys[py.K_3]:
                    self.transition = True
                elif keys[py.K_4]:
                    self.transition = True
                elif keys[py.K_5]:
                    self.game_state = GameState.GAME_OVER

                # Handle Character Movement
                if (keys[py.K_SPACE] or keys[py.K_UP]) and not self.character.is_jumping:
                    self.character.is_jumping = True
                    self.character.Y_change = self.character.jump_velocity
                    self.character.state = 'Running'
                if (keys[py.K_d] or keys[py.K_RIGHT]):
                    self.character.X_change = self.character.move_speed
                    self.character.facing = 'Right'
                    self.character.state = 'Running'
                if (keys[py.K_a] or keys[py.K_LEFT]):
                    self.character.facing = 'Left'
                    self.character.state = 'Running'
                    if self.game_state == GameState.RUNNING:
                        self.character.X_change = -self.character.move_speed * 1.7
                    elif self.game_state == GameState.BOSS_FIGHT:
                        self.character.X_change = -self.character.move_speed

            if event.type == py.KEYUP:
                #self.character.state = 'Resting'
                if event.key == py.K_d or event.key == py.K_RIGHT or event.key == py.K_a or event.key == py.K_LEFT:
                    self.character.X_change = 0

    def draw_background(self):
        '''
        Checks th
        '''

        if self.game_state == GameState.RUNNING:
            #Load Background
            bg = py.image.load("Game Images/Backgrounds&Objects/Game_Background_Extended.jpg").convert()
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

    def draw_transition(self):
        # Load scrolling Ground
        forest_transition = py.image.load("Game Images/Backgrounds&Objects/transition.png").convert_alpha()
        forest_transition = py.transform.scale(forest_transition, (2400, 540))

        # Update scroll position
        scroll_speed = 15
        self.transition_scroll_x += scroll_speed

        if self.transition_scroll_x == 1695 and self.game_state == GameState.MENU:
            self.game_state = GameState.RUNNING
        elif self.transition_scroll_x == 1695 and self.game_state == GameState.RUNNING:
            self.game_state = GameState.BOSS_FIGHT
        elif self.transition_scroll_x == 1695 and self.game_state == GameState.BOSS_FIGHT:
            self.game_state = GameState.RUNNING


        if self.transition_scroll_x >= 3600:
            self.transition = False
            self.transition_scroll_x = 0
        else:
            self.screen.blit(forest_transition, (1200 -self.transition_scroll_x, 0))
        

    # Draw and update character position
    def draw_character(self):

        if self.game_state == GameState.RUNNING or self.game_state == GameState.BOSS_FIGHT:
            character_image = py.image.load(self.character.change_image()).convert_alpha()
            character_image = py.transform.scale(character_image, (132, 165))
            self.screen.blit(character_image, (self.character.player_X, self.character.player_Y))

    def update_character_position(self):
        if self.character.is_jumping:
            # Apply jump velocity
            self.character.player_Y -= self.character.Y_change
            
            # Apply gravity
            self.character.Y_change -= self.character.gravity
            
            # Check if character has returned to 
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

    # Define the Mechanics of each Gamestate
    def menu_state(self):
        '''
        '''
        bg = py.image.load("Game Images/Backgrounds&Objects/Start_Menu_Placeholder.jpg").convert()
        bg = py.transform.scale(bg, self.screen.get_size())
        self.screen.blit(bg, (0,0))

    def character_select_state(self):
        '''
        '''
        self.screen.fill((100, 100, 200))  # Blueish screen for character select

    def running_state(self):
        '''
        '''
        self.obstacle_spawn_timer += 1
        if self.obstacle_spawn_timer > random.randint(100, 300):  # spawn frequency
            y_position = self.screen.get_height() - 115  # based on ground height
            obstacle = Obstacle(self.screen.get_width(), y_position)
            self.obstacles.add(obstacle)
            self.obstacle_spawn_timer = 0

    def boss_fight_state(self):
        if self.needs_redraw or not self.last_frame:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.cached_images['forest'], (0, 0))
            self.last_frame = self.screen.copy()
            self.needs_redraw = False
        else:
            self.screen.blit(self.last_frame, (0, 0))

    def game_over_state(self):
        '''
        '''
        self.screen.fill((50, 50, 50))  # Gray screen for game over

    # Game loop
    def run_game(self):
        self.running = True
        while self.running:
            # Add while self.game_state != GameState.Game_Over
            self.handle_global_events()
                
            self.draw_background()
            self.draw_character()
            self.obstacles.update()
            self.obstacles.draw(self.screen)
            self.update_character_position()
            self.update_character_horizontal_position()

            if self.transition:
                self.draw_transition()

            py.display.flip()
            self.clock.tick(70)
            self.states[self.game_state]()
            # Add functionality to write high schore and current character choice to new file
        py.quit()


if __name__ == '__main__':
    game = Game()
    game.run_game()