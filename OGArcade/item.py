import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ITEM_CONFIG

class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, speed, image=None):
        super().__init__()
        self.item_type = item_type
        self.config = ITEM_CONFIG[item_type]
        self.points = self.config["points"]
        self.is_hazard = self.config["is_hazard"]
        self.is_heal = self.config["is_heal"]
        self.penalize_miss = self.config["penalize_miss"]
        self.speed = speed
        self.radius = 18
        self.size = self.radius * 2

        if image:
            self.image = pygame.transform.scale(image, (self.size, self.size))
        else:
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            color = self.config["color"]
            if self.is_hazard:
                pygame.draw.rect(self.image, color, (2, 2, self.size - 4, self.size - 4), border_radius=4)
                pygame.draw.line(self.image, (255, 255, 255), (6, 6), (self.size - 6, self.size - 6), 3)
                pygame.draw.line(self.image, (255, 255, 255), (self.size - 6, 6), (6, self.size - 6), 3)
            elif self.is_heal:
                pygame.draw.polygon(self.image, color, [
                    (self.radius, 2), (self.size - 2, self.radius),
                    (self.radius, self.size - 2), (2, self.radius)
                ])
            else:
                pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius - 2)
                pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius - 6, 2)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, SCREEN_WIDTH - self.size - 20)
        self.rect.y = -self.size

    def update(self):
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT