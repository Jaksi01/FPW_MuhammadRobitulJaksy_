import pygame
import sys

pygame.init()

# ====================== WINDOW ======================
WIDTH, HEIGHT = 1280, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

clock = pygame.time.Clock()

# ====================== LOAD ASSETS ======================
background = pygame.image.load("Assets/Main_menu/Background_UI_Final.png").convert()

player_img = pygame.image.load("Assets/Main_menu/character_yellow_walk_a.png").convert_alpha()

bee_frames = [
    pygame.image.load("Assets/Main_menu/bee_b.png").convert_alpha(),
    pygame.image.load("Assets/Main_menu/bee_a.png").convert_alpha()
]

fly_frames = [
    pygame.image.load("Assets/Main_menu/fly_b.png").convert_alpha(),
    pygame.image.load("Assets/Main_menu/fly_a.png").convert_alpha()
]

button_box = pygame.image.load("Assets/Main_menu/button_rectangle_border.png").convert_alpha()

# ====================== BUTTON CLASS ======================
class Button:
    def __init__(self, text, x, y):
        self.image = button_box
        self.rect = self.image.get_rect(center=(x, y))

        self.font = pygame.font.Font(None, 52)
        self.color = (40, 40, 40)
        self.raw_text = text
        self.text = self.font.render(text, True, self.color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

        self.hovered = False
        self.clicked = False

    def draw(self, surface):
        img = self.image.copy()
        scale_x, scale_y = img.get_size()

        if self.hovered:
            img = pygame.transform.scale(img, (int(scale_x * 1.05), int(scale_y * 1.05)))

        if self.clicked:
            img = pygame.transform.scale(img, (int(scale_x * 0.95), int(scale_y * 0.95)))

        r = img.get_rect(center=self.rect.center)
        surface.blit(img, r)

        self.text_rect = self.text.get_rect(center=r.center)
        surface.blit(self.text, self.text_rect)

    def update(self):
        mouse = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse)
        self.clicked = self.hovered and pygame.mouse.get_pressed()[0]

# ====================== ANIMATED SPRITES ======================
class FloatObject:
    def __init__(self, img, x, y):
        self.image = img
        self.x = x
        self.base_y = y
        self.offset = 0
        self.direction = 1

    def update(self):
        self.offset += 0.3 * self.direction
        if self.offset > 10 or self.offset < -10:
            self.direction *= -1

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.base_y + self.offset))


class MovingEnemy:
    def __init__(self, frames, x, y, min_x, max_x, speed):
        self.frames = frames
        self.frame_index = 0
        self.anim_speed = 0.15

        self.x = x
        self.y = y
        self.min_x = min_x
        self.max_x = max_x
        self.speed = speed
        self.direction = 1

    def update(self):
        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.x += self.speed * self.direction
        if self.x < self.min_x:
            self.direction = 1
        elif self.x > self.max_x:
            self.direction = -1

    def draw(self, surface):
        img = self.frames[int(self.frame_index)]
        if self.direction > 0:
            img = pygame.transform.flip(img, True, False)

        surface.blit(img, (self.x, self.y))

# ====================== OBJECTS ======================
player_float = FloatObject(player_img, 150, 400)
bee = MovingEnemy(bee_frames, 900, 100, 850, 1100, 2)
fly = MovingEnemy(fly_frames, 1050, 250, 1000, 1180, 2)
OFFSET_X = -60

button_new_game = Button("New Game", WIDTH//2 + OFFSET_X, 200)
button_credits = Button("Credits", WIDTH//2 + OFFSET_X, 300)
button_quit = Button("Quit Game", WIDTH//2 + OFFSET_X, 400)

buttons = [button_new_game, button_credits, button_quit]

# ==============================================================
def run_main_menu():
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player_float.update()
        bee.update()
        fly.update()

        for b in buttons:
            b.update()

        if button_new_game.clicked:
            return "start_game"

        if button_credits.clicked:
            print("Show Credits!")

        if button_quit.clicked:
            pygame.quit()
            sys.exit()

        screen.blit(background, (0, 0))

        player_float.draw(screen)
        bee.draw(screen)
        fly.draw(screen)

        for b in buttons:
            b.draw(screen)

        pygame.display.update()

# ==============================================================
if __name__ == "__main__":
    action = run_main_menu()
    print(action)
