from math import sin, cos
from backend.maths.geometry import center_of_mass, shoelace_area, find_com, find_moment_of_inertia_triangle, \
    segment_intersection
from backend.maths.vector import Vector2D
from math import pi
from backend.convex import monotone_chain


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
        self.radius = self.set_radius()

    def set_radius(self):
        return max(i.magnitude() for i in self._points)

    def intersections(self, obj2):
        if self.x.distance(obj2.x) > self.radius + obj2.radius:
            return []
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
                assert segment_intersection(l1, l2) == segment_intersection(l2, l1)
                # print(l1, l2)
                if inters:
                    intersections.append(inters)
        # print(intersections, 'INTERSECTIONS')
        return intersections

    @property
    def points(self):
        n_points = []
        for point in self._points:
            n_points.append(point.rotate(self.o) + self.x)
        return n_points


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
