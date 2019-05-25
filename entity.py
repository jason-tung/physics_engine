from config import tick_speed
from utils import rotate_point_about_origin, _build_triangle_point_mass, _find_com_points
from math import sin, cos


class Entity(object):

    def __init__(self, mass):

        self.x = None
        self.y = None

        self.vx = None
        self.vy = None

        self.ax = None
        self.ay = None

        self.o = None  # theta
        self.w = None  # omega
        self.a = None  # alpha
        self.static = False

        self.su = None  # static friction
        self.ku = None  # kinetic friction

        self.m = mass  # mass
        self.i = None  # moment of inertia

        # determine if handler should process these movements
        self.handler_update = False

    def load(self, d):

        for k, v in d.items():
            setattr(self, k, v)

    def __hash__(self):
        return id(self)


# class Circle(Entity):
#
#     def __init__(self, mass, center, radius):
#         super(Circle, self).__init__(mass)
#         self.radius = radius
#         self.center = center
#
#     def collision(self, other): # circles only
#         return ((self.x - other.x)**2+(self.y - other.y)**2)**.5 <= max(self.radius, other.radius)


class Polygon(Entity):

    def __init__(self, mass, points):
        # calculate the center of mass
        super(Polygon, self).__init__(mass)

        self.x, self.y = self.center_of_mass(points)
        # translate all points to have center at 0, 0

        self._points = [[x - self.x, y - self.y] for x, y in points]

    def center_of_mass(self, points):
        # break into many triangles
        # each point is part of two triangles
        tmp_x = sum(i[0] for i in points) / len(points)
        tmp_y = sum(i[1] for i in points) / len(points)
        cor = [[tmp_x, tmp_y]]
        mass_points = []
        for i in range(len(points)-1):
            mass_points.append(_build_triangle_point_mass(cor + points[i:i+2]))
        mass_points.append(_build_triangle_point_mass(cor + [points[-1], points[0]]))

        return _find_com_points(*zip(*mass_points))



    @property
    def points(self):
        n_points = []
        for point in self._points:
            x, y = rotate_point_about_origin(point, self.o)
            x += self.x
            y += self.y
            n_points.append(point)
        return n_points

    def tick_forces(self):

        self.vx += self.ax / tick_speed
        self.vy += self.ay / tick_speed

        self.w += self.a / tick_speed

if __name__ == '__main__':
    p = Polygon(10, [[0, 0], [1, 1], [0, 1], [1, 0]])
    print(p.x, p.y)