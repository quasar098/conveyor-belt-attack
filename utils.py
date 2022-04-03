from constants import *
from os import getcwd as _getcwd
from os.path import join as _join
from pygame import Surface as _Surface, SRCALPHA as _SRCALPHA
from math import sin as _sin, cos as _cos, pi as _pi
from pygame.font import Font as _Font
from pygame.mixer import Channel as _Channel, Sound as _Sound, set_num_channels as _setnum, get_num_channels as _getnum
from pygame.image import load as _load
# noinspection PyUnresolvedReferences
from numpy import clip as clamp, sin, cos, pi


texture_storage: dict[str, _Surface] = {}
text_storage: dict[str, _Surface] = {}
sound_storage: dict[str, _Sound] = {}
channels: list[_Channel] = []


def get_path(*path: str) -> str:
    return _join(_getcwd(), *path)


def play_sound(path: str, volume=0.4, looping=0) -> bool:
    """Returns true if the sound was played"""
    if _getnum() != 40:
        _setnum(40)
    if len(channels) == 0:
        for _ in range(40):
            channels.append(_Channel(_))
    if path not in sound_storage:
        try:
            sound_storage[path] = _Sound(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"no file {path}")
    for channel in channels:
        if not channel.get_busy():
            channel.set_volume(volume)
            channel.play(sound_storage[path], loops=looping)
            return True
    return False


def fetch_text(text: str, font: _Font) -> _Surface:
    if text not in text_storage:
        text_storage[text] = font.render(text, True, (0, 0, 0))
    return text_storage[text]


def fetch_texture(path: str) -> _Surface:
    if path not in texture_storage:
        try:
            texture_storage[path] = _load(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"no texture {path} exists!")
    return texture_storage[path]


def text_with_border(font: _Font,
                     text: str, color: Color,
                     outline_color: Color) -> _Surface:
    """shadow included"""
    width = 2
    precision = 8
    _ = font.render(text, True, outline_color)
    surf = _Surface((_.get_size()[0]+width*3, _.get_size()[1]+width*5), _SRCALPHA)
    _2 = font.render(text, True, (0, 0, 0, 1))
    _2.set_alpha(60)
    for i in range(precision):
        surf.blit(_2, (_sin(i/precision*_pi*2)*width+width*1.5, _cos(i/precision*_pi*2)*width+width*3.5))
    for i in range(precision):
        surf.blit(_, (_sin(i/precision*_pi*2)*width+width*1.5, _cos(i/precision*_pi*2)*width+width*1.5))
    surf.blit(font.render(text, True, color), (width*1.5, width*1.5))
    return surf


def cserp(val: float):
    """lerp but cosine interpolation instead of linear (from 0 to 1) (unclamped)"""
    return 1-(cos(val*pi)*0.5+0.5)
