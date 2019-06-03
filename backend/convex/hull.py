from math import sin, cos
from backend.maths.geometry import center_of_mass, segment_intersection, point_segment_distance
from backend.maths.vector import Vector2D
from math import pi
from backend.convex import monotone_chain
from config import collision_epsilon


class ConvexHull:

    def __init__(self, points):
        # calculate the center of mass
        if not isinstance(points[0], Vector2D):
            points = [Vector2D(*i) for i in points]
        self.x, self.area = center_of_mass(points)
        self.o = 0
        # print(self.x, 'COM')
        # translate all points to have center at 0, 0

        self._points = monotone_chain.build_convex([i - self.x for i in points])
        self.points = self.gen_points()

    @property
    def AABB(self):
        pts = self.points
        x1 = max(i.x for i in pts) + collision_epsilon
        x2 = min(i.x for i in pts) - collision_epsilon
        y1 = max(i.y for i in pts) + collision_epsilon
        y2 = min(i.y for i in pts) - collision_epsilon

        return Vector2D(x2, y2), Vector2D(x1, y1)

    def gen_points(self):
        n_points = []
        for point in self._points:
            n_points.append(point.rotate(self.o) + self.x)
        return n_points

    def __eq__(self, other):
        return self.x == other.x and self.o == other.o and self._points == other.__points

    def __hash__(self):
        return hash((self.x, self.o, self._points))

    def __setattr__(self, name, val):
        super(ConvexHull, self).__setattr__(name, val)
        if name in 'xo' and '_points' in self.__dict__:
            self.points = self.gen_points()

    def __getitem__(self, item):
        return self.points[item]

    def __len__(self):
        return len(self._points)

    def intersections(self, obj2):
        """
        Legacy code deprecated
        :param obj2:
        :return:
        """
        pts1 = self.points
        pts2 = obj2.points

        intersections = []

        for i in range(len(pts1)):
            l1 = [pts1[i - 1], pts1[i]]
            # print("l1", l1)
            for j in range(len(pts2)):
                l2 = [pts2[j - 1], pts2[j]]
                inters = segment_intersection(l1, l2)
                # if not inters: continue
                # assert segment_intersection(l1, l2) == segment_intersection(l2, l1)
                # print(l1, l2)
                if inters:
                    intersections.append(inters)
        # print(intersections, 'INTERSECTIONS')
        return intersections

    def distance(self, other):
        x = self.intersections(other)
        if x:
            f = sum(x) / len(x)
            return (0, (f, (f, f)))
        res = (float('inf'), None)
        for i in range(len(self)):
            for j in range(len(other)):
                seg1 = [self[i], self[i - 1]]
                seg2 = [other[j], other[j - 1]]
                # print(seg1, seg2)
                res = min(res,
                          (point_segment_distance(other[j], seg1), (other[j], seg1)),
                          (point_segment_distance(self[i], seg2), (self[i], seg2)))
        return res


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
    p = ConvexHull(1, points)
    p.o = 0
    print(p.points)
