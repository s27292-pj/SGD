import pygame
import sys
import os
import random
import math
import json
from PIL import Image

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RefleX Inferno")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Fonts
FONT = pygame.font.SysFont("arial", 36)
SMALL_FONT = pygame.font.SysFont("arial", 24)
TINY_FONT = pygame.font.SysFont("arial", 18)

# Player data file
PLAYER_DATA_FILE = "player_data.json"
player_data = {}

# Player skins
PLAYER_SKINS_DIR = "assets/player_skins"
player_skins = {}
# Skin unlocks map: level -> skin filename
SKIN_UNLOCKS = {
    2: "cow.png",
    3: "enderman.png", 
    4: "pig.png",
    5: "villager.png"
}
# XP required for each level
XP_PER_LEVEL = {
    1: 100, 2: 250, 3: 500, 4: 1000, 5: 2000
}

# Player settings
player_size = 30
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 7
player1_skin_name = "default.png"
player2_skin_name = "default.png"
# Score and timer
score = 0
start_ticks = 0
xp_gained = 0

# Bullet system - simple straight bullets
bullets = []
bullet_speed = 2  # Start fast
bullet_spawn_timer = 0
bullet_spawn_delay = 800  # Moderate start - 0.8 seconds between spawns
bullet_spawn_delay_min = 200  # Faster minimum delay

# Colorful bullet colors
bullet_colors = [
    (255, 100, 100),  # Red
    (100, 100, 255),  # Blue  
    (255, 255, 100),  # Yellow
    (255, 100, 255),  # Magenta
    (100, 255, 100),  # Green
    (255, 150, 50),   # Orange
    (150, 100, 255),  # Purple
]

# Game states
START, MENU, MODE_SELECT, CHARACTER_SELECT, PLAYING, PAUSED, GAME_OVER = 0, 1, 2, 3, 4, 5, 6
game_state = START
current_level = 1

# Music system
pygame.mixer.init()
current_music = None
current_volume = 0.5
is_muted = False
pygame.mixer.music.set_volume(current_volume)

# High score system
HIGH_SCORES_FILE = "high_scores.json"
high_scores = {1: 0, 2: 0, 3: 0}  # Add Level 3 high score

# Menu background
menu_background = None
menu_background_frames = []
menu_frame_idx = 0
menu_frame_timer = 0
menu_frame_delay = 16  # 60fps animation

# Title animation variables
title_scale = 1.0
title_scale_direction = 1
title_animation_timer = 0

# Add multiplayer mode
multiplayer_mode = False
player2_x = WIDTH // 2 - player_size // 2
player2_y = HEIGHT // 2 - player_size // 2

# Add a global variable for selected_skin_index
selected_skin_index = 0

# Add new variables for multiplayer skin selection
player1_selected_skin = None
player2_selected_skin = None
multiplayer_selection_step = 1  # 1 = Player 1 selecting, 2 = Player 2 selecting

# Define skin lists globally
all_skins = ["default.png", "cow.png", "enderman.png", "pig.png", "villager.png"]

