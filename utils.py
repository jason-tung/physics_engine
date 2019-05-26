from math import sin, cos
from config import moment_of_inertia_plates


def distance(point1, point2):
    a, b = point1
    c, d = point2
    return ((a - c)**2 + (b - d)**2)**0.5


def apollonius(a, b, c):

    def formula(x, y, z):
        # returns the median for x
        return ((2 * y**2 + 2 * z**2 - x**2)/4)**0.5
    res = []
    for i, j, k in (a, b, c), (b, c, a), (c, a, b):
        res.append(formula(i, j, k))
    return res


def rotate_point_about_origin(point, theta):

    x, y = point
    n_x = cos(theta) * x - sin(theta) * y
    n_y = sin(theta) * x + cos(theta) * y

    return n_x, n_y


def _find_com_points(points, masses):

    M = sum(masses)

    x_sum = 0
    y_sum = 0

    for (x, y), mass in zip(points, masses):
        x_sum += mass * x
        y_sum += mass * y

    return x_sum / M, y_sum / M


def _shoelace_area(points):
    #print(points)
    (ax, ay), (bx, by), (cx, cy) = points

    return abs(ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) / 2


def _build_triangle_point_mass(points):

    x = sum(i[0] for i in points) / len(points)
    y = sum(i[1] for i in points) / len(points)

    mass = _shoelace_area(points)

    return (x, y), mass


# Return true if line segments AB and CD intersect
# def intersect(A,B,C,D):
#     def ccw(A, B, C):
#         return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
#
#     return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B ,C) != ccw(A, B ,D)
def intersect(A,B,C,D):

    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
# return true if intersecting [x1,y1,x2,y2],[x1,y1,x2,y2]
def segment_intersection(line1, line2):

    if not intersect(*line1, *line2):
        return False

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def find_moment_of_inertia_triangle(points, mass):
    # triangle -> collection of N rectangular plates
    # I_plate = 1/12 * M(a^2 + b^2)
    # assume first point will be the central axis
    # break into moment_of_inertia_plates and then use parallel axis theorem
    # print(points)
    area = _shoelace_area(points)

    base = distance(points[1], points[2])

    leg1 = distance(points[0], points[1])
    leg2 = distance(points[0], points[2])

    altitude_length = 2 * area / base

    median_length = apollonius(base, leg1, leg2)[0]

    dx = altitude_length / moment_of_inertia_plates

    moment_of_inertia = 0

    for i in range(0, moment_of_inertia_plates):
        # iterate bottom up the triangle
        # you are i+1 / moment_of_inertia_plates completed

        multiplier = (moment_of_inertia_plates - (i + 0.5)) / moment_of_inertia_plates

        length = base * multiplier
        this_area = length * dx
        this_mass = (this_area / area) * mass
        moment_of_inertia += 1/12 * this_mass * (length**2 + dx**2)  # add the current moment of inertia
        moment_of_inertia += (median_length * multiplier)**2 * this_mass  # apply the parallel axis theorem MR^2
    #print(moment_of_inertia, mass)
    return moment_of_inertia

if __name__ == '__main__':
    print(find_moment_of_inertia_triangle([[0, -1], [1, 1], [0, 0]], 100))
