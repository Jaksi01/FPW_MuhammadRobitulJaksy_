import pygame
from player import Player   # pastikan file player.py sudah versi terbaru

pygame.init()

# ===== SETUP =====
screen_width = 1280
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Platformer Debug")

TILE_SIZE = 64

# ===== TILE MAP =====
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
    
    # dekorasi
    "C": "Assets/Decorations/cactus.png",
    "B": "Assets/Decorations/bush.png",
    "R": "Assets/Decorations/sign_right.png",
    "F": "Assets/Decorations/flag_green_a.png",
    "*": "Assets/Decorations/star.png",
}

# ===== LOAD WORLD =====
def load_world(path):
    with open(path, "r") as f:
        return [list(row.rstrip("\n")) for row in f]

world = load_world("world.txt")
world_width = len(world[0]) * TILE_SIZE

# ===== TILE GROUPS =====
SOLID_TILES = ["G","D","d","h","H","T","W","w","=","S","L"]

solid_tiles = pygame.sprite.Group()
decor_tiles = pygame.sprite.Group()
coin_tiles  = pygame.sprite.Group()
flag_tiles  = pygame.sprite.Group()

for y, row in enumerate(world):
    for x, tile in enumerate(row):
        if tile == ".":
            continue

        img = pygame.image.load(tile_images[tile]).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

        sprite = pygame.sprite.Sprite()
        sprite.image = img
        sprite.rect = img.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))

        if tile in SOLID_TILES:
            solid_tiles.add(sprite)
        elif tile == "*":
            coin_tiles.add(sprite)
        elif tile == "F":
            flag_tiles.add(sprite)
        else:
            decor_tiles.add(sprite)

# ===== BACKGROUND =====
bg_images = [
    pygame.image.load("Assets/Backgrounds/bg1.jpg").convert(),
    pygame.image.load("Assets/Backgrounds/bg2.jpg").convert(),
    pygame.image.load("Assets/Backgrounds/bg1.jpg").convert(),
]

camera_x = 0

def draw_background(screen, camera_x):
    index = camera_x // screen_width
    index = min(index, len(bg_images) - 1)
    screen.blit(bg_images[index], (0, 0))

def update_camera(player_x):
    global camera_x
    camera_x = player_x - screen_width // 2
    camera_x = max(0, min(camera_x, world_width - screen_width))

# ===== DEBUG COLLIDER =====
def draw_debug(screen, camera_x, player, solid_tiles):

    # Collider player (MERAH)
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        pygame.Rect(
            player.rect.x - camera_x,
            player.rect.y,
            player.rect.width,
            player.rect.height
        ),
        2
    )

    # Collider tile solid (BIRU)
    for t in solid_tiles:
        pygame.draw.rect(
            screen,
            (0, 120, 255),
            pygame.Rect(
                t.rect.x - camera_x,
                t.rect.y,
                t.rect.width,
                t.rect.height
            ),
            2
        )

# ===== PLAYER =====
player = Player(100, 100)
player_group = pygame.sprite.GroupSingle(player)

# ===== MAIN LOOP =====
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player
    player_group.update(dt, solid_tiles)
    update_camera(player.rect.centerx)

    # Draw background
    draw_background(screen, camera_x)

    # Draw tiles
    for t in solid_tiles:
        screen.blit(t.image, (t.rect.x - camera_x, t.rect.y))

    for d in decor_tiles:
        screen.blit(d.image, (d.rect.x - camera_x, d.rect.y))

    for c in coin_tiles:
        screen.blit(c.image, (c.rect.x - camera_x, c.rect.y))

    for f in flag_tiles:
        screen.blit(f.image, (f.rect.x - camera_x, f.rect.y))

    # Draw player
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

    # === DEBUG COLLISION BOX ===
    draw_debug(screen, camera_x, player, solid_tiles)

    pygame.display.flip()

pygame.quit()
