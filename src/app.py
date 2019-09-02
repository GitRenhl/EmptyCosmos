import pyxel
from src.camera import Camera
from src.starmap import StarMap
from src.mymath import Vec2


class App:
    def __init__(self):
        pyxel.init(256, 256, fps=60)
        # pyxel.mouse(True)

        self.camera = Camera(100, 100)
        self.star_map = StarMap(self.camera)

        self.last_map_pos = tuple(self.camera.d_pos)
        self.mouse_pos_when_press = None

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
        if pyxel.btn(pyxel.KEY_ALT):
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.star_map.gen_new_map()

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.star_map.select_hovered_system(move_camera=True)

        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
            self.mouse_pos_when_press = pyxel.mouse_x, pyxel.mouse_y
            self.last_map_pos = tuple(self.camera.position)

        if pyxel.btnr(pyxel.MOUSE_RIGHT_BUTTON):
            self.mouse_pos_when_press = None

        if self.mouse_pos_when_press:
            tmp_pos = Vec2(self.last_map_pos[::])
            old_mx, old_my = self.mouse_pos_when_press
            tmp_pos.x -= pyxel.mouse_x - old_mx
            tmp_pos.y -= pyxel.mouse_y - old_my

            self.camera.move_to(tmp_pos.x, tmp_pos.y, smooth=True)

        self.camera.update()
        self.star_map.update()

    def draw(self):
        pyxel.cls(0)
        self.star_map.draw()

#         star_system = self.star_map.selected_system
#         if star_system:
#             text = f"""Name:
#    {star_system.name}
# Type: {star_system.color}
# """
#             pyxel.rect(1, 1, 70, pyxel.height * 0.7, 1)
#             pyxel.text(3, 3, text, 7)
#             # pyxel.text(3, 17, star_system.name, 7)

        self._draw_mouse()
