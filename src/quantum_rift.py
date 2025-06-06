#----------------------------------------------------------#
# Name: Quantum Rift
# Purpose: A 2D indie game designed to keep a player mesme-
#          rised through its creative aesthetics and features.
# Author: Ashley Beebakee (https://github.com/OmniAshley)
# Date Created: 01/06/2025
# Last Updated: 05/06/2025
# Python Version: 3.10.6
#----------------------------------------------------------#

# Importing necessary libraries
import pygame
import sys
import os

class QuantumRiftGame:
    """Main class for the Quantum Rift game."""
    def __init__(self, width=800, height=600):
        # Initialize Pygame and game window
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Quantum Rift")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load background image
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bg_path = os.path.join(base_dir, "assets", "backgrounds", "background.png")
        bg_path = os.path.normpath(bg_path)
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        else:
            self.background = None
            print(f"Background image not found at {bg_path}")

        # Animation info: state: (folder, filename, sheet_w, sheet_h, num_frames, frame_w, frame_h)
        self.anim_info = {
            "idle":   ("idle",   "idle.png",   256, 80,  4,  64, 80),
            "run":    ("run",    "run.png",    640, 80,  8,  80, 80),
            "attack": ("attack", "attack.png", 768, 80,  8,  96, 80),
            "jump":   ("jump",   "jump.png",   960, 64, 15,  64, 64),
            "dead":   ("dead",   "dead.png",   640, 64,  8,  80, 64),
        }
        self.animations = {}
        self.load_animations(base_dir)

        self.player_state = "idle"
        self.player_frame = 0
        self.player_anim_timer = 0
        self.player_anim_speed = 0.15  # Adjust for animation speed
        self.player_facing_right = True  # Track direction

        # Player position
        self.player_x = self.width // 2 - 32
        self.ground_y = self.height - 100
        self.player_y = self.ground_y

        # Jump physics
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10

    def load_animations(self, base_dir):
        for state, (folder, filename, sheet_w, sheet_h, num_frames, frame_w, frame_h) in self.anim_info.items():
            frames = []
            sheet_path = os.path.join(base_dir, "assets", "characters", folder, filename)
            sheet_path = os.path.normpath(sheet_path)
            if os.path.exists(sheet_path):
                sheet = pygame.image.load(sheet_path).convert_alpha()
                for i in range(num_frames):
                    frame = sheet.subsurface((i * frame_w, 0, frame_w, frame_h))
                    frames.append(frame)
            else:
                print(f"Animation spritesheet not found: {sheet_path}")
            self.animations[state] = frames

    def run(self):
        # Main game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            prev_state = self.player_state

            # Movement logic
            if keys[pygame.K_j]:
                self.player_state = "attack"
            elif self.is_jumping:
                self.player_state = "jump"
            elif keys[pygame.K_SPACE] and not self.is_jumping:
                self.is_jumping = True
                self.jump_velocity = self.jump_strength
                self.player_state = "jump"
            elif keys[pygame.K_a] or keys[pygame.K_d]:
                self.player_state = "run"
            else:
                self.player_state = "idle"

            # Allow horizontal movement at all times
            if keys[pygame.K_a]:
                self.player_x -= 4
                self.player_facing_right = False
            if keys[pygame.K_d]:
                self.player_x += 4
                self.player_facing_right = True

            # Jump physics update
            if self.is_jumping:
                self.player_y += self.jump_velocity
                self.jump_velocity += self.gravity
                if self.player_y >= self.ground_y:
                    self.player_y = self.ground_y
                    self.is_jumping = False

            # Reset frame if state changed
            if self.player_state != prev_state:
                self.player_frame = 0
                self.player_anim_timer = 0

            # Animation frame update
            frames = self.animations.get(self.player_state, [])
            if frames:
                self.player_anim_timer += self.player_anim_speed
                if self.player_anim_timer >= 1:
                    self.player_anim_timer = 0
                    self.player_frame = (self.player_frame + 1) % len(frames)
                self.player_frame = self.player_frame % len(frames)
                current_frame = frames[self.player_frame]
            else:
                current_frame = None

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((10, 10, 30))  # Fallback color

            # Draw player, flip if facing left
            if current_frame:
                if self.player_facing_right:
                    self.screen.blit(current_frame, (self.player_x, self.player_y))
                else:
                    flipped = pygame.transform.flip(current_frame, True, False)
                    self.screen.blit(flipped, (self.player_x, self.player_y))

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()

def main():
    game = QuantumRiftGame()
    game.run()

if __name__ == "__main__":
    main()