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

    def load(self, d):

        for k, v in d.items():
            setattr(self, k, v)


class Circle(Entity):

    def __init__(self, mass, center, radius):
        super(Circle, self).__init__(mass)
        self.radius = radius
        self.center = center

    def collision(self, other): # circles only
        return ((self.x - other.x)**2+(self.y - other.y)**2)**.5 <= max(self.radius,other.radius)

        # convex hull - will need sp


class Polygon(Entity):

    def __init__(self, mass, points):
        # calculate the center of mass
        super(Polygon, self).__init__(mass)

        self.x = sum(i[0] for i in points)/len(points)
        self.y = sum(i[1] for i in points)/len(points)

        # compu