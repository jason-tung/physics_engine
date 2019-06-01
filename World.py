from backend.collision_handler import Handler
from frontend.canvas import Canvas
from math import sin, cos
from heapq import *
from config import AUTO_ZOOM
from backend.quantity import *
from debug_tools.collision import assert_collisions


class World:

    def __init__(self):

        self.objects = []
        self.canvas = Canvas()
        self.handler = Handler(self)
        self.handler.objects = self.objects
        self.heap = []
        self.tick = 0

    def add_heap_unit(self, quantity: [Torque, Force]):
        # print(quantity, type(quantity))
        # print(self.heap)
        if isinstance(quantity, Torque):
            if quantity.t == 0:
                return
        else:
            if quantity.frc_func().magnitude() == 0:
                return

        if quantity.applier:
            if not any(type(i) == type(quantity) and i.obj == quantity.obj and i.applier == quantity.applier for _, i in self.heap):
                heappush(self.heap, (self.tick + quantity.n_ticks, quantity))

        else:
            heappush(self.heap, (self.tick + quantity.n_ticks, quantity))

        # print('FINAL', self.heap)

    def tick_forces(self):
        print(self.heap)
        for _, i in self.heap:
            # if i.__class__ == Torque: continue
            i.apply()
            print(i, 'applied', i.obj)
            #print(i.__dict__)

        while self.heap and self.heap[0][0] <= self.tick:
            #print(self.heap[0][0], self.tick)
            _, quantity = heappop(self.heap)
            # if quantity.__class__ == Torque: continue
            quantity.apply()
        print('APPLIED', self.objects)

    def add_object(self, obj):
        self.objects.append(obj)

    def rebuild_canvas(self):
        self.canvas.build(self.objects)

    def mainloop(self):
        while True:
            print('\n', self.tick, '\n')
            assert_collisions(self.objects)
            self.tick_forces()
            print(self.heap)

            if AUTO_ZOOM:
                self.canvas.build(self.objects)
            for i in self.objects:
                print(i)

            for frc in self.handler.tick():
                pass
            self.canvas.update()
            self.tick += 1
            assert_collisions(self.objects)


if __name__ == '__main__':
    from backend.quantity import Gravity
    from maths.vector import Vector2D
    w = World()
    x = 9
    p1 = Polygon(10000, [(-10, 500), (-10, 510), (10, 510), (10, 500)])
    p3 = Polygon(10000, [(-20-x, 511), (-20-x, 521), (0-x, 521), (0-x, 511)])
    points = []
    radius = 500
    n_sides = 50
    from math import pi
    for theta in range(0, 360, 360//n_sides):
        points.append([cos(pi/180 * theta) * radius, sin(pi/180 * theta) * radius])

    p2 = Polygon(10**16, points)
    # p2.v = Vector2D(0.01, 1)
    # p3 = Polygon(1000000000000, [(20, 5), (21, 5), (21, 6), (20, 6)])
    t = Torque(p1, 10, 1, 10)
    #p1.v = Vector2D(0.23, -0.1)
    w.add_heap_unit(t)
    active = [p1, p3, p2]
    for g in gen_gravs(active):
        w.add_heap_unit(g)
    for i in active:
        w.add_object(i)
    print(p1.points)
    print(p2.points)
    print("what?")
    w.rebuild_canvas()
    w.mainloop()