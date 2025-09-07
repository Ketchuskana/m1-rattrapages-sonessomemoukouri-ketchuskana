import pygame
import random

class Fuel:
    def __init__(self, x_min, x_max, speed, image):
        """
        x_min, x_max : zone horizontale de spawn
        speed : vitesse de descente
        image : image du bonus
        """
        self.img = image
        self.rect = pygame.Rect(
            random.randint(x_min, x_max - self.img.get_width()),
            -self.img.get_height(),
            self.img.get_width(),
            self.img.get_height()
        )
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.img, self.rect)
