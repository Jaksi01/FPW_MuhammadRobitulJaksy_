import pygame

def rotate_center(image, angle):
    """Rotate an image while keeping its center."""
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=image.get_rect().center)
    return rotated_image, rotated_rect

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.original_image = pygame.image.load("Assets/bullets/fireball.png").convert_alpha()

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 10 * direction
        self.direction = direction

        self.rotation_angle = 0
        self.rotation_speed = 14

        self.lifetime = 2000
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt, solid_tiles, enemies, camera_x, screen_width):

        # ===== MATI kalau keluar layar =====
        if self.rect.right < camera_x - 200 or self.rect.left > camera_x + screen_width + 200:
            self.kill()
            return

        # ===== GERAK =====
        self.rect.x += self.speed

        # ===== ROTASI TANPA MECELAT =====
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
        cx, cy = self.rect.center
        self.image, new_rect = rotate_center(self.original_image, self.rotation_angle)
        self.rect = new_rect
        self.rect.center = (cx, cy)

        # ===== LIFETIME =====
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
            return

        # ===== COLLISION: SOLID =====
        for t in solid_tiles:
            if self.rect.colliderect(t.rect):
                self.kill()
                return

        # ===== COLLISION: ENEMY =====
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.kill()
                self.kill()
                return

    
             #DEBUG COLLIDER 
    # ============================================
    def draw_debug(self, surface, camera_x):
        debug_rect = pygame.Rect(
            self.rect.x - camera_x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(surface, (255, 140, 0), debug_rect, 2)
