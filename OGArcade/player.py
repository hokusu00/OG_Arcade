import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, image=None):
        super().__init__()
        self.width = 100
        self.height = 30
        self.speed = 8

        if image:
            self.image = pygame.transform.scale(image, (self.width, self.height))
        else:
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 230, 230), (0, 0, self.width, self.height), border_radius=6)
            pygame.draw.rect(self.image, (20, 40, 60), (4, 4, self.width - 8, self.height - 8), border_radius=4)

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 25

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.move_left()
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.move_right()

    def reset_position(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 25