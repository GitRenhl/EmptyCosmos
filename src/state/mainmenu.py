import pyxel
from . import BaseState


class MainMenuState(BaseState):

    def __init__(self, game):
        super().__init__(game)
        self.text = "Press Enter to play.."
        self.text_color = 12

        text_size = self._game.get_text_pix_width(self.text)
        self.text_pos = (
            self._game.PYXEL_WIDTH_CENTER - text_size // 2,
            self._game.PYXEL_HEIGHT_CENTER)


    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self._game.state_machine.change("gameplay")

    def draw(self):
        pyxel.cls(0)

        if pyxel.frame_count // 30 % 2:
            pyxel.text(*self.text_pos, self.text, self.text_color)
