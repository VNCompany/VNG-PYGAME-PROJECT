import random


def check_intersection_pre(el, rect):
    return rect[0] <= el[0] <= rect[3] and rect[1] <= el[1] <= rect[2] or \
           rect[0] <= el[3] <= rect[3] and rect[1] <= el[1] <= rect[2] or \
           rect[0] <= el[0] <= rect[3] and rect[1] <= el[2] <= rect[2] or \
           rect[0] <= el[3] <= rect[3] and rect[1] <= el[2] <= rect[2]


def check_intersection(xy1: tuple, xy2: tuple, size: tuple):
    ax = xy1[0]
    ay = xy1[1]
    ax1 = ax + size[0]
    ay1 = ay + size[1]

    bx = xy2[0]
    by = xy2[1]
    bx1 = bx + size[0]
    by1 = by + size[1]

    return check_intersection_pre((ax, ay, ax1, ay1), (bx, by, bx1, by1))


def characters_generator(count: int, q: int, size: tuple, add_width: int = 300):
    points = []

    min_width = 950
    width = (count * size[0] * size[1]) // 500 + add_width + 102 + min_width

    q_counter = 0
    for i in range(count):
        not_valid = True
        while not_valid:
            x = random.randrange(min_width, width)
            y = random.randrange(5, 394)

            not_valid = False
            for point in points:
                if check_intersection((x, y), (point[0], point[1]), size):
                    not_valid = True
                    break

            if not not_valid:
                if q_counter == q:
                    q_counter = 0
                    points.append((x, y, "m"))
                else:
                    points.append((x, y, "e"))
                    q_counter += 1
    return points
