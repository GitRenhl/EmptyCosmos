import pyxel
import random
import string
from src.mymath import Vec2


class StarSystem:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def draw(self, x, y):
        pyxel.pix(x, y, self.color)


class StarMap:
    def __init__(self, camera):
        self._cam = camera
        self.d_scale = 1  # TODO add scale
        self.size = (500, 500)
        self.stars_systems = {}
        self.hovered_system_pos = ()
        self.selected_system_pos = ()

        self.gen_new_map()

    def _add_star(self, x, y, system, *, force=False):
        pos = x, y
        if not force and self.stars_systems.get(pos):
            return False

        self.stars_systems[pos] = system
        return True

    @staticmethod
    def _gen_s_system_name(pos):
        ascii_upp = string.ascii_uppercase
        digs = string.digits

        def get_random_char():
            return random.choice(ascii_upp)

        def get_random_char_or_num():
            char = random.choice(ascii_upp + digs)
            return char

        full_name = ""
        prefix = ""
        code = ""
        name = ""
        for _ in range(3):
            prefix += get_random_char()

        for _ in range(4):
            code += get_random_char_or_num()
            name += get_random_char_or_num()

        full_name = f"{prefix} {code}-{name}"

        return full_name

    def gen_new_map(self):
        self.stars_systems.clear()
        num_of_stars = 1000  # int(self.size[0] * self.size[1] * 0.01)
        # print(num_of_stars)
        self._add_star(0, 0, StarSystem("SOL", 7))
        unique_names = set()
        for _ in range(num_of_stars):
            while True:
                tmp = len(unique_names)
                new_name = self._gen_s_system_name(0)
                unique_names.add(new_name)
                if tmp < len(unique_names):
                    break
                else:
                    print("Same name was generated", new_name)

        for _ in range(num_of_stars):
            i = 0
            valid = True

            star_system = StarSystem(unique_names.pop(), random.randint(1, 15))
            while valid and i < 10:
                i += 1
                r_pos = (random.randint(0, self.size[0]),
                         random.randint(0, self.size[1]))
                valid = not self._add_star(r_pos[0], r_pos[1], star_system)
            if i > 1:
                print("When added system:", i, valid)

    def _pos_system_hov_by_mouse(self):
        sys_position = ()
        cmx = int(self._cam.d_pos.x) + pyxel.mouse_x
        cmy = int(self._cam.d_pos.y) + pyxel.mouse_y
        MARGIN = 3
        margin_range = range(-MARGIN, MARGIN+1)
        systems = []
        for y in margin_range:
            for x in margin_range:
                mpos = cmx - x, cmy - y
                system = self.stars_systems.get(mpos)
                if system:
                    systems.append(mpos)
        if len(systems) == 1:
            sys_position = systems[0]

        elif len(systems) > 1:
            best_distance = float("inf")
            mpos = Vec2(cmx, cmy)
            for pos in systems:
                distance = mpos.distance_to(pos)
                if distance < best_distance:
                    best_distance = distance
                    sys_position = pos

        return sys_position

    def select_hover_system(self, *, move_camera=False):
        if move_camera and self.selected_system_pos and self.is_hovered_a_selected():
            s_pos = self.selected_system_pos
            self._cam.move_to(s_pos[0],
                              s_pos[1],
                              smooth=True)
        else:
            self.selected_system_pos = self.hovered_system_pos[::]

        if self.hovered_system_pos:
            return True
        else:
            return False

    def _draw_circ_and_name(self, sys_pos, circ_col, name_col):
        dx, dy = self._cam.d_pos
        x, y = sys_pos
        system = self.stars_systems.get((x, y)).name
        x -= dx
        y -= dy
        name_len = len(system)
        center_x = name_len * 4 // 2
        pyxel.circb(x, y, 3, circ_col)
        pyxel.text(x - center_x, y - 10, system, name_col)

    def is_hovered_a_selected(self):
        return self.hovered_system_pos == self.selected_system_pos

    def update(self):
        self.hovered_system_pos = self._pos_system_hov_by_mouse()

    def draw(self):
        dx, dy = self._cam.d_pos
        for pos, system in self.stars_systems.items():
            x = pos[0] - dx
            y = pos[1] - dy
            system.draw(x, y)

        if self.hovered_system_pos and not self.is_hovered_a_selected():
            self._draw_circ_and_name(self.hovered_system_pos, 8, 6)

        if self.selected_system_pos:
            self._draw_circ_and_name(self.selected_system_pos, 11, 7)
