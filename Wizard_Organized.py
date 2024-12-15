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

import enum
import pygame as py
import random

class GameState(enum.Enum):
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    RUNNING = "running"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"
    CONTROLS = "controls"

class Score:
    def __init__(self):
        self.score = 0
        self.score_delay = 0
        self.path = 'Game Images/Backgrounds&Objects/{}.png'
        self.number_images = {}

        for i in range(10):
            try:
                img = py.image.load(self.path.format(f'{i}')).convert_alpha()
                self.number_images[str(i)] = py.transform.scale(img, (20, 30))  # Adjust size as needed
            except Exception as e:
                print(f"Error loading number image for {i}: {e}")

    def increment(self):
        """
        Increment the score by a specified amount
        """
        self.score_delay += 1
        if self.score_delay % 6 == 0:
            self.score += 1

    def reset(self):
        """
        Reset the score to zero
        """
        self.score = 0

    def draw_score(self, screen, x_pos = 20, y_pos = 20, high_score = None):
       
        if high_score:
            score_str = str(high_score).zfill(3)
        else:
            score_str = str(self.score).zfill(3)
        
        for digit in score_str:
            number_image = self.number_images.get(digit)
            if number_image:
                screen.blit(number_image, (x_pos, y_pos))
                x_pos += 20

class Character(py.sprite.Sprite):
    path = 'Game Images/Characters/{}_{}_{}_{}.png'
    
    def __init__(self, character="Knight"):
        py.sprite.Sprite.__init__(self)
        self.timer = 0
        self.player_X = 50
        self.player_Y = 330
        self.Y_change = 0
        self.gravity = 0.7
        self.character = character
        self.is_jumping = False
        self.jump_velocity = 15
        self.ground_level = 330
        self.image_changer_time = 12

        # Movement variables
        self.X_change = 0
        self.move_speed = 5

        # Character Attributes
        self.frame = 1
        self.facing = 'Right'
        self.state = 'Resting'
        
        # Image-related attributes
        self.character_image = None
        self.character_rect = None

    def change_image(self):
        """
        Update character animation frame
        """
        self.timer += 1

        if self.timer >= self.image_changer_time:
            self.timer = 0
            self.frame = 2 if self.frame == 1 else 1

        return Character.path.format(self.character, self.frame, self.facing, self.state)

    def draw(self, screen):
        """
        Draw the character on the screen
        """
        character_image = py.image.load(self.change_image()).convert_alpha()
        character_image = py.transform.scale(character_image, (132, 165))
        screen.blit(character_image, (self.player_X, self.player_Y))

    def update_vertical_position(self):
        """
        Update vertical position with jumping and gravity
        """
        if self.is_jumping:
            # Apply jump velocity
            self.player_Y -= self.Y_change
            
            # Apply gravity
            self.Y_change -= self.gravity
            
            # Check if character has returned to ground
            if self.player_Y >= self.ground_level:
                self.player_Y = self.ground_level
                self.Y_change = 0
                self.is_jumping = False

    def update_horizontal_position(self, screen, game_state):
        """
        Update horizontal position with movement constraints
        """
        if self.X_change == 0 and game_state == GameState.RUNNING:
            self.X_change = -5

        # Update horizontal position
        self.player_X += self.X_change
        
        # Get screen width
        screen_width = screen.get_width()
        character_width = 100  # Match the width in draw method
        
        # Prevent character from moving off screen
        self.player_X = max(0, min(self.player_X, screen_width - character_width))

    def handle_movement(self, keys):
        """
        Handle character movement based on key presses
        """
        # Jumping
        if (keys[py.K_SPACE] or keys[py.K_UP]) and not self.is_jumping:
            self.is_jumping = True
            self.Y_change = self.jump_velocity
            self.state = 'Running'
        
        # Right movement
        if (keys[py.K_d] or keys[py.K_RIGHT]):
            self.X_change = self.move_speed
            self.facing = 'Right'
            self.state = 'Running'
        
        # Left movement
        if (keys[py.K_a] or keys[py.K_LEFT]):
            self.facing = 'Left'
            self.state = 'Running'
            self.X_change = -self.move_speed * 1.7

