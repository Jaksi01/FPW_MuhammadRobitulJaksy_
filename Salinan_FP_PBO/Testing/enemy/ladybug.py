import pygame

class Ladybug(pygame.sprite.Sprite):
    def __init__(self, x, y, frame1, frame2):
        super().__init__()

        # === DIBALIK PERSIS SEPERTI SHADOW_FLY ===
        self.frames_left = [frame1, frame2]   # sprite asli menghadap kiri
        self.frames_right = [
            pygame.transform.flip(frame1, True, False),
            pygame.transform.flip(frame2, True, False)
        ]
        # ===================

        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 150

        self.image = self.frames_right[0]  # mulai menghadap kanan
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 2
        self.direction = 1

        self.start_x = x
        self.max_range = 160

    def update(self, dt, solid_tiles):
        # animasi
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % 2

        # arah benar
        if self.direction == 1:
            self.image = self.frames_right[self.frame_index]
        else:
            self.image = self.frames_left[self.frame_index]

        # gerak
        self.rect.x += self.speed * self.direction

        # patrol
        if abs(self.rect.x - self.start_x) >= self.max_range:
            self.direction *= -1

        # tabrak tembok
        if pygame.sprite.spritecollide(self, solid_tiles, False):
            self.direction *= -1
            self.rect.x += self.direction * self.speed
