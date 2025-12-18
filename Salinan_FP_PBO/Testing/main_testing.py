import pygame
import os

from Testing.player_testing import Player
from Testing.objects import Star, Coin, Door, Checkpoint
from Testing.enemy.enemy_manager import EnemyManager
from Testing.fireball import Fireball
from Testing.ui_hud import UIHUD
from Testing.ui_game_completed import GameCompletedUI   # ← UI selesai game

pygame.init()

# ======================================
# FUNCTION: run_game()  ← dipanggil launcher.py
# ======================================
def run_game():

    screen_width = 1280
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("My Platformer Debug")

    TILE_SIZE = 64
    DEBUG_COLLIDER = True

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
        base_path = os.path.dirname(__file__)
        full_path = os.path.join(base_path, filename)
        with open(full_path, "r") as f:
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

    # LOAD MAP OBJECTS
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
                    Checkpoint(
                        wX, wY,
                        checkpoint_empty,
                        checkpoint_flag1,
                        checkpoint_flag2
                    )
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

    def draw_background(screen, camera_x):
        index = camera_x // screen_width
        index = min(index, len(bg_images)-1)
        screen.blit(bg_images[index], (0, 0))

    def update_camera(px):
        nonlocal camera_x
        camera_x = px - screen_width // 2
        camera_x = max(0, min(camera_x, world_width - screen_width))

    player = Player(100, 100, fireball_group)
    player_group = pygame.sprite.GroupSingle(player)

    ui = UIHUD()

    # ==== UI GAME COMPLETED ====
    ui_completed = GameCompletedUI(screen_width, screen_height)

    def draw_debug_collider(surface, rect, camera_x, color=(0,255,0)):
        debug_rect = pygame.Rect(rect.x - camera_x, rect.y, rect.width, rect.height)
        pygame.draw.rect(surface, color, debug_rect, 2)

    clock = pygame.time.Clock()
    running = True

    # =====================================================================================
    #                                    GAME LOOP
    # =====================================================================================
    while running:

        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    player.shoot()

        player_group.update(dt, solid_tiles, hazard_tiles, world_width)
        enemy_manager.update(dt, solid_tiles)
        checkpoint_group.update(dt)
        fireball_group.update(
            dt,
            solid_tiles,
            enemy_manager.enemies,
            camera_x,
            screen_width
        )
        coin_group.update(dt)

        # FIREBALL HIT ENEMY
        for fireball in fireball_group:
            for enemy in enemy_manager.enemies:
                if fireball.rect.colliderect(enemy.rect):
                    fireball.trigger_hit()
                    enemy.kill()

        # ENEMY HIT PLAYER
        for enemy in enemy_manager.enemies:
            if player.rect.colliderect(enemy.rect):
                if not player.immune:
                    direction = enemy.rect.centerx - player.rect.centerx
                    player.take_damage(direction)

        # HAZARD HIT PLAYER
        for h in hazard_tiles:
            if player.rect.colliderect(h.rect):
                if h.tile_type == "S":
                    if not player.immune:
                        direction = -1 if player.facing_right else 1
                        player.take_damage(direction)
                else:
                    player.hp = 0

        if player.hp <= 0:
            player.respawn()

        # STAR
        pygame.sprite.spritecollide(player, star_group, dokill=True)

        # COIN
        coins_collected = pygame.sprite.spritecollide(player, coin_group, dokill=True)
        if coins_collected:
            ui.coin_count += len(coins_collected)

        # CHECKPOINT
        hit_cp = pygame.sprite.spritecollide(player, checkpoint_group, False)
        if hit_cp:
            hit_cp[0].activate(player)

        # DOOR HIT → GAME COMPLETED
        door_hit = pygame.sprite.spritecollide(player, door_group, False)
        if door_hit:
            door_hit[0].set_open()
            print("GAME END - Player masuk pintu!")

            # Kirim data ke UI selesai game
            ui_completed.set_results(
                stars=len(star_group),
                coins=ui.coin_count
            )

            # Masuk ke UI selesai game
            return show_completed_ui(screen, ui_completed)

        update_camera(player.rect.centerx)

        draw_background(screen, camera_x)

        # DRAW TILE OBJECTS
        for t in solid_tiles:
            screen.blit(t.image, (t.rect.x - camera_x, t.rect.y))
        for h in hazard_tiles:
            screen.blit(h.image, (h.rect.x - camera_x, h.rect.y))
        for d in decor_tiles:
            screen.blit(d.image, (d.rect.x - camera_x, d.rect.y))
        for s in star_group:
            screen.blit(s.image, (s.rect.x - camera_x, s.rect.y))
        for c in coin_group:
            screen.blit(c.image, (c.rect.x - camera_x, c.rect.y))
        for dr in door_group:
            screen.blit(dr.image, (dr.rect.x - camera_x, dr.rect.y))
        for cp in checkpoint_group:
            screen.blit(cp.image, (cp.rect.x - camera_x, cp.rect.y))

        enemy_manager.draw(screen, camera_x)

        for f in fireball_group:
            screen.blit(f.image, (f.rect.x - camera_x, f.rect.y))

        if player.visible:
            screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

        # DEBUG COLLIDER
        if DEBUG_COLLIDER:
            draw_debug_collider(screen, player.rect, camera_x)

            for t in solid_tiles:
                draw_debug_collider(screen, t.rect, camera_x, (255,0,0))
            for h in hazard_tiles:
                draw_debug_collider(screen, h.rect, camera_x, (255,255,0))
            for enemy in enemy_manager.enemies:
                draw_debug_collider(screen, enemy.rect, camera_x, (0,255,255))
            for deco in decor_tiles:
                draw_debug_collider(screen, deco.rect, camera_x, (0,200,255))
            for cp in checkpoint_group:
                draw_debug_collider(screen, cp.rect, camera_x, (255,0,255))
            for fb in fireball_group:
                draw_debug_collider(screen, fb.rect, camera_x, (255,128,0))

        ui.draw(screen, player)

        pygame.display.flip()

    pygame.quit()



# =====================================================================================
#                       FUNCTION: SHOW COMPLETED UI
# =====================================================================================
def show_completed_ui(screen, ui_completed):

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # kembali ke launcher

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ui_completed.handle_click(event.pos):
                    print("Back to Main Menu")
                    return  # kembali ke launcher.py

        ui_completed.draw(screen)
        pygame.display.flip()
