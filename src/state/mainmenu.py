import pyxel
import random as rand
from . import BaseState


class MainMenuState(BaseState):

    def __init__(self, game):
        super().__init__(game)
        self.text = "Press ENTER to play.."
        self.text_color = 1

        text_size = self._game.get_text_pix_width(self.text)
        self.text_pos = (
            self._game.PYXEL_WIDTH_CENTER - text_size // 2,
            self._game.PYXEL_HEIGHT_CENTER)

        self.particles = []
        for _ in range(200):
            x = rand.randint(-10, pyxel.width + 10)
            y = rand.randint(-10, pyxel.height + 10)
            z = rand.randint(1, 6)
            self.particles.append([x, y, z])
        self.particles = tuple(self.particles)
        self.particles_color = 1

    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self._game.state_machine.change("gameplay")

        for position in self.particles:
            position[0] += 0.5 / (position[2] / 10 + 1)
            position[0] %= pyxel.width

            # position[1] += 0.1 / (position[2] / 10 + 1)
            # position[1] %= pyxel.height

    def draw(self):
        pyxel.cls(0)
        # m_pos = (
        #     (pyxel.mouse_x - self._game.PYXEL_WIDTH_CENTER) * 0.01,
        #     (pyxel.mouse_y - self._game.PYXEL_HEIGHT_CENTER) * 0.01
        # )

        for position in self.particles:
            x, y, z = position
            # x += m_pos[0] / (z * 10)
            # y += m_pos[1] / (z * 10)

            pyxel.pix(int(x), int(y), self.particles_color + (6-z))

        if pyxel.frame_count // 30 % 2:
            pyxel.text(*self.text_pos, self.text, self.text_color)
        if pyxel.frame_count % 30 == 29:
            self.text_color = (self.text_color + 1) % 15 + 1
