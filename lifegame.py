class LifeGame:
    def __init__(self, size=[10, 10]):
        """
        Life Game as Python class
        rule:
            When there are more than or less than three lives around a life, it will die.
            When there are three lives around a blank place, it will become alive.
        :param size: [width, height] or -1. When size=-1 it means no limit
        """
        from decimal import Decimal
        er = 0
        if type(size) in [float, int, Decimal]:
            if round(size) == -1:
                self._tpe = 1
                self._area = set()
            else:
                er = 1
        elif type(size) in [tuple, list]:
            if len(size) == 2:
                if type(size[0]) in [float, int, Decimal] and type(size[1]) in [float, int, Decimal]:
                    self._tpe = 0
                    self._width = round(size[0])
                    self._height = round(size[1])
                    self._area = [[0 for x in range(self._width)] for x in range(self._height)]
                else:
                    er = 1
            else:
                er = 1
        if er: raise ValueError("size: [width, height] or -1. When size=-1 it means no limit")

    def area(self):
        """
        To give you the area now
        :return: (list) self._area
        """
        return self._area

    def animate(self, pos=(0, 0)):
        """
        Let position 'pos' become alive.
        :param pos: (row, column)
        """
        if self._tpe == 0:
            self._area[pos[0]][pos[1]] = 1
        elif self._tpe == 1:
            self._area.add(pos)

    def kill(self, pos=(0, 0)):
        """
        Let position 'pos' die.
        :param pos: (row, column)
        """
        if self._tpe == 0:
            self._area[pos[0]][pos[1]] = 1
        elif self._tpe == 1 and pos in self._area:
            self._area.remove(pos)

    def count(self, pos=(0, 0)):
        num = 0
        if self._tpe == 0:
            l1 = len(self._area)
            l2 = len(self._area[0])
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if pos[0]+x < 0 or pos[1]+y < 0 or pos[0]+x >= l1 or pos[1]+y >= l2 or (x, y) == (0, 0): pass
                    else:
                        num += self._area[pos[0]+x][pos[1]+y]

        elif self._tpe == 1:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (pos[0]+x, pos[1]+y) in self._area and (x, y) != (0, 0):
                        num += 1

        return num

    def limited_area(self):
        """
        Convert infinity to finite
        :return:lifegame.LifeGame object
        """
        if self._tpe == 1:
            if self._area:
                rs = [a[0] for a in self._area]
                cs = [a[1] for a in self._area]
                rs = [r - min(rs) for r in rs]
                cs = [c - min(cs) for c in cs]
                limited = LifeGame([max(cs) + 1, max(rs) + 1])
                for x in zip(rs, cs):
                    limited.animate(x)
            else:
                limited = LifeGame([1, 1])
            return limited
        else:
            return self

    def unlimited_area(self):
        """
        Convert finite to infinity
        :return:lifegame.LifeGame object
        """
        if self._tpe == 0:
            unlimited = LifeGame(-1)
            for row in range(len(self._area)):
                for column in range(len(self._area[row])):
                    if round(self._area[row][column]) == 1:
                        unlimited._area.append((row, column))
            return unlimited
        else:
            return self

    def listpos(self):
        """
        List the positions to be checked
        :return: list
        """

    def printarea(self, p=['  ', '█'], sep=''):
        """
        Print the current status of the area
        :arg p:list, when alive print p[1], died print p[0]
        """
        if self._tpe == 0:
            s = ""
            k = 0
            for row in self._area:
                for i in row:
                    s += p[round(i)] + sep
                s += "\n"
                k += 1
            if k >= 50:
                for x in s.split("\n"):
                    print(x)
            else:
                print(s)
        else:
            # generate an equivalent finite graph for printing
            self.limited_area().printarea(p, sep)

    def check(self, detail=False):
        """
        Check and make changes
        :return:None
        """
        if self._tpe == 1:
            import time
            newarea = {k for k in self._area}
            cl = {k for k in self._area}  # find points that need to be checked
            for point in self._area:
                r, c = point
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        cl.add((r + x, c + y))
            # check every point in cl and make changes
            for point in cl:
                n = self.count(point)
                if n == 3 and not point in newarea:
                    if detail:
                        print("Ani", point)
                    newarea.add(point)
                elif (n > 3 or n < 2) and point in self._area:
                    if detail:
                        print("Del", point)
                    newarea.remove(point)

            self._area = newarea

        elif self._tpe == 0:
            newarea = [[c for c in r] for r in self._area]
            a, b = len(self._area), len(self._area[0])
            for r in range(a):
                for c in range(b):
                    if not self.near([r, c]):
                        continue
                    n = self.count([r, c])
                    if round(n) == 3:
                        newarea[r][c] = 1
                    elif (round(n) > 3 or round(n) < 2) and self._area[r][c] == 1:
                        newarea[r][c] = 0
            self._area = [[c for c in r] for r in newarea]

    def near(self, p):
        if self._tpe == 0:
            l1 = len(self._area)
            l2 = len(self._area[0])
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if p[0]+x < 0 or p[1]+y < 0 or p[0]+x >= l1 or p[1]+y >= l2: pass
                    elif self._area[p[0]+x][p[1]+y]:
                        return True
            return False

        elif self._tpe == 1:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (p[0]+x, p[1]+y) in self._area:
                        return True
            return False
