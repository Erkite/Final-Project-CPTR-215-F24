# Alden Thacker & Peyton Wall
# CPTR-215 Final Project - Wizard Run Game
# 11/07/2024 - started framework
# 11/12/2024 - continued framework
# 12/06/2024 - player creation and movement
# 12/07/2024 - transitions
# 12/09/2024 - first version of collision
# 12/11/2024 - HELP Screen, quit button
# 12/12/2024 - persistent character selection, high scores, collision finished, and extra Easter egg
# 12/15/2024 - background music, randomly choosen obstacles, and added the dragon to the boss mode state

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

# Music
# https://www.fesliyanstudios.com/royalty-free-music/download/viking-feast/2073

import enum
import pygame as py
import random

class Score:
    '''
    Loads different images to display the score as the game progresses. The score will be
    displayed at the top-left of the screen. Score always starts at 0 and will be reset
    every new time the game is played.
    '''
    def __init__(self):
        self.score = 0
        self.score_delay = 0
        self.path = 'Game Images/Backgrounds&Objects/{}.png'
        self.number_images = {}

        # load all custom number images to cache
        for i in range(10):
            try:
                img = py.image.load(self.path.format(f'{i}')).convert_alpha()
                self.number_images[str(i)] = py.transform.scale(img, (20, 30))
            except Exception as e:
                print(f"Error loading number image for {i}: {e}")

    def increment(self):
        '''
        Increment the score by a specified amount
        '''
        self.score_delay += 1
        if self.score_delay % 6 == 0:
            self.score += 1

    def reset(self):
        '''
        Reset the score to zero
        '''
        self.score = 1

    def draw_score(self, screen, x_pos = 20, y_pos = 20, high_score = None):
        '''
        Displays the score in the top left corner of the screen by drawing the numbers
        that correlates with the current score. Custom drawn pngs are used as the number
        images.
        '''
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
    '''
    Includes what character is displayed on the screen and the movement
    of that character during gameplay.
    '''
    # Define File path
    path = 'Game Images/Characters/{}_{}_{}_{}.png'
    
    def __init__(self, character = 'Knight'):
        py.sprite.Sprite.__init__(self)
        self.character = character
        self.ground_level = 330
        self.timer = 0

        # Movement variables
        self.is_jumping = False
        self.jump_velocity = 15
        self.move_speed = 5
        self.player_Y = 330
        self.Y_change = 0
        self.player_X = 50
        self.X_change = 0
        self.gravity = 0.7

        # Character Image Attributes
        self.image_changer_time = 12
        self.character_image = None
        self.character_rect = None
        self.state = 'Resting'
        self.facing = 'Right'
        self.frame = 1

    def change_image(self):
        '''
        Update character animation frame
        '''
        self.timer += 1

        if self.timer >= self.image_changer_time:
            self.timer = 0
            self.frame = 2 if self.frame == 1 else 1

        return Character.path.format(self.character, self.frame, self.facing, self.state)

    def draw(self, screen):
        '''
        Draw the character on the screen
        '''
        # Transform image size
        character_image = py.transform.scale(py.image.load(self.change_image()).convert_alpha(), (132, 165))
        # Draw image
        screen.blit(character_image, (self.player_X, self.player_Y))

    def update_vertical_position(self):
        '''
        Update vertical position with jumping and gravity
        '''
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
        '''
        Update horizontal position with movement constraints
        '''
        if self.X_change == 0 and game_state == GameState.RUNNING:
            self.X_change = -5

        # Update horizontal position
        self.player_X += self.X_change
        
        # Get screen width
        screen_width = screen.get_width()
        character_width = 100
        
        # Prevent character from moving off screen
        self.player_X = max(0, min(self.player_X, screen_width - character_width))

class ObstacleType(enum.Enum):
    '''
    Defines the obstacle variables
    '''
    ROCK = "rock"
    BOXES = "boxes"
    BABY_DRAGON = "baby_dragon"
    FIREBALL = "fireball"

