from collision_handler import Handler
from canvas import Canvas
from math import sin, cos
from entity import Polygon
from utils import distance
from heapq import *
from config import AUTO_ZOOM
from math import acos


class Quantity:
    def __init__(self):
        self.n_ticks = None

    def apply(self):
        pass

    def __le__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __eq__(self, other):
        return True


class Force(Quantity):

    def __init__(self, object: Polygon, force, n_ticks):
        """
        :param object:
        :param n_ticks:
        :param fx:
        :param fy:
        :param magnitude:
        :param target:
        """
        if n_ticks == 0: raise ValueError("duration of force cannot be 0")
        super(Force, self).__init__()
        self.obj = object

        if hasattr(force, '__call__'):
            self.frc_func = force
        else:
            self.frc_func = lambda: force

        self.n_ticks = n_ticks
        self.ticked = False

    def apply(self):
        # newton's second law
        fx, fy = self.frc_func()
        if not self.ticked:
            self.ticked = True
        else:
            self.obj.ax -= self.ax
            self.obj.ay -= self.ay
        if not self.n_ticks: return False

        m = self.obj.m

        self.ax = fx / m
        self.ay = fy / m

        self.obj.ax += self.ax
        self.obj.ay += self.ay
        self.n_ticks -=1
        return True


class Torque(Quantity):

    def __init__(self, object: Polygon, magnitude, direction, n_ticks):
        super(Torque, self).__init__()
        # direction == 1 -> clockwise
        # direction == -1 -> counter clockwise

        self.obj = object
        self.t = magnitude * direction
        self.n_ticks = n_ticks
        self.ticked = False

    def apply(self):
        # torque = I * alpha
        if not self.n_ticks:
            self.obj.a -= self.alpha
            return False
        if not self.ticked:
            i = self.obj.i
            self.alpha = self.t / i

            self.obj.a += self.alpha
            self.ticked = True

        self.n_ticks -= 1
        return True


class World:

    def __init__(self):

        self.objects = []
        self.canvas = Canvas()
        self.handler = Handler()
        self.handler.objects = self.objects
        self.heap = []
        self.tick = 0

    def add_heap_unit(self, quantity: Quantity):
        heappush(self.heap, (self.tick + quantity.n_ticks, quantity))

    def tick_forces(self):

        for _, i in self.heap:
            i.apply()
            print(i.__dict__)

        while self.heap and self.heap[0][0] <= self.tick:
            print(self.heap[0][0], self.tick)
            _, quantity = heappop(self.heap)

    def tick_velocities(self):
        for i in self.objects:
            i.tick_velocities()

    def add_object(self, obj):
        self.objects.append(obj)

    def rebuild_canvas(self):
        self.canvas.build(self.objects)

    def mainloop(self):
        while True:
            self.tick_forces()
            self.tick_velocities()

            if AUTO_ZOOM: self.canvas.build(self.objects)
            for i in self.objects:
                if i.m == 1000:
                    pass
                    # print(i.ax, i.ay)

                i.tick_movement_no_collisions()
            self.canvas.update()
            self.tick += 1


if __name__ == '__main__':
    from gravity import gravity
    w = World()
    p1 = Polygon(1000, [(0, 0), (4, 0), (4, 4), (0, 4)])
    p2 = Polygon(10**9, [(2, 3.5), (-1, 9), (2, 9), (5, 6)])
    points = []
    radius = 3
    n_sides = 300
    from math import pi
    for theta in range(0, 360, 360//n_sides):
        points.append([cos(pi/180 * theta) * radius + 10, sin(pi/180 * theta) * radius + 10])

    p2 = Polygon(10**10, points)


    #p3 = Polygon(1000000000000, [(20, 5), (21, 5), (21, 6), (20, 6)])
    t = Torque(p1, 10, 1, 10)
    g = gravity(p1, p2)
    p1.vx = 0.25
    w.add_heap_unit(g)
    w.add_heap_unit(t)
    for i in [p1, p2]:
        w.add_object(i)
    print(p1.points)
    print(p2.points)
    print("what?")
    w.rebuild_canvas()
    w.mainloop()

    p1.vx = 0.015
