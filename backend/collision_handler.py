from collections import defaultdict
from maths.geometry import segment_intersection
from backend.entity import Polygon
from backend.quantity import Force, Torque
from maths.vector import Vector2D
from math import sin, cos
from itertools import chain


class Handler:

    def __init__(self):
        # enqueue all lasting forces here
        # for each object compute all forces acting on it
        # get a net force
        self.objects = []

    def tick(self):
        return self.iterate_forces()

    @staticmethod
    def compute(obj1: Polygon, obj2: Polygon):
        # return the forces acted on object one by object two
        # first check for possible collision

        inters = Handler.collisions(obj1, obj2)

        if not inters:
            return None, None
        else:
            point = sum(inters) / len(inters)
            m = obj1.m + obj2.m

            v1 = obj1.velocity(point)
            v2 = obj2.velocity(point)

            # assume the collision is elastic
            # velocities now must be decomposed into v_com and v_point
            # for now decompose everything into v_com

            v1_f = (obj1.m - obj2.m) / m * v1 + (2 * obj2.m) / m * v2
            v2_f = (2 * obj1.m) / m * v1 + (obj1.m - obj2.m) / m * v2
            # print('\n\n\n', v1_f, v2_f, '\n\nHERE')
            if v1_f == v1 or v2_f == v2:
                return None, None

            collision_time = max(obj1.col_ticks, obj2.col_ticks)

            def decompose(obj, force_vec, point):
                # print(force_vec)
                ang = force_vec.angle(obj.x - point)
                dist = point.distance(obj.x)
                a, b = obj.velocity(point)
                t_magnitude = 1 if a * b < 0 else -1
                t_magnitude *= force_vec.magnitude() * dist * sin(ang) * 0.5
                f_vec = force_vec * cos(ang)

                return f_vec, t_magnitude

            f1, t1 = decompose(obj1, obj1.m * (v1_f - v1) / collision_time, point)
            f2, t2 = decompose(obj2, obj2.m * (v2_f - v2) / collision_time, point)
            print(f1, f2)
            print(t1, t2)
            print('\n\n\n\n\n')
            return (Force(obj1, f1, collision_time, applier=obj2),
                    Torque(obj1, abs(t1), 1 if t1 > 0 else -1, collision_time, applier=obj2)), \
                   (Force(obj2, f2, collision_time, applier=obj1),
                    Torque(obj2, abs(t2), 1 if t2 > 0 else -1, collision_time, applier=obj1))

    @staticmethod
    def collisions(obj1, obj2):
        if obj1.x.distance(obj2.x) > obj1.radius + obj2.radius:
            return []
        pts1 = obj1.points
        pts2 = obj2.points

        # print(pts1)
        # print(pts2)
        # print("pts1",pts1)
        # print("x,y", com1)

        intersections = []

        for i in range(len(pts1)):
            l1 = [pts1[i - 1], pts1[i]]
            # print("l1", l1)
            for j in range(len(pts2)):
                l2 = [pts2[j - 1], pts2[j]]
                inters = segment_intersection(l1, l2)
                # print(l1, l2)
                if inters:
                    intersections.append(inters)
        # print(intersections, 'INTERSECTIONS')
        return intersections

    def iterate_forces(self):

        apply = defaultdict(list)

        for i in range(len(self.objects)):
            update_fail = False
            for v_vect, w in [(self.objects[i].v, self.objects[i].w),
                              (Vector2D(), self.objects[i].w),
                              (self.objects[i].v, 0)]:
                self.objects[i].x += v_vect
                self.objects[i].o += w
                collision = False
                obj1 = self.objects[i]
                for j in range(i + 1, len(self.objects)):
                    obj2 = self.objects[j]

                    a, b = self.compute(obj1, obj2)
                    if a and not update_fail:
                        apply[obj1].extend(a)
                        apply[obj2].extend(b)
                        collision = True

                if collision:
                    self.objects[i].x -= v_vect
                    self.objects[i].o -= w
                    update_fail = True
                else:
                    break
            # if collision:
            #     self.objects[i].v = Vector2D()
            #     self.objects[]

        print(apply)

        return [j for i in apply.values() for j in i]
