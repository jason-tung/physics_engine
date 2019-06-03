from heapq import *


def broad_sweep(objs):

    AABB = [(obj.AABB, obj) for obj in objs]
    AABB.sort(key=lambda x: x[0])
    # key_points = sorted({vec.x for i in AABB for vec in i[0]})

    def solve1D(AABB):
        """
        Only check for intersections in the "y" direction, ignore x
        :param objs: AABB created in broad_sweep
        :return: list of potential intersections in this dimension
        """
        # print('AABB', AABB)
        # print(AABB[0][0][0].x, AABB[0][0][0].y)
        AABB = sorted(AABB, key=lambda x: (x[0][0].y, x[0][1].y))
        # print([i[0] for i in AABB])
        inters = set()
        heap = []

        for i in AABB:
            obj = i[1]
            x1, x2 = i[0][0].y, i[0][1].y
           #  print(x1, x2)
            while heap and heap[0][0] <= x1:
                heappop(heap)

            for i in range(len(heap)):
                inters.add(frozenset({obj, heap[i][-1]}))
            heappush(heap, (x2, id(obj), obj))
        # print(inters)
        return inters

    heap = []
    inters = set()

    for i, obj in AABB:
        x1, x2 = i[0].x, i[1].x
        # print(x1, x2)
        while heap and heap[0][0] <= x1:
            heappop(heap)
        heappush(heap, (x2, i, obj))
        inters |= solve1D([[i[1], i[2]] for i in heap])
    print(len(inters))
    return inters


