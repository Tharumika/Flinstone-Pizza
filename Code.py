import pygame
import cv2
import numpy as np
import time
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bedrock Pizza')

video_playing = True
image_displayed = False
image_display_start_time = 0  # Initialize the timer


# Load jump sound
jump_sound = pygame.mixer.Sound('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/sounds/jump.wav')
losing_sound = pygame.mixer.Sound('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/sounds/losing.wav')

# Load background music
background_music = 'C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/sounds/playing music.mp3'

# Define cloud properties
clouds = [
    {"x": 100, "y": 50, "speed": 1},  # Cloud 1
    {"x": 300, "y": 100, "speed": 0.8},  # Cloud 2
    {"x": 500, "y": 70, "speed": 1.2},  # Cloud 3
]

# Load cloud image (make sure to adjust the image size to 156x55 px if needed)
cloud_image = pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/clouds/1.png').convert_alpha()

# Play the background music
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play indefinitely (-1 for looping)

# Set up the game clock and frames per second
clock = pygame.time.Clock()
FPS = 60

# Define the variables
GRAVITY = 0.75
GROUND_LEVEL = 525

# Set the cloud's width and height
cloud_width = 156
cloud_height = 55

# Player action variables
moving_left = False
moving_right = False

# Define some colors
BG = (0, 0, 150)  # Background color
RED = (255, 0, 0)  # Red color

