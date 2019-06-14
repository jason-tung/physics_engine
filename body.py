from vector import Vector2D
from math import sin, cos


class Body:

    def __init__(self, mass, width):

        self.position = Vector2D()
        self.rotation = 0
        self.velocity = Vector2D()
        self.angular_velocity = 0
        self.force = Vector2D()
        self.torque = 0
        self.friction = 0.2

        self.width = width
        self.mass = mass
        self.inv_mass = 1 / mass
        self.I = mass * (width.x**2 + width.y**2) / 12
        self.invI = 1 / self.I

    @property
    def points(self):
        res = []
        for x, y in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
            res.append(self.position + 0.5 * Vector2D(x * self.width.x,
                                                y * self.width.y).rotate(self.rotation))
        return res

    def __hash__(self):
        return id(self)