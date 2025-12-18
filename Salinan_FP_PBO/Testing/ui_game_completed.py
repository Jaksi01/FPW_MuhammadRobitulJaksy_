import pygame

class GameCompletedUI:
    def __init__(self, screen_width, screen_height):
        base = "Assets/UI/UI_Game_Completed/"

        # Background panel
        self.bg = pygame.image.load(base + "button_rectangle_gradient.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (screen_width, screen_height))

        # Panel tengah
        self.panel = pygame.image.load(base + "button_rectangle_border.png").convert_alpha()
        self.panel_rect = self.panel.get_rect(center=(screen_width // 2, screen_height // 2))

        # Stars
        self.star_white = pygame.image.load(base + "star_outline.png").convert_alpha()
        self.star_yellow = pygame.image.load(base + "star.png").convert_alpha()

        # Coin icon
        self.coin_icon = pygame.image.load(base + "hud_coin.png").convert_alpha()

        # Button Main Menu
        self.btn_mainmenu = pygame.image.load(base + "button_rectangle_line.png").convert_alpha()
        self.btn_rect = self.btn_mainmenu.get_rect(center=(screen_width // 2, screen_height // 2 + 220))

        # Fonts
        self.font_title = pygame.font.Font(None, 90)
        self.font_sub = pygame.font.Font(None, 55)
        self.font_text = pygame.font.Font(None, 50)

        self.stars_collected = 0
        self.coins_collected = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

    def set_results(self, stars, coins):
        self.stars_collected = stars
        self.coins_collected = coins

    def draw(self, screen):

        # Background
        screen.blit(self.bg, (0, 0))

        # Panel
        screen.blit(self.panel, self.panel_rect)

        center_x = self.screen_width // 2

        # Title
        title = self.font_title.render("GAME COMPLETED", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(center_x, 140)))

        # Stars Collected label
        txt_star = self.font_sub.render("Stars Collected", True, (255, 255, 255))
        screen.blit(txt_star, txt_star.get_rect(center=(center_x, 250)))

        # Stars (3)
        start_x = center_x - 140
        for i in range(3):
            img = self.star_yellow if i < self.stars_collected else self.star_white
            screen.blit(img, (start_x + i * 140, 300))

        # Coins Collected label
        txt_coin_label = self.font_sub.render("Coins Collected", True, (255, 255, 255))
        screen.blit(txt_coin_label, txt_coin_label.get_rect(center=(center_x, 420)))

        # Coin icon + text
        screen.blit(self.coin_icon, (center_x - 60, 460))
        txt_coin = self.font_text.render(str(self.coins_collected), True, (255, 255, 255))
        screen.blit(txt_coin, txt_coin.get_rect(midleft=(center_x, 475)))

        # Button
        screen.blit(self.btn_mainmenu, self.btn_rect)

        # Button text
        txt_btn = self.font_text.render("MAIN MENU", True, (255, 255, 255))
        screen.blit(txt_btn, txt_btn.get_rect(center=self.btn_rect.center))

    def handle_click(self, pos):
        return self.btn_rect.collidepoint(pos)
