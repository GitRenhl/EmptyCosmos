from .base import BaseState


class StateMachine:

    __slots__ = ("__game",
                 "_states",
                 "_current_name",
                 "_current")

    def __init__(self, game, states={}):
        self.__game = game
        self._states = states
        self._current_name = None
        self._current = BaseState(self.__game)

    @property
    def current(self):
        return self._current

    def change(self, state_name, *enter_args, **enter_kwargs):
        self._states[state_name]
        if state_name == self._current_name:
            return
        self._current.exit()
        self._current = self._states[state_name](self.__game)
        self._current_name = state_name
        self._current.enter(*enter_args, **enter_kwargs)

    def update(self):
        self._current.update()

    def draw(self):
        self._current.draw()
