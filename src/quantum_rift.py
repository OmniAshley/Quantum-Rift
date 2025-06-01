#----------------------------------------------------------#
# Name: Quantum Rift
# Purpose: A 2D indie game designed to keep a player mesme-
#          rised through its creative aesthetics and features.
# Author: Ashley Beebakee (https://github.com/OmniAshley)
# Date Created: 01/06/2025
# Last Updated: 02/06/2025
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

    def run(self):
        # Main game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((10, 10, 30))  # Fallback color

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()

def main():
    game = QuantumRiftGame()
    game.run()

if __name__ == "__main__":
    main()