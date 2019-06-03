from backend.collision_handler import Handler
from frontend.canvas import Canvas
from math import sin, cos
from heapq import *
from config import AUTO_ZOOM, RENDER_RATE
from backend.quantity import *
import dill as pickle


class World:

    def __init__(self):

        self.objects = {}
        self.canvas = Canvas()
        self.handler = Handler(self)
        self.handler.objects = self.objects
        self.tick = 0

    def add_force(self, quantity: [Torque, Force]):
        heappush(self.heap, (self.tick + quantity.n_ticks, quantity))

    # print('FINAL', self.heap)

    def tick_forces(self):
        for i in self.objects:
            i.tick_forces()

    def add_object(self, obj):
        self.objects[obj.name] = obj

    def rebuild_canvas(self):
        self.canvas.build(self.objects.values())

    def mainloop(self):
        while True:
            print('\n', self.tick, '\n')
            self.tick_forces()
            print(self.heap)

            if self.tick % RENDER_RATE == 0:
                if AUTO_ZOOM:
                    self.canvas.build(self.objects.values())

                self.canvas.update()
            # for i in self.objects:
            #    print(i)
            self.handler.tick()

            self.tick += 1

    def save(self, path):
        self.canvas = None
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        self.canvas = Canvas()
        self.rebuild_canvas()

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as f:
            world = pickle.load(f)
            world.canvas = Canvas()
            world.rebuild_canvas()
            return world


if __name__ == '__main__':
    from backend.quantity import Gravity
    from backend.maths.vector import Vector2D
    from backend.entity import Polygon

    w = World()
    x = 6
    p1 = Polygon('p1', 10000, [(-10, 500), (-10, 510), (10, 510), (10, 500)])
    p3 = Polygon('p3', 10000, [(-20 - x, 511), (-20 - x, 521), (0 - x, 521), (0 - x, 511)])
    points = []
    radius = 500
    n_sides = 50
    from math import pi

    for theta in range(0, 360, 360 // n_sides):
        points.append([cos(pi / 180 * theta) * radius, sin(pi / 180 * theta) * radius])
    from random import shuffle

    shuffle(points)

    p2 = Polygon('p2', 0.25 * 10 ** 16, points)
    z = 1500
    active = []
    for i in range(50):
        y = i * 21
        p = Polygon(i, 10 ** 5, [(-20 + x, 500 + y),
                              (-20 + x, 520 + y),
                              (20 + x, 520 + y),
                              (20 + x, 500 + y)])

        active.append(p)
    active.append(p2)
    p3 = Polygon('p3', 10 ** 12, [(-150, 600), (-100, 600), (-100, 700), (-150, 700)])
    p3.v = Vector2D(-20, 10)
    active.append(p3)

    for g in gen_gravs(active):
        w.add_heap_unit(g)

    for i in active:
        w.add_object(i)
    print(p1.points)
    print(p2.points)
    print("what?")
    print("---+++")
    w.save("new_test.pkl")
    w.objects = []
    w = w.load("new_test.pkl")
    print("FDSFDSFDSFDSF")
    print(w.objects)
    print("+++---")
    w.mainloop()
