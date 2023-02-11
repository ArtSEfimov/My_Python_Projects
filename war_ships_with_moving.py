import random
import string


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * length

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value

    @property
    def is_move(self):
        return self._is_move

    @is_move.setter
    def is_move(self, value):
        self._is_move = value

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
        current_x = self._x if self.tp == 2 else (self._x + go)
        current_y = self._y if self.tp == 1 else (self._y + go)
        self.set_start_coords(current_x, current_y)

    def is_collide(self, ship):
        if self is ship:
            return False
        if any(
                map(
                    lambda x: x is None, (ship.x, ship.y)
                )
        ):
            return False

        # self
        xl_1 = (self.x + self.length) if self.tp == 1 else (self.x + 1)
        yl_1 = (self.y + self.length) if self.tp == 2 else (self.y + 1)

        # ship
        xl_2 = ship.x + ship.length if ship.tp == 1 else ship.x + 1
        yl_2 = ship.y + ship.length if ship.tp == 2 else ship.y + 1

        size_x = max(xl_1, xl_2) + 1
        size_y = max(yl_1, yl_2) + 1

        field = [[0 for _ in range(size_x)]
                 for _ in range(size_y)]

        # self
        if self.tp == 1:  # horizontal orientation
            field = [
                [self.length if j in range(self.x, xl_1) and self.y == i else field[i][j] for j in range(size_x)]
                for i in range(size_y)
            ]
        elif self.tp == 2:  # vertical orientation
            field = [
                [self.length if i in range(self.y, yl_1) and self.x == j else field[i][j] for j in range(size_x)]
                for i in range(size_y)
            ]

        # ship
        if ship.tp == 1:  # horizontal orientation
            field = [
                [ship.length if j in range(ship.x, xl_2) and ship.y == i else field[i][j] for j in range(size_x)]
                for i in range(size_y)
            ]
        elif ship.tp == 2:  # vertical orientation
            field = [
                [ship.length if i in range(ship.y, yl_2) and ship.x == j else field[i][j] for j in range(size_x)]
                for i in range(size_y)
            ]

        def is_cross():
            ship_sum = 0
            for i in range(self.y - 1, yl_1 + 1):
                for j in range(self.x - 1, xl_1 + 1):
                    ship_sum += field[i][j]
            return ship_sum

        return is_cross() != pow(self.length, 2)

    def is_out_pole(self, size):
        x = self._x
        y = self._y
        t = self.tp
        length = self.length
        x_l = x + length if t == 1 else x
        y_l = y + length if t == 2 else y

        return any(
            map(
                lambda part_of_ship: part_of_ship not in range(size), range(x, x_l)
            )
        ) or any(
            map(
                lambda part_of_ship: part_of_ship not in range(size), range(y, y_l)
            )
        )

    def __repr__(self):
        return f'{self._length}'

    def __str__(self):
        return f'{self._length}'


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = list()
        self.ships_coordinates = {}
        self.__field = [
            [0 for _ in range(self._size)] for _ in range(self._size)
        ]

    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, value):
        self.__field = value

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
                current_x = random.randint(0, self._size - 1)
                current_y = random.randint(0, self._size - 1)
                ship.set_start_coords(current_x, current_y)
                if self.field[current_y][current_x] == 0:
                    if not any(
                            map(
                                lambda x: ship.is_collide(x), self._ships
                            )
                    ) and not ship.is_out_pole(self._size):
                        if ship.tp == 1:  # horizontal orientation

                            self.field = [
                                [1 if j in range(ship.x, ship.x + ship.length) and ship.y == i
                                 else self.field[i][j]
                                 for j in range(self._size)]
                                for i in range(self._size)
                            ]

                            self.ships_coordinates[ship] = [(x, ship.y) for x in range(ship.x, ship.x + ship.length)]

                        elif ship.tp == 2:  # vertical orientation
                            self.field = [
                                [1 if i in range(ship.y, ship.y + ship.length) and ship.x == j else self.field[i][j]
                                 for j in range(self._size)]
                                for i in range(self._size)
                            ]

                            self.ships_coordinates[ship] = [(ship.x, y) for y in range(ship.y, ship.y + ship.length)]

                        break
                else:
                    continue

    def get_ships(self):
        return self._ships

    def move_ships(self):
        for ship in self._ships:
            if not ship.is_move:
                continue
            reserve_coords = ship.get_start_coords()
            if ship.tp == 1:  # horizontal orientation
                self.field = [
                    [0 if j in range(ship.x, ship.x + ship.length) and ship.y == i
                     else self.field[i][j]
                     for j in range(self._size)]
                    for i in range(self._size)
                ]
            elif ship.tp == 2:  # vertical orientation
                self.field = [
                    [0 if i in range(ship.y, ship.y + ship.length) and ship.x == j
                     else self.field[i][j]
                     for j in range(self._size)]
                    for i in range(self._size)
                ]

            for attract in range(2):
                ship.set_start_coords(*reserve_coords)
                ship.move((-1 if attract else 1))

                if not any(
                        map(
                            lambda x: ship.is_collide(x), self._ships
                        )
                ) and not ship.is_out_pole(self._size):
                    if ship.tp == 1:  # horizontal orientation
                        self.field = [
                            [1 if j in range(ship.x, ship.x + ship.length) and ship.y == i
                             else self.field[i][j]
                             for j in range(self._size)]
                            for i in range(self._size)
                        ]

                        self.ships_coordinates[ship] = [(x, ship.y) for x in range(ship.x, ship.x + ship.length)]

                    elif ship.tp == 2:  # vertical orientation
                        self.field = [
                            [1 if i in range(ship.y, ship.y + ship.length) and ship.x == j else self.field[i][
                                j]
                             for j in range(self._size)]
                            for i in range(self._size)
                        ]

                        self.ships_coordinates[ship] = [(ship.x, y) for y in range(ship.y, ship.y + ship.length)]

                    break  # success

                else:
                    continue

            # unsuccessful
            else:
                ship.set_start_coords(*reserve_coords)
                if ship.tp == 1:  # horizontal orientation
                    self.field = [
                        [1 if j in range(ship.x, ship.x + ship.length) and ship.y == i
                         else self.field[i][j]
                         for j in range(self._size)]
                        for i in range(self._size)
                    ]

                elif ship.tp == 2:  # vertical orientation
                    self.field = [
                        [1 if i in range(ship.y, ship.y + ship.length) and ship.x == j else self.field[i][j]
                         for j in range(self._size)]
                        for i in range(self._size)
                    ]

    def show(self):
        for row in self.field:
            for elem in row:
                print(elem, end=' ')
            print()

    def get_pole(self):
        return tuple(
            tuple(row) for row in self.field
        )


