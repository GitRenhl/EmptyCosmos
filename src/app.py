import pyxel
from src import state as State


class App:
    def __init__(self):
        pyxel.init(256, 256, fps=60)
        self.PYXEL_WIDTH_CENTER = pyxel.width // 2
        self.PYXEL_HEIGHT_CENTER = pyxel.height // 2

        states = {
            'mainmenu': State.MainMenuState,
            'gameplay': State.GameplayState,
        }

        self.state_machine = State.StateMachine(self, states)
        self.state_machine.change('mainmenu')

        pyxel.run(self.update, self.draw)

    @staticmethod
    def get_text_pix_width(text):
        return len(text) * pyxel.FONT_WIDTH

    def _draw_mouse(self):
        x, y = pyxel.mouse_x+1, pyxel.mouse_y + 1

        pyxel.line(x, y, x + 3, y + 3, 1)
        pyxel.line(x, y, x + 2, y, 1)
        pyxel.line(x, y, x, y + 2, 1)
        y -= 1
        pyxel.line(x, y, x + 3, y + 3, 7)
        pyxel.line(x, y, x + 2, y, 7)
        pyxel.line(x, y, x, y + 2, 7)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        self._draw_mouse()
