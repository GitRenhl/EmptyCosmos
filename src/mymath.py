from pygame.math import Vector2 as Vec2

# class Vec2:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

#     @property
#     def xy(self):
#         return self.x, self.y


def lerp(a, b, t):
    return a + (b - a) * t
