import pyxel
from .base import BaseState


class MainMenuState(BaseState):

    def __init__(self, game):
        super().__init__(game)
        self.text1 = "MainMenu"
        self.text2 = "Press Enter to play.."
        x, y = pyxel.width//2, pyxel.height // 2
        self.text1_pos = (
            x - self._game.get_text_pix_width(self.text1) // 2,
            y - 5)
        self.text2_pos = (
            x - self._game.get_text_pix_width(self.text2) // 2,
            y + 5)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self._game.state_machine.change("gameplay")

    def draw(self):
        pyxel.cls(0)

        pyxel.text(*self.text1_pos, self.text1, 7)
        if pyxel.frame_count // 30 % 2:
            pass
        else:
            pyxel.text(*self.text2_pos, self.text2, 12)
