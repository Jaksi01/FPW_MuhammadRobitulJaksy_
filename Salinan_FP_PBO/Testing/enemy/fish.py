import pygame
import random

TILE_SIZE = 64

class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, image_up, image_down):
        super().__init__()

        self.img_up = image_up
        self.img_down = image_down
        self.image = self.img_up

        self.rect = self.image.get_rect(topleft=(x, y))

        self.start_y = y
        self.range_pixels = 3 * TILE_SIZE
        self.speed = 150
        self.direction = -1

        # offset acak biar gak serempak
        self.time_offset = random.uniform(0, 1.5)

        self.empty_image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    def update(self, dt, solid_tiles):
        # --- Pergerakan tapi diberi offset ---
        movement = self.direction * self.speed * (dt / 1000)

        # tambahkan sedikit jeda per ikan
        movement *= (1 + self.time_offset)

        self.rect.y += movement

        if self.rect.y <= self.start_y - self.range_pixels:
            self.rect.y = self.start_y - self.range_pixels
            self.direction = 1

        if self.rect.y >= self.start_y + self.range_pixels:
            self.rect.y = self.start_y + self.range_pixels
            self.direction = -1

        # animasi naik / turun
        if self.direction == -1:
            self.image = self.img_up
        else:
            self.image = self.img_down

        # cek air
        self.hide_if_inside_water(solid_tiles)

    def hide_if_inside_water(self, solid_tiles):
        inside_water = False

        for tile in solid_tiles:
            if tile.rect.colliderect(self.rect):

                if hasattr(tile, "image") and tile.image is not None:
                    pixel = tile.image.get_at((0, 0))

                    if pixel.b > 150:
                        inside_water = True
                        break

        if inside_water:
            self.image = self.empty_image
        else:
            self.image = self.img_up if self.direction == -1 else self.img_down
