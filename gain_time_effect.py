import pygame
from utils import *


class GainTimeEffect:
    def __init__(self, font: pygame.font.Font):
        self.surfaces = []
        self.font = font

    def show_gain(self, amount: float, pos: list[int, int]) -> None:
        self.surfaces.insert(0, {"surface": fetch_text(f"+{int(amount*10)/10}s", self.font), "pos": pos, "timer": 1})

    def draw(self, surface: pygame.Surface, deltatime: float) -> None:
        for _ in self.surfaces:
            _["surface"].set_alpha(int(clamp(_["timer"], 0, 1)*255))
            _["timer"] -= deltatime/75
            _["pos"][1] -= deltatime/5
            surface.blit(_["surface"], _["pos"])
            if _["timer"] < 0:
                self.surfaces.remove(_)
