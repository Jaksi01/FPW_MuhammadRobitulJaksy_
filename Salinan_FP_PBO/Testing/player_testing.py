import pygame
import os
from Testing.fireball import Fireball

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, fireball_group):
        super().__init__()

        self.fireball_group = fireball_group

        self.animations = {"idle": [], "walk": [], "jump": [], "hit": []}
        self.load_animations()

        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.animations[self.state][0]

        frame_w = self.image.get_width()
        frame_h = self.image.get_height()
        self.rect = pygame.Rect(x, y, frame_w, frame_h)

        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -13
        self.on_ground = False
        self.jump_held = False

        self.facing_right = True

        # HP & Lives
        self.hp = 3
        self.lives = 3

        # Respawn point (default)
        self.spawn_x = x
        self.spawn_y = y

        self.immune = False
        self.immune_duration = 1000
        self.last_hit_time = 0

        self.visible = True

        # Knockback
        self.is_knockback = False
        self.knockback_timer = 0
        self.knockback_duration = 150
        self.knockback_force = 4

        # Shoot cooldown
        self.shoot_cooldown = 300
        self.last_shoot = 0

    # ================= SHOOT =================
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot < self.shoot_cooldown:
            return

        self.last_shoot = now
        direction = 1 if self.facing_right else -1

        px = self.rect.centerx + (30 * direction)
        py = self.rect.centery

        fireball = Fireball(px, py, direction)
        self.fireball_group.add(fireball)

    # ================= RESPAWN =================
    def reset_after_respawn(self):
        self.is_knockback = False
        self.knockback_timer = 0
        self.immune = False
        self.visible = True
        self.vel_x = 0
        self.vel_y = 0
        self.hp = 3

    def respawn(self):
        """Dipanggil langsung dari main ketika player mati"""
        self.die()

    # ================= DEATH / LIVES =================
    def die(self):
        self.lives -= 1
        print("Player mati! Sisa nyawa:", self.lives)

        if self.lives <= 0:
            print("=== GAME OVER ===")
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        # Respawn ke checkpoint
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.reset_after_respawn()

    # ================= LOAD ANIMATION =================
    def load_folder(self, path):
        frames = []
        for f in sorted(os.listdir(path)):
            if f.endswith(".png"):
                frames.append(pygame.image.load(path + f).convert_alpha())
        return frames

    def load_animations(self):
        base = "Assets_Testing/Player/"
        self.animations["idle"] = self.load_folder(base + "idle/")
        self.animations["walk"] = self.load_folder(base + "walk/")
        self.animations["jump"] = self.load_folder(base + "jump/")
        self.animations["hit"]  = self.load_folder(base + "hit/")

    # ================= DAMAGE =================
    def take_damage(self, direction):
        if self.immune:
            return

        self.hp -= 1
        self.immune = True
        self.last_hit_time = pygame.time.get_ticks()

        self.state = "hit"
        self.frame_index = 0

        self.is_knockback = True
        self.knockback_timer = pygame.time.get_ticks()

        self.vel_x = self.knockback_force if direction < 0 else -self.knockback_force
        self.vel_y = -6

        if self.hp <= 0:
            self.die()

    def check_instant_death_tiles(self, hazards):
        for t in hazards:
            tile_type = getattr(t, "tile_type", None)
            if self.rect.colliderect(t.rect):
                if tile_type in ("W", "L"):
                    self.die()
                    return

    # ================= PHYSICS =================
    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def move(self, dt, solids, world_width):
        keys = pygame.key.get_pressed()

        if self.is_knockback:
            if pygame.time.get_ticks() - self.knockback_timer > self.knockback_duration:
                self.is_knockback = False

        if not self.is_knockback:
            self.vel_x = 0
            if keys[pygame.K_LEFT]:
                self.vel_x = -5
                self.facing_right = False
            if keys[pygame.K_RIGHT]:
                self.vel_x = 5
                self.facing_right = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force
            self.jump_held = True
            self.on_ground = False

        if not keys[pygame.K_SPACE]:
            self.jump_held = False

        if not self.jump_held and self.vel_y < -3:
            self.vel_y = -3

        # Move X
        self.rect.x += self.vel_x
        self.rect.x = max(0, min(self.rect.x, world_width - self.rect.width))

        for t in solids:
            if self.rect.colliderect(t.rect):
                if self.vel_x > 0:
                    self.rect.right = t.rect.left
                elif self.vel_x < 0:
                    self.rect.left = t.rect.right

        # Move Y
        self.apply_gravity()
        self.on_ground = False

        for t in solids:
            if self.rect.colliderect(t.rect):
                if self.vel_y > 0:
                    self.rect.bottom = t.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = t.rect.bottom
                    self.vel_y = 0

    # ================= IMMUNITY =================
    def update_immunity(self):
        if not self.immune:
            return

        now = pygame.time.get_ticks()

        if now - self.last_hit_time > self.immune_duration:
            self.immune = False
            self.visible = True
            return

        self.visible = ((now // 100) % 2 == 1)

    # ================= STATE =================
    def update_state(self):
        if self.state == "hit":
            if self.frame_index >= len(self.animations["hit"]) - 1:
                self.state = "idle"
        else:
            if not self.on_ground:
                self.state = "jump"
            elif self.vel_x != 0:
                self.state = "walk"
            else:
                self.state = "idle"

    # ================= ANIMATION =================
    def animate(self):
        frames = self.animations[self.state]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0

        frame = frames[int(self.frame_index)]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame

    # ================= UPDATE =================
    def update(self, dt, solids, hazards, world_width):
        self.move(dt, solids, world_width)
        self.check_instant_death_tiles(hazards)
        self.update_immunity()
        self.update_state()
        self.animate()

    # ================= DEBUG =================
    def draw_debug(self, surface, camera_x):
        debug_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y,
                                 self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (0, 255, 255), debug_rect, 2)