def load_music(level):
    """Load music for specific level"""
    global current_music
    try:
        music_path = os.path.join("assets", "music", f"level_{level}.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            if level == 3:
                pygame.mixer.music.set_pos(45)
            current_music = f"level_{level}"
        else:
            print(f"Music file not found: {music_path}")
    except Exception as e:
        print(f"Error loading music: {e}")

def load_menu_music():
    """Load and play menu music"""
    global current_music
    try:
        music_path = os.path.join("assets", "music", "menu.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.set_pos(40)
            current_music = "menu"
        else:
            print(f"Menu music file not found: {music_path}")
    except Exception as e:
        print(f"Error loading menu music: {e}")

def load_game_over_music():
    """Load and play game over music"""
    global current_music
    try:
        music_path = os.path.join("assets", "music", "game_over.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(0)  # Play once, don't loop
            pygame.mixer.music.set_pos(38)
            current_music = "game_over"
        else:
            print(f"Game over music file not found: {music_path}")
    except Exception as e:
        print(f"Error loading game over music: {e}")

def stop_music():
    """Stop current music"""
    global current_music
    pygame.mixer.music.stop()
    current_music = None

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_text_with_rect(text, font, color, surface, x, y):
    """Draw text with simple rectangle background"""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    
    # Draw simple rectangle background
    bg_rect = textrect.inflate(20, 10)  # Add some padding
    pygame.draw.rect(surface, (50, 50, 50), bg_rect)  # Dark grey rectangle
    pygame.draw.rect(surface, (100, 100, 100), bg_rect, 2)  # Border
    
    # Draw text on top
    surface.blit(textobj, textrect)

def spawn_bullet_level_1():
    """Spawn straight bullets for Level 1"""
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    color = random.choice(bullet_colors)
    size = random.randint(4, 8)
    
    if edge == 'top':
        x = random.randint(0, WIDTH)
        y = -10
        dx = 0
        dy = bullet_speed
    elif edge == 'bottom':
        x = random.randint(0, WIDTH)
        y = HEIGHT + 10
        dx = 0
        dy = -bullet_speed
    elif edge == 'left':
        x = -10
        y = random.randint(0, HEIGHT)
        dx = bullet_speed
        dy = 0
    else:  # right
        x = WIDTH + 10
        y = random.randint(0, HEIGHT)
        dx = -bullet_speed
        dy = 0
    
    bullets.append({
        'x': x, 'y': y, 'dx': dx, 'dy': dy, 
        'color': color, 'size': size
    })

def spawn_bullet_level_2():
    """Spawn straight and diagonal bullets for Level 2"""
    bullet_type = random.choice(['straight', 'diagonal'])
    color = random.choice(bullet_colors)
    size = random.randint(4, 8)
    
    if bullet_type == 'straight':
        # Same as level 1
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            x = random.randint(0, WIDTH)
            y = -10
            dx = 0
            dy = bullet_speed
        elif edge == 'bottom':
            x = random.randint(0, WIDTH)
            y = HEIGHT + 10
            dx = 0
            dy = -bullet_speed
        elif edge == 'left':
            x = -10
            y = random.randint(0, HEIGHT)
            dx = bullet_speed
            dy = 0
        else:  # right
            x = WIDTH + 10
            y = random.randint(0, HEIGHT)
            dx = -bullet_speed
            dy = 0
    else:
        # Random diagonal bullets from random positions along edges
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            x = random.randint(-50, WIDTH + 50)
            y = -10
            angle = random.uniform(-60, 60) * (3.14159 / 180)
            dx = math.sin(angle) * bullet_speed
            dy = math.cos(angle) * bullet_speed
        elif edge == 'bottom':
            x = random.randint(-50, WIDTH + 50)
            y = HEIGHT + 10
            angle = random.uniform(120, 240) * (3.14159 / 180)
            dx = math.sin(angle) * bullet_speed
            dy = math.cos(angle) * bullet_speed
        elif edge == 'left':
            x = -10
            y = random.randint(-50, HEIGHT + 50)
            angle = random.uniform(30, 150) * (3.14159 / 180)
            dx = math.cos(angle) * bullet_speed
            dy = math.sin(angle) * bullet_speed
        else:  # right
            x = WIDTH + 10
            y = random.randint(-50, HEIGHT + 50)
            angle = random.uniform(210, 330) * (3.14159 / 180)
            dx = math.cos(angle) * bullet_speed
            dy = math.sin(angle) * bullet_speed
    bullets.append({
        'x': x, 'y': y, 'dx': dx, 'dy': dy,
        'color': color, 'size': size
    })

def spawn_bullet_level_3():
    """Spawn advanced bullet patterns for Level 3"""
    pattern_type = random.choice(['curved_trajectory', 'sine_wave', 'spiral_curve', 'bouncing_wave', 'zigzag_pattern'])
    color = random.choice(bullet_colors)
    size = random.randint(4, 8)
    
    if pattern_type == 'curved_trajectory':
        # Bullets that curve as they move
        for i in range(3):  # 3 curved bullets
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                x = random.randint(50, WIDTH - 50)
                y = -10
                dx = random.uniform(-1, 1)
                dy = random.uniform(bullet_speed * 0.8, bullet_speed * 1.2)
            elif edge == 'bottom':
                x = random.randint(50, WIDTH - 50)
                y = HEIGHT + 10
                dx = random.uniform(-1, 1)
                dy = random.uniform(-bullet_speed * 1.2, -bullet_speed * 0.8)
            elif edge == 'left':
                x = -10
                y = random.randint(50, HEIGHT - 50)
                dx = random.uniform(bullet_speed * 0.8, bullet_speed * 1.2)
                dy = random.uniform(-1, 1)
            else:  # right
                x = WIDTH + 10
                y = random.randint(50, HEIGHT - 50)
                dx = random.uniform(-bullet_speed * 1.2, -bullet_speed * 0.8)
                dy = random.uniform(-1, 1)
            
            bullets.append({
                'x': x, 'y': y, 'dx': dx, 'dy': dy, 
                'color': color, 'size': size, 'type': 'curved', 'curve_factor': random.uniform(0.1, 0.3)
            })
    
    elif pattern_type == 'sine_wave':
        # Bullets that move in sine wave pattern
        for i in range(4):  # 4 sine wave bullets
            x = random.randint(50, WIDTH - 50)
            y = -10
            dx = 0
            dy = random.uniform(bullet_speed * 0.8, bullet_speed * 1.2)
            
            bullets.append({
                'x': x, 'y': y, 'dx': dx, 'dy': dy, 
                'color': color, 'size': size, 'type': 'sine', 'sine_offset': i * 1.5, 'sine_amplitude': random.uniform(2, 4)
            })
    
    elif pattern_type == 'spiral_curve':
        # Bullets that spiral outward from edge
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            center_x = random.randint(100, WIDTH - 100)
            center_y = -50
        elif edge == 'bottom':
            center_x = random.randint(100, WIDTH - 100)
            center_y = HEIGHT + 50
        elif edge == 'left':
            center_x = -50
            center_y = random.randint(100, HEIGHT - 100)
        else:  # right
            center_x = WIDTH + 50
            center_y = random.randint(100, HEIGHT - 100)
        
        for i in range(6):  # 6 spiral bullets
            angle = (i / 6) * 2 * 3.14159
            speed = random.uniform(bullet_speed * 0.8, bullet_speed * 1.2)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            bullets.append({
                'x': center_x, 'y': center_y, 
                'dx': dx, 'dy': dy, 'color': color, 'size': size, 'type': 'spiral', 'spiral_angle': angle
            })
    
    elif pattern_type == 'bouncing_wave':
        # Bullets that bounce off screen edges
        for i in range(3):  # 3 bouncing bullets
            x = random.randint(50, WIDTH - 50)
            y = -10
            dx = random.uniform(-bullet_speed * 0.5, bullet_speed * 0.5)
            dy = random.uniform(bullet_speed * 0.8, bullet_speed * 1.2)
            
            bullets.append({
                'x': x, 'y': y, 'dx': dx, 'dy': dy, 
                'color': color, 'size': size, 'type': 'bouncing'
            })
    
    elif pattern_type == 'zigzag_pattern':
        # Bullets that zigzag as they move
        for i in range(4):  # 4 zigzag bullets
            x = random.randint(50, WIDTH - 50)
            y = -10
            dx = 0
            dy = random.uniform(bullet_speed * 0.8, bullet_speed * 1.2)
            
            bullets.append({
                'x': x, 'y': y, 'dx': dx, 'dy': dy, 
                'color': color, 'size': size, 'type': 'zigzag', 'zigzag_offset': i * 1.0, 'zigzag_frequency': random.uniform(0.1, 0.2)
            })

def spawn_bullet():
    """Spawn bullets based on current level"""
    if current_level == 1:
        spawn_bullet_level_1()
    elif current_level == 2:
        spawn_bullet_level_2()
    elif current_level == 3:
        spawn_bullet_level_3()

def check_collision(player_x, player_y, player_size, bullet_x, bullet_y, bullet_size):
    """Check collision between player and bullet"""
    return (player_x < bullet_x + bullet_size and
            player_x + player_size > bullet_x and
            player_y < bullet_y + bullet_size and
            player_y + player_size > bullet_y)

def load_high_scores():
    """Load high scores from JSON file"""
    global high_scores
    try:
        if os.path.exists(HIGH_SCORES_FILE):
            print(f"Loading high scores from {HIGH_SCORES_FILE}")
            with open(HIGH_SCORES_FILE, 'r') as f:
                loaded_scores = json.load(f)
            # Convert string keys to integers
            high_scores = {int(k): v for k, v in loaded_scores.items()}
            print(f"Loaded high scores: {high_scores}")
        else:
            print(f"High scores file not found, creating default")
            # Create default high scores file
            save_high_scores()
    except Exception as e:
        print(f"Error loading high scores: {e}")
        print(f"Falling back to default high scores")
        high_scores = {1: 0, 2: 0, 3: 0}

def save_high_scores():
    """Save high scores to JSON file"""
    try:
        with open(HIGH_SCORES_FILE, 'w') as f:
            json.dump(high_scores, f)
    except Exception as e:
        print(f"Error saving high scores: {e}")

def update_high_score(level, score):
    """Update high score for a level if current score is higher"""
    if score > high_scores.get(level, 0):
        high_scores[level] = score
        save_high_scores()
        return True
    return False

def load_menu_background():
    """Load and prepare animated menu background GIF"""
    global menu_background_frames
    try:
        gif_path = os.path.join("assets", "background.gif")
        pil_gif = Image.open(gif_path)
        
        print(f"Loading menu background: {pil_gif.size}, {pil_gif.mode}")
        
        # Extract all frames from the animated GIF
        frame_count = 0
        while True:
            try:
                # Create a copy of the current frame
                frame_image = pil_gif.copy()
                
                # Convert to RGBA if needed
                if frame_image.mode == 'P':
                    frame_image = frame_image.convert('RGBA')
                elif frame_image.mode != 'RGBA':
                    frame_image = frame_image.convert('RGBA')
                
                # Convert PIL image to pygame surface and scale
                frame_surface = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, 'RGBA')
                scaled_frame = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
                menu_background_frames.append(scaled_frame)
                
                frame_count += 1
                pil_gif.seek(frame_count)
            except EOFError:
                # No more frames
                break
        
        print(f"Loaded {len(menu_background_frames)} frames for menu background")
        
    except Exception as e:
        print(f"Error loading menu background: {e}")
        menu_background_frames = []

def load_player_skins():
    """Load all player skins from the assets folder."""
    global player_skins
    try:
        for filename in os.listdir(PLAYER_SKINS_DIR):
            if filename.endswith(".png"):
                path = os.path.join(PLAYER_SKINS_DIR, filename)
                image = pygame.image.load(path).convert_alpha()
                scaled_image = pygame.transform.scale(image, (player_size, player_size))
                player_skins[filename] = scaled_image
        print(f"Loaded {len(player_skins)} skins.")
    except Exception as e:
        print(f"Error loading player skins: {e}")

def load_player_data():
    """Load player progress from JSON file."""
    global player_data
    try:
        if os.path.exists(PLAYER_DATA_FILE):
            with open(PLAYER_DATA_FILE, 'r') as f:
                player_data = json.load(f)
        else:
            # Create default data
            player_data = {
                "level": 1, "xp": 0, "xp_to_next_level": XP_PER_LEVEL[1],
                "unlocked_skins": ["default.png"],
                "player1_skin": "default.png", "player2_skin": "default.png"
            }
            save_player_data()
    except Exception as e:
        print(f"Error loading player data: {e}")
        # Fallback to default
        player_data = {
            "level": 1, "xp": 0, "xp_to_next_level": XP_PER_LEVEL[1],
            "unlocked_skins": ["default.png"],
            "player1_skin": "default.png", "player2_skin": "default.png"
        }

def save_player_data():
    """Save player progress to JSON file."""
    try:
        with open(PLAYER_DATA_FILE, 'w') as f:
            json.dump(player_data, f, indent=2)
    except Exception as e:
        print(f"Error saving player data: {e}")

def reset_player_positions():
    """Reset both players to center position"""
    global player_x, player_y, player2_x, player2_y
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT // 2 - player_size // 2
    player2_x = WIDTH // 2 - player_size // 2
    player2_y = HEIGHT // 2 - player_size // 2

def set_level_difficulty(level):
    """Set bullet speed and spawn delay based on level"""
    global bullet_speed, bullet_spawn_delay
    if level == 1:
        bullet_speed, bullet_spawn_delay = 3, 400
    elif level == 2:
        bullet_speed, bullet_spawn_delay = 3.5, 300
    elif level == 3:
        bullet_speed, bullet_spawn_delay = 4, 250

# Main loop
running = True

# Load initial data
load_high_scores()
load_menu_background()
load_player_data()
load_player_skins()

while running:
    # Animate menu background
    if game_state in [START, MENU] and menu_background_frames:
        now = pygame.time.get_ticks()
        if now - menu_frame_timer > menu_frame_delay:
            menu_frame_idx = (menu_frame_idx + 1) % len(menu_background_frames)
            menu_frame_timer = now
        current_menu_frame = menu_background_frames[menu_frame_idx]
    else:
        current_menu_frame = None
    
    # Background handling
    if game_state in [START, MENU]:
        # Use animated menu background for menu states
        if current_menu_frame:
            WIN.blit(current_menu_frame, (0, 0))
        else:
            WIN.fill((20, 20, 40))  # Fallback to dark background
    else:
        # Use dark background for gameplay
        WIN.fill((20, 20, 40))  # Dark blue-gray background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # --- Handle mute/volume keys for all states ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                is_muted = not is_muted
                if is_muted:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(current_volume)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                if not is_muted:
                    current_volume = max(0.0, current_volume - 0.1)
                    pygame.mixer.music.set_volume(current_volume)
            elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                if not is_muted:
                    current_volume = min(1.0, current_volume + 0.1)
                    pygame.mixer.music.set_volume(current_volume)
        # --- End mute/volume keys ---

        if game_state == START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = MENU
                load_menu_music()  # Load menu music when entering menu
        elif game_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    current_level = int(event.key - pygame.K_0)  # Set current_level here
                    game_state = 'MODE_SELECT'
                elif event.key == pygame.K_s:
                    multiplayer_mode = False
                    game_state = PLAYING
                    # Reset game state
                    reset_player_positions()
                    score = 0
                    start_ticks = pygame.time.get_ticks()
                    bullets.clear()
                    set_level_difficulty(current_level)
                    load_music(current_level)
                elif event.key == pygame.K_m:
                    multiplayer_mode = True
                    game_state = PLAYING
                    # Reset game state
                    reset_player_positions()
                    score = 0
                    start_ticks = pygame.time.get_ticks()
                    bullets.clear()
                    set_level_difficulty(current_level)
                    load_music(current_level)
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                game_state = PAUSED
                pygame.mixer.music.pause()
        elif game_state == PAUSED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                game_state = PLAYING
                pygame.mixer.music.unpause()
        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = MENU
                load_menu_music()  # Return to menu music
        elif game_state == 'MODE_SELECT':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    multiplayer_mode = False
                    game_state = CHARACTER_SELECT
                elif event.key == pygame.K_2:
                    multiplayer_mode = True
                    game_state = CHARACTER_SELECT
        elif game_state == CHARACTER_SELECT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    selected_skin_index = (selected_skin_index + 1) % len(all_skins)
                elif event.key == pygame.K_a:
                    selected_skin_index = (selected_skin_index - 1) % len(all_skins)
                elif event.key == pygame.K_RETURN:
                    # Only allow selection of unlocked skins
                    unlocked = player_data.get("unlocked_skins", ["default.png"])
                    current_skin = all_skins[selected_skin_index]
                    if current_skin in unlocked:
                        if multiplayer_mode:
                            if multiplayer_selection_step == 1:
                                # Player 1 selects
                                player1_selected_skin = current_skin
                                multiplayer_selection_step = 2
                                # Reset selection to first skin for player 2
                                selected_skin_index = 0
                            else:
                                # Player 2 selects - start game
                                player2_selected_skin = current_skin
                                player1_skin_name = player1_selected_skin
                                player2_skin_name = player2_selected_skin
                                
                                # Save selections and start game
                                player_data['player1_skin'] = player1_skin_name
                                player_data['player2_skin'] = player2_skin_name
                                save_player_data()
                                
                                # Reset multiplayer selection variables
                                player1_selected_skin = None
                                player2_selected_skin = None
                                multiplayer_selection_step = 1
                                
                                game_state = PLAYING
                                reset_player_positions()
                                score = 0
                                xp_gained = 0
                                start_ticks = pygame.time.get_ticks()
                                bullets.clear()
                                
                                set_level_difficulty(current_level)
                                load_music(current_level)
                        else:
                            # Single player - start immediately
                            player1_skin_name = current_skin
                            player2_skin_name = current_skin
                            
                            player_data['player1_skin'] = player1_skin_name
                            save_player_data()
                            
                            game_state = PLAYING
                            reset_player_positions()
                            score = 0
                            xp_gained = 0
                            start_ticks = pygame.time.get_ticks()
                            bullets.clear()
                            
                            set_level_difficulty(current_level)
                            load_music(current_level)

    # Game logic and rendering
    if game_state == PLAYING:
        keys = pygame.key.get_pressed()
        if multiplayer_mode:
            # Player 1: WASD
            if keys[pygame.K_w]:
                player_y -= player_speed
            if keys[pygame.K_s]:
                player_y += player_speed
            if keys[pygame.K_a]:
                player_x -= player_speed
            if keys[pygame.K_d]:
                player_x += player_speed
            # Player 2: Arrows
            if keys[pygame.K_UP]:
                player2_y -= player_speed
            if keys[pygame.K_DOWN]:
                player2_y += player_speed
            if keys[pygame.K_LEFT]:
                player2_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player2_x += player_speed
            # Keep both players on screen
            player_x = max(0, min(WIDTH - player_size, player_x))
            player_y = max(0, min(HEIGHT - player_size, player_y))
            player2_x = max(0, min(WIDTH - player_size, player2_x))
            player2_y = max(0, min(HEIGHT - player_size, player2_y))
        else:
            # Single player: WASD or arrows
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_y -= player_speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_y += player_speed
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_x += player_speed
            player_x = max(0, min(WIDTH - player_size, player_x))
            player_y = max(0, min(HEIGHT - player_size, player_y))
        
        # Spawn bullets
        now = pygame.time.get_ticks()
        if now - bullet_spawn_timer > bullet_spawn_delay:
            spawn_bullet()
            bullet_spawn_timer = now
            # Increase difficulty over time - more aggressive
            bullet_spawn_delay = max(bullet_spawn_delay_min, bullet_spawn_delay - 3)  # Faster decrease
            # Increase bullet speed every 15 seconds (faster progression)
            if (now - start_ticks) % 15000 < 100:  # Every 15 seconds
                bullet_speed += 0.3  # Larger speed increase
        
        # Update bullets
        for bullet in bullets[:]:
            # Normal movement for all bullets
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']

            # Remove bullets that are off screen
            if (bullet['x'] < -20 or bullet['x'] > WIDTH + 20 or 
                bullet['y'] < -20 or bullet['y'] > HEIGHT + 20):
                bullets.remove(bullet)
                continue

            # Check collision with player
            if multiplayer_mode:
                if check_collision(player_x, player_y, player_size, bullet['x'], bullet['y'], bullet.get('size', 6)) or \
                   check_collision(player2_x, player2_y, player_size, bullet['x'], bullet['y'], bullet.get('size', 6)):
                    game_state = GAME_OVER
                    load_game_over_music()
                    break
            else:
                if check_collision(player_x, player_y, player_size, bullet['x'], bullet['y'], bullet.get('size', 6)):
                    game_state = GAME_OVER
                    load_game_over_music()
                    break
        
        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(WIN, bullet['color'], (int(bullet['x']), int(bullet['y'])), bullet.get('size', 6))
        
        # Draw player(s)
        p1_skin = player_skins.get(player1_skin_name)
        if p1_skin:
            WIN.blit(p1_skin, (player_x, player_y))

        if multiplayer_mode:
            p2_skin = player_skins.get(player2_skin_name)
            if p2_skin:
                WIN.blit(p2_skin, (player2_x, player2_y))
        
        # Calculate running time and score
        elapsed_ms = pygame.time.get_ticks() - start_ticks
        elapsed_sec = elapsed_ms // 1000
        score = elapsed_sec
        
        # Draw UI
        current_high_score = high_scores.get(current_level, 0)
        ui_text = f"Lvl: {player_data.get('level', 1)} | Score: {score} | High: {current_high_score} | Time: {elapsed_sec}s"
        draw_text(ui_text, SMALL_FONT, WHITE, WIN, WIDTH // 2, 30)
        
        xp_text = f"XP: {player_data.get('xp', 0)} / {player_data.get('xp_to_next_level', 100)}"
        draw_text(xp_text, SMALL_FONT, GOLD, WIN, WIDTH // 2, 60)
        
        # Draw volume/mute status in the top right
        vol_text = f"MUTE" if is_muted else f"VOL: {int(current_volume*100)}%"
        draw_text_with_rect(vol_text, TINY_FONT, WHITE, WIN, WIDTH - 70, HEIGHT - 30)
        
        # Update UI instructions for multiplayer
        if multiplayer_mode:
            draw_text_with_rect("PLAYER 1: WASD | PLAYER 2: ARROWS", TINY_FONT, WHITE, WIN, WIDTH // 2, HEIGHT - 60)
    elif game_state == PAUSED:
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)  # Semi-transparent
        overlay.fill((0, 0, 0))
        WIN.blit(overlay, (0, 0))
        
        # Draw pause text
        draw_text_with_rect("PAUSED", FONT, BLUE, WIN, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text_with_rect("Press P to resume", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2)
        draw_text_with_rect("Press ESC to quit to menu", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2 + 40)
        
        # Handle ESC to quit to menu while paused
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = MENU
            load_menu_music()
    elif game_state == GAME_OVER:
        # This part should only run ONCE per game over
        if xp_gained == 0:
            xp_gained = score * current_level  # Simple XP formula
            player_data["xp"] += xp_gained
            
            # Check for level up
            current_level_data = player_data.get("level", 1)
            xp_needed = player_data.get("xp_to_next_level", 100)
            if player_data["xp"] >= xp_needed:
                player_data["level"] += 1
                new_level = player_data["level"]
                # Unlock new skin
                if new_level in SKIN_UNLOCKS:
                    # Avoid duplicates
                    if SKIN_UNLOCKS[new_level] not in player_data["unlocked_skins"]:
                        player_data["unlocked_skins"].append(SKIN_UNLOCKS[new_level])
                # Set next XP goal
                player_data["xp_to_next_level"] = XP_PER_LEVEL.get(new_level, 99999)

            save_player_data()
        
        # Check for new high score
        is_new_high_score = update_high_score(current_level, score)
        current_high_score = high_scores.get(current_level, 0)
        
        draw_text_with_rect("Game Over!", FONT, RED, WIN, WIDTH // 2, HEIGHT // 2 - 80)
        if is_new_high_score:
            draw_text_with_rect("NEW HIGH SCORE!", FONT, GOLD, WIN, WIDTH // 2, HEIGHT // 2 - 40)
        draw_text_with_rect(f"Level {current_level} - Final Score: {score}", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2 - 10)
        draw_text_with_rect(f"High Score: {current_high_score}", TINY_FONT, GOLD, WIN, WIDTH // 2, HEIGHT // 2 + 35)
        draw_text_with_rect("Press R to return to menu", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2 + 85)
        draw_text_with_rect(f"+{xp_gained} XP", FONT, GOLD, WIN, WIDTH // 2, HEIGHT // 2 + 125)
    
    # Animate title
    if game_state == START:
        now = pygame.time.get_ticks()
        if now - title_animation_timer > 50:  # Update every 50ms
            title_scale += 0.01 * title_scale_direction  # Change scale
            
            # Reverse scale direction when reaching limits
            if title_scale >= 1.2:
                title_scale_direction = -1
            elif title_scale <= 0.8:
                title_scale_direction = 1
            
            title_animation_timer = now

    if game_state == START:
        # Draw animated title
        title_text = "RefleX Inferno"
        title_surface = FONT.render(title_text, True, BLUE)
        
        # Scale the title
        scaled_width = int(title_surface.get_width() * title_scale)
        scaled_height = int(title_surface.get_height() * title_scale)
        scaled_surface = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        # Center the scaled title
        title_rect = scaled_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        
        # Draw background rectangle for title
        bg_rect = title_rect.inflate(20, 10)
        pygame.draw.rect(WIN, (50, 50, 50), bg_rect)
        pygame.draw.rect(WIN, (100, 100, 100), bg_rect, 2)
        
        # Draw the animated title
        WIN.blit(scaled_surface, title_rect)
        draw_text_with_rect("Press SPACE to start", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2)
        draw_text_with_rect("WASD or Arrow Keys to move. Avoid bullets!", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2 + 40)
    elif game_state == MENU:
        draw_text_with_rect("Select Level", FONT, BLUE, WIN, WIDTH // 2, HEIGHT // 2 - 160)
        draw_text_with_rect("Press 1 - Level 1 (Straight Bullets)", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2 - 100)
        draw_text_with_rect(f"High Score: {high_scores.get(1, 0)}", TINY_FONT, GOLD, WIN, WIDTH // 2, HEIGHT // 2 - 70)
        draw_text_with_rect("Press 2 - Level 2 (Straight + Diagonal)", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text_with_rect(f"High Score: {high_scores.get(2, 0)}", TINY_FONT, GOLD, WIN, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text_with_rect("Press 3 - Level 3 (Complex Patterns)", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2 + 60)
        draw_text_with_rect(f"High Score: {high_scores.get(3, 0)}", TINY_FONT, GOLD, WIN, WIDTH // 2, HEIGHT // 2 + 90)
        draw_text_with_rect("WASD to move. Avoid bullets!", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT // 2 + 140)
    elif game_state == 'MODE_SELECT':
        draw_text_with_rect("1 - Single Player  |  2 - Multiplayer", FONT, BLUE, WIN, WIDTH // 2, HEIGHT // 2)
    elif game_state == CHARACTER_SELECT:
        if multiplayer_mode:
            if multiplayer_selection_step == 1:
                draw_text_with_rect("Player 1: Select Your Skin (Use A/D and Enter)", FONT, BLUE, WIN, WIDTH // 2, 100)
            else:  # step 2
                draw_text_with_rect("Player 2: Select Your Skin (Use A/D and Enter)", FONT, BLUE, WIN, WIDTH // 2, 100)
        else:
            draw_text_with_rect("Select Character Skin (Use A/D and Enter)", FONT, BLUE, WIN, WIDTH // 2, 100)
        
        # Get all available skins (including locked ones)
        unlocked = player_data.get("unlocked_skins", ["default.png"])
        player_level = player_data.get("level", 1)
        
        # Draw all skins
        for i, skin_name in enumerate(all_skins):
            skin_image = player_skins.get(skin_name)
            if skin_image:
                x = 150 + i * 150
                y = HEIGHT // 2
                
                # Check if skin is unlocked
                is_unlocked = skin_name in unlocked
                required_level = None
                for level, skin in SKIN_UNLOCKS.items():
                    if skin == skin_name:
                        required_level = level
                        break
                
                # Draw skin
                if is_unlocked:
                    # Normal skin
                    WIN.blit(skin_image, (x, y))
                    
                    # Draw selection borders
                    if multiplayer_mode:
                        if i == selected_skin_index:
                            # Current selection - gold border
                            pygame.draw.rect(WIN, GOLD, (x - 10, y - 10, player_size + 20, player_size + 20), 4)
                        if player1_selected_skin == skin_name:
                            # Player 1 selection - blue border
                            pygame.draw.rect(WIN, BLUE, (x - 15, y - 15, player_size + 30, player_size + 30), 3)
                        if player2_selected_skin == skin_name:
                            # Player 2 selection - red border
                            pygame.draw.rect(WIN, RED, (x - 15, y - 15, player_size + 30, player_size + 30), 3)
                    else:
                        # Single player - just gold border for current selection
                        if i == selected_skin_index:
                            pygame.draw.rect(WIN, GOLD, (x - 10, y - 10, player_size + 20, player_size + 20), 4)
                else:
                    # Locked skin - draw with dark overlay
                    dark_surface = pygame.Surface((player_size, player_size))
                    dark_surface.set_alpha(128)
                    dark_surface.fill((0, 0, 0))
                    WIN.blit(skin_image, (x, y))
                    WIN.blit(dark_surface, (x, y))
                    
                    # Draw lock icon or level requirement
                    if required_level:
                        lock_text = f"Lvl {required_level}"
                        lock_surface = TINY_FONT.render(lock_text, True, RED)
                        lock_rect = lock_surface.get_rect(center=(x + player_size//2, y + player_size + 15))
                        WIN.blit(lock_surface, lock_rect)
        
        # Show current selection info
        current_skin = all_skins[selected_skin_index]
        if current_skin in unlocked:
            if multiplayer_mode:
                if multiplayer_selection_step == 1:
                    draw_text_with_rect(f"Player 1: {current_skin.replace('.png', '').replace('_', ' ').title()}", SMALL_FONT, BLUE, WIN, WIDTH // 2, HEIGHT - 100)
                else:
                    draw_text_with_rect(f"Player 2: {current_skin.replace('.png', '').replace('_', ' ').title()}", SMALL_FONT, RED, WIN, WIDTH // 2, HEIGHT - 100)
            else:
                draw_text_with_rect(f"Selected: {current_skin.replace('.png', '').replace('_', ' ').title()}", SMALL_FONT, WHITE, WIN, WIDTH // 2, HEIGHT - 100)
        else:
            draw_text_with_rect(f"Locked: {current_skin.replace('.png', '').replace('_', ' ').title()}", SMALL_FONT, RED, WIN, WIDTH // 2, HEIGHT - 100)
        
        # Show player selections in multiplayer
        if multiplayer_mode and (player1_selected_skin or player2_selected_skin):
            selection_text = ""
            if player1_selected_skin:
                selection_text += f"P1: {player1_selected_skin.replace('.png', '').replace('_', ' ').title()}"
            if player2_selected_skin:
                if selection_text:
                    selection_text += " | "
                selection_text += f"P2: {player2_selected_skin.replace('.png', '').replace('_', ' ').title()}"
            draw_text_with_rect(selection_text, TINY_FONT, WHITE, WIN, WIDTH // 2, HEIGHT - 60)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
