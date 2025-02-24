import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
SCALE = 2  # Zoom factor
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Rift")

# Colors
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)

# Clock for frame rate
clock = pygame.time.Clock()
FPS = 60

# Directory
user_dir = "C:/Users/zetra/OneDrive/Career and Prospects/Python Projects/Quantum-Rift/assets/freeknight_v1/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/"

# Load assets
background = pygame.image.load("background.png")  # Background image
idle_sheet = pygame.image.load(user_dir+"_Idle.png")
run_sheet = pygame.image.load(user_dir+"_Run.png")
jump_sheet = pygame.image.load(user_dir+"_Jump.png")
fall_sheet = pygame.image.load(user_dir+"_Fall.png")
turn_sheet = pygame.image.load(user_dir+"_TurnAround.png")

# Sprite sheet settings
SPRITE_WIDTH = 120  # Width of each frame
SPRITE_HEIGHT = 80  # Height of each frame
IDLE_FRAMES = 10
RUN_FRAMES = 10
JUMP_FRAMES = 3
FALL_FRAMES = 3
TURN_FRAMES = 3

def load_sprites(sheet, columns, width, height):
    """Extracts individual frames from a sprite sheet and scales them."""
    sprites = []
    for col in range(columns):
        frame = sheet.subsurface((col * width, 0, width, height))
        frame = pygame.transform.scale(frame, (width * SCALE, height * SCALE))  # Apply zoom
        sprites.append(frame)
    return sprites

# Load animations
idle_animation = load_sprites(idle_sheet, IDLE_FRAMES, SPRITE_WIDTH, SPRITE_HEIGHT)
run_animation = load_sprites(run_sheet, RUN_FRAMES, SPRITE_WIDTH, SPRITE_HEIGHT)
jump_animation = load_sprites(jump_sheet, JUMP_FRAMES, SPRITE_WIDTH, SPRITE_HEIGHT)
fall_animation = load_sprites(fall_sheet, FALL_FRAMES, SPRITE_WIDTH, SPRITE_HEIGHT)
turn_animation = load_sprites(turn_sheet, TURN_FRAMES, SPRITE_WIDTH, SPRITE_HEIGHT)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = idle_animation[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, HEIGHT - 150)
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_power = -12
        self.on_ground = False
        self.running = False
        self.frame_index = 0
        self.animation_speed = 0.15
        self.current_animation = idle_animation
        self.facing_right = True
        self.turning = False
        self.turn_complete = True  # Track if turn animation has completed

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False
        running = keys[K_LSHIFT]
        new_direction = None

        if keys[K_LEFT]:
            new_direction = False
            self.rect.x -= self.speed * (2 if running else 1)
            moving = True
        elif keys[K_RIGHT]:
            new_direction = True
            self.rect.x += self.speed * (2 if running else 1)
            moving = True
        
        # Turn animation logic
        if new_direction is not None and new_direction != self.facing_right:
            self.turning = True
            self.turn_complete = False
            self.frame_index = 0
            self.current_animation = turn_animation
            self.facing_right = new_direction
        
        # Ensure turn animation completes before switching to movement animations
        if self.turning:
            if self.frame_index >= len(turn_animation) - 1:
                self.turning = False
                self.turn_complete = True
                self.current_animation = run_animation if moving and running else idle_animation if not moving else run_animation
        else:
            # Set correct animations based on movement
            if moving:
                self.current_animation = run_animation if running else run_animation
            else:
                self.current_animation = idle_animation
        
        # Jump & Fall animations
        if keys[K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            self.current_animation = jump_animation
        
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.velocity_y = 0
            self.current_animation = idle_animation
        elif self.velocity_y < 0:
            self.current_animation = jump_animation
        elif self.velocity_y > 0 and not self.on_ground:
            self.current_animation = fall_animation
        
        # Animate player
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0
        self.image = self.current_animation[int(self.frame_index)]

# Create player
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    all_sprites.update()
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
