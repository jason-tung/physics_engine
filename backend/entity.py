from math import sin, cos
from maths.geometry import build_triangle_point_mass, shoelace_area, find_com, find_moment_of_inertia_triangle
from maths.vector import Vector2D
from math import pi


class Entity(object):

    def __init__(self, mass, col_ticks=1):
        self.x = Vector2D()
        self.v = Vector2D()

        self.o = 0  # theta
        self.w = 0  # omega
        self.static = False

        self.su = None  # static friction
        self.ku = None  # kinetic friction

        self.m = mass  # mass
        self.i = None  # moment of inertia

        # determine if handler should process these movements
        self.handler_update = False
        self.col_ticks = col_ticks

    def velocity(self, point):
        """
        Get the instantanous velocity of a point
        :param point: Vector2D
        :return: Vector2D
        """
        if not isinstance(point, Vector2D):
            point = Vector2D(*point)
        dist_vec = point - self.x
        tang_vec = dist_vec.unit().rotate(pi / 2) * dist_vec.magnitude() * self.w
        return self.v + tang_vec

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

    def __init__(self, mass, points, col_ticks=1):
        # calculate the center of mass
        super(Polygon, self).__init__(mass, col_ticks)
        if not isinstance(points[0], Vector2D):
            points = [Vector2D(*i) for i in points]
        self.x, self.area = self.center_of_mass(points)
        # print(self.x, 'COM')
        # translate all points to have center at 0, 0

        self._points = [i - self.x for i in points]
        self.i = self.moment_of_inertia_about_center()
        self.radius = self.set_radius()

    def center_of_mass(self, points):
        # break into many triangles
        # each point is part of two triangles
        cor = [sum(points) / len(points)]
        mass_points = []
        area = 0
        for i in range(len(points) - 1):
            triangle = cor + points[i:i + 2]
            # print(triangle)
            mass_points.append(build_triangle_point_mass(triangle))
            area += shoelace_area(triangle)
            # print(triangle, area)
        mass_points.append(build_triangle_point_mass(cor + [points[-1], points[0]]))
        area += shoelace_area(cor + [points[-1], points[0]])
        return Vector2D(*find_com(*zip(*mass_points))), area

    def moment_of_inertia_about_center(self):
        moi = 0
        cor = [Vector2D()]
        #  print(self._points)
        print(self.points)
        for i in range(len(self._points) - 1):
            triangle = cor + self._points[i:i + 2]
            area = shoelace_area(triangle)
            moi += find_moment_of_inertia_triangle(cor + self._points[i:i + 2], self.m * area / self.area)
        #  print(triangle, moi)

        moi += find_moment_of_inertia_triangle(cor + [self._points[-1], self._points[0]],
                                               self.m * shoelace_area(
                                                   cor + [self._points[-1], self._points[0]]) / self.area)
        # print('ed', _shoelace_area(cor + [self._points[-1], self._points[0]]), moi)
        return moi

    def set_radius(self):
        return max(i.magnitude() for i in self._points)

    @property
    def points(self):
        n_points = []
        for point in self._points:
            n_points.append(point.rotate(self.o) + self.x)
        return n_points


if __name__ == '__main__':

    points = []
    radius = 10
    n_sides = 360
    import matplotlib.pyplot as plt

    for theta in range(0, 360, 360 // n_sides):
        points.append([cos(pi / 180 * theta) * radius + 10, sin(pi / 180 * theta) * radius + 10])
    # print(points)
    plt.plot(*zip(*points))
    plt.show()
    # print(points)
    p = Polygon(1, points)
    p.o = 0
    print(p.points)
