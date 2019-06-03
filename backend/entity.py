from math import sin, cos
from backend.maths.vector import Vector2D
from math import pi
from backend.convex import hull


class Entity:

    def __init__(self, name, mass, col_ticks=1, loss=0.99):

        self.name = name

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
        self.loss = loss

        self.forces = []
        self.torques = []

    def velocity(self, point):
        # if self.v.magnitude() > 20: self.v = Vector2D(0.1, 0.1)
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

    def __hash__(self):
        return id(self)


class Polygon(Entity, hull.ConvexHull):

    def __init__(self, name, mass, points, col_ticks=1):
        # calculate the center of mass
        Entity.__init__(self, name, mass, col_ticks)
        hull.ConvexHull.__init__(self, points)

    def __repr__(self):
        return str({'m': self.m, 'x': self.x, 'v': self.v, 'w': self.w})


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
