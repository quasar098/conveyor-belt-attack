import pygame
from utils import *
from block import Block
from random import randint as rand


class ConveyerBelt:
    def __init__(self, top: int, speed: int):
        self.rect = pygame.Rect(0, top, pygame.display.get_surface().get_width(), 200)
        self.speed: float = speed
        self.passengers: list[Block] = []
        self._delay = 0
        self.front = pygame.transform.scale(
            fetch_texture(get_path("assets", "images", f"conveyer_front.png")), (1320, 200)
        )
        self.back = pygame.transform.scale(
            fetch_texture(get_path("assets", "images", f"conveyer_back.png")), (1280, 200)
        )
        self._frame = 0

    def draw(self, surface: pygame.Surface, deltatime: float, speedmod=1):
        self._frame += deltatime*speedmod
        surface.blit(self.back, self.rect.topleft)
        surface.blit(self.front, [self._frame % 20-20, self.rect.top])

    def add_occasionally(self, deltatime: float, survival_bonus_tiers):
        if not self._delay > deltatime:
            self._delay += deltatime/75
            return
        self._delay = 0
        tier = 1
        while survival_bonus_tiers > 1:
            if rand(1, 5) > 3:
                tier += 1
            survival_bonus_tiers -= 1
        if tier < 4 and not (survival_bonus_tiers > 4):  # no more boxes after 2 min
            self.passengers.append(Block(150, tier, False))

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        play_sound(get_path("assets", "sounds", "hit_belt.wav"))
                        return True
        return False
