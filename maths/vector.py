from math import sin, cos


class Vector2D:

    __slots__ = 'x', 'y'

    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self + Vector2D(other, other)
        return Vector2D(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -(self - other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self - Vector2D(other, other)
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return Vector2D(self.x / other, self.y / other)

    def __rtruediv__(self, other):
        return Vector2D(other / self.x, other / self.y)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __getitem__(self, index):

        ret = [self.x, self.y]
        return ret[index]

    def __repr__(self):
        return f'<{self.x:.2f}, {self.y:.2f}>'

    def magnitude(self):

        return (self.x ** 2 + self.y ** 2) ** 0.5

    def rotate(self, theta):

        x, y = self

        n_x = cos(theta) * x - sin(theta) * y
        n_y = sin(theta) * x + cos(theta) * y

        return Vector2D(n_x, n_y)

    def distance(self, vector):
        x1, y1 = self
        x2, y2 = vector
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


class PseudoVector:

    def __init__(self, magnitude=0, direction=0):
        self.mag = magnitude
        self.dir = direction
