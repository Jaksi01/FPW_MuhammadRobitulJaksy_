import pygame

class GameCompletedUI:
    def __init__(self, screen_width, screen_height):
        base = "Assets/UI/UI_Game_Completed/"

        # Background
        self.bg = pygame.image.load(base + "button_rectangle_gradient.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (screen_width, screen_height))

        # Panel
        self.panel = pygame.image.load(base + "button_rectangle_border.png").convert_alpha()

        # Stars
        self.star_white = pygame.image.load(base + "star_outline.png").convert_alpha()
        self.star_yellow = pygame.image.load(base + "star.png").convert_alpha()

        # Coin
        self.coin_icon = pygame.image.load(base + "hud_coin.png").convert_alpha()

        # Button
        self.btn_mainmenu = pygame.image.load(base + "button_rectangle_line.png").convert_alpha()

        # Screen size
        self.screen_width = screen_width
        self.screen_height = screen_height

        # ===== PANEL SIZE =====
        panel_width = int(screen_width * 0.82)
        panel_height = int(screen_height * 0.68)
        self.panel = pygame.transform.scale(self.panel, (panel_width, panel_height))
        self.panel_rect = self.panel.get_rect(center=(screen_width // 2, screen_height // 2))

        # ===== BUTTON =====
        self.btn_mainmenu = pygame.transform.scale(self.btn_mainmenu, (280, 90))
        self.btn_rect = self.btn_mainmenu.get_rect(
            center=(self.panel_rect.centerx, self.panel_rect.bottom - 60)
        )

        # ===== FONTS =====
        self.font_title = pygame.font.Font(None, 80)
        self.font_text = pygame.font.Font(None, 48)
        self.font_number = pygame.font.Font(None, 54)

        # Data
        self.stars_collected = 0
        self.coins_collected = 0

    def set_results(self, stars, coins):
        self.stars_collected = stars
        self.coins_collected = coins

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.panel, self.panel_rect)

        # ===== TITLE =====
        title = self.font_title.render("GAME COMPLETED", True, (30, 30, 30))
        screen.blit(
            title,
            (
                self.panel_rect.centerx - title.get_width() // 2,
                self.panel_rect.top + 60
            )
        )

        # ===== STARS LABEL =====
        txt_stars = self.font_text.render("Stars Collected", True, (40, 40, 40))
        screen.blit(
            txt_stars,
            (
                self.panel_rect.centerx - txt_stars.get_width() // 2,
                self.panel_rect.top + 120
            )
        )

        # ===== STARS =====
        star_y = self.panel_rect.top + 185
        start_x = self.panel_rect.centerx - 140

        for i in range(3):
            img = self.star_yellow if i < self.stars_collected else self.star_white
            screen.blit(img, (start_x + i * 110, star_y))

        # ===== COINS LABEL =====
        txt_coin = self.font_text.render("Coins Collected", True, (40, 40, 40))
        screen.blit(
            txt_coin,
            (
                self.panel_rect.centerx - txt_coin.get_width() // 2,
                self.panel_rect.top + 300
            )
        )

        # ===== COIN ICON + NUMBER =====
        coin_y = self.panel_rect.top + 350
        screen.blit(self.coin_icon, (self.panel_rect.centerx - 90, coin_y))

        coin_text = self.font_number.render(str(self.coins_collected), True, (20, 20, 20))
        screen.blit(coin_text, (self.panel_rect.centerx - 20, coin_y + 6))

        # ===== MAIN MENU BUTTON =====
        screen.blit(self.btn_mainmenu, self.btn_rect)

        btn_text = self.font_text.render("MAIN MENU", True, (30, 30, 30))
        screen.blit(
            btn_text,
            (
                self.btn_rect.centerx - btn_text.get_width() // 2,
                self.btn_rect.centery - btn_text.get_height() // 2
            )
        )

    def handle_click(self, pos):
        return self.btn_rect.collidepoint(pos)
