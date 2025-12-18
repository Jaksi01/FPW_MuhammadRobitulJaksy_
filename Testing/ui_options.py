import pygame

import pygame

class OptionsUI:
    def __init__(self, screen_width, screen_height):
        base = "Assets/UI/UI_Game_Completed/"

        # Background
        self.bg = pygame.image.load(base + "button_rectangle_gradient.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (screen_width, screen_height))

        # Panel
        self.panel = pygame.image.load(base + "button_rectangle_border.png").convert_alpha()
        self.panel = pygame.transform.scale(
            self.panel,
            (int(screen_width * 0.7), int(screen_height * 0.65))
        )
        self.panel_rect = self.panel.get_rect(center=(screen_width//2, screen_height//2))

        # Button assets
        self.button_img = pygame.image.load(base + "button_rectangle_line.png").convert_alpha()
        self.button_img = pygame.transform.scale(self.button_img, (300, 90))

        # Buttons rect
        self.btn_continue = self.button_img.get_rect(
            center=(screen_width//2, self.panel_rect.centery + 40)
        )
        self.btn_mainmenu = self.button_img.get_rect(
            center=(screen_width//2, self.panel_rect.centery + 150)
        )

        # Fonts
        self.font_title = pygame.font.Font(None, 90)
        self.font_button = pygame.font.Font(None, 50)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.panel, self.panel_rect)

        # Title
        title = self.font_title.render("OPTIONS", True, (30, 30, 30))
        screen.blit(
            title,
            (self.panel_rect.centerx - title.get_width()//2,
             self.panel_rect.top + 40)
        )

        # Buttons
        screen.blit(self.button_img, self.btn_continue)
        screen.blit(self.button_img, self.btn_mainmenu)

        # Button text
        txt_continue = self.font_button.render("CONTINUE", True, (30, 30, 30))
        txt_menu = self.font_button.render("MAIN MENU", True, (30, 30, 30))

        screen.blit(
            txt_continue,
            (self.btn_continue.centerx - txt_continue.get_width()//2,
             self.btn_continue.centery - txt_continue.get_height()//2)
        )
        screen.blit(
            txt_menu,
            (self.btn_mainmenu.centerx - txt_menu.get_width()//2,
             self.btn_mainmenu.centery - txt_menu.get_height()//2)
        )

    def handle_click(self, pos):
        if self.btn_continue.collidepoint(pos):
            return "continue"
        if self.btn_mainmenu.collidepoint(pos):
            return "menu"
        return None
