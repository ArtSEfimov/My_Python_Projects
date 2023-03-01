import random


class MyList(list):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            modify_slice = slice((start - 1 if start not in (len(self) - 1, 0) else None),
                                 (stop - 1 if stop not in (len(self), -1) else None),
                                 step)
            return super().__getitem__(modify_slice)
        if item > 0:
            if item - 1 in range(len(self)):
                return super().__getitem__(item - 1)
        else:
            if abs(item) in range(1, len(self) + 1):
                return super().__getitem__(item)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            modify_slice = slice((start - 1 if start not in (len(self) - 1, 0) else None),
                                 (stop - 1 if stop not in (len(self), -1) else None),
                                 step)
            super().__setitem__(modify_slice, value)
        else:
            if key > 0:
                if key - 1 in range(len(self)):
                    return super().__setitem__(key - 1, value)
            else:
                if abs(key) in range(1, len(self) + 1):
                    return super().__setitem__(key, value)


class FieldStructure:
    def __init__(self, data):
        self.data = data
        self.next_element = None
        self.previous_element = None

    def connect_elements(self, next_element=None, previous_element=None):
        if next_element:
            self.next_element = next_element
        if previous_element:
            self.previous_element = previous_element


class Checker:
    def __init__(self, color):
        self.color = color.lower()
        self.on_the_head = True
        self.position = 1
        self.is_up = False

    def __repr__(self):
        return self.color

    def __str__(self):
        # return 'b' if self.color == 'black' else 'w'
        return str(self.is_up)


class Field:
    def __init__(self):
        self.white_home = FieldStructure(MyList([0] * 6))
        self.black_home = FieldStructure(MyList([0] * 6))
        self.white_yard = FieldStructure(MyList([0] * 6))
        self.black_yard = FieldStructure(MyList([0] * 6))

        self.white_start = self.white_home
        self.black_start = self.black_home

    def init_field_and_create_field_structure(self):
        self.white_home.connect_elements(next_element=self.white_yard)
        self.white_yard.connect_elements(previous_element=self.white_home, next_element=self.black_home)
        self.black_home.connect_elements(next_element=self.black_yard)
        self.black_yard.connect_elements(previous_element=self.black_home, next_element=self.white_home)

    def show_field(self):
        start = self.white_start
        for _ in range(4):
            tmp_data = start.data
            for element in tmp_data:
                if type(element) == MyList:
                    print(*element)
                else:
                    print(element)
            print()

            start = start.next_element


class Game:
    def __init__(self):
        self.field = Field()
        self.field.init_field_and_create_field_structure()

        self.white_checkers = [Checker('white') for _ in range(15)]
        self.black_checkers = [Checker('black') for _ in range(15)]

        self.field.white_home.data[1] = MyList(checker for checker in self.white_checkers)
        self.field.white_home.data[1][-1].is_up = True
        self.field.black_home.data[1] = MyList(checker for checker in self.black_checkers)
        self.field.black_home.data[1][-1].is_up = True

    @staticmethod
    def throw_dices():
        first_dice = random.randint(1, 6)
        second_dice = random.randint(1, 6)
        return first_dice, second_dice

    def computer_step(self):  # black checkers
        first_dice, second_dice = self.throw_dices()
        # for checker in self.black_checkers:


g = Game()

g.field.show_field()
