from math import sin, cos, acos


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
        if type(other) == Vector2D:
            return self.x * other.x + self.y * other.y
        elif type(other) == int or type(other) == float:
            return Vector2D(self.x * other, self.y * other)
        elif type(other) == Matrix22:
            return other * self
        else:
            assert False

    def __rmul__(self, other):
        if type(other) == Matrix22:
            return Vector2D(other.col1.x * self.x + other.col2.x * self.y,
                            other.col1.y * self.x + other.col2.y * self.y)
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

    def __hash__(self):
        return hash((self.x, self.y))

    # can be sorted lexicographically
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x, self.y).__lt__((other.x, other.y))

    def __gt__(self, other):
        return (self.x, self.y).__gt__((other.x, other.y))

    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))

    def cross(self, other):
        if type(other) == Vector2D:
            return self.x * other.y - self.y * other.x
        elif type(other) == float or type(other) == int:
            return Vector2D(-other * self.y, other * self.x)
        else:
            assert False

    def crossXY(self, other):
        x0 = self.x
        x1 = self.y
        # x1y0 = x1 * other.x
        # x0y1 = x0 * other.y
        return Vector2D(x1 * other.cross(self), x0 * self.cross(other))

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

    def angle(self, other):
        try:
            return acos(self * other / (self.magnitude() * other.magnitude()))
        except ZeroDivisionError:
            return 0

    def unit(self):
        return self / self.magnitude()

    def project(self, other):
        # return proj_other (self)
        # other -> u
        # self -> v
        try:
            return (other * self) / self.magnitude() * self.unit()
        except ZeroDivisionError:
            return Vector2D()

    def set(self, x, y):
        self.x = x
        self.y = y


class Matrix22:

    def __init__(self, v1=None, v2=None):

        if v1 is not None and v2 is not None:
            self.col1 = v1
            self.col2 = v2
        elif v1 is not None and type(v1) == int or type(v1) == float:
            c = cos(v1)
            s = sin(v1)
            self.col1 = Vector2D(c, s)
            self.col2 = Vector2D(-s, c)
        else:
            self.col1 = Vector2D()
            self.col2 = Vector2D()

    def invert(self):

        a, b, c, d, = self.col1.x, self.col2.x, self.col1.y, self.col2.y
        det = a * d - b * c
        assert det != 0
        det = 1 / det

        res = Matrix22()
        res.col1.x = det * d
        res.col2.x = -det * b
        res.col1.y = -det * c
        res.col2.y = det *a

        return res

    def transpose(self):

        return Matrix22(Vector2D(self.col1.x, self.col2.x), Vector2D(self.col1.y, self.col2.y))

    def __mul__(self, other):

        if type(other) == Matrix22:
            return Matrix22(self * other.col1, self * other.col2)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __abs__(self):
        return Matrix22(abs(self.col1), abs(self.col2))

    def __add__(self, other):
        return Matrix22(self.col1 + other.col1, self.col2 + other.col2)