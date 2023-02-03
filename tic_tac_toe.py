import random


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return True if self.value == 0 else False


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    @classmethod
    def input_value(cls, value):
        if value == 0:
            return cls.FREE_CELL
        if value == 1:
            return cls.HUMAN_X
        if value == 2:
            return cls.COMPUTER_O

    def __init__(self):
        self.pole = tuple(tuple(Cell() for _ in range(3)) for _ in range(3))
        self.is_human_win = self.is_computer_win = self.is_draw = False

    @staticmethod
    def check_indexes(i, j):
        if not all(
                map(
                    lambda x: x in range(3), (i, j)
                )
        ):
            raise IndexError('некорректно указанные индексы')

    def __getitem__(self, item):
        i, j = item
        self.check_indexes(i, j)
        return self.pole[i][j].value

    def __setitem__(self, key, value):
        i, j = key
        self.check_indexes(i, j)
        self.pole[i][j].value = value
        if self.computer_win_condition():
            self.is_computer_win = True
        if self.human_win_condition():
            self.is_human_win = True
        if not self.is_there_free_cells():
            self.is_draw = True

    def init(self):
        for i in range(3):
            for j in range(3):
                self.pole[i][j].value = self.input_value(0)
        self.is_human_win = self.is_computer_win = self.is_draw = False

    def show(self):
        for i in range(3):
            for j in range(3):
                if self.pole[i][j].value == self.input_value(0):
                    print('#', end=' ')
                elif self.pole[i][j].value == self.input_value(1):
                    print('X', end=' ')
                elif self.pole[i][j].value == self.input_value(2):
                    print('O', end=' ')
            print()

    def check_free(self, i, j):
        return self.pole[i][j].value == self.input_value(0)

    def human_go(self):
        while True:
            i, j = map(int, input(
                f'Ваш ход\nВведите координаты вашего знака (числа в диапазоне от 0 до 2) через пробел (например: {random.randint(0, 2)} {random.randint(0, 2)})\n').split())
            self.check_indexes(i, j)
            if self.check_free(i, j):
                break
            continue
        self.pole[i][j].value = self.input_value(1)
        if self.computer_win_condition():
            self.is_computer_win = True
        if self.human_win_condition():
            self.is_human_win = True
        if not self.is_there_free_cells():
            self.is_draw = True

    def computer_go(self):
        while True:
            i, j = random.randint(0, 2), random.randint(0, 2)
            if self.check_free(i, j):
                break
            continue
        self.pole[i][j].value = self.input_value(2)
        if self.computer_win_condition():
            self.is_computer_win = True
        if self.human_win_condition():
            self.is_human_win = True
        if not self.is_there_free_cells():
            self.is_draw = True

    def _human_win_getter(self):
        return self.__human_win

    def _human_win_setter(self, value):
        if isinstance(value, bool):
            self.__human_win = value

    is_human_win = property()
    is_human_win = is_human_win.getter(_human_win_getter)
    is_human_win = is_human_win.setter(_human_win_setter)

    @property
    def is_computer_win(self):
        return self.__computer_win

    @is_computer_win.setter
    def is_computer_win(self, value):
        if isinstance(value, bool):
            self.__computer_win = value

    def _is_draw_getter(self):
        return self.__is_draw

    def _is_draw_setter(self, value):
        if isinstance(value, bool):
            self.__is_draw = value

    is_draw = property(_is_draw_getter)
    is_draw = is_draw.setter(_is_draw_setter)

    def somebody_win(self, reason):
        return any(
            map(
                lambda x: all(
                    map(
                        lambda y: y.value == reason, x
                    )
                ), self.pole
            )
        ) or any(
            map(
                lambda x: all(
                    map(
                        lambda y: y.value == reason, x
                    )
                ), [[self.pole[i][j] for i in range(len(self.pole))] for j in range(len(self.pole[0]))]
            )
        ) or all(
            map(
                lambda y: y.value == reason, [self.pole[i][j] for j in range(3) for i in range(3) if i == j]
            )
        ) or all(
            map(
                lambda y: y.value == reason, [self.pole[i][j] for i in range(3) for j in range(3) if j == 2 - i]
            )
        )

    def human_win_condition(self):
        return self.somebody_win(1)

    def computer_win_condition(self):
        return self.somebody_win(2)

    def is_there_free_cells(self):
        return any(map(lambda x: x.value == 0, [e
                                                for row in self.pole
                                                for e in row]))

    def __bool__(self):
        return not any(
            (self.is_human_win, self.is_computer_win, self.is_draw)
        )


game = TicTacToe()
game.init()
step_game = 0
print("Знак человека: \'X\'")
print("Знак компьютера: \'O\'\n")
while game:
    game.show()
    print()
    if step_game % 2 == 0:
        game.human_go()
    else:
        print('Ход компьютера:')
        game.computer_go()

    step_game += 1

game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")
