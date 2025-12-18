# Enemies/enemy_base.py

import pygame

class EnemyBase:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # digunakan untuk collision player → enemy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.visible = True   # fish menggunakan ini untuk hide saat di air

    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
