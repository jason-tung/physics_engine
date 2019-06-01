def assert_collisions(objs):

    for i in range(len(objs)):
        for j in range(i+1, len(objs)):
            h = objs[i].intersections(objs[j])
            assert not h