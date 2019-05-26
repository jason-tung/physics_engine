from config import tick_speed
from utils import rotate_point_about_origin, _build_triangle_point_mass, _find_com_points, find_moment_of_inertia_triangle, _shoelace_area
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

        (self.x, self.y), self.area = self.center_of_mass(points)
        # translate all points to have center at 0, 0

        self._points = [[x - self.x, y - self.y] for x, y in points]
        self.i = self.moment_of_inertia_about_center()

    def center_of_mass(self, points):
        # break into many triangles
        # each point is part of two triangles
        tmp_x = sum(i[0] for i in points) / len(points)
        tmp_y = sum(i[1] for i in points) / len(points)
        cor = [[tmp_x, tmp_y]]
        mass_points = []
        area = 0
        for i in range(len(points)-1):
            triangle = cor + points[i:i+2]
            #print(triangle)
            mass_points.append(_build_triangle_point_mass(triangle))
            area += _shoelace_area(triangle)
            #print(triangle, area)
        mass_points.append(_build_triangle_point_mass(cor + [points[-1], points[0]]))
        area += _shoelace_area(cor + [points[-1], points[0]])
        return _find_com_points(*zip(*mass_points)), area

    def moment_of_inertia_about_center(self):
        moi = 0
        cor = [[0, 0]]
      #  print(self._points)
        for i in range(len(self._points)-1):
            triangle = cor + self._points[i:i+2]
            area = _shoelace_area(triangle)
            moi += find_moment_of_inertia_triangle(cor + self._points[i:i+2], self.m * area / self.area)
            print(triangle, moi)

        moi += find_moment_of_inertia_triangle(cor + [self._points[-1], self._points[0]],
                                               self.m * _shoelace_area(cor + [self._points[-1], self._points[0]]) / self.area)
        #print('ed', _shoelace_area(cor + [self._points[-1], self._points[0]]), moi)
        return moi


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

    points = []
    radius = 10
    n_sides = 360
    from math import pi
    import matplotlib.pyplot as plt

    for theta in range(0, 360, 360//n_sides):
        points.append([cos(pi/180 * theta) * radius, sin(pi/180 * theta) * radius])
    #print(points)
    plt.plot(*zip(*points))
    plt.show()
    #print(points)
    p = Polygon(1, points)
    #p = Polygon(1, [[0, 0], [0, 1], [1, 1], [1, 0]])
    print(p.x, p.y, p.area, p.i)