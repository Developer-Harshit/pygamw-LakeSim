# Basic Screen

import pygame
import sys

print("Starting Game")

from scripts.consts import BLUE, RED, BG_COLOR, FPS
from scripts.spring import Spring, Blob, Lake
from scripts.util import draw_circle, get_curve


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Water")

        self.screen = pygame.display.set_mode((960, 640), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()

        ks1 = 0.006
        ks2 = 0.005
        kd1 = 0.045
        kd2 = 0.032
        spacing = 50

        # ks1 = 0.001
        # ks2 = 0.004
        # kd1 = 0.01
        # kd2 = 0.07
        # spacing = 10

        self.lake = Lake(
            (50, 200),
            (self.screen.get_width() - 50, 200),
            self.screen.get_height() - 100,
            spacing,
            ks1,
            ks2,
            kd1,
            kd2,
        )
        self.blob = Blob((0, 0), 10, RED, True)
        self.left_click = False

    def run(self):
        running = True
        while running:
            WIDTH = self.screen.get_width()
            HEIGHT = self.screen.get_height()

            # For Background ------------------------------------------------------|
            self.screen.fill(BG_COLOR)

            # Mouse ---------------------------------------------------------------|
            self.blob.pos = list(pygame.mouse.get_pos())
            self.blob.render(self.screen)

            # For Lake ------------------------------------------------------------|
            if self.left_click:
                self.lake.pull_blob()
            else:
                self.lake.update()

            self.lake.render(self.screen)

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                # Quit ------------------------------------------------------------|
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left Click
                        self.left_click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left Click
                        self.left_click = False

                    pass
            # Rendering Screen ----------------------------------------------------|
            self.screen.blit(
                pygame.transform.scale(self.screen, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
print("Game Over")
