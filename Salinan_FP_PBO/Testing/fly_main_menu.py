import pygame
class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y, frame1, frame2):
        super().__init__()

        self.frames = [frame1, frame2]
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 150

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # vertical bobbing movement
        self.start_y = y
        self.offset = 0
        self.speed = 0.05
        self.going_up = False

    def update(self, dt):
        # animate
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % 2
            self.image = self.frames[self.frame_index]

        # smooth up/down movement
        if self.going_up:
            self.offset -= self.speed * dt
            if self.offset <= -10:
                self.going_up = False
        else:
            self.offset += self.speed * dt
            if self.offset >= 10:
                self.going_up = True

        self.rect.y = self.start_y + self.offset