class SeaBattle:
    alphabet = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЭЮЯ'

    def __init__(self, size):
        self._size = size
        self.accordance_coordinates = {self.alphabet[i]: i for i in range(size)}
        self.alphabet_for_field = {i[1]: i[0] for i in self.accordance_coordinates.items()}
        self.computer = GamePole(size)
        self.human = GamePole(size)

        self.computer.init()
        self.human.init()

    def show_two_fields(self):
        for i in range(self._size + 1):
            if i == 0:
                print('\t', ' '.join([self.alphabet_for_field[i] for i in range(self._size)]), 4 * '\t',
                      ' '.join([self.alphabet_for_field[i] for i in range(self._size)]), sep='')
            else:
                for j in range(self._size + 2):
                    if j == 0:
                        print(i, end='')
                    elif j == 1:
                        print(end='\t')
                    else:
                        print(self.human.field[i - 1][j - 2], end=' ' if j != self._size + 1 else 3 * '\t')

                for j in range(self._size + 2):
                    if j == 0:
                        print(i, end='')
                    elif j == 1:
                        print(end='\t')
                    else:
                        print(self.computer.field[i - 1][j - 2], end=' ' if j != self._size + 1 else 3 * '\t')
                print()

    # def find_x(self, ship_object: Ship):
    #     current_x, current_y = ship_object.get_start_coords()
    #     for _ in range(ship_object.length):
    #         if self.computer_field[current_y][current_x] == 'X':
    #             return current_x, current_y
    #         else:
    #             current_x += (1 if ship_object.tp == 1 else 0)
    #             current_y += (1 if ship_object.tp == 2 else 0)
    #
    # def find_damaged_ship(self, field_object: GamePole):
    #     for ship in field_object.get_ships():
    #         if not ship.is_move:  # ship is damaged
    #             coord_x, coord_y = self.find_x(ship)

    @staticmethod
    def put_points(field, size, x, y, killed_flag=False, length=None, tp=None, x0=None, y0=None):
        for tmp_y in range(y - 1, y + 2):
            for tmp_x in range(x - 1, x + 2):
                if all(
                        map(lambda s: s in range(size), (tmp_y, tmp_x))
                ) and tmp_y != y and tmp_x != x:
                    field[tmp_y][tmp_x] = '.'
        if killed_flag:
            xl = (x0 + length) if tp == 1 else x0 + 1
            yl = (y0 + length) if tp == 2 else y0 + 1
            for i in range(y0 - 1, yl + 1):
                for j in range(x0 - 1, xl + 1):
                    if all(
                            map(lambda s: s in range(size), (i, j))
                    ) and field[i][j] != 'X':
                        field[i][j] = '.'

    def the_game(self):
        count = 0
        self.show_two_fields()
        print()
        while True:
            if count % 2 or not count % 2:  # computer`s step
                while self.human.get_ships():
                    # I'll make an damaged_dict and put {ship: deleted coords} there

                    # damaged_ships = list(filter(lambda ship: ship[0].length != len(ship[1]),
                    #                        self.human.ships_coordinates.items()))
                    if damaged_ships:  # if there are damaged ships
                    # for ship in damaged_ships:
                    #     if abs(len(self.human.ships_coordinates[ship]) - ship.length) > 1:
                    #         if ship.tp == 2:
                    #             current_x = ship.x
                    #             current_y = list(range(-))

                    else:  # if there are no damaged ships

                        current_x = random.randint(0, self._size - 1)
                        current_y = random.randint(0, self._size - 1)
                        current_cell = self.human.field[current_y][current_x]
                        if current_cell == '.':
                            continue
                        elif current_cell == 0:
                            self.human.field[current_y][current_x] = '.'
                            count += 1
                            self.human.move_ships()
                            self.show_two_fields()
                            print()
                            break
                        elif current_cell == 1:
                            self.human.field[current_y][current_x] = 'X'

                            # put points around human 'X' diagonally
                            self.put_points(self.human.field, self._size, current_x, current_y)

                            for ship, coords in self.human.ships_coordinates.items():
                                if (current_x, current_y) in coords:
                                    ship.is_move = False
                                    ship[coords.index((current_x, current_y))] = 'X'
                                    coords.remove((current_x, current_y))
                                    if not coords:
                                        # put points around killed ship
                                        self.put_points(self.human.field, self._size, current_x, current_y,
                                                        killed_flag=True, length=ship.length,
                                                        tp=ship.tp, x0=ship.x, y0=ship.y)

                                        del self.human.ships_coordinates[ship]

                                    break  # breaking the 'for' cycle
                            self.human.move_ships()
                            self.show_two_fields()
                            print()

                            continue

                count += 1
            else:  # human`s step
                count += 1

            if any(
                    map(lambda x: not x, (self.human.ships_coordinates, self.computer.ships_coordinates))
            ):
                break
        print()


sb = SeaBattle(10)

sb.the_game()
