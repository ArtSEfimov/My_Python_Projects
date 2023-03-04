import random


class MyList(list):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_color = None

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
        if isinstance(value, MyList):
            if value:
                value.content_color = value[1].color
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            modify_slice = slice((start - 1 if start not in (len(self) - 1, 0) else None),
                                 (stop - 1 if stop not in (len(self), -1) else None),
                                 step)
            super().__setitem__(modify_slice, value)
        else:
            if key > 0:
                if key - 1 in range(len(self)):
                    super().__setitem__(key - 1, value)
            else:
                if abs(key) in range(1, len(self) + 1):
                    super().__setitem__(key, value)


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
    __COUNTER = 0

    def __init__(self, color):
        self.color = color.lower()
        self.on_the_head = True
        self.__position = 1

        self.is_up = False
        self.is_single = False

    def get_position(self):
        return self.__position

    def set_position(self, value):
        self.change_counter_value()
        self.__position = value

    @classmethod
    def change_counter_value(cls, reset_flag=False):
        if reset_flag:
            cls.__COUNTER = 0
        else:
            cls.__COUNTER += 1

    @classmethod
    def get_counter(cls):
        return cls.__COUNTER

    position = property(get_position, set_position)

    def __repr__(self):
        return self.position

    def __str__(self):
        # return 'b' if self.color == 'black' else 'w'
        return f'{self.color}-{self.position}-{self.is_up}'


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

        self.checker_class = Checker

        self.white_checkers = [Checker('white') for _ in range(15)]
        self.black_checkers = [Checker('black') for _ in range(15)]

        self.first_step_flag = True

        self.white_head = self.field.white_home.data[1] = MyList([checker for checker in self.white_checkers])
        self.white_head[-1].is_up = True
        self.black_head = self.field.black_home.data[1] = MyList([checker for checker in self.black_checkers])
        self.black_head[-1].is_up = True

    @staticmethod
    def throw_dices():
        first_dice = random.randint(1, 6)
        second_dice = random.randint(1, 6)
        return first_dice, second_dice

    def computer_step(self):  # black checkers
        self.first_dice, self.second_dice = self.throw_dices()
        if self.first_step_flag:
            self.first_step_flag = False
        print(self.first_priority('black'))
        self.field.show_field()

    def first_priority(self, color):
        priority_checker_list = [checker
                                 for checker in (self.white_checkers if color == 'white' else self.black_checkers)
                                 if checker.is_up]

        not_singles_checkers = list(
            filter(
                lambda c: not c.is_single, priority_checker_list
            )
        )
        field_map = dict()
        current_field_element = self.field.white_home if color == 'white' else self.field.black_home
        start_for_next_part = 0
        for _ in range(4):
            field_map.update({i + start_for_next_part: current_field_element.data[i] for i in range(1, 7)})
            current_field_element = current_field_element.next_element
            start_for_next_part = max(field_map.keys())

        def make_priority_cells_list(head=None):
            if head:
                return [k for k in range(2, 19) if field_map[k] == 0]
            return [k for k in range(13, 25) if field_map[k] == 0]

        def make_another_cells_list(current_color, head=None, tower_length=1):
            if head:
                return [k
                        for k in range(2, 19)
                        if len(field_map[k]) <= tower_length and field_map[k].color == current_color]
            return [k
                    for k in range(13, 25)
                    if len(field_map[k]) <= tower_length and field_map[k].color == current_color]

        another_cells_numbers = list()

        priority_cells_numbers = make_priority_cells_list(
            head=(self.white_head if color == 'white' else self.black_head)
        )

        if priority_cells_numbers:
            if not_singles_checkers:
                for dice in range(self.first_dice, self.second_dice):
                    for checker in not_singles_checkers:
                        if checker.position + dice in priority_cells_numbers:
                            checker.position += dice
                            if checker.get_counter() == 2:
                                break  # breaking the cycle with checkers
                    if self.checker_class.get_counter() == 2:
                        self.checker_class.change_counter_value(reset_flag=True)
                        return True  # breaking the cycle with dices

            if priority_checker_list:  # this means, that __COUNTER != 2, the step is not finished
                for dice in range(self.first_dice, self.second_dice):
                    for checker in priority_checker_list:
                        if checker.position + dice in priority_cells_numbers:
                            checker.position += dice
                            if checker.get_counter() == 2:
                                break  # breaking the cycle with checkers
                    if self.checker_class.get_counter() == 2:
                        self.checker_class.change_counter_value(reset_flag=True)
                        return True  # breaking the cycle with dices

        else:  # we need others cells (maybe without '0')
            while self.checker_class.get_counter() != 2:
                tower = 1
                another_cells_numbers = make_another_cells_list(
                    color,
                    head=(self.white_head if color == 'white' else self.black_head),
                    tower_length=tower
                )
                if another_cells_numbers:
                    if priority_checker_list:
                        for dice in range(self.first_dice, self.second_dice):
                            for checker in priority_checker_list:
                                if checker.position + dice in another_cells_numbers:
                                    checker.position += dice
                                    if checker.get_counter() == 2:
                                        break  # breaking the cycle with checkers
                            if self.checker_class.get_counter() == 2:
                                self.checker_class.change_counter_value(reset_flag=True)
                                return True  # breaking the cycle with dices
                else:
                    tower += 1
                    if tower > 15:
                        return False
                    continue


g = Game()
g.computer_step()
