import random


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * length

    @property
    def tp(self):
        return self._tp

    @property
    def length(self):
        return self._length

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        go = go if self._is_move else 0
        current_x = self._x if self.tp == 1 else (self._x + go)
        current_y = self._y if self.tp == 2 else (self._y + go)
        self.set_start_coords(current_x, current_y)

    def is_collide(self, ship):
        if self is ship:
            return False
        if any(
                map(
                    lambda x: x is None, (ship._x, ship._y)
                )
        ):
            return False
        x_1 = self._x
        y_1 = self._y
        t_1 = self.tp
        l_1 = self.length
        x_1_l = x_1 + l_1 if t_1 == 2 else x_1
        y_1_l = y_1 + l_1 if t_1 == 1 else y_1

        x_2 = ship._x
        y_2 = ship._y
        t_2 = ship.tp
        l_2 = ship.length
        x_2_l = x_2 + l_2 if t_2 == 2 else x_2
        y_2_l = y_2 + l_2 if t_2 == 1 else y_2

        x_max = max(x_1_l, x_2_l)
        y_max = max(y_1_l, y_2_l)

        field = [
            [0 for _ in range(y_max + 1)]
            for _ in range(x_max + 1)
        ]
        if t_1 == 1:
            field = [
                [1 if j in range(y_1, y_1 + l_1) and x_1 == i else field[i][j] for j in range(y_max + 1)]
                for i in range(x_max + 1)
            ]
        else:
            field = [
                [1 if i in range(x_1, x_1 + l_1) and y_1 == j else field[i][j] for j in range(y_max + 1)]
                for i in range(x_max + 1)
            ]
        if t_2 == 1:
            field = [
                [1 if j in range(y_2, y_2 + l_2) and x_2 == i else field[i][j] for j in range(y_max + 1)]
                for i in range(x_max + 1)
            ]
        else:
            field = [
                [1 if i in range(x_2, x_2 + l_2) and y_2 == j else field[i][j] for j in range(y_max + 1)]
                for i in range(x_max + 1)
            ]

        def is_cross(x, x_l, y, y_l, t):
            for i in range(x - 1, x_l + 2):
                if i in range(len(field)):
                    for j in range(y - 1, y_l + 2):
                        if j in range(len(field[i])):
                            if i in range(x, x_l + (1 if t == 1 else 0)) and j in range(y, y_l + (1 if t == 2 else 0)):
                                pass
                            else:
                                if field[i][j] != 0:
                                    return True

            return False

        return is_cross(x_1, x_1_l, y_1, y_1_l, t_1)

    def is_out_pole(self, size):
        x = self._x
        y = self._y
        t = self.tp
        l = self.length
        x_l = x + l if t == 2 else x
        y_l = y + l if t == 1 else y

        return any(
            map(
                lambda x: x not in range(size + 1), (x_l, y_l)
            )
        )

    def __str__(self):
        return f'{self._length}'


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = list()

        self.__field = [
            [0 for _ in range(self._size)] for _ in range(self._size)
        ]

    def init(self):
        n = 4
        count = 1

        for _ in range(4):
            self._ships.extend(
                [Ship(n, tp=random.randint(1, 2)) for _ in range(count)]
            )
            count += 1
            n -= 1

        for ship in self._ships:
            while True:
                current_x = random.randint(0, 9)
                current_y = random.randint(0, 9)
                ship.set_start_coords(current_x, current_y)
                if self.__field[current_x][current_y] == 0:
                    if not any(
                            map(
                                lambda x: ship.is_collide(x), self._ships
                            )
                    ) and not ship.is_out_pole(self._size):
                        if ship.tp == 1:  # horizontal orientation
                            if all(
                                    map(
                                        lambda x: x == 0, self.__field[current_x][current_y:current_y + ship.length]
                                    )
                            ):
                                self.__field = [
                                    [1 if j in range(ship.y, ship.y + ship.length) and ship.x == i
                                     else self.__field[i][j]
                                     for j in range(self._size)]
                                    for i in range(self._size)
                                ]
                            else:
                                continue
                        else:  # vertical orientation
                            self.__field = [
                                [1 if i in range(ship.x, ship.x + ship.length) and ship.y == j else self.__field[i][j]
                                 for j in range(self._size)]
                                for i in range(self._size)
                            ]

                        break
                else:
                    continue

    def get_ships(self):
        return self._ships

    def move_ships(self):
        for ship in self._ships:
            reserve_coords = ship.get_start_coords()
            if ship.tp == 1:  # horizontal orientation
                self.__field = [
                    [0 if j in range(ship.y, ship.y + ship.length) and ship.x == i
                     else self.__field[i][j]
                     for j in range(self._size)]
                    for i in range(self._size)
                ]
            elif ship.tp == 2:  # vertical orientation
                self.__field = [
                    [0 if i in range(ship.x, ship.x + ship.length) and ship.y == j
                     else self.__field[i][j]
                     for j in range(self._size)]
                    for i in range(self._size)
                ]

            for attract in range(2):
                ship.set_start_coords(*reserve_coords)
                ship.move((-1 if attract else 1))
                current_x, current_y = ship.get_start_coords()

                if self.__field[current_x][current_y] == 0:
                    if not any(
                            map(
                                lambda x: ship.is_collide(x), self._ships
                            )
                    ) and not ship.is_out_pole(self._size):
                        if ship.tp == 1:  # horizontal orientation
                            if all(
                                    map(
                                        lambda x: x == 0, self.__field[current_x][current_y:current_y + ship.length]
                                    )
                            ):
                                self.__field = [
                                    [1 if j in range(ship.y, ship.y + ship.length) and ship.x == i
                                     else self.__field[i][j]
                                     for j in range(self._size)]
                                    for i in range(self._size)
                                ]
                            else:
                                continue
                        elif ship.tp == 2:  # vertical orientation
                            if all(
                                    map(
                                        lambda x: x == 0, self.__field[current_x + ship.length][current_y:current_y]
                                    )
                            ):
                                self.__field = [
                                    [1 if i in range(ship.x, ship.x + ship.length) and ship.y == j else self.__field[i][
                                        j]
                                     for j in range(self._size)]
                                    for i in range(self._size)
                                ]
                            else:
                                continue
                        break  # success
                else:
                    continue
            # unsuccessful
            ship.set_start_coords(*reserve_coords)
            self.show()
            print()

    def show(self):
        for row in self.__field:
            for elem in row:
                print(elem, end=' ')
            print()

    def get_pole(self):
        return tuple(
            tuple(row) for row in self.__field
        )


g = GamePole(10)
g.init()
for r in g.get_pole():
    for e in r:
        print(e, end=' ')
    print()
print()
g.move_ships()
for r in g.get_pole():
    for e in r:
        print(e, end=' ')
    print()
