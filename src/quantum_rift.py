#----------------------------------------------------------#
# Name: Quantum Rift
# Purpose: A 2D indie game designed to keep a player mesme-
#          rised through its creative aesthetics and features.
# Author: Ashley Beebakee (https://github.com/OmniAshley)
# Date Created: 01/06/2025
# Last Updated: 20/06/2025
# Python Version: 3.10.6
# Design: Tiled Map Editor, Pygame as Game Engine
#----------------------------------------------------------#

# Importing necessary libraries
from pytmx.util_pygame import load_pygame
import pygame
import sys
import os

class QuantumRiftGame:
    """Main class for the Quantum Rift game."""
    def load_tiled_map(self, map_name):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        map_path = os.path.join(base_dir, "tiled", f"{map_name}.tmx")
        return load_pygame(map_path)

    def draw_tiled_layers(self, tmx_data, layers):
        for layer_name in layers:
            layer = tmx_data.get_layer_by_name(layer_name)
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    self.screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

    def __init__(self, width=800, height=640):
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
        self.ground_y = self.height - 128
        self.player_y = self.ground_y

        # Jump physics
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.jump_anim_timer = 0
        self.jump_anim_duration = 0  # Will be set on jump start

        # Attack state
        self.attack_variation = 1  # 1 or 2
        self.attack_active = False
        self.attack_frame_start = 0
        self.attack_frame_end = 4
        self.attack_frame_count = 0

        # Load Tiled map
        self.tmx_data = self.load_tiled_map("intro_map")
        print("Available layers:", [layer.name for layer in self.tmx_data.layers])
        self.tiled_layers = ["Tile Layer 1", "Tile Layer 2"]

    def show_main_menu(self):
        font = pygame.font.SysFont("Arial", 48)
        small_font = pygame.font.SysFont("Arial", 28)
        menu_active = True
        while menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu_active = False

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((10, 10, 30))

            title = font.render("Quantum Rift", True, (200, 220, 255))
            prompt = small_font.render("Press ENTER to Start", True, (180, 180, 200))
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 3))
            self.screen.blit(prompt, (self.width // 2 - prompt.get_width() // 2, self.height // 2))
            pygame.display.flip()
            self.clock.tick(60)

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
        self.show_main_menu()
        # Main game loop
        while self.running:
            attack_key_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    attack_key_pressed = True

            keys = pygame.key.get_pressed()
            prev_state = self.player_state

            # Attack logic
            # Start attack if not active and K is held down
            if not self.attack_active and keys[pygame.K_k]:
                self.player_state = "attack"
                self.attack_active = True
                if self.attack_variation == 1:
                    self.attack_frame_start = 0
                    self.attack_frame_end = 4
                else:
                    self.attack_frame_start = 4
                    self.attack_frame_end = 8
                self.player_frame = self.attack_frame_start
                self.attack_frame_count = self.attack_frame_start

            # If attack is active, keep playing attack frames
            if self.attack_active:
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
                self.jump_anim_timer += 1  # Count frames during jump
                if self.player_y >= self.ground_y:
                    self.player_y = self.ground_y
                    self.is_jumping = False
                    self.jump_anim_timer = 0  # Reset on landing

            # Reset frame if state changed (except for attack)
            if self.player_state != prev_state and self.player_state != "attack":
                self.player_frame = 0
                self.player_anim_timer = 0

            # Animation frame update
            frames = self.animations.get(self.player_state, [])
            if frames:
                if self.player_state == "jump" and (self.is_jumping or self.jump_anim_timer > 0):
                    # --- Synchronize jump animation with jump duration ---
                    if self.jump_anim_timer == 1:  # Just started jump
                        # Estimate jump duration in frames (time to go up and down)
                        # t = 2 * abs(v0) / g
                        self.jump_anim_duration = int(abs(2 * self.jump_strength / self.gravity))
                    progress = self.jump_anim_timer / max(1, self.jump_anim_duration)
                    progress = min(1, progress)
                    frame_idx = int(progress * (len(frames) - 1))
                    self.player_frame = frame_idx
                    current_frame = frames[self.player_frame]
                else:
                    # ...existing code for other states...
                    self.player_anim_timer += self.player_anim_speed
                    if self.player_anim_timer >= 1:
                        self.player_anim_timer = 0
                        if self.player_state == "attack" and self.attack_active:
                            self.player_frame += 1
                            if self.player_frame >= self.attack_frame_end:
                                self.attack_active = False
                                self.attack_variation = 2 if self.attack_variation == 1 else 1
                                if keys[pygame.K_k]:
                                    self.player_state = "attack"
                                    self.attack_active = True
                                    if self.attack_variation == 1:
                                        self.attack_frame_start = 0
                                        self.attack_frame_end = 4
                                    else:
                                        self.attack_frame_start = 4
                                        self.attack_frame_end = 8
                                    self.player_frame = self.attack_frame_start
                                    self.attack_frame_count = self.attack_frame_start
                                else:
                                    self.player_state = "idle"
                                    self.player_frame = 0
                        else:
                            self.player_frame = (self.player_frame + 1) % len(frames)
                    if self.player_state == "attack" and self.attack_active:
                        self.player_frame = max(self.attack_frame_start, min(self.player_frame, self.attack_frame_end - 1))
                    else:
                        self.player_frame = self.player_frame % len(frames)
                    current_frame = frames[self.player_frame]
            else:
                current_frame = None

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((10, 10, 30))  # Fallback color
            
            # Draw Tiled map layers before everything else
            self.draw_tiled_layers(self.tmx_data, self.tiled_layers)

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