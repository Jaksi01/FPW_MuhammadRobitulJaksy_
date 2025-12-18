import pygame

# ===================== STAR =====================
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

# ===================== COIN =====================
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, frame1, frame2):
        super().__init__()

        self.frames = [frame1, frame2]
        self.frame_index = 0

        self.anim_timer = 0
        self.anim_speed = 150  # ms per frame

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % 2
            self.image = self.frames[self.frame_index]

# ===================== DOOR =====================
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, img_closed, img_open):
        super().__init__()
        self.image_closed = img_closed
        self.image_open = img_open
        self.image = self.image_closed
        self.rect = self.image.get_rect(topleft=(x, y))

        self.open = False

    def set_open(self):
        self.open = True
        self.image = self.image_open

# ===================== CHECKPOINT =====================
class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, pole_img, flag1, flag2):
        super().__init__()

        self.pole = pole_img
        self.flag_frames = [flag1, flag2]

        self.activated = False
        self.frame_index = 0
        self.anim_speed = 150
        self.anim_timer = 0

        self.image = self.pole
        self.rect = self.image.get_rect(topleft=(x, y))

    def activate(self, player):
        """Player menyentuh checkpoint → simpan posisi respawn"""
        if not self.activated:
            self.activated = True
            self.frame_index = 0
            self.anim_timer = 0

            # SET RESPAWN PLAYER
            player.spawn_x = self.rect.x
            player.spawn_y = self.rect.y - 32  # sedikit di atas checkpoint

            print("Checkpoint activated → Respawn diset ke:", player.spawn_x, player.spawn_y)

    def update(self, dt):
        if not self.activated:
            return

        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.flag_frames)

        self.image = self.flag_frames[self.frame_index]
