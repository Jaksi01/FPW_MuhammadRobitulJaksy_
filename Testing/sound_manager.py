import pygame

class SoundManager:
    def __init__(self):
        # === SFX ===
        self.jump = pygame.mixer.Sound("Assets/Sounds/sound_ingame/sfx_jump.ogg")
        self.jump_high = pygame.mixer.Sound("Assets/Sounds/sound_ingame/sfx_jump-high.ogg")
        self.coin = pygame.mixer.Sound("Assets/Sounds/sound_ingame/sfx_coin.ogg")
        self.magic = pygame.mixer.Sound("Assets/Sounds/sound_ingame/sfx_magic.ogg")
        self.throw = pygame.mixer.Sound("Assets/Sounds/sound_ingame/sfx_throw.ogg")
        self.bump = pygame.mixer.Sound("Assets/Sounds/sound_ingame/sfx_bump.ogg")
        self.hurt = pygame.mixer.Sound("Assets/Sounds/sound_ingame/sfx_hurt.ogg")
        self.disappear = pygame.mixer.Sound("Assets/Sounds/sound_ingame/sfx_disappear.ogg")
        self.click = pygame.mixer.Sound("Assets/Sounds/sound_ingame/click-a.ogg")

        # set volume
        self.jump.set_volume(0.4)
        self.jump_high.set_volume(0.5)
        self.coin.set_volume(0.5)
        self.magic.set_volume(0.7)
        self.throw.set_volume(0.4)
        self.bump.set_volume(0.3)
        self.hurt.set_volume(0.6)
        self.disappear.set_volume(0.6)
        self.click.set_volume(0.5)

    # === BGM ===
    def play_menu_bgm(self):
        pygame.mixer.music.load("Assets/Sounds/sound_bgm/main_menu_bgm.mp3")
        pygame.mixer.music.set_volume(0.8)  
        pygame.mixer.music.play(-1)

    def play_ingame_bgm(self):
        pygame.mixer.music.load("Assets/Sounds/sound_bgm/ingame_bgm.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def stop_bgm(self):
        pygame.mixer.music.stop()
