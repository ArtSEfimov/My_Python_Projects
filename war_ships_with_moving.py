import random
import secrets
import time


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * length

    @property
    def cells(self):
        return self._cells

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
        self.damaged_ships_coordinates = {}
        self.__field = [
            [0 for _ in range(self._size)] for _ in range(self._size)
        ]
        self.missed_cells = tuple()

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

    def put_missed_points(self):
        for i in range(self._size):
            for j in range(self._size):
                if self.field[i][j] == 0 and (j, i) in self.missed_cells:
                    self.field[i][j] = '.'

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

                        self.ships_coordinates[ship] = [(x, ship.y) for x in range(ship.x, ship.x + ship.length)]

                        self.field = [
                            [1 if j in range(ship.x, ship.x + ship.length) and ship.y == i
                             else (self.field[i][j])
                             for j in range(self._size)]
                            for i in range(self._size)
                        ]

                    elif ship.tp == 2:  # vertical orientation

                        self.ships_coordinates[ship] = [(ship.x, y) for y in range(ship.y, ship.y + ship.length)]

                        self.field = [
                            [1 if i in range(ship.y, ship.y + ship.length) and ship.x == j
                             else (self.field[i][j])
                             for j in range(self._size)]
                            for i in range(self._size)
                        ]

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
        self.put_missed_points()

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

        self.timer_marker = None
        self.message_marker = None

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
                        print((self.computer.field[i - 1][j - 2]
                               if self.computer.field[i - 1][j - 2] in ('.', 'X')
                               else ('.' if (j - 2, i - 1) in self.computer.missed_cells
                                     else '0')), end=' ' if j != self._size + 1 else 3 * '\t')
                print()

    def if_win_show_two_fields(self):
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

    @staticmethod
    def put_points(field, size, x, y, killed_flag=False, length=None, tp=None, x0=None, y0=None):
        for tmp_y in range(y - 1, y + 2):
            for tmp_x in range(x - 1, x + 2):
                if all(
                        map(lambda s: s in range(size), (tmp_y, tmp_x))
                ) and tmp_y != y and tmp_x != x:
                    field[tmp_y][tmp_x] = '.'
        if killed_flag:
            xl = (x0 + length) if tp == 1 else (x0 + 1)
            yl = (y0 + length) if tp == 2 else (y0 + 1)
            for i in range(y0 - 1, yl + 1):
                for j in range(x0 - 1, xl + 1):
                    if all(
                            map(lambda s: s in range(size), (i, j))
                    ) and field[i][j] != 'X':
                        field[i][j] = '.'

    @staticmethod
    def coordinates_go_in_a_row(coordinates, ship_tp):
        coordinates.sort(key=lambda t: t[0] if ship_tp == 1 else t[1])
        for i in range(len(coordinates) - 1):
            if abs(
                    coordinates[i][ship_tp - 1] - coordinates[i + 1][ship_tp - 1]
            ) > 1:
                return False
        return True

    def find_point_near_the_ship(self, ship_coordinates: tuple):
        def inner_func(another_coordinates: tuple):

            ship_x, ship_y = ship_coordinates
            another_x, another_y = another_coordinates

            if another_x > ship_x:
                for x in range(ship_x + 1, another_x + 1):
                    if self.human.field[ship_y][x] == '.':
                        return False
            else:
                for x in range(another_x, ship_x):
                    if self.human.field[ship_y][x] == '.':
                        return False

            if another_y > ship_y:
                for y in range(ship_y + 1, another_y + 1):
                    if self.human.field[y][ship_x] == '.':
                        return False
            else:
                for y in range(another_y, ship_y):
                    if self.human.field[y][ship_x] == '.':
                        return False
            return True

        return inner_func

    @staticmethod
    def is_x_near_the_point(field, size, x, y):
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i in range(size) and j in range(size):
                    if field[i][j] == 'X':
                        return True
        return False

    def the_game(self):

        count = 0
        self.show_two_fields()
        print()
        while True:
            if count % 2:  # computer`s step
                while self.human.ships_coordinates:

                    if self.human.damaged_ships_coordinates:  # if there are damaged ships
                        outer_ship = outer_coordinates = None

                        for ship, coordinates in self.human.damaged_ships_coordinates.items():
                            max_possible_radius = max(self.human.ships_coordinates.keys(),
                                                      key=lambda x: x.length).length
                            if len(coordinates) == 1:
                                point_x, point_y = coordinates[0]
                                while True:
                                    possible_radius = 1 if secrets.randbelow(100) > 20 \
                                        else random.randint(1, max_possible_radius - 1)

                                    possible_coordinates = [(x, y)
                                                            for x in
                                                            range(point_x - possible_radius,
                                                                  point_x + possible_radius + 1)
                                                            for y in
                                                            range(point_y - possible_radius,
                                                                  point_y + possible_radius + 1)
                                                            if x in range(self._size) and y in range(self._size) and
                                                            (x == point_x or y == point_y) and
                                                            self.human.field[y][x] not in ('.', 'X')]

                                    if possible_radius > 1:
                                        possible_coordinates = list(
                                            filter(self.find_point_near_the_ship((point_x, point_y)),
                                                   possible_coordinates))
                                    if possible_coordinates:
                                        break

                            elif len(coordinates) >= 2:
                                if not self.coordinates_go_in_a_row(coordinates, ship.tp):
                                    possible_coordinates = self.human.ships_coordinates[ship].copy()
                                else:
                                    possible_coordinates = list()
                                    if ship.tp == 1:
                                        min_x = min(
                                            [t[0] for t in coordinates]
                                        )
                                        for x in range(min_x - (max_possible_radius - len(coordinates)), min_x):
                                            if all(map(lambda c: c in range(self._size), (x, ship.y))):
                                                possible_coordinates.append((x, ship.y))
                                        max_x = max(
                                            [t[0] for t in coordinates]
                                        )
                                        for x in range(max_x + 1, max_x + (max_possible_radius - len(coordinates)) + 1):
                                            if all(map(lambda c: c in range(self._size), (x, ship.y))):
                                                possible_coordinates.append((x, ship.y))

                                        for x in (max_x, min_x):
                                            possible_coordinates = list(filter(
                                                self.find_point_near_the_ship((x, ship.y)),
                                                possible_coordinates))

                                    else:
                                        min_y = min(
                                            [t[1] for t in coordinates]
                                        )
                                        for y in range(min_y - (max_possible_radius - len(coordinates)), min_y):
                                            if all(map(lambda c: c in range(self._size), (ship.x, y))):
                                                possible_coordinates.append((ship.x, y))

                                        max_y = max(
                                            [t[1] for t in coordinates]
                                        )
                                        for y in range(max_y + 1, max_y + (max_possible_radius - len(coordinates)) + 1):
                                            if all(map(lambda c: c in range(self._size), (ship.x, y))):
                                                possible_coordinates.append((ship.x, y))

                                        for y in range(min_y, max_y):
                                            possible_coordinates = list(filter(
                                                self.find_point_near_the_ship((ship.x, y)),
                                                possible_coordinates))

                            current_x, current_y = random.choice(possible_coordinates)
                            current_cell = self.human.field[current_y][current_x]
                            if current_cell == 0:
                                self.human.field[current_y][current_x] = '.'
                                self.human.missed_cells += (current_x, current_y),
                                self.timer_marker = 2
                                self.message_marker = 'МИМО!'
                                break
                            elif current_cell == 1:
                                self.human.field[current_y][current_x] = 'X'

                                # This is requires for the cases if I hit to another ship
                                for tmp_ship, tmp_coordinates in self.human.ships_coordinates.items():
                                    if (current_x, current_y) in tmp_coordinates:

                                        # put points around human 'X' diagonally
                                        self.put_points(self.human.field, self._size, current_x, current_y)

                                        tmp_ship.is_move = False
                                        tmp_ship[tmp_coordinates.index((current_x, current_y))] = 'X'
                                        tmp_coordinates.remove((current_x, current_y))
                                        if not tmp_coordinates:

                                            # put points around killed ship
                                            self.put_points(self.human.field, self._size, current_x, current_y,
                                                            killed_flag=True, length=tmp_ship.length,
                                                            tp=tmp_ship.tp, x0=tmp_ship.x, y0=tmp_ship.y)

                                            if tmp_ship in self.human.damaged_ships_coordinates:
                                                self.human.damaged_ships_coordinates[tmp_ship].clear()
                                            self.message_marker = 'ПОТОПИЛ!'
                                        else:
                                            outer_ship = tmp_ship
                                            outer_coordinates = (current_x, current_y)
                                            self.message_marker = 'ПОПАЛ!'
                                        count += 1
                                        break
                                self.timer_marker = 4
                        if outer_ship is not None and outer_coordinates is not None:
                            self.human.damaged_ships_coordinates.setdefault(outer_ship, []).append(
                                outer_coordinates
                            )
                        self.human.damaged_ships_coordinates = {item[0]: item[1]
                                                                for item in self.human.damaged_ships_coordinates.items()
                                                                if item[1]}

                        break
                    else:  # if there are no damaged ships

                        current_x = random.randint(0, self._size - 1)
                        current_y = random.randint(0, self._size - 1)
                        current_cell = self.human.field[current_y][current_x]
                        if current_cell in ('X', '.'):  # here you can adapt difficulty
                            if current_cell == '.':
                                if self.is_x_near_the_point(self.human.field, self._size, current_x, current_y):
                                    continue
                                else:
                                    self.timer_marker = 0
                                    self.message_marker = 'СНОВА МИМО!'
                                    break
                            continue
                        elif current_cell == 0:
                            self.human.field[current_y][current_x] = '.'
                            self.human.missed_cells += (current_x, current_y),
                            self.timer_marker = 2
                            self.message_marker = 'МИМО!'
                            break
                        elif current_cell == 1:
                            self.human.field[current_y][current_x] = 'X'

                            # put points around human 'X' diagonally
                            self.put_points(self.human.field, self._size, current_x, current_y)

                            for ship, coordinates in self.human.ships_coordinates.items():
                                if (current_x, current_y) in coordinates:
                                    ship.is_move = False
                                    ship[coordinates.index((current_x, current_y))] = 'X'
                                    coordinates.remove((current_x, current_y))
                                    if not coordinates:
                                        # put points around killed ship
                                        self.put_points(self.human.field, self._size, current_x, current_y,
                                                        killed_flag=True, length=ship.length,
                                                        tp=ship.tp, x0=ship.x, y0=ship.y)

                                        if ship in self.human.damaged_ships_coordinates:
                                            self.human.damaged_ships_coordinates.pop(ship, None)
                                        self.message_marker = 'ПОТОПИЛ!'
                                    else:
                                        self.human.damaged_ships_coordinates.setdefault(ship, []).append(
                                            (current_x, current_y)
                                        )
                                        self.message_marker = 'ПОПАЛ!'
                                    break  # breaking the 'for' cycle
                            self.timer_marker = 4
                            count += 1
                    self.human.ships_coordinates = {item[0]: item[1]
                                                    for item in self.human.ships_coordinates.items()
                                                    if item[1]}

                    break
                print('Ход соперника:', end='\t')
                print(f'<{self.alphabet[current_x]}{current_y + 1}>', end='\t')
                print(self.message_marker)
            else:  # human`s step
                while self.computer.ships_coordinates:
                    while True:
                        input_data = input('Введите координаты: ').split()
                        if len(input_data) == 2:
                            current_x, current_y = input_data
                        elif len(input_data) == 1:
                            unpack_data = input_data[0]
                            if len(unpack_data) == 2:
                                current_x, current_y = unpack_data[0], unpack_data[1]
                            elif len(unpack_data) == 3:
                                current_x, current_y = unpack_data[0], unpack_data[1:]
                            else:
                                print('Введены некорректные значения, повторите ввод')
                                continue
                        else:
                            print('Введены некорректные значения, повторите ввод')
                            continue
                        try:
                            current_x = int(self.alphabet.index(current_x.upper()))
                            current_y = int(current_y) - 1
                            current_cell = self.computer.field[current_y][current_x]
                        except (ValueError, IndexError):
                            print('Введены некорректные значения, повторите ввод')
                            continue
                        if current_x < 0 or current_y < 0:
                            print('Введены некорректные значения, повторите ввод')
                            continue
                        if current_cell == 'X':
                            print('Вы сюда уже ходили, повторите ввод\n')
                            continue
                        break

                    if current_cell in ('.', 0):
                        if current_cell == '.':
                            if self.is_x_near_the_point(self.computer.field, self._size, current_x, current_y):
                                print('Вы сюда уже ходили, повторите ввод\n')
                                continue
                        self.computer.field[current_y][current_x] = '.'
                        if (current_x, current_y) not in self.computer.missed_cells:
                            self.computer.missed_cells += (current_x, current_y),
                        self.timer_marker = 2
                        self.message_marker = 'МИМО!'
                        break

                    elif current_cell == 1:
                        self.computer.field[current_y][current_x] = 'X'

                        # This is requires for the cases if I hit to another ship
                        for tmp_ship, tmp_coordinates in self.computer.ships_coordinates.items():
                            if (current_x, current_y) in tmp_coordinates:

                                # put points around human 'X' diagonally
                                self.put_points(self.computer.field, self._size, current_x, current_y)

                                tmp_ship.is_move = False
                                tmp_ship[tmp_coordinates.index((current_x, current_y))] = 'X'
                                tmp_coordinates.remove((current_x, current_y))
                                if not tmp_coordinates:

                                    # put points around killed ship
                                    self.put_points(self.computer.field, self._size, current_x, current_y,
                                                    killed_flag=True, length=tmp_ship.length,
                                                    tp=tmp_ship.tp, x0=tmp_ship.x, y0=tmp_ship.y)

                                    if tmp_ship in self.computer.damaged_ships_coordinates:
                                        self.computer.damaged_ships_coordinates[tmp_ship].clear()
                                    self.message_marker = 'ПОТОПИЛ!'
                                else:
                                    self.computer.damaged_ships_coordinates.setdefault(tmp_ship, []).append(
                                        (current_x, current_y)
                                    )
                                    self.message_marker = 'ПОПАЛ!'
                                break
                        self.timer_marker = 2

                        self.computer.ships_coordinates = {item[0]: item[1]
                                                           for item in self.computer.ships_coordinates.items()
                                                           if item[1]}
                        count += 1
                        break
                print('Ваш ход:', end='\t')
                print(f'<{self.alphabet[current_x]}{current_y + 1}>', end='\t')
                print(self.message_marker)

            if not self.human.ships_coordinates:
                print()
                self.if_win_show_two_fields()
                print('\nТы проиграл, кожаный!')
                break
            elif not self.computer.ships_coordinates:
                print()
                self.if_win_show_two_fields()
                print('\nТебе повезло, кожаный!')
                break
            else:
                print()
                self.show_two_fields()
                print()
                self.human.move_ships()
                self.computer.move_ships()
                time.sleep(self.timer_marker)
                count += 1
                self.timer_marker = None
                self.message_marker = None
                continue


sb = SeaBattle(10)
sb.the_game()
