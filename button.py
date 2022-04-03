import pygame
from utils import text_with_border, WHITE, BLACK, ORANGE, play_sound


class Button:
    def __init__(self, rect: pygame.Rect,
                 font: pygame.font.Font,
                 text: str,
                 callback=lambda *_: None,
                 callback_args=(),
                 sound_path: str = None):
        self.font = font
        self.text = text
        self.rect = rect
        self._text_surf = text_with_border(self.font, self.text, WHITE, BLACK)
        self.callback = callback
        self.callback_args = callback_args
        self.sound_path = sound_path

    def change_text(self, text: str):
        self.text = text
        self._text_surf = text_with_border(self.font, self.text, WHITE, BLACK)
        return self

    def set_callback(self, callback):
        self.callback = callback

    def set_callback_args(self, c_args):
        self.callback_args = c_args

    def draw(self, surface: pygame.Surface):
        border_width = 2
        rect = self.rect.move(0, int(self.rect.collidepoint(pygame.mouse.get_pos())*pygame.mouse.get_pressed(3)[0])*7)
        pygame.draw.rect(surface, BLACK, self.rect.move(0, 7))
        pygame.draw.rect(surface, ORANGE.lerp((0, 0, 0), 0.1),
                         self.rect.inflate(-border_width*2, -border_width*2).move(0, 7))
        pygame.draw.rect(surface, BLACK, rect)
        pygame.draw.rect(surface, ORANGE, rect.inflate(-border_width*2, -border_width*2))
        surface.blit(self._text_surf, self._text_surf.get_rect(center=rect.center))

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.callback(*self.callback_args)
                        if self.sound_path is not None:
                            play_sound(self.sound_path, 0.4)
