from math import sin, cos


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


def find_moment_of_inertia():
    pass


if __name__ == '__main__':
    pass
