import pygame

class Bee(pygame.sprite.Sprite):
    def __init__(self, x, y, frame1, frame2):
        super().__init__()
        
        self.frames = [frame1, frame2]
        self.frame_index = 0
        self.anim_speed = 200      # ms per frame
        self.anim_timer = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # movement
        self.direction = 1
        self.speed = 1.5
        self.max_offset = 50
        self.start_x = x

    def update(self, dt):
        # animate
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % 2
            self.image = self.frames[self.frame_index]

        # move left-right
        self.rect.x += self.direction * self.speed

        if abs(self.rect.x - self.start_x) >= self.max_offset:
            self.direction *= -1   # balik arah