class Dragon:
    # Define image path
    path = 'Game Images/Characters/Dragon_Frame_{}_{}.png'

    def __init__(self):
        self.boss_fight_timer = 0
    
    # Animation variables
        self.animation_complete = False
        self.animation_speed = 10
        self.animation_timer = 0
        self.current_frame = 1
        self.dragon_X = -174
        
    # Image variables
        self.facing = 'Right'
        self.direction = 1

    # Fireball variables
        self.fireball_frame = 1
        self.fireball_timer = 0
        self.fireball_changer_time = 7
        self.fireball_x = 0
        self.fireball_y = 0
        
        self.fireballs_dict = {
            'left_fireball_one': (4500, 400),
            'left_fireball_two': (5000, 200),
            'left_fireball_three': (5500, 400),

            'right_fireball_one': (-4500, 400),
            'right_fireball_two': (-5000, 200),
            'right_fireball_three': (-5500, 400)
        }

    def change_image(self):
        '''
        Changes the images for the dragon animation
        while in the boss fight game state
        ''' 
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1

            if self.current_frame > 6:
                self.current_frame = 1

        return Dragon.path.format(self.current_frame, self.facing)

    def draw(self, screen):
        '''
        draws the dragon onto the screen for the boss fight
        '''
        self.boss_fight_timer += 1
        #print(self.boss_fight_timer) # for debugging and fine tuning
       
        # Dragon moves right until it's top left corner has reached x = 0, then it moves left
        if 200 <= self.boss_fight_timer <= 575:
            self.facing = 'Right'
            self.dragon_X += self.direction
            if self.dragon_X == 0:
                self.direction = -1

        # Sets new starting point
        if self.boss_fight_timer == 600:
            self.dragon_X = 960

        # Dragon moves left until it's has moved it's entire width, then it moves right
        elif 1360 <= self.boss_fight_timer <= 1735:
            self.facing = 'Left'
            self.dragon_X += self.direction
            if self.dragon_X == 786:
                self.direction = 1
                
        # creating variable of dragon image and drawing it
        image = py.transform.scale(py.image.load(self.change_image()).convert_alpha(), (174, 366))
        screen.blit(image, (self.dragon_X, 0))

    def draw_fireballs(self, screen):
        '''
        Draws animated fireballs during the boss fight state
        Moves fireballs across the screen with each call
        '''
        self.fireball_timer += 1

        if self.fireball_timer >= self.fireball_changer_time:
            self.fireball_timer = 0
            self.fireball_frame = 2 if self.fireball_frame == 1 else 1

        # Determine fireball positions based on dragon's facing direction
        if self.facing == 'Left':
            # Move fireballs from right to left
            for key in ['left_fireball_one', 'left_fireball_two', 'left_fireball_three']:
                x, y = self.fireballs_dict[key]
                x -= 8  # Move fireball to the left

                if x < -1040:
                    x = 1185

                self.fireballs_dict[key] = (x, y)
                
                fireball = py.transform.scale(
                    py.image.load(f'Game Images/Backgrounds&Objects/Left_fireball_{self.fireball_frame}.png'), 
                    (225, 150)
                )
                screen.blit(fireball, (x, y))
        else:
            # Move fireballs from left to right
            for key in ['right_fireball_one', 'right_fireball_two', 'right_fireball_three']:
                x, y = self.fireballs_dict[key]
                x += 8  # Move fireball to the right
                
                # Wrap around if off screen
                if x > 2000:
                    x = -225
                
                self.fireballs_dict[key] = (x, y)
                
                fireball = py.transform.scale(
                    py.image.load(f'Game Images/Backgrounds&Objects/Right_fireball_{self.fireball_frame}.png'), 
                    (225, 150)
                )
                screen.blit(fireball, (x, y))
    
    def check_fireball_collision(self, player_x, player_y):
        """
        Checks if the player collides with any fireballs during the boss fight
        """
        # Fireball hitbox dimensions (slightly smaller than full fireball size for more precise collision)
        fireball_width = 180
        fireball_height = 100
        player_width = 110
        player_height = 140

        # Shrink the fireball's hitbox
        hitbox_shrink_x = 40  # Amount to shrink width (10px on each side)
        hitbox_shrink_y = 30  # Amount to shrink height (5px on each side)
        fireball_width = fireball_width - hitbox_shrink_x
        fireball_height = fireball_height - hitbox_shrink_y

        # Check collision for both left and right fireballs
        fireball_keys = [
            'left_fireball_one', 'left_fireball_two', 'left_fireball_three',
            'right_fireball_one', 'right_fireball_two', 'right_fireball_three'
        ]

        for key in fireball_keys:
            fireball_x, fireball_y = self.fireballs_dict[key]
            # Adjust fireball hitbox position to center the smaller box
            hitbox_x = fireball_x + hitbox_shrink_x // 2
            hitbox_y = fireball_y + hitbox_shrink_y // 2

            # Check if the player's bounding box intersects with the adjusted fireball hitbox
            if (player_x + player_width > hitbox_x and
                player_x < hitbox_x + fireball_width and
                player_y + player_height > hitbox_y and
                player_y < hitbox_y + fireball_height):
                return True

        return False
    
    def reset(self):
        '''
        '''
        self.boss_fight_timer = 0
        self.facing = 'Right'
        self.dragon_X = -174
        self.direction = 1
        self.fireballs_dict = {
            'left_fireball_one': (4500, 400),
            'left_fireball_two': (5000, 200),
            'left_fireball_three': (5500, 400),
            'right_fireball_one': (-4500, 400),
            'right_fireball_two': (-5000, 200),
            'right_fireball_three': (-5500, 400)
        }

