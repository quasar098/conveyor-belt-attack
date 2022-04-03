import pygame
# noinspection PyUnresolvedReferences
from constants import TIER_COLORS
from utils import *


class Block:
    def __init__(self, ylevel: int, tier=1, do_points=True):
        self.y = ylevel
        self.x = -75
        self.tier = tier
        self.grabbed = False
        self.do_points = do_points
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        color = TIER_COLORS[clamp(self.tier - 1, 0, len(TIER_COLORS)-1)]
        rect = pygame.Rect(69, 420, 75, 75)  # note for job people: you dont notice
        if self.grabbed:
            self.x, self.y = pygame.mouse.get_pos()
        rect.center = (self.x, self.y)
        pygame.draw.rect(surface, (0, 0, 0), rect.inflate(2, 2))
        pygame.draw.rect(surface, color, rect)
        self.rect: pygame.Rect = rect
        _ = fetch_text(f"{self.tier}", font)
        surface.blit(_, _.get_rect(center=(self.x, self.y)))

    def do_start_grab(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        return True
        return False

    def do_let_go(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    if self.grabbed:
                        return True
        return False
