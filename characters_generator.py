import random
import time
from defines import WIDTH, HEIGHT


class IRect:
    def __init__(self, name, wh, *args):
        if len(args) == 4:
            p1 = args[0]
            p2 = args[1]
            p3 = args[2]
            p4 = args[3]
        elif len(args) == 3 and type(args[2]) is tuple:
            p1 = args[0]
            p2 = args[1]
            p3, p4 = args[2]
        elif len(args) == 3 and type(args[2]) is int:
            p1 = args[0]
            p2 = args[1]
            p3, p4 = args[2], args[2]
        elif len(args) == 1:
            p1, p2, p3, p4 = args[0]
        else:
            p1, p2, p3, p4 = 0, 0, 0, 0

        self.x1 = p1
        self.y1 = p2
        self.Name = name
        if wh:
            self.x2 = p1 + p3
            self.y2 = p2 + p4
            self.Width = p3
            self.Height = p4
        else:
            self.Width = p3 - p1
            self.Height = p4 - p2
            self.x2 = p3
            self.y2 = p4

    def get_coords(self, wh=False):
        if wh:
            return self.x1, self.y1, self.Width, self.Height
        else:
            return self.x1, self.y1, self.x2, self.y2

    def get_points(self):
        return self.x1, self.y1

    def get_tuple(self):
        return self.get_points() + (self.Name,)

    def __eq__(self, other):
        return (self.x1 == other.x1 and
                self.y1 == other.y1 and
                self.x2 == other.x2 and
                self.y2 == other.y2)

    def check_intersection(self, other):
        if self == other:
            return True
        if (self.x1 < other.x2 < self.x2) and (self.y1 < other.y2 < self.y2):
            return True
        if (self.x1 < other.x2 < self.x2) and (self.y1 < other.y1 < self.y2):
            return True
        if (self.x1 < other.x1 < self.x2) and (self.y1 < other.y2 < self.y2):
            return True
        if (self.x1 < other.x1 < self.x2) and (self.y1 < other.y1 < self.y2):
            return True
        return False


def characters_generator_old(count: int, m_probability: float, size: tuple, add_width: int = 300):
    points = []

    min_width = WIDTH + 200
    width = (count * size[0] * size[1]) // HEIGHT + 902 + min_width

    for i in range(count):
        not_valid = True
        while not_valid:
            x = random.randrange(min_width, width)
            y = random.randrange(2, HEIGHT - 104)
            rect = IRect("a", True, x, y, size)

            not_valid = False
            for point in points:
                if rect.check_intersection(IRect("b", True, point[0], point[1], size)):
                    not_valid = True
                    break

            if not not_valid:
                m_p = int(m_probability * 100)
                if m_p <= 0:
                    rect.Name = "e"
                elif m_p > 98:
                    rect.Name = "m"
                else:
                    rnd = random.randrange(m_p, 101)
                    if rnd == m_p:
                        rect.Name = "m"
                    else:
                        rect.Name = "e"
                points.append(rect.get_tuple())
    return points


def characters_generator(count: int, m_probability: float, size: tuple):
    start_x_pos = WIDTH + 200
    rows = HEIGHT // size[1]
    cols = count // rows * 3
    m_p = int(m_probability * 100)

    field = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(0)
        field.append(row)

    points = []
    for i in range(count):
        while True:
            r = random.randrange(0, rows * 100)
            c = random.randrange(0, cols * 100)
            r = r // 100
            c = c // 100
            if field[r][c] == 0:
                # Meteorite generation
                if m_p <= 0:
                    name = 1
                elif m_p > 98:
                    name = 2
                else:
                    rnd = random.randrange(m_p, 101)
                    if rnd == m_p:
                        name = 2
                    else:
                        name = 1
                field[r][c] = name
                break

    random.shuffle(field)
    for r in field:
        random.shuffle(r)

    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > 0:
                name = "e" if field[i][j] == 1 else "m"
                pos_x = start_x_pos + (j * size[0])
                pos_y = i * size[1]
                points.append((pos_x, pos_y, name))
    return points