class Obstacle(py.sprite.Sprite):
    def __init__(self, x, y, image_path="Game Images/Backgrounds&Objects/rock.gif"):
        super().__init__()
        self.image = py.image.load(image_path).convert_alpha()
        self.image = py.transform.scale(self.image, (70, 70))  # obstacle size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5  # speed of obstacle
        self.width = 70

    def update(self):
        """
        Move the obstacle to the left and remove when off-screen
        """
        self.rect.x -= self.speed  # movement of obstacle going left
        if self.rect.right < 0:  # delete the obstacle when it's off the screen
            self.kill()

class Game:
    def __init__(self):
        # Create and name screen and declare font
        py.init()
        self.screen = py.display.set_mode((960, 540))
        py.display.set_caption("Wizard Run")

        self.high_score_file = 'game_progress.txt'
        self.high_score = 0
        
        # Set a default character
        self.selected_character = 'Dark_Knight'

        # Read existing high score and character
        try:
            with open(self.high_score_file, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    # Use the saved character from the file
                    self.selected_character = lines[0].strip()
                    try:
                        self.high_score = int(lines[1].strip())
                    except ValueError:
                        self.high_score = 0
        except FileNotFoundError:
            # Create the file if it doesn't exist
            with open(self.high_score_file, 'w') as file:
                file.write(f"{self.selected_character}\n{self.high_score}")


        self.cached_backgrounds = {
            'background': self._load_and_scale_image("Game Images/Backgrounds&Objects/Game_Background_Extended.jpg"),
            'forest': self._load_and_scale_image("Game Images/Backgrounds&Objects/FOREST.jpg"),
            'ground': self._load_and_scale_image("Game Images/Backgrounds&Objects/ground.png", True),
            'transition': self._load_and_scale_image("Game Images/Backgrounds&Objects/transition.png", True)
        }
        

        # Call GameStates
        self.states = {
            GameState.MENU: self.menu_state,
            GameState.CHARACTER_SELECT: self.character_select_state,
            GameState.CONTROLS: self.controls_state, 
            GameState.RUNNING: self.running_state,
            GameState.BOSS_FIGHT: self.boss_fight_state,
            GameState.GAME_OVER: self.game_over_state,
        }

        # Game Variables
        self.game_score = Score()
        self.is_fullscreen = False
        self.clock = py.time.Clock()
        self.game_state = GameState.MENU
        self.dragon_eye_open = False
        self.needs_redraw = True
        self.running = True
        self.timer = 0
        self.frame = 1

        # Initialize Character
        self.character = Character(self.selected_character)

        # Initialize Obstacles
        self.obstacles = py.sprite.Group()
        self.obstacle_spawn_timer = 0

        # Scroll Variables
        self.transition = False
        self.transition_scroll_x = 0
        self.bg_scroll_x = 0
        self.ground_scroll_x = 0

        py.mixer.init()
        py.mixer.music.load("bg_music.mp3")
        py.mixer.music.play(-1)
        
    def _load_and_scale_image(self, path, use_alpha=False):
        """Helper method to load and scale images efficiently"""
        if "Game_Background_Extended" in path:
            img = py.image.load(path).convert_alpha()
            return py.transform.scale(img, (8640, 540))

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

            if event.type == py.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = py.mouse.get_pos()
                if 306 <= mouse_x <= 670 and 376 <= mouse_y <= 501:
                    self.dragon_eye_open = True
                

            if event.type == py.MOUSEBUTTONUP:
                self.dragon_eye_open = False
                mouse_x, mouse_y = py.mouse.get_pos()
                if self.game_state == GameState.MENU:
                    if 820 <= mouse_x <= 910 and 50 <= mouse_y <= 84:
                        self.game_state = GameState.CONTROLS
                    elif 672 <= mouse_x <= 927 and 213 <= mouse_y <= 276:
                        self.transition = True
                    elif 696 <= mouse_x <= 896 and 335 <= mouse_y <= 377:
                        self.running = False
                    elif 43 <= mouse_x <= 235 and 184 <= mouse_y <= 412:
                        self.game_state = GameState.CHARACTER_SELECT

                elif self.game_state == GameState.CHARACTER_SELECT:
                    if 74 <= mouse_x <= 176 and 89 <= mouse_y <= 133:
                        self.game_state = GameState.MENU
                    elif 79 <= mouse_x <= 308 and 189 <= mouse_y <= 467:
                        self.character.character = 'Knight'
                        self.game_state = GameState.MENU
                    elif 341 <= mouse_x <= 583 and 182 <= mouse_y <= 467:
                        self.character.character = 'Wizard'
                        self.game_state = GameState.MENU
                    elif 622 <= mouse_x <= 861 and 177 <= mouse_y <= 474:
                        self.character.character = 'Dark_Knight'
                        self.game_state = GameState.MENU

                elif self.game_state == GameState.CONTROLS:
                    if 26 <= mouse_x <= 128 and 28 <= mouse_y <= 69:
                        self.game_state = GameState.MENU

                elif self.game_state == GameState.GAME_OVER:
                    if 422 <= mouse_x <= 637 and 347 <= mouse_y <= 422:
                        self.game_state = GameState.RUNNING
                    if 397 <= mouse_x <= 561 and 455 <= mouse_y <= 529:
                        self.game_state = GameState.MENU
                    self.game_score.reset()


                
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
                elif keys[py.K_6]:
                    self.game_state = GameState.CONTROLS

                # Handle Character Movement
                if self.game_state == GameState.BOSS_FIGHT or self.game_state == GameState.RUNNING:
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
        """
        Draw scrolling background for running state
        """
        if self.game_state == GameState.RUNNING:
            # Load Background
            bg = self.cached_backgrounds['background']
            
            scroll_speed = 3
            screen_width = self.screen.get_width()
            
            # Use the full width of the background image for scrolling
            self.bg_scroll_x = (self.bg_scroll_x + scroll_speed) % bg.get_width()
            
            # Blit the background twice to create a continuous scroll
            self.screen.blit(bg, (-self.bg_scroll_x, 0))
            self.screen.blit(bg, (bg.get_width() - self.bg_scroll_x, 0))

            self.draw_ground()

    def draw_ground(self):
        """
        Draw scrolling ground
        """
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
        """
        Handle transition between game states
        """
        # Load scrolling Ground
        forest_transition = py.image.load("Game Images/Backgrounds&Objects/transition.png").convert_alpha()
        forest_transition = py.transform.scale(forest_transition, (2400, 540))

        # Update scroll position
        scroll_speed = 15
        self.transition_scroll_x += scroll_speed

        if self.transition_scroll_x == 1695:
            if self.game_state == GameState.MENU:
                self.game_state = GameState.RUNNING
            elif self.game_state == GameState.RUNNING:
                self.game_state = GameState.BOSS_FIGHT
            elif self.game_state == GameState.BOSS_FIGHT:
                self.game_state = GameState.RUNNING

        if self.transition_scroll_x >= 3600:
            self.transition = False
            self.transition_scroll_x = 0
        else:
            self.screen.blit(forest_transition, (1200 - self.transition_scroll_x, 0))

    def menu_state(self):
        """
        Menu state rendering
        """
        if self.dragon_eye_open:
            frame = 2
        else:
            frame = 1

        bg = py.image.load(f"Game Images/Backgrounds&Objects/Main_Menu_{frame}.jpg").convert_alpha()
        bg = py.transform.scale(bg, self.screen.get_size())
        self.screen.blit(bg, (0,0))

        self.character.facing = 'Right'
        self.character.state = 'Resting'
        self.character.image_changer_time = 24
        character_image = py.image.load(self.character.change_image()).convert_alpha()
        character_image = py.transform.scale(character_image, (176, 220))
        self.screen.blit(character_image, (65, 182))

        self.game_score.draw_score(self.screen, 55, 78, self.high_score)

    def character_select_state(self):
        """
        Character selection state rendering
        """
        self.timer += 1

        if self.timer >= 24:
            self.timer = 0
            if self.frame == 1:
                self.frame = 2
            else:
                self.frame = 1

        bg = py.image.load(f"Game Images/Backgrounds&Objects/Character_Select_{self.frame}.png").convert_alpha()
        bg = py.transform.scale(bg, self.screen.get_size())
        self.screen.blit(bg, (0,0))

    def controls_state(self):
        bg = py.image.load(f"Game Images/Backgrounds&Objects/Controls.jpg").convert_alpha()
        bg = py.transform.scale(bg, self.screen.get_size())
        self.screen.blit(bg, (0,0))

    def running_state(self):
        """
        Running state logic for spawning obstacles and checking collisions
        """
        self.game_score.increment()
        self.character.state = 'Running'
        # Spawn obstacles
        self.obstacle_spawn_timer += 1
        if self.obstacle_spawn_timer > random.randint(100, 300):
            y_position = self.screen.get_height() - 115
            obstacle = Obstacle(self.screen.get_width(), y_position)
            self.obstacles.add(obstacle)
            self.obstacle_spawn_timer = 0
        
            
        # Check for collisions with adjusted hitboxes
        for obstacle in self.obstacles:
            # adding horizontal padding to make collision match visuals
            char_left = self.character.player_X + 40  # adjust character's left side hitbox
            char_right = self.character.player_X + 90  # adjust the character's right side hitbox
            char_bottom = self.character.player_Y + 150  # adjust character's bottom hitbox
            
            # Obstacle hitbox adjustments
            obstacle_left = obstacle.rect.x + 10  # added padding to obstacle's left side
            obstacle_right = obstacle.rect.x + obstacle.width - 10  # reduce obstacle's right side
            obstacle_top = obstacle.rect.y + 10  # add padding to obstacle's top
            
            # check if character overlaps with obstacle
            if (char_left < obstacle_right and 
                char_right > obstacle_left and 
                char_bottom > obstacle_top):
                self.game_state = GameState.GAME_OVER
                break
    
    def boss_fight_state(self):
        self.game_score.increment()
        if self.needs_redraw or not self.last_frame:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.cached_backgrounds['forest'], (0, 0))
            self.last_frame = self.screen.copy()
            self.needs_redraw = False
        else:
            self.screen.blit(self.last_frame, (0, 0))

    def game_over_state(self):
        """
        Game over state rendering
        """
        if self.game_score.score >= self.high_score:
            self.high_score = self.game_score.score
            image = 2
            x_pos = 550
            y_pos = 323
            
        else:
            image = 1
            x_pos = 496
            y_pos = 323

        # Write new high score and character
        with open(self.high_score_file, 'w') as file:
            file.write(f"{self.character.character}\n{self.high_score}")

        # Draw Game_Over image
        game_over_overlay = py.transform.scale(py.image.load(f"Game Images/Backgrounds&Objects/Game_Over_Overlay_{image}.png").convert_alpha(), self.screen.get_size())
        self.screen.blit(game_over_overlay, (0,0))

        # Draw new score
        self.game_score.draw_score(self.screen, x_pos, y_pos)

        # Reset Character state and Score
        self.character.facing = 'Right'
        

    def run_game(self):
        """
        Main game loop
        """
        while self.running:
            self.handle_global_events()
                
            self.draw_background()
            if self.game_state == GameState.RUNNING or self.game_state == GameState.BOSS_FIGHT:
                self.character.draw(self.screen)
            
            # Obstacle management
            self.obstacles.update()
            if self.game_state == GameState.RUNNING:
                self.obstacles.draw(self.screen)
            
            # Character position updates
            self.character.update_vertical_position()
            self.character.update_horizontal_position(self.screen, self.game_state)

            if self.transition:
                self.draw_transition()

            if self.game_state in [GameState.RUNNING, GameState.BOSS_FIGHT]:
                self.game_score.draw_score(self.screen)

            py.display.flip()
            self.clock.tick(70)
            
            # Call the current game state method
            self.states[self.game_state]()

        py.quit()


if __name__ == '__main__':
    game = Game()
    game.run_game()