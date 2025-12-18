import pygame

class Worm(pygame.sprite.Sprite):
    def __init__(self, x, y, frame1, frame2):
        super().__init__()

        self.frames_right = [frame1, frame2]
        self.frames_left = [
            pygame.transform.flip(frame1, True, False),
            pygame.transform.flip(frame2, True, False)
        ]

        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 200

        self.image = self.frames_right[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 1
        self.direction = 1

        self.start_x = x
        self.max_range = 64  # 1 tile

    def update(self, dt, solid_tiles):
        # animasi
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % 2

        # arah animasi
        if self.direction == 1:
            self.image = self.frames_right[self.frame_index]
        else:
            self.image = self.frames_left[self.frame_index]

        # gerak
        self.rect.x += self.speed * self.direction

        # batas patrol
        if abs(self.rect.x - self.start_x) >= self.max_range:
            self.direction *= -1

        # kalau nabrak tile
        if pygame.sprite.spritecollide(self, solid_tiles, False):
            self.direction *= -1
            self.rect.x += self.direction * self.speed
