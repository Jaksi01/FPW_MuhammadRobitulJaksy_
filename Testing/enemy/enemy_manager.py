import pygame
from Testing.enemy.fish import Fish
from Testing.enemy.bee import Bee
from Testing.enemy.ladybug import Ladybug
from Testing.enemy.shadow_fly import ShadowFly
from Testing.enemy.worm import Worm

class EnemyManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()

        self.fish_up = pygame.image.load("Assets/enemy/fish/fish_purple_up.png").convert_alpha()
        self.fish_down = pygame.image.load("Assets/enemy/fish/fish_purple_down.png").convert_alpha()

        self.bee_frame1 = pygame.image.load("Assets/enemy/bee/bee_a.png").convert_alpha()
        self.bee_frame2 = pygame.image.load("Assets/enemy/bee/bee_b.png").convert_alpha()

        self.ladybug_frame1 = pygame.image.load("Assets/enemy/ladybug/ladybug_a.png").convert_alpha()
        self.ladybug_frame2 = pygame.image.load("Assets/enemy/ladybug/ladybug_b.png").convert_alpha()

        self.shadow_frame1 = pygame.image.load("Assets/enemy/shadow_fly/shadow_a.png").convert_alpha()
        self.shadow_frame2 = pygame.image.load("Assets/enemy/shadow_fly/shadow_b.png").convert_alpha()

        self.worm_frame1 = pygame.image.load("Assets/enemy/worm/worm_a.png").convert_alpha()
        self.worm_frame2 = pygame.image.load("Assets/enemy/worm/worm_b.png").convert_alpha()

    def spawn_fish(self, x, y):
        self.enemies.add(Fish(x, y, self.fish_up, self.fish_down))

    def spawn_bee(self, x, y):
        self.enemies.add(Bee(x, y, self.bee_frame1, self.bee_frame2))

    def spawn_ladybug(self, x, y):
        self.enemies.add(Ladybug(x, y, self.ladybug_frame1, self.ladybug_frame2))

    def spawn_shadow_fly(self, x, y):
        self.enemies.add(ShadowFly(x, y, self.shadow_frame1, self.shadow_frame2))

    def spawn_worm(self, x, y):
        self.enemies.add(Worm(x, y, self.worm_frame1, self.worm_frame2))

    def update(self, dt, solid_tiles):
        for enemy in self.enemies:
            enemy.update(dt, solid_tiles)

    def draw(self, screen, camera_x):
        for enemy in self.enemies:
            screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))
