import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_manager import GameManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("OG Arcade Catcher")
    clock = pygame.time.Clock()

    manager = GameManager()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                keep_running = manager.handle_events(event)
                if not keep_running:
                    running = False

        manager.update()
        manager.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()