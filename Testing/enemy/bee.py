import pygame

class Bee(pygame.sprite.Sprite):
    def __init__(self, x, y, frame1, frame2):
        super().__init__()
        
        # Animasi
        self.frames = [frame1, frame2]
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 150  # ms per frame

        # Posisi
        self.rect = frame1.get_rect(topleft=(x, y))

        # Movement
        self.speed = 2
        self.direction = 1  # 1 = kanan, -1 = kiri

        # Jarak maksimum ±160px dari posisi awal
        self.start_x = x
        self.max_range = 160  

        # --- FIX: sprite aslinya ternyata menghadap ke kiri ---
        self.frame_left = frame1
        self.frame_right = pygame.transform.flip(frame1, True, False)
        self.frame2_left = frame2
        self.frame2_right = pygame.transform.flip(frame2, True, False)

    def update(self, dt, solid_tiles):
        # Animasi
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % 2

        # Pilih frame sesuai arah
        if self.direction == 1:  # kanan
            current_frame = self.frame_right if self.frame_index == 0 else self.frame2_right
        else:  # kiri
            current_frame = self.frame_left if self.frame_index == 0 else self.frame2_left

        self.image = current_frame

        # Gerak
        self.rect.x += self.speed * self.direction

        # Range balik
        distance_from_start = abs(self.rect.x - self.start_x)
        if distance_from_start >= self.max_range:
            self.direction *= -1

        # Tembok balik
        hit = pygame.sprite.spritecollide(self, solid_tiles, False)
        if hit:
            self.direction *= -1
            self.rect.x += self.direction * self.speed
