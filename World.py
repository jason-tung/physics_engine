from backend.collision_handler import Handler
from frontend.canvas import Canvas
from math import sin, cos
from heapq import *
from config import AUTO_ZOOM, RENDER_RATE
from backend.quantity import *
import json
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
            heappush(self.heap, (self.tick + quantity.n_ticks, quantity))

        # print('FINAL', self.heap)

    def tick_forces(self):
        # print(self.heap)
        for _, i in self.heap:
            # if i.__class__ == Torque: continue
            i.apply()
            # print(i, 'applied', i.obj)
            #print(i.__dict__)

        while self.heap and self.heap[0][0] <= self.tick:
            #print(self.heap[0][0], self.tick)
            _, quantity = heappop(self.heap)
            # if quantity.__class__ == Torque: continue
            quantity.apply()
        # print('APPLIED', self.objects)

    def add_object(self, obj):
        self.objects.append(obj)

    def rebuild_canvas(self):
        self.canvas.build(self.objects)

    def mainloop(self):
        while True:
            print('\n', self.tick, '\n')
            self.tick_forces()
            print(self.heap)

            if self.tick % RENDER_RATE == 0:
                if AUTO_ZOOM:
                    self.canvas.build(self.objects)

                self.canvas.update()
            #for i in self.objects:
            #    print(i)
            self.handler.tick()

            self.tick += 1

    def save_objs(self,*args):
        #save to a name if providede otherwise use default name "world"
        dump = [k.toJSON for k in self.objects]
        savename = "world.txt" if len(args) == 0 else args[0]
        with open("saved_worlds/" + savename, 'w') as f:
            json.dump(dump,f)

    def reload_with_json(self, filename):
        with open("saved_worlds/" + filename, 'r') as f:
            # for line in f:
            #     obj = line.strip().replace(" ","").split(",")
            #     for property in obj:
            #         kv_pair = property.split(":")
            #         print(kv_pair)
            return


if __name__ == '__main__':
    from backend.quantity import Gravity
    from maths.vector import Vector2D
    from random import randint
    w = World()
    x = 6
    p1 = Polygon(10000, [(-10, 500), (-10, 510), (10, 510), (10, 500)])
    p3 = Polygon(10000, [(-20-x, 511), (-20-x, 521), (0-x, 521), (0-x, 511)])
    points = []
    radius = 500
    n_sides = 50
    from math import pi
    for theta in range(0, 360, 360//n_sides):
        points.append([cos(pi/180 * theta) * radius, sin(pi/180 * theta) * radius])

    p2 = Polygon(0.5 * 10**16, points)
    z = 1500
    active = []
    for i in range(50):
        y = i * 21
        p = Polygon(10**5, [(-20 + x, 500 + y),
                            (-20 + x, 520 + y),
                            (20 + x, 520 + y),
                            (20 + x, 500 + y)])

        active.append(p)
    active.append(p2)
    p3 = Polygon(10**12, [(-150, 600), (-100, 600), (-100, 700), (-150, 700)])
    p3.v = Vector2D(20, 0)
    active.append(p3)

    for g in gen_gravs(active):
        w.add_heap_unit(g)

    for i in active:
        w.add_object(i)
    print(p1.points)
    print(p2.points)
    print("what?")
    w.rebuild_canvas()
    print("---+++")
    print(w.save_objs("new_test.txt"))
    w.objects = []
    w.reload_with_json("new_test.txt")
    print("+++---")
    #w.mainloop()