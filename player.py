import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Animations
        self.animations = {
            "idle": [],
            "walk": [],
            "jump": [],
            "hit": []
        }

        self.load_animations()

        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.animations[self.state][self.frame_index]
        base_rect = self.image.get_rect(topleft=(x, y))

        # collider awal
        self.rect = base_rect.inflate(-24, -6)
        self.rect.y -= 3

        # ==== Tambah lebar ke kanan (sisi kiri tetap) ====
        old_left = self.rect.left
        self.rect.width += 10
        self.rect.left = old_left

       # ==== GESER SISI KIRI KE KANAN (SISI KANAN HARUS TETAP) ====
        SHIFT = 20              # jumlah geseran yang kamu mau
        old_right = self.rect.right
        self.rect.left += SHIFT
        self.rect.right = old_right


        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.on_ground = False

    def load_folder(self, path):
        frames = []
        for file in sorted(os.listdir(path)):
            if file.endswith('.png'):
                img = pygame.image.load(path + file).convert_alpha()
                frames.append(img)
        return frames

    def load_animations(self):
        base = "Assets/Player/"
        self.animations["idle"] = self.load_folder(base + "idle/")
        self.animations["walk"] = self.load_folder(base + "walk/")
        self.animations["jump"] = self.load_folder(base + "jump/")
        self.animations["hit"]  = self.load_folder(base + "hit/")

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def move(self, dt, tiles):
        keys = pygame.key.get_pressed()

        # Horizontal Movement
        self.vel_x = 0        
        if keys[pygame.K_LEFT]:
            self.vel_x = -5
        if keys[pygame.K_RIGHT]:
            self.vel_x = 5

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -12
            self.on_ground = False

        # Move X
        self.rect.x += self.vel_x

        if self.vel_x == 0:
            self.rect.x += 0.1

        # Collision X
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.vel_x > 0:
                    self.rect.right = t.rect.left
                elif self.vel_x < 0:
                    self.rect.left = t.rect.right

        # Move Y
        self.apply_gravity()
        self.on_ground = False

        # Collision Y
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.vel_y > 0:
                    self.rect.bottom = t.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = t.rect.bottom
                    self.vel_y = 0

    def update_state(self):
        if not self.on_ground:
            self.state = "jump"
        elif self.vel_x != 0:
            self.state = "walk"
        else:
            self.state = "idle"

    def animate(self):
        frames = self.animations[self.state]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]

    def update(self, dt, tiles):
        self.move(dt, tiles)
        self.update_state()
        self.animate()
