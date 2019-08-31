import pyxel
from src.mymath import Vec2, lerp


class Camera:
    _half_screen = (0, 0)

    def __init__(self, x, y):
        self._pos = Vec2(x, y)
        self._target_pos = Vec2(x, y)
        if Camera._half_screen == (0, 0):
            Camera._half_screen = (pyxel.width // 2, pyxel.height // 2)

    @property
    def position(self):
        return Vec2(self._pos)

    @property
    def d_pos(self):
        return self._pos - self._half_screen

    def move_to(self, x, y, *, smooth=False):
        if smooth:
            self._target_pos.x = x
            self._target_pos.y = y
        else:
            self._target_pos.x = x
            self._target_pos.y = y
            self._pos.x = x
            self._pos.y = y

    def update(self):
        self._pos.x = lerp(self._pos.x, self._target_pos.x, 0.1)
        self._pos.y = lerp(self._pos.y, self._target_pos.y, 0.1)
        # self._pos = self._pos.slerp(self._target_pos, 0.1)