class Obstacle(py.sprite.Sprite):
    def __init__(self, x, y, obstacle_type = "rock", frame = 1):
        super().__init__()
        # Set image path based on obstacle type
        image_path = f"Game Images/Backgrounds&Objects/{obstacle_type}_{frame}.png"
        self.image = py.image.load(image_path).convert_alpha()
        # Changes image dimentions
        if obstacle_type == "rock":
           w = 70
           h = 70
        if obstacle_type == "boxes":
            w = 100
            h = 100
        if obstacle_type == "fireball":
            w = 150
            h = 100
            
        self.image = py.transform.scale(self.image, (w, h))  # obstacle size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5  # speed of obstacle
        self.width = 70

    def update(self):
        '''
        Move the obstacle to the left and remove when off-screen
        '''
        self.rect.x -= self.speed  # movement of obstacle going left
        if self.rect.right < 0:  # delete the obstacle when it's off the screen
            self.kill()

class GameState(enum.Enum):
    '''
    Defining the different game states the game can be in (essentially the different
    screens the player sees).
    '''
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    RUNNING = "running"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"
    CONTROLS = "controls"

class Game:
    def __init__(self):
    # Create and name screen and declare font
        py.init()
        self.screen = py.display.set_mode((960, 540))
        py.display.set_caption("Dragon Run")

        # initialize mixer module, load the background music, and play the music
        py.mixer.init()
        py.mixer.music.load("bg_music.mp3")
        py.mixer.music.play(-1)

        # assign high score file and start the high score at 0
        self.high_score_file = 'game_progress.txt'
        self.high_score = 0
        
        # Set variable to hold saved character or default character if first time opening the game
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

        # create a set of all cached backgrounds
        self.cached_backgrounds = {
            'background_1': self._load_and_scale_image("Game Images/Backgrounds&Objects/Game_Background_1.jpg"),
            'background_2': self._load_and_scale_image("Game Images/Backgrounds&Objects/Game_Background_2.jpg"),
            'background_3': self._load_and_scale_image("Game Images/Backgrounds&Objects/Game_Background_3.jpg"),
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

        # General Game Variables
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

        # Transition Variables
        self.transition = False
        self.transition_scroll_x = 0
        
        # Background Variable
        self.bg_scroll_x = 0
        self.ground_scroll_x = 0
        self.background_timer = 0
        self.background_changer_time = 12
        self.background_frame = 1

        # Boss fight variables
        self.dragon = Dragon()
        
    def _load_and_scale_image(self, path, use_alpha=False):
        '''
        Helper method to load and scale images efficiently
        '''
        if "Game_Background" in path:
            img = py.image.load(path).convert_alpha()
            return py.transform.scale(img, (8640, 540))

        if use_alpha:
            img = py.image.load(path).convert_alpha()
        else:
            img = py.image.load(path).convert()
        return py.transform.scale(img, self.screen.get_size())

    def handle_global_events(self):
        ''' 
        Handles Quit functionality, as well as event queue for all
        keypress and mouseclick events.
        '''
        # Quit button functionality
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
                return
            
            # Dragon Easter Egg event
            if event.type == py.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = py.mouse.get_pos()
                if 306 <= mouse_x <= 670 and 376 <= mouse_y <= 501:
                    self.dragon_eye_open = True

            # Define all clickable 'boxes' / ranges of pixels in each game state
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
                        self.dragon.reset()
                        self.game_state = GameState.RUNNING
                        self.game_score.reset()
                    if 397 <= mouse_x <= 561 and 455 <= mouse_y <= 529:
                        self.game_state = GameState.MENU
                        self.game_score.reset()


            # Gamestate Navigation shortcuts for debugging (delete later)
            
            if event.type == py.KEYDOWN:
                keys = py.key.get_pressed()
                '''
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
                '''
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

            # Stops character movement when nkey is let up
            if event.type == py.KEYUP:
                #self.character.state = 'Resting'
                if event.key == py.K_d or event.key == py.K_RIGHT or event.key == py.K_a or event.key == py.K_LEFT:
                    self.character.X_change = 0

    def draw_background(self):
        '''
        Draw scrolling background for running state
        '''
        if self.game_state == GameState.RUNNING:
            self.background_timer += 1
            if self.background_timer >= self.background_changer_time:
                self.background_timer = 0
                self.background_frame += 1
    
            if self.background_frame == 3:
                self.background_frame = 1

            # Load Background
            bg = self.cached_backgrounds[f'background_{self.background_frame}']
            
            # Use the full width of the background image for scrolling
            self.bg_scroll_x = (self.bg_scroll_x + 3) % bg.get_width()
            
            # Blit the background twice to create a continuous scroll
            self.screen.blit(bg, (-self.bg_scroll_x, 0))
            self.screen.blit(bg, (bg.get_width() - self.bg_scroll_x, 0))

            self.draw_ground()

    def draw_ground(self):
        '''
        Draw scrolling ground
        '''
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
        '''
        Handle transition between game states
        '''
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
        '''
        Menu state rendering
        '''
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
        '''
        Character selection state rendering
        '''
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
        '''
        Transforms and draws the control pannel onto the screen
        '''
        control_page = py.transform.scale(py.image.load(f"Game Images/Backgrounds&Objects/Controls.jpg").convert_alpha(), self.screen.get_size())
        self.screen.blit(control_page, (0,0))

    def running_state(self):
        '''
        Running state logic for spawning obstacles and checking collisions
        '''
        self.game_score.increment()
        if self.game_score.score % 450 == 0:
            self.dragon.boss_fight_timer = 0
            self.transition = True 

        self.character.state = 'Running'
        # Spawn obstacles
        self.obstacle_spawn_timer += 1
        if self.obstacle_spawn_timer > random.randint(100, 300):
            y_position = self.screen.get_height() - 115

            # Randomly choose between rock and boxes
            obstacle_type = random.choice(['rock', 'boxes'])
            if obstacle_type == 'boxes':
               obstacle = Obstacle(self.screen.get_width(), y_position-30, obstacle_type) 
            else:
                obstacle = Obstacle(self.screen.get_width(), y_position, obstacle_type)            
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
        '''
        Boss fight state with dragon and fireballs
        '''
        self.game_score.increment()
        if self.game_score.score % 450 == 0:
            self.dragon.reset()
            self.transition = True 

        # Fill screen with forest background
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.cached_backgrounds['forest'], (0, 0))

        # Draw Dragon
        self.dragon.draw(self.screen)

        # Draw Fireballs consistently
        self.dragon.draw_fireballs(self.screen)

        if self.dragon.check_fireball_collision(self.character.player_X, self.character.player_Y):
            self.game_state = GameState.GAME_OVER

    def game_over_state(self):
        '''
        Game over state happens when a player collides with an obstacle. When this
        state occurs, the score and character being used are written to "game_progress.txt"
        as a means of saving that information. There will also be buttons to either "Play Again"
        or go back to the "Menu" (Home Screen).
        '''
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
        '''
        Main game loop that handles global events, draws the game background, and updates the obstacles.
        It also handles transitions, draws the scores, sets the tick speed, and updates what is being
        displayed on the screen.
        '''
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