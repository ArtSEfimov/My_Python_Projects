import random
import time

from data_structures import MyStack
from field_and_checker import Checker, Field


class Game:
    def __init__(self):
        self.field = Field()
        self.field.init_field_and_create_field_structure()

        self.white_checkers = [Checker('white') for _ in range(15)]
        self.black_checkers = [Checker('black') for _ in range(15)]

        self.who_steps = 'computer'

        self.first_step_flag = True
        self.head_reset = True

        self.first_dice = self.second_dice = None

        self.white_head = self.field.white_home.data[1] = MyStack()
        for checker in self.white_checkers:
            self.white_head.add_element(checker)
        self.white_head.top.is_up = True
        self.white_head.color = self.white_head.top.color

        self.black_head = self.field.black_home.data[1] = MyStack()
        for checker in self.black_checkers:
            self.black_head.add_element(checker)
        self.black_head.top.is_up = True
        self.black_head.color = self.black_head.top.color

    @staticmethod
    def throw_dices():
        first_dice = random.randint(1, 6)
        second_dice = random.randint(1, 6)
        return first_dice, second_dice

    def finished(self, color):
        if color == 'black':
            return self.field.get_sum_of_structure(self.field.white_yard, color) == 15
        return self.field.get_sum_of_structure(self.field.black_yard, color) == 15

    def play_the_game(self):
        color = 'black' if self.who_steps == 'computer' else 'white'
        while not self.finished(color):
            self.head_reset = True
            self.computer_step()
            time.sleep(3)

    def computer_step(self):  # black checkers
        # self.first_dice, self.second_dice = self.throw_dices()
        self.first_dice, self.second_dice = [int(i) for i in input().split()]
        # флаг первого хода (пригодится, когда надо будет снимать с головы две шашки)
        if self.first_step_flag:
            self.first_step_flag = False
        step_result = self.checking_move()
        if isinstance(step_result, bool):
            if step_result:
                print('success')  # ход удался, ходит следующий игрок
            else:
                print('no success')
        else:
            print('50/50 success')

        self.who_steps = 'human'

        print(self.first_dice, self.second_dice)
        self.field.show_field()

    # функция для описания четвертей поля в зависимиости от цвета шашки
    def get_quarters(self, color):
        quarters = {
            (1 if color == 'white' else 3): self.field.white_home,
            (2 if color == 'white' else 4): self.field.white_yard,
            (3 if color == 'white' else 1): self.field.black_home,
            (4 if color == 'white' else 2): self.field.black_yard
        }
        return quarters

    # определим, в какой части поля находится клетка, которая уже записана в свойство шашки
    def get_position(self, color, position):
        quarters = self.get_quarters(color)

        position_in_mylist = position % 6
        position_in_mylist = position_in_mylist if position_in_mylist else 6
        home = quarters[((position - 1) // 6) + 1]
        return home, position_in_mylist  # часть поля

    def remove_checker_from_old_position(self, checker: Checker):
        old_position = checker.position
        color = checker.color
        old_home, position_in_mylist = self.get_position(color, old_position)
        old_home = old_home.data
        old_home[position_in_mylist].pop_element()
        if old_home[position_in_mylist].is_empty():
            old_home[position_in_mylist] = 0

    def move_checker_to_new_position(self, checker: Checker, reverse_flag=False):
        if reverse_flag:
            checker.position = checker.backup_position
            _ = checker.backup_position
        position = checker.position
        color = checker.color
        new_home, position_in_mylist = self.get_position(color, position)
        new_home = new_home.data

        if new_home[position_in_mylist] == 0:  # это значит,что там ноль, а не стэк, значит стэк нужно создавать заново
            new_home[position_in_mylist] = MyStack()
        # это значит что там уже стэк
        new_home[position_in_mylist].add_element(checker)
        if new_home[position_in_mylist] is self.black_head or new_home[position_in_mylist] is self.white_head:
            self.head_reset = True

    def is_checker_from_head(self, checker):
        return checker is self.black_head.top or checker is self.white_head.top

    def get_possible_checker_list(self, color):
        return [checker
                for checker in (self.white_checkers if color == 'white' else self.black_checkers)
                if checker.is_up]

    def get_phase_of_game(self):
        if self.field.get_occupied_of_structure(self.field.black_home, 'black') <= 4:
            return 1
        if self.field.get_occupied_of_structure(self.field.black_yard, 'black') <= 3 \
                or self.field.get_occupied_of_structure(self.field.white_home, 'black') < 3:
            return 2
        if self.field.get_sum_of_structure(self.field.black_home, 'black') <= 3:
            return 3
        return 4

    def get_field_map(self, color):
        field_map = dict()
        current_field_element = self.field.white_home if color == 'white' else self.field.black_home
        start_for_next_part = 0
        for _ in range(4):
            field_map.update({i + start_for_next_part: current_field_element.data[i] for i in range(1, 7)})
            current_field_element = current_field_element.next_element
            start_for_next_part = max(field_map.keys())
        return field_map

    def get_from(self, color):
        current_phase = self.get_phase_of_game()
        possible_checker_list = self.get_possible_checker_list(color)

        # формируем список НЕОДИНОКИХ шашек (походить ими - в приоритете)
        def get_not_singles_checkers(borders_tuple=None):
            if borders_tuple:
                left_border, right_border = borders_tuple
                return [
                    checker for checker in possible_checker_list
                    if not checker.is_single and checker.position in range(left_border, right_border + 1)
                ]
            return [
                checker for checker in possible_checker_list
                if not checker.is_single
            ]

        # список ОСТАЛЬНЫХ шашек (которые не одиночные, но всё ещё наверху и могут "ходить")
        def get_singles_checkers(borders_tuple=None):
            if borders_tuple:
                left_border, right_border = borders_tuple

                return [
                    checker for checker in possible_checker_list
                    if checker.is_single and checker.position in range(left_border, right_border + 1)
                ]
            return [
                checker for checker in possible_checker_list
                if checker.is_single
            ]

        # singles_checkers = list()
        # not_singles_checkers = list()
        checker_list = list()

        if current_phase == 1:
            borders = (
                (1, 1), (10, 12), (7, 9), (13, 24), (5, 6), (2, 4)
            )
            for border in borders:
                checker_list.extend(get_not_singles_checkers(border))
                checker_list.extend(get_singles_checkers(border))

        if current_phase == 2:
            borders = (
                (1, 6), (7, 12), (13, 18), (19, 24)
            )
            for border in borders:
                checker_list.extend(get_not_singles_checkers(border))
                checker_list.extend(get_singles_checkers(border))

        return checker_list

    def get_to(self, color):

        def generate_list(left_border, right_border, empty_flag=True):
            if empty_flag:
                return [k
                        for k in range(left_border, right_border + 1)
                        if field_map[k] == 0]

            def generate_another_list():
                tower = 1
                another_list = list()
                while tower < 16:
                    tmp_list = [k for k in range(left_border, right_border + 1)
                                if isinstance(field_map[k], MyStack)
                                and field_map[k].color == color
                                and len(field_map[k]) == tower]
                    if tmp_list:
                        another_list.extend(tmp_list)
                    tower += 1
                return another_list

            return generate_another_list()

        current_phase = self.get_phase_of_game()
        field_map = self.get_field_map(color)
        cells_list = list()
        if current_phase == 1:

            borders = (
                (2, 4), (7, 8), (5, 6), (9, 12), (13, 18), (19, 24)
            )

            for left, right in borders:
                cells_list.extend(generate_list(left, right))
            for left, right in borders:
                cells_list.extend(generate_list(left, right, empty_flag=False))

            return cells_list

        if current_phase == 2:

            borders = (
                (4, 6), (2, 3), (13, 18), (10, 12), (7, 9), (19, 24)
            )

            for left, right in borders:
                cells_list.extend(generate_list(left, right))
            for left, right in borders:
                cells_list.extend(generate_list(left, right, empty_flag=False))

            return cells_list

    def compare_counts(self, tuple_12, tuple_21):
        if all(map(lambda x: x is not None, tuple_12)) and all(map(lambda x: x is not None, tuple_21)):
            tuple_12 = sum(tuple_12)
            tuple_21 = sum(tuple_21)
            if tuple_21 > tuple_12:  # если True, то прямой порядок хода (первый, второй)
                return self.first_dice, self.second_dice
            if tuple_21 < tuple_12:
                return self.second_dice, self.first_dice
            return random.choice(
                (
                    (self.first_dice, self.second_dice),
                    (self.second_dice, self.first_dice)
                )
            )

        if all(map(lambda x: x is not None, tuple_12)):
            return self.first_dice, self.second_dice
        if all(map(lambda x: x is not None, tuple_21)):
            return self.second_dice, self.first_dice

        if any(map(lambda x: x is not None, tuple_12)) and any(map(lambda x: x is not None, tuple_21)):
            tuple_12, _ = tuple_12
            tuple_21, _ = tuple_21
            if tuple_21 > tuple_12:  # если True, то прямой порядок хода (первый, второй)
                return self.first_dice, None
            if tuple_21 < tuple_12:
                return self.second_dice, None
            return random.choice((self.first_dice, self.second_dice)), None

        if any(map(lambda x: x is not None, tuple_12)):
            return self.first_dice, None
        return self.second_dice, None

    def checking_move(self):

        result_1, checker_1, count_1 = self.move('black', self.first_dice)
        result_2, checker_2, count_2 = self.move('black', self.second_dice)
        count_12 = (count_1, count_2)
        print(count_12)

        if result_1:
            self.remove_checker_from_old_position(checker_1)
            self.move_checker_to_new_position(checker_1, reverse_flag=True)

        if result_2:
            self.remove_checker_from_old_position(checker_2)
            self.move_checker_to_new_position(checker_2, reverse_flag=True)

        result_2, checker_2, count_2 = self.move('black', self.second_dice)
        result_1, checker_1, count_1 = self.move('black', self.first_dice)

        count_21 = (count_2, count_1)
        print(count_21)

        if result_2:
            self.remove_checker_from_old_position(checker_2)
            self.move_checker_to_new_position(checker_2, reverse_flag=True)

        if result_1:
            self.remove_checker_from_old_position(checker_1)
            self.move_checker_to_new_position(checker_1, reverse_flag=True)

        value_1, value_2 = self.compare_counts(count_12, count_21)
        if value_1 is not None:
            self.move('black', value_1)
        if value_2 is not None:
            self.move('black', value_2)

    def is_success_move(self, checker, dice):
        if self.is_checker_from_head(checker):
            self.head_reset = False
        # убираем шашку со старой позиции)

        self.remove_checker_from_old_position(checker)
        # присваеваем ей ноувю позицию
        checker.position += dice
        # размещаем ее на новой позиции
        self.move_checker_to_new_position(checker)


    def move(self, color, dice):

        checker_list = self.get_from(color)
        cells_list = self.get_to(color)

        checker = None
        count = None

        if checker_list:
            for cell_index, cell_value in enumerate(cells_list):
                for checker_index, checker_value in enumerate(checker_list):

                    if checker_value.position + dice == cell_value:
                        if self.is_checker_from_head(checker_value):
                            if not self.head_reset:
                                break

                        new_count_value = checker_index + cell_index
                        if count is None:
                            count = new_count_value
                            checker = checker_value
                        else:
                            if count > new_count_value:
                                count = new_count_value
                                checker = checker_value
                            elif count == new_count_value:
                                checker = random.choice((checker, checker_value))
                        break

            self.is_success_move(checker, dice)
            return True, checker, count
        return False, None, None  # ход не удался


g = Game()
print(g.get_field_map('black'))
print(g.get_to('black')
      )
g.play_the_game()
