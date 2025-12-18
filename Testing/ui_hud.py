import pygame
import os

class UIHUD:
    def __init__(self):
        # ===== HEARTS =====
        self.heart_full = pygame.image.load("Assets/UI/hud_heart.png").convert_alpha()
        self.heart_empty = pygame.image.load("Assets/UI/hud_heart_empty.png").convert_alpha()

        self.heart_full = pygame.transform.scale(self.heart_full, (45, 45))
        self.heart_empty = pygame.transform.scale(self.heart_empty, (45, 45))

        # ===== COIN ICON =====
        self.coin_icon = pygame.image.load("Assets/UI/hud_coin.png").convert_alpha()
        self.coin_icon = pygame.transform.scale(self.coin_icon, (45, 45))

        # ===== NUMBER IMAGES =====
        self.numbers = []
        for i in range(10):
            path = f"Assets/UI_Number/hud_character_{i}.png"
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (35, 35))
            self.numbers.append(img)

        # Coin counter internal
        self.coin_count = 0

        # Batas HP default
        self.default_max_hp = 3

    # =============================
    # DRAW COINS
    # =============================
    def draw_coin(self, screen, coin_amount):
        screen.blit(self.coin_icon, (20, 20))

        x_offset = 75
        for digit in str(coin_amount):
            num_img = self.numbers[int(digit)]
            screen.blit(num_img, (x_offset, 25))
            x_offset += 32

    # =============================
    # DRAW HEARTS
    # =============================
    def draw_hearts(self, screen, current_hp, max_hp):
        x_start = screen.get_width() - (max_hp * 50) - 20

        for i in range(max_hp):
            if i < current_hp:
                screen.blit(self.heart_full, (x_start + i * 50, 20))
            else:
                screen.blit(self.heart_empty, (x_start + i * 50, 20))

    # =============================
    # DRAW MAIN
    # =============================
    def draw(self, screen, player):
        
        current_hp = player.hp
        max_hp = self.default_max_hp

        # Coin internal UI
        self.draw_coin(screen, self.coin_count)

        # Hearts
        self.draw_hearts(screen, current_hp, max_hp)
