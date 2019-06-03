from math import sqrt
from backend.maths.vector import Vector2D

dist = float('inf')


def support_poly(polygon, direction):
    best_point = polygon[0]
    best_dot = best_point * direction
    for i in range(1, len(polygon)):
        p = polygon[i]
        d = p * direction

        if d > best_dot:
            best_dot = d
            best_point = p
    return best_point


def support_circle(circle, direction):
    mag = sqrt(direction * direction)
    s = circle[1] / mag
    center = circle[0]
    return Vector2D(center[0] + s * direction[0], center[1] + s * direction[1])


def support(poly1, poly2, support1, support2, direction):
    return support1(poly1, direction) - support2(poly2, -direction)


def collide_poly_poly(poly1, poly2):
    return collide(poly1, poly2, support_poly, support_poly)


def collide_poly_circle(poly, circle):
    return collide(poly, circle, support_poly, support_circle)


def collide(shape1, shape2, support1, support2):
    s = support(shape1, shape2, support1, support2, Vector2D(-1, -1))
    simplex = [s]
    d = -s

    for i in range(100):
        a = support(shape1, shape2, support1, support2, d)
        # print(a)

        if a * d < 0:
            return False

        simplex.append(a)

        if do_simplex(simplex, d):
            return True

    raise RuntimeError("infinite loop in GJK algorithm")


def do_simplex(simplex, d):
    l = len(simplex)

    if l == 2:
        b = simplex[0]
        a = simplex[1]
        a0 = -a
        ab = b - a

        if ab * a0 >= 0:
            cross = ab.crossXY(a0)
            d.x = cross.x
            d.y = cross.y
        else:
            simplex.pop(0)
            d.x = a0.x
            d.y = a0.y
    else:
        c = simplex[0]
        b = simplex[1]
        a = simplex[2]
        a0 = -a
        ab = b - a
        ac = c - a

        if ab * a0 >= 0:
            cross = ab.crossXY(a0)

            if ac * cross >= 0:
                cross = ac.crossXY(a0)

                if ab * cross >= 0:
                    return True
                else:
                    simplex.pop(1)
                    d.x = cross.x
                    d.y = cross.y
            else:
                simplex.pop(0)
                d.x = cross.x
                d.y = cross.y
        else:
            if ac * a0 >= 0:
                cross = ac.crossXY(a0)
                # print(ab, cross)
                if ab * cross >= 0:
                    return True
                else:
                    simplex.pop(1)
                    d.x = cross.x
                    d.y = cross.y
            else:
                simplex.pop(1)
                simplex.pop(0)
                d.x = a0.x
                d.y = a0.y

    return False
