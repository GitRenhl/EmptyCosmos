class BaseState:
    __slots__ = ("_game")

    def __init__(self, game):
        self._game = game

    def update(self):
        pass

    def draw(self):
        pass

    def enter(self, *args, **kwargs):
        pass

    def exit(self):
        return None