# Load background images for levels
levels_data = {
    1: pygame.transform.scale(pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/background/level 1.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    2: pygame.transform.scale(pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/background/level 2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    3: pygame.transform.scale(pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/background/level 3.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    4: pygame.transform.scale(pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/background/level 4.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    5: pygame.transform.scale(pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/background/level 5.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    6: pygame.transform.scale(pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/background/level 6.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    7: pygame.transform.scale(pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/background/level 7.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    8: pygame.transform.scale(pygame.image.load('C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/background/level 8.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
}

# Variable to track the current level
current_level = 1

# Load the rock image
rock_img = pygame.image.load(r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\img\Obstacles\rock.png")
rock_img = pygame.transform.scale(rock_img, (50, 50))  # Scale the rock image to appropriate size
rock_mask = pygame.mask.from_surface(rock_img)

# Load the shell image
shell_img = pygame.image.load(r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\img\Obstacles\shell.png")
shell_img = pygame.transform.scale(shell_img, (60, 60))  # Scale the shell image to appropriate size
shell_mask = pygame.mask.from_surface(shell_img)

# Load the pitfall image
pitfall_img = pygame.image.load(r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\img\Obstacles\pitfall.png")
pitfall_img = pygame.transform.scale(pitfall_img, (200, 400))  # Scale the pitfall image to appropriate size
pitfall_mask = pygame.mask.from_surface(pitfall_img)

# Load the log trap image
log_trap_img = pygame.image.load(r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\img\Obstacles\log_trap.png")
log_trap_img = pygame.transform.scale(log_trap_img, (150, 100))  # Scale the log trap image
log_trap_rect = pygame.Rect(264, 447, 150, 100)  # Position of the log trap
log_trap_mask = pygame.mask.from_surface(log_trap_img)

# Load the cat trap image
cat_trap_img = pygame.image.load(r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\img\Obstacles\cat_trap.png")
cat_trap_img = pygame.transform.scale(cat_trap_img, (150, 50))  # Scale the cat trap image
cat_trap_rect = pygame.Rect(917, 466, 150, 50)  # Position of the cat trap
cat_trap_mask = pygame.mask.from_surface(cat_trap_img)

# Load the water pitfall image for level 7
water_pitfall_img = pygame.image.load(r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\img\Obstacles\water_pitfall.png")
water_pitfall_img = pygame.transform.scale(water_pitfall_img, (300, 271))  # Scale the image to the given dimensions
water_pitfall_rects = [
    pygame.Rect(613, 449, 300, 271),  # First water pitfall at (613, 449)
    pygame.Rect(152, 449, 300, 271)   # Second water pitfall at (152, 449)
]
water_pitfall_mask = pygame.mask.from_surface(water_pitfall_img)

# Load the Barney image for level 8
bar_trap_img = pygame.image.load(r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\img\sprites\Barney\barney.png")
bar_trap_img = pygame.transform.scale(bar_trap_img, (250, 250))  # Adjust size as needed
bar_trap_mask = pygame.mask.from_surface(bar_trap_img)
bar_trap_rect = pygame.Rect(950, 300, 250, 250)  # Position of Barney in level 8 (adjust coordinates as needed)

# Define rock positions and their Rect objects for level 2
level_2_rocks = [
    pygame.Rect(818, 491, 50, 50),  # Rock at (818, 491) with a size of 50x50
    pygame.Rect(585, 487, 50, 50)  # Rock at (585, 487) with a size of 50x50
]

# Define shell positions and their Rect objects for level 3
level_3_shells = [
    pygame.Rect(406, 450, 50, 50),  # Shell at (406, 450) with a size of 50x50
    pygame.Rect(627, 453, 50, 50),  # Shell at (627, 453) with a size of 50x50
    pygame.Rect(834, 450, 50, 50),  # Shell at (834, 450) with a size of 50x50
]

# Define pitfall positions and their Rect objects for level 4
level_4_pitfalls = [
    pygame.Rect(151, 435, 50, 50),  # Pitfall at (151, 455-20) with a size of 50x50
    pygame.Rect(670, 435, 50, 50)   # Pitfall at (670, 455-20) with a size of 50x50
]

# Function to draw rocks (only for level 2)
def draw_rocks():
    if current_level == 2:  # Draw rocks only in level 2
        for rock_rect in level_2_rocks:
            screen.blit(rock_img, (rock_rect.x, rock_rect.y))

# Function to draw shells (only for level 3)
def draw_shells():
    if current_level == 3:  # Draw shells only in level 3
        for shell_rect in level_3_shells:
            screen.blit(shell_img, (shell_rect.x, shell_rect.y))

# Function to draw pitfalls (only for level 4)
def draw_pitfalls():
    if current_level == 4:  # Draw pitfalls only in level 4
        for pitfall_rect in level_4_pitfalls:
            screen.blit(pitfall_img, (pitfall_rect.x, pitfall_rect.y))

# Function to draw water pitfalls (only for level 7)
def draw_water_pitfalls():
    if current_level == 7:  # Draw water pitfall only in level 7
        for water_pitfall_rect in water_pitfall_rects:
            screen.blit(water_pitfall_img, (water_pitfall_rect.x, water_pitfall_rect.y))

# Function to draw the log trap (level 6)
def draw_log_trap():
    screen.blit(log_trap_img, (log_trap_rect.x, log_trap_rect.y))

# Function to draw the cat trap (level 6)
def draw_cat_trap():
    screen.blit(cat_trap_img, (cat_trap_rect.x, cat_trap_rect.y))

# Function to draw Barney (only for level 8)
def draw_barney():
    if current_level == 8:
        screen.blit(bar_trap_img, (bar_trap_rect.x, bar_trap_rect.y))

# Function to draw the background based on the current level
def draw_bg():
    if current_level in levels_data:
        screen.blit(levels_data[current_level], (0, 0))
        if current_level == 2:
            draw_rocks()  # Draw rocks for level 2
        if current_level == 3:
            draw_shells()  # Draw shells for level 3
        if current_level == 4:
            draw_pitfalls()  # Draw pitfalls for level 4
        if current_level == 6:
            draw_log_trap()  # Draw log trap for level 6
            draw_cat_trap()  # Draw cat trap for level 6
        if current_level == 7:
            draw_water_pitfalls()  # Draw water pitfalls for level 7
        if current_level == 8:
            draw_barney()  # Draw Barney for level 8
    else:
        print("Level not found!")
        pygame.quit()
        exit()

# Function to handle level transitions
def next_level():
    global current_level
    current_level += 1
    if current_level > len(levels_data):  # No more levels
        print("Congratulations! You completed the game!")
        pygame.quit()
        exit()
    # Reset player position
    player.rect.x = 0
    player.rect.y = GROUND_LEVEL - player.rect.height
    player.vel_y = 0
    player.in_air = False

# Class to create a dino
class Dino(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        self.load_images()

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        path = 'C:/Users/Rasika.DESKTOP-C0CCE55/Desktop/Flinstone Pizza/img/sprites/dino/'
        idle_image = pygame.image.load(f'{path}2.png').convert_alpha()
        self.animation_list.append([pygame.transform.scale(idle_image, (int(idle_image.get_width() * 0.14), int(idle_image.get_height() * 0.14)))]) 

        run_left_images = []
        for i in range(1, 2):
            img = pygame.image.load(f'{path}{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * 0.14), int(img.get_height() * 0.14)))
            run_left_images.append(img)
        self.animation_list.append(run_left_images)

        run_right_images = []
        for i in range(3, 4):
            img = pygame.image.load(f'{path}{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * 0.14), int(img.get_height() * 0.14)))
            run_right_images.append(img)
        self.animation_list.append(run_right_images)
    
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            self.action = 1
        elif moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
            self.action = 2
        else:
            self.action = 0

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.y >= GROUND_LEVEL - self.rect.height:
            self.rect.y = GROUND_LEVEL - self.rect.height
            self.vel_y = 0
            self.in_air = False
        else:
            self.in_air = True

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    # Function to display "Game Completed" screen
    def game_completed_screen():
        font = pygame.font.SysFont(None, 72)
        text = font.render("Congratulations! You Completed the Game!", True, 255, 255, 0)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)  # Display for 3 seconds
        pygame.quit()
        exit()

# OpenCV video setup
video_path = r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\start_vid\1.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video file.")
    pygame.quit()
    exit()
playback_speed = 0.05  

# Load the image to display after video playback
#image_path = r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\start_vid\gaaa.jpg"
image_path = r"C:\Users\Rasika.DESKTOP-C0CCE55\Desktop\Flinstone Pizza\start_vid\gaaa.jpg"
post_video_image = pygame.image.load(image_path)
# Time to display the image (in seconds)
image_display_duration = 3  # Adjust this to your desired duration

# Create the player object
player = Dino('player', 200, GROUND_LEVEL - 40, 3, 5)

# Function to display "Game Completed" screen
def game_completed_screen():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Congratulations! You Completed the Game!", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    
    bg_rect = pygame.Rect(text_rect)
    bg_rect.inflate_ip(30,30)
    pygame.draw.rect(screen,(0,0,255),bg_rect)
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)  # Display for 3 seconds
    pygame.quit()
    exit()

# Main game loop
run = True

while run:
    clock.tick(FPS)

    # Read the next frame from the video
    if video_playing:
        # Read the next frame from the video
        ret, frame = cap.read()
        if not ret:
            video_playing = False  # End video playback
        else:
            # Convert the frame to a Pygame surface and display it
            frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
            screen.blit(frame_surface, (0, 0))
            pygame.display.update()
            
            # Slow down playback
            pygame.time.delay(int(1000 * playback_speed))  # Delay in milliseconds
    elif not image_displayed:
            # Show the image for a specific duration
            screen.blit(pygame.transform.scale(post_video_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            if image_display_start_time == 0:  # Record the time when the image is first displayed
                image_display_start_time = time.time()
            elif time.time() - image_display_start_time > image_display_duration:
                image_displayed = True  # End image display and move to gameplay
    else:
        # Once the image ends, proceed to gameplay
        draw_bg()
    
    # Update cloud positions
    for cloud in clouds:
        cloud["x"] += cloud["speed"]  # Move the cloud to the right
        if cloud["x"] > SCREEN_WIDTH:  # If the cloud is off-screen
            cloud["x"] = -cloud_width  # Reset to the left side (outside of screen width)

    draw_bg()
    for cloud in clouds:
        screen.blit(cloud_image, (cloud["x"], cloud["y"]))
    
    # Handle events (key presses, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP) and not player.in_air:  # Allow jump only if the dino is not in the air
                player.vel_y = -27  # Adjust jump strength
                player.in_air = True
                jump_sound.play()  # Play jump sound

    # Update player animation and movement
    player.update_animation()
    player.move(moving_left, moving_right)

    # Check for collisions with log trap in level 6
    if current_level == 6:
        player_mask = player.get_mask()
        log_offset = (log_trap_rect.x - player.rect.x, log_trap_rect.y - player.rect.y)
        if player_mask.overlap(log_trap_mask, log_offset):
            print("Dino touched the log trap! Restarting Level 6...")
            losing_sound.play()  # Play losing sound
            player.rect.x = 0  # Reset to starting position
            player.rect.y = GROUND_LEVEL - player.rect.height
            player.vel_y = 0
            player.in_air = False

        # Check for collisions with cat trap in level 6
        cat_offset = (cat_trap_rect.x - player.rect.x, cat_trap_rect.y - player.rect.y)
        if player_mask.overlap(cat_trap_mask, cat_offset):
            print("Dino touched the cat trap! Restarting Level 6...")
            losing_sound.play()  # Play losing sound
            player.rect.x = 0  # Reset to starting position
            player.rect.y = GROUND_LEVEL - player.rect.height
            player.vel_y = 0
            player.in_air = False

    # Check for collisions between the player and rocks (only in level 2)
    if current_level == 2:
        player_mask = player.get_mask()
        for rock_rect in level_2_rocks:
            offset = (rock_rect.x - player.rect.x, rock_rect.y - player.rect.y)
            if player_mask.overlap(rock_mask, offset):
                # Restart level 2
                print("Restarting Level 2!")
                losing_sound.play()  # Play losing sound
                player.rect.x = 0  # Reset the player position to the starting point
                player.rect.y = GROUND_LEVEL - player.rect.height
                player.vel_y = 0
                player.in_air = False
                break  # No need to check further collisions

    # Check for collisions with shells in level 3
    if current_level == 3:
        player_mask = player.get_mask()
        for shell_rect in level_3_shells:
            offset = (shell_rect.x - player.rect.x, shell_rect.y - player.rect.y)
            if player_mask.overlap(shell_mask, offset):
                # Handle shell collision (e.g., restart level or apply effects)
                print("Dino touched a shell! Restarting Level 3...")
                losing_sound.play()  # Play losing sound
                player.rect.x = 0  # Reset to starting position
                player.rect.y = GROUND_LEVEL - player.rect.height
                player.vel_y = 0
                player.in_air = False
                break

    # Check for collisions with pitfalls in level 4
    if current_level == 4:
        player_mask = player.get_mask()
        for pitfall_rect in level_4_pitfalls:
            offset = (pitfall_rect.x - player.rect.x, pitfall_rect.y - player.rect.y)
            if player_mask.overlap(pitfall_mask, offset):
                print("Dino fell into a pitfall! Restarting Level 4...")
                losing_sound.play()  # Play losing sound
                # Reset player position to the starting point of level 4
                player.rect.x = 0
                player.rect.y = GROUND_LEVEL - player.rect.height
                player.vel_y = 0
                player.in_air = False
                break  # Stop checking other pitfalls after a collision

    # Check for collisions with water pitfalls in level 7
    if current_level == 7:
        player_mask = player.get_mask()
        for water_pitfall_rect in water_pitfall_rects:
            offset = (water_pitfall_rect.x - player.rect.x, water_pitfall_rect.y - player.rect.y)
            if player_mask.overlap(water_pitfall_mask, offset):
                print("Dino fell into a water pitfall! Restarting Level 7...")
                losing_sound.play()  # Play losing sound
                player.rect.x = 0  # Reset to starting position
                player.rect.y = GROUND_LEVEL - player.rect.height
                player.vel_y = 0
                player.in_air = False
                break  # Stop checking other water pitfalls after a collision

    # Check for collision with Barney in level 8
    if current_level == 8:
        player_mask = player.get_mask()
        bar_offset = (bar_trap_rect.x - player.rect.x, bar_trap_rect.y - player.rect.y)
        if player_mask.overlap(bar_trap_mask, bar_offset):
            print("Dino touched Barney! Game Completed!")
            game_completed_screen()

    # Move to the next level if the player goes off the screen
    if player.rect.x > SCREEN_WIDTH:
        next_level()

    # Draw the player
    player.draw()

    pygame.display.update()

pygame.quit()
