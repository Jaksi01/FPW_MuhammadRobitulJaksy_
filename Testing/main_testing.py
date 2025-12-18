import pygame
import os

from Testing.player_testing import Player
from Testing.objects import Star, Coin, Door, Checkpoint
from Testing.enemy.enemy_manager import EnemyManager
from Testing.fireball import Fireball
from Testing.ui_hud import UIHUD
from Testing.ui_game_completed import GameCompletedUI
from Testing.ui_game_over import GameOverUI
from Testing.ui_options import OptionsUI
from Testing.sound_manager import SoundManager

pygame.init()
pygame.mixer.init()

def run_game():

    # ================= SOUND =================
    sound = SoundManager()
    sound.play_ingame_bgm()

    screen_width = 1280
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("My Platformer Debug")

    TILE_SIZE = 64
    DEBUG_COLLIDER = True

    # ================= MAP ASSETS =================
    tile_images = {
        "G": "Assets/Tiles/ground/terrain_grass_block.png",
        "D": "Assets/Tiles/ground/terrain_dirt_cloud.png",
        "d": "Assets/Tiles/ground/terrain_dirt_cloud_left.png",
        "h": "Assets/Tiles/ground/terrain_dirt_horizontal_left.png",
        "H": "Assets/Tiles/ground/terrain_dirt_horizontal_right.png",
        "T": "Assets/Tiles/ground/terrain_sand_vertical_top.png",
        "W": "Assets/Tiles/water/water_top.png",
        "w": "Assets/Tiles/water/water.png",
        "=": "Assets/Tiles/bridges/bridge.png",
        "S": "Assets/Tiles/spikes/block_spikes.png",
        "L": "Assets/Tiles/lava/lava_top.png",
        "C": "Assets/Decorations/cactus.png",
        "B": "Assets/Decorations/bush.png",
        "R": "Assets/Decorations/sign_exit.png",
        "F": "Assets/Decorations/flag_green_a.png",
        "*": "Assets/Decorations/star.png",
        "/": "Assets/Decorations/door_closed.png",
        "E": "Assets/enemy/fish/fish_purple_up.png",
        "b": "Assets/enemy/bee/bee_a.png",
        "x": "Assets/enemy/ladybug/ladybug_1.png",
        "f": "Assets/enemy/shadow_fly/shadow_fly_1.png",
        "m": "Assets/enemy/worm/worm_a.png",
        "K": "Assets/Decorations/coin_a.png",
        "P": "Assets/Decorations/checkpoint_empty.png"
    }

    checkpoint_flag1 = pygame.image.load("Assets/Decorations/flag_blue_a.png").convert_alpha()
    checkpoint_flag2 = pygame.image.load("Assets/Decorations/flag_blue_b.png").convert_alpha()
    checkpoint_empty = pygame.image.load("Assets/Decorations/flag_off.png").convert_alpha()

    def load_world(filename):
        base = os.path.dirname(__file__)
        with open(os.path.join(base, filename), "r") as f:
            return [list(row.strip()) for row in f]

    world = load_world("world_testing.txt")
    world_width = len(world[0]) * TILE_SIZE

    SOLID_TILES = ["G","D","d","h","H","T","=","W","w","S"]
    HAZARD_TILES = ["S","L","W"]

    solid_tiles = pygame.sprite.Group()
    hazard_tiles = pygame.sprite.Group()
    decor_tiles = pygame.sprite.Group()
    star_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    checkpoint_group = pygame.sprite.Group()

    coin_a = pygame.image.load("Assets/Decorations/coin_a.png").convert_alpha()
    coin_b = pygame.image.load("Assets/Decorations/coin_b.png").convert_alpha()

    enemy_manager = EnemyManager()
    door_open_image = pygame.image.load("Assets/Decorations/door_open.png").convert_alpha()
    fireball_group = pygame.sprite.Group()

    # ================= LOAD MAP =================
    for y, row in enumerate(world):
        for x, tile in enumerate(row):
            if tile == ".":
                continue

            wX = x * TILE_SIZE
            wY = y * TILE_SIZE

            if tile == "E": enemy_manager.spawn_fish(wX, wY); continue
            if tile == "b": enemy_manager.spawn_bee(wX, wY); continue
            if tile == "x": enemy_manager.spawn_ladybug(wX, wY); continue
            if tile == "f": enemy_manager.spawn_shadow_fly(wX, wY); continue
            if tile == "m": enemy_manager.spawn_worm(wX, wY); continue

            if tile == "*":
                img = pygame.image.load(tile_images[tile]).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                star_group.add(Star(wX, wY, img))
                continue

            if tile == "K":
                coin_group.add(Coin(wX, wY, coin_a, coin_b))
                continue

            if tile == "/":
                img = pygame.image.load(tile_images[tile]).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                door_group.add(Door(wX, wY, img, door_open_image))
                continue

            if tile == "P":
                checkpoint_group.add(
                    Checkpoint(wX, wY, checkpoint_empty, checkpoint_flag1, checkpoint_flag2)
                )
                continue

            img = pygame.image.load(tile_images[tile]).convert_alpha()
            img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))

            sprite = pygame.sprite.Sprite()
            sprite.image = img
            sprite.rect = img.get_rect(topleft=(wX,wY))
            sprite.tile_type = tile

            if tile in HAZARD_TILES:
                hazard_tiles.add(sprite)
            elif tile in SOLID_TILES:
                solid_tiles.add(sprite)
            else:
                decor_tiles.add(sprite)

    bg_images = [
        pygame.image.load("Assets/Backgrounds/bg1.jpg").convert(),
        pygame.image.load("Assets/Backgrounds/bg2.jpg").convert(),
        pygame.image.load("Assets/Backgrounds/bg1.jpg").convert(),
    ]

    camera_x = 0

    def draw_background(screen, cam):
        idx = min(cam // screen_width, len(bg_images)-1)
        screen.blit(bg_images[idx], (0, 0))

    def update_camera(px):
        nonlocal camera_x
        camera_x = max(0, min(px - screen_width//2, world_width - screen_width))

    player = Player(100, 100, fireball_group)
    player_group = pygame.sprite.GroupSingle(player)

    ui = UIHUD()
    ui_completed = GameCompletedUI(screen_width, screen_height)
    ui_game_over = GameOverUI(screen_width, screen_height)
    ui_options = OptionsUI(screen_width, screen_height)

    clock = pygame.time.Clock()
    paused = False

    # ================= GAME LOOP =================
    while True:
        dt = clock.tick(60)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                sound.stop_bgm()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    sound.click.play()

                if event.key == pygame.K_LSHIFT and not paused:
                    sound.throw.play()
                    player.shoot()

            if paused and event.type == pygame.MOUSEBUTTONDOWN:
                sound.click.play()
                action = ui_options.handle_click(event.pos)
                if action == "continue":
                    paused = False
                elif action == "restart":
                    sound.stop_bgm()
                    return run_game()
                elif action == "menu":
                    sound.stop_bgm()
                    return

        if paused:
            ui_options.draw(screen)
            pygame.display.flip()
            continue

        # ===== UPDATE =====
        player_group.update(dt, solid_tiles, hazard_tiles, world_width)
        enemy_manager.update(dt, solid_tiles)
        checkpoint_group.update(dt)
        fireball_group.update(dt, solid_tiles, enemy_manager.enemies, camera_x, screen_width)
        coin_group.update(dt)

        # FIREBALL HIT
        for f in fireball_group:
            for e in enemy_manager.enemies:
                if f.rect.colliderect(e.rect):
                    sound.bump.play()

        for e in enemy_manager.enemies:
            if player.rect.colliderect(e.rect) and not player.immune:
                sound.hurt.play()
                player.take_damage(e.rect.centerx - player.rect.centerx)

        for h in hazard_tiles:
            if player.rect.colliderect(h.rect):
                if h.tile_type == "S":
                    if not player.immune:
                        sound.hurt.play()
                        player.take_damage(-1 if player.facing_right else 1)
                else:
                    sound.disappear.play()
                    player.hp = 0

        if player.hp <= 0:
            sound.disappear.play()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        sound.click.play()
                        action = ui_game_over.handle_click(event.pos)
                        if action == "restart":
                            sound.stop_bgm()
                            return run_game()
                        elif action == "menu":
                            sound.stop_bgm()
                            return
                ui_game_over.draw(screen)
                pygame.display.flip()

        if pygame.sprite.spritecollide(player, star_group, dokill=True):
            sound.magic.play()

        if pygame.sprite.spritecollide(player, coin_group, dokill=True):
            sound.coin.play()
            ui.coin_count += 1

        hit_cp = pygame.sprite.spritecollide(player, checkpoint_group, False)
        if hit_cp:
            hit_cp[0].activate(player)

        door_hit = pygame.sprite.spritecollide(player, door_group, False)
        if door_hit:
            sound.stop_bgm()
            ui_completed.set_results(len(star_group), ui.coin_count)
            return show_completed_ui(screen, ui_completed)

        update_camera(player.rect.centerx)
        draw_background(screen, camera_x)

        for grp in [solid_tiles, hazard_tiles, decor_tiles, star_group, coin_group, door_group, checkpoint_group]:
            for obj in grp:
                screen.blit(obj.image, (obj.rect.x - camera_x, obj.rect.y))

        enemy_manager.draw(screen, camera_x)

        for f in fireball_group:
            screen.blit(f.image, (f.rect.x - camera_x, f.rect.y))

        if player.visible:
            screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

        ui.draw(screen, player)
        pygame.display.flip()


def show_completed_ui(screen, ui_completed):
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        ui_completed.draw(screen)
        pygame.display.flip()
