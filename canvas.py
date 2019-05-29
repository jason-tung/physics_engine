# Import a library of functions called 'pygame'
import pygame
from math import pi
from entity import Polygon
from itertools import chain

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)


class Canvas:

    def __init__(self):
        self.h, self.v = 1500, 1000

        pygame.init()
        self.screen = pygame.display.set_mode((self.h, self.v))

    def build(self, objects):
        disp = [i.points for i in objects]

        l = min(i[0] for i in chain(*disp))
        r = max(i[0] for i in chain(*disp))

        d = min(i[1] for i in chain(*disp))
        u = max(i[1] for i in chain(*disp))

        # apply a scale + translation for each point
        # (l, d) -> 10, 10 (r, u) -> 490, 990

        size_v = u - d
        size_h = r - l

        scale_1 = (self.v - 20) / size_v
        scale_2 = (self.h - 20) / size_h

        self.scale = min(scale_1, scale_2)
        #print(l, r, d, u)


        def lin_transform(a, b):
        #    print(a, b)
            a -= l
            b -= d

        #   print(a, b)

            a *= self.scale
            b *= self.scale

            a += 10
            b += 10
            #print(a, b)
        #    print(a, b)
            return a, self.v - b

        self.transform_func = lin_transform
        self.objects = objects

    def update(self):
        disp = [i.points for i in self.objects]
        clock = pygame.time.Clock()

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        #clock.tick(30)

        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.

        # Clear the screen and set the screen background
        self.screen.fill(WHITE)

        # This draws a triangle using the polygon command

        for points in disp:
            #print([self.transform_func(*point) for point in points])
            pygame.draw.polygon(self.screen, BLACK, [self.transform_func(*point) for point in points], 2)

        # pygame.draw.polygon(screen, BLACK, p1.points, 5)
        # pygame.draw.polygon(screen, BLACK, p2.points, 5)
        pygame.transform.flip(self.screen, True, True)
        pygame.display.flip()


if __name__ == '__main__':
    p1 = Polygon(0, [(0, 0), (4, 0), (4, 4), (0, 4)])
    p2 = Polygon(0, [(2, 3.5), (-1, 9), (2, 9), (5, 6)])
    p1.o, p2.o = 0, 0

    c = Canvas([p1, p2])
    c.update()