import pygame

class GameOverUI:
    def __init__(self, screen_width, screen_height):
        base = "Assets/UI/UI_Game_Completed/"

        # Background
        self.bg = pygame.image.load(base + "button_rectangle_gradient.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (screen_width, screen_height))

        # Panel
        self.panel = pygame.image.load(base + "button_rectangle_border.png").convert_alpha()
        self.panel = pygame.transform.scale(
            self.panel,
            (int(screen_width * 0.8), int(screen_height * 0.65))
        )
        self.panel_rect = self.panel.get_rect(center=(screen_width//2, screen_height//2))

        # Buttons
        self.btn_img = pygame.image.load(base + "button_rectangle_line.png").convert_alpha()
        self.btn_restart = pygame.transform.scale(self.btn_img, (300, 90))
        self.btn_menu = pygame.transform.scale(self.btn_img, (300, 90))

        self.btn_restart_rect = self.btn_restart.get_rect(
            center=(screen_width//2, self.panel_rect.bottom - 180)
        )
        self.btn_menu_rect = self.btn_menu.get_rect(
            center=(screen_width//2, self.panel_rect.bottom - 90)
        )

        # Fonts
        self.font_title = pygame.font.Font(None, 100)
        self.font_btn = pygame.font.Font(None, 50)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.panel, self.panel_rect)

        # TITLE
        title = self.font_title.render("GAME OVER", True, (30, 30, 30))
        screen.blit(
            title,
            (self.panel_rect.centerx - title.get_width()//2,
             self.panel_rect.top + 60)
        )

        # BUTTONS
        screen.blit(self.btn_restart, self.btn_restart_rect)
        screen.blit(self.btn_menu, self.btn_menu_rect)

        txt_restart = self.font_btn.render("RESTART", True, (30, 30, 30))
        txt_menu = self.font_btn.render("MAIN MENU", True, (30, 30, 30))

        screen.blit(
            txt_restart,
            (self.btn_restart_rect.centerx - txt_restart.get_width()//2,
             self.btn_restart_rect.centery - txt_restart.get_height()//2)
        )
        screen.blit(
            txt_menu,
            (self.btn_menu_rect.centerx - txt_menu.get_width()//2,
             self.btn_menu_rect.centery - txt_menu.get_height()//2)
        )

    def handle_click(self, pos):
        if self.btn_restart_rect.collidepoint(pos):
            return "restart"
        if self.btn_menu_rect.collidepoint(pos):
            return "menu"
        return None
