import pygame
from utils import *
from block import Block


class CraftingTooltip:
    def __init__(self, rect: pygame.Rect, font: pygame.font.Font):
        self.shown = True
        self.rect = rect
        self.back_surf = fetch_texture(get_path("assets", "images", "craft_tip.png"))
        self.font = font

    def draw(self, surface: pygame.Surface, boxes: list[Block]):
        for box in boxes.__reversed__():
            if box.rect.collidepoint(pygame.mouse.get_pos()):
                if not box.grabbed:
                    surface.blit(self.back_surf, self.rect.topleft)
                    i1, i2, o1 = CRAFTINGS[box.tier]
                    sqrct = pygame.Rect(0, 0, 77, 77)
                    # i1
                    _ = fetch_text(f"{i1}", self.font)
                    sqrct.center = self.rect.move(39, 39).topleft
                    pygame.draw.rect(surface, (0, 0, 0), sqrct.inflate(2, 2))
                    pygame.draw.rect(surface, TIER_COLORS[i1-1], sqrct)
                    surface.blit(_, _.get_rect(center=self.rect.move(40, 40).topleft))
                    # i2
                    _ = fetch_text(f"{i2}", self.font)
                    sqrct.center = self.rect.move(139, 39).topleft
                    pygame.draw.rect(surface, (0, 0, 0), sqrct.inflate(2, 2))
                    pygame.draw.rect(surface, TIER_COLORS[i2-1], sqrct)
                    surface.blit(_, _.get_rect(center=self.rect.move(140, 40).topleft))
                    # o1
                    _ = fetch_text(f"{o1}", self.font)
                    sqrct.center = self.rect.move(-40, 39).topright
                    pygame.draw.rect(surface, (0, 0, 0), sqrct.inflate(2, 2))
                    pygame.draw.rect(surface, TIER_COLORS[o1-1], sqrct)
                    surface.blit(_, _.get_rect(center=self.rect.move(-40, 40).topright))
                    return
