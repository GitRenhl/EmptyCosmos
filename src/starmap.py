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
        self.pos_hovered_system = ()
        self.pos_selected_system = ()
        self.selected_system = None

        self.gen_new_map()

    def clear(self):
        self.stars_systems.clear()
        self.pos_hovered_system = ()
        self.pos_selected_system = ()

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
        self.clear()
        num_of_stars = 500  # int(self.size[0] * self.size[1] * 0.01)
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
            valid = False

            star_system = StarSystem(unique_names.pop(), random.randint(1, 15))
            while not valid and i < 10:
                i += 1
                r_pos = (random.randint(0, self.size[0]),
                         random.randint(0, self.size[1]))
                valid = self._add_star(r_pos[0], r_pos[1], star_system)
            if i > 1 and not valid:
                print("Cant add star system. Attempts:", i)

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

    def select_hovered_system(self, *, move_camera=False):
        if move_camera and self.pos_selected_system and self.is_selected_a_hover():
            s_pos = self.pos_selected_system
            self._cam.move_to(s_pos[0],
                              s_pos[1],
                              smooth=True)
        else:
            self.pos_selected_system = self.pos_hovered_system[::]
            self.selected_system = self.stars_systems.get(
                self.pos_selected_system)

    def _draw_circ_and_name(self, sys_pos, circ_col, name_col):
        dx, dy = self._cam.d_pos
        star_system_name = self.stars_systems.get(sys_pos).name
        x = sys_pos[0] - int(dx)
        y = sys_pos[1] - int(dy)
        name_length = len(star_system_name)
        center_x = name_length * 4 // 2
        pyxel.circb(x, y, 3, circ_col)
        pyxel.text(x - center_x, y - 10, star_system_name, name_col)

    def is_selected_a_hover(self):
        return self.pos_hovered_system == self.pos_selected_system

    def update(self):
        self.pos_hovered_system = self._pos_system_hov_by_mouse()

    def draw(self):
        dx, dy = self._cam.d_pos
        dx = int(dx)
        dy = int(dy)
        for pos, system in self.stars_systems.items():
            x = pos[0] - dx
            y = pos[1] - dy
            system.draw(x, y)

        if self.pos_hovered_system and not self.is_selected_a_hover():
            self._draw_circ_and_name(self.pos_hovered_system, 8, 6)

        if self.pos_selected_system:
            self._draw_circ_and_name(self.pos_selected_system, 11, 7)
