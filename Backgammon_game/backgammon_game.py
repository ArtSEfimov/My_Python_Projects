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
            # time.sleep(3)

    # def debag_func(self):
    #     for i, e in enumerate(self.throw_list):
    #         if i == len(self.throw_list) - 1:
    #             c = 1
    #         yield e

    def computer_step(self):  # black checkers

        # self.first_dice, self.second_dice = self.throw_dices()
        # self.throw_list.append((self.first_dice, self.second_dice))
        # print(self.throw_list)

        # self.first_dice, self.second_dice = next(self.gen)
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
        print(self.get_phase_of_game())

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

    def get_position_color(self, position_number, color='black'):
        value, position = self.get_position(color, position_number)
        value = value.data[position]
        if isinstance(value, MyStack):
            if value.color == color:
                return 1

        return 0

    def get_phase_of_game(self):
        # if (self.field.get_sum_of_structure(self.field.black_home, 'black') >= 6 \
        #         and self.field.get_occupied_of_structure(self.field.black_home, 'black') \
        #         + self.get_position_color(7) <= 4) or \
        #         (self.black_head.count > 2 and
        #          self.field.get_occupied_of_structure(self.field.black_home, 'black') < 4):
        #     return 1

        if self.field.get_sum_of_structure(self.field.black_home, 'black') >= 6 and (self.field.get_count_of_free_cells(
                self.field.black_home) + self.get_position_color(7)) != 0 and self.black_head.count > 2 and (
                self.field.get_occupied_of_structure(self.field.black_home, 'black') + self.get_position_color(7)) <= 4:
            return 1

        if (self.field.get_count_of_free_cells(self.field.white_home) != 0 and \
            self.field.get_sum_of_structure(self.field.white_home, 'black') < self.field.get_occupied_of_structure(
                    self.field.white_home, 'black') + self.field.get_count_of_free_cells(self.field.white_home)) or \
                self.field.get_occupied_of_structure(self.field.white_home, 'black') < 4:
            return 2

        # если:
        # в ЧЕРНОМ ДОМЕ есть еще шашки
        # ИЛИ в ЧЕРНОМ САДУ меньше или равно 4 занятых ЧЕРНЫМИ клеток И там есть свободные клетки
        # ??? И ЧЕРНЫХ шашек в ЧЕРНОМ САДУ и ЧЕРНОМ ДОМЕ больше чем занятых клеток в ЧЕРНОМ САДУ
        # if self.field.get_sum_of_structure(self.field.black_home, 'black') != 0 or self.field.get_occupied_of_structure(
        #         self.field.black_yard, 'black') <= 4 and \
        #         self.field.get_count_of_free_cells(self.field.black_yard) != 0 and (
        #         self.field.get_sum_of_structure(self.field.black_home, 'black') + self.field.get_sum_of_structure(
        #     self.field.black_yard, 'black') > self.field.get_occupied_of_structure(self.field.black_yard, 'black')
        # ):
        if self.field.get_count_of_free_cells(self.field.white_yard) == 6 and (
                self.field.get_count_of_free_cells(self.field.black_yard) != 0 or (
                self.field.get_sum_of_structure(self.field.black_home, 'black') + self.field.get_sum_of_structure(
            self.field.black_yard, 'black') > self.field.get_occupied_of_structure(self.field.black_yard, 'black'))
        ):
            return 3

        # if self.get_emptiness_from_last_checker('black') > 1:
        # if self.field.get_count_of_free_cells(self.field.black_yard) != 0
        if (
                self.field.get_sum_of_structure(self.field.black_home, 'black') + self.field.get_sum_of_structure(
            self.field.black_yard, 'black') != 0
        ):
            return 4

        if self.field.get_sum_of_structure(self.field.white_yard, 'black') <= 15:
            return 5

    def get_field_map(self, color):
        field_map = dict()
        current_field_element = self.field.white_home if color == 'white' else self.field.black_home
        start_for_next_part = 0
        for _ in range(4):
            field_map.update({i + start_for_next_part: current_field_element.data[i] for i in range(1, 7)})
            current_field_element = current_field_element.next_element
            start_for_next_part = max(field_map.keys())
        return field_map

    def get_from(self, color):  # может быть color понадобится для определения фазы игры в зависимости от цвета
        current_phase = self.get_phase_of_game()

        if current_phase == 1:
            return {
                1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,

                7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12,
                # 7: 9, 8: 10, 9: 11, 10: 12, 11: 13, 12: 14, # trying

                13: -5, 14: -4, 15: -3, 16: -2, 17: -1, 18: 0,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 2:
            return {
                1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,

                7: 7, 8: 12, 9: 11, 10: 10, 11: 9, 12: 8,  # trying_1

                # 7: 7, 8: 14, 9: 13, 10: 12, 11: 11, 12: 10,  # original

                # 7: 7, 8: 16, 9: 15, 10: 14, 11: 13, 12: 12,  # trying_2

                # 13: -5, 14: -4, 15: -3, 16: -2, 17: -1, 18: 0, ORIGINAL
                13: -7, 14: -6, 15: -5, 16: -4, 17: -3, 18: -2,

                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 3:
            return {
                # 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2,
                # 7: 1, 8: 12, 9: 11, 10: 10, 11: 9, 12: 8,

                1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1,

                # 8: 4, 9: 3, 10: 2, 11: 1, 12: 0,
                # 8: 6, 9: 5, 10: 4, 11: 3, 12: 2, # original
                8: 0, 9: 0, 10: 0, 11: 0, 12: 0,

                13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 4:
            # return {
            #     # 1: 25, 2: 22, 3: 19, 4: 16, 5: 13, 6: 10, # original
            #     1: 13, 2: 12, 3: 11, 4: 10, 5: 9, 6: 8,
            #     7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2,
            #     13: 5, 14: 4, 15: 3, 16: 2, 17: 1, 18: 0,
            #     19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0
            # }
            return {
                1: 19, 2: 18, 3: 17, 4: 16, 5: 15, 6: 14,
                7: 13, 8: 12, 9: 11, 10: 10, 11: 9, 12: 8,
                13: 7, 14: 6, 15: 5, 16: 4, 17: 3, 18: 2,
                # 7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2,
                # 13: 13, 14: 12, 15: 11, 16: 10, 17: 9, 18: 8,

                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 5:
            return {
                1: 23, 2: 22, 3: 21, 4: 20, 5: 19, 6: 18,
                7: 17, 8: 16, 9: 15, 10: 14, 11: 13, 12: 12,
                13: 11, 14: 10, 15: 9, 16: 8, 17: 7, 18: 6,
                19: 5, 20: 4, 21: 3, 22: 2, 23: 1, 24: 0
            }

    def get_to(self, color):

        current_phase = self.get_phase_of_game()

        if current_phase == 1:
            return {
                2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7,
                8: 8, 9: 9, 10: 10, 11: 11, 12: 12,

                # 13: 19, 14: 18, 15: 17, 16: 16, 17: 15, 18: 14,
                13: 21, 14: 20, 15: 19, 16: 18, 17: 17, 18: 16,

                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 2:
            return {
                2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7,
                8: 8, 9: 9, 10: 10, 11: 11, 12: 12,

                13: 23, 14: 22, 15: 21, 16: 20, 17: 19, 18: 18,
                # 13: 21, 14: 20, 15: 19, 16: 18, 17: 17, 18: 16,  # trying

                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 3:
            return {
                2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
                # 8: 12, 9: 13, 10: 14, 11: 15, 12: 16,
                8: 8, 9: 9, 10: 10, 11: 11, 12: 12,

                # 13: 13, 14: 12, 15: 11, 16: 10, 17: 9, 18: 8, # original

                # 13: 11, 14: 10, 15: 9, 16: 8, 17: 7, 18: 6,  # trying_3

                13: 7, 14: 6, 15: 5, 16: 4, 17: 3, 18: 2,  # trying_1

                # 13: 9, 14: 8, 15: 7, 16: 6, 17: 5, 18: 4,  # trying_2

                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 4:
            return {
                2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 5:
            return {
                2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
                7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12,
                13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18,
                19: 19, 20: 20, 21: 21, 22: 22, 23: 23, 24: 24
            }

    def compare_counts(self, tuple_12, tuple_21):
        count_12, checker_11, checker_12 = tuple_12
        count_21, checker_21, checker_22 = tuple_21

        if all(map(lambda x: x is not None, count_12)) and all(map(lambda x: x is not None, count_21)):
            count_12 = sum(count_12)
            count_21 = sum(count_21)
            if count_12 > count_21:  # если True, то прямой порядок хода (первый, второй)
                return self.first_dice, checker_11, self.second_dice, checker_12
            if count_21 > count_12:
                return self.second_dice, checker_21, self.first_dice, checker_22
            return random.choice(
                (
                    (self.first_dice, checker_11, self.second_dice, checker_12),
                    (self.second_dice, checker_21, self.first_dice, checker_22)
                )
            )

        if all(map(lambda x: x is not None, count_12)):
            return self.first_dice, checker_11, self.second_dice, checker_12
        if all(map(lambda x: x is not None, count_21)):
            return self.second_dice, checker_21, self.first_dice, checker_22

        if any(map(lambda x: x is not None, count_12)) and any(map(lambda x: x is not None, count_21)):
            mark_12 = sum(0 if x is None else x for x in count_12)
            mark_21 = sum(0 if x is None else x for x in count_21)

            if mark_12 > mark_21:  # если True, то прямой порядок хода (первый, второй)
                count_1, count_2 = count_12
                if count_1 is not None:
                    return self.first_dice, checker_11, None, None
                return self.second_dice, checker_12, None, None
            if mark_21 > mark_12:
                count_2, count_1 = count_21
                if count_2 is not None:
                    return self.second_dice, checker_21, None, None
                return self.first_dice, checker_22, None, None

            count, _ = count_12
            if count is not None:
                checker_1 = checker_11
                dice_1 = self.first_dice
            else:
                checker_1 = checker_12
                dice_1 = self.second_dice

            count, _ = count_21
            if count is not None:
                checker_2 = checker_21
                dice_2 = self.second_dice
            else:
                checker_2 = checker_22
                dice_2 = self.first_dice

            return *random.choice(((dice_1, checker_1), (dice_2, checker_2))), None, None

        if any(map(lambda x: x is not None, count_12)):
            count, _ = count_12
            if count is not None:
                checker = checker_11
                dice = self.first_dice
            else:
                checker = checker_12
                dice = self.second_dice

            return dice, checker, None, None
        count, _ = count_21
        if count is not None:
            checker = checker_21
            dice = self.second_dice
        else:
            checker = checker_22
            dice = self.first_dice
        return dice, checker, None, None

    def checking_move(self):

        # ПРЯМОЙ порядок хода (ПЕРВЫЙ -> ВТОРОЙ)

        result_11, checker_11, count_1 = self.move('black', self.first_dice)
        result_12, checker_12, count_2 = self.move('black', self.second_dice)

        count_12 = (count_1, count_2)

        print(count_12)

        if result_12:
            self.remove_checker_from_old_position(checker_12)
            self.move_checker_to_new_position(checker_12, reverse_flag=True)

        if result_11:
            self.remove_checker_from_old_position(checker_11)
            self.move_checker_to_new_position(checker_11, reverse_flag=True)

        # ОБРАТНЫЙ порядок хода (ВТОРОЙ -> ПЕРВЫЙ)

        result_21, checker_21, count_2 = self.move('black', self.second_dice)
        result_22, checker_22, count_1 = self.move('black', self.first_dice)

        count_21 = (count_2, count_1)  # порядок хода такой: второй, первый

        print(count_21)

        if result_22:
            self.remove_checker_from_old_position(checker_22)
            self.move_checker_to_new_position(checker_22, reverse_flag=True)

        if result_21:
            self.remove_checker_from_old_position(checker_21)
            self.move_checker_to_new_position(checker_21, reverse_flag=True)

        dice_1, checker_1, dice_2, checker_2 = self.compare_counts((count_12, checker_11, checker_12),
                                                                   (count_21, checker_21, checker_22)
                                                                   )

        if dice_1 is not None:
            self.is_success_move(checker_1, dice_1)
        if dice_2 is not None:
            self.is_success_move(checker_2, dice_2)

        if all(map(lambda x: x is not None, (dice_1, dice_2))):
            return True
        elif any(map(lambda x: x is not None, (dice_1, dice_2))):
            return None
        return False

    def is_success_move(self, checker, dice):

        if self.is_checker_from_head(checker):
            self.head_reset = False

        # убираем шашку со старой позиции
        self.remove_checker_from_old_position(checker)

        # присваеваем ей ноувю позицию
        checker.position += dice

        # размещаем ее на новой позиции
        self.move_checker_to_new_position(checker)

    @staticmethod
    def get_plus_ratio(count):

        ratios = {  # 1 choice
            2: 8, 3: 9, 4: 10, 5: 11,
            6: 12, 7: 13, 8: 14, 9: 15, 10: 16,
            11: 17, 12: 18, 13: 19, 14: 20, 15: 21
        }

        return ratios[count]  # trying_2

    @staticmethod
    def get_minus_ratio(count):

        ratios = {  # 1 choice
            1: 7, 2: 14, 3: 15, 4: 16, 5: 17,
            6: 18, 7: 19, 8: 20, 9: 21, 10: 22,
            11: 23, 12: 24, 13: 25, 25: 26, 15: 27
        }

        return ratios[count]  # trying_2

    @staticmethod
    def get_head_ratio(count):

        ratios = {
            1: 20, 2: 19, 3: 18, 4: 17, 5: 16,
            6: 15, 7: 14, 8: 13, 9: 14, 10: 15,
            11: 16, 12: 17, 13: 18, 14: 19, 15: 20
        }

        return ratios[count]  # trying_2

    @staticmethod
    def punishment(current_phase, old_position):  # штраф за оставление позиции
        if current_phase == 1:
            ratios = {
                1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2,
                8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }
            return ratios[old_position]

        if current_phase == 2:
            ratios = {
                1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1,
                8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                13: 2, 14: 2, 15: 2, 16: 2, 17: 2, 18: 2,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }
            return ratios[old_position]

        if current_phase == 3:
            ratios = {
                1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2,
                13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }
            return ratios[old_position]

        if current_phase == 4:
            ratios = {
                1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1,
                8: 2, 9: 2, 10: 2, 11: 2, 12: 2,
                13: 3, 14: 3, 15: 3, 16: 3, 17: 3, 18: 3,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }
            return ratios[old_position]

        return 0

    @staticmethod
    def encouragement(current_phase, new_position):  # поощрение за занятие пустой позиции
        if current_phase == 1:
            ratios = {
                2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2,
                8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }
            return ratios[new_position]

        if current_phase == 2:
            ratios = {
                2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2,
                8: 1, 9: 1, 10: 1, 11: 1, 12: 1,
                13: 3, 14: 3, 15: 3, 16: 3, 17: 3, 18: 3,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }
            return ratios[new_position]

        if current_phase == 3:
            ratios = {
                2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1,
                8: 3, 9: 3, 10: 3, 11: 3, 12: 3,
                13: 2, 14: 2, 15: 2, 16: 2, 17: 2, 18: 2,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }
            return ratios[new_position]

        if current_phase == 5:
            ratios = {
                2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
                8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1,
                19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 2
            }
            return ratios[new_position]

        return 0

    def get_last_white_checker_position(self):

        last_white_checker_position = None

        match_positions = {None: None,
                           1: 13, 2: 14, 3: 15, 4: 16, 5: 17, 6: 18,
                           7: 19, 8: 20, 9: 21, 10: 22, 11: 23, 12: 24
                           }
        if any(
                map(
                    lambda x: 1 <= x.position <= 12, self.white_checkers
                )
        ):
            last_white_checker_position = sorted((checker for checker in self.white_checkers if checker.position >= 1),
                                                 key=lambda x: x.position)[0].position

        return match_positions[last_white_checker_position]

    def manage_the_last_quarter(self, old_position):
        """Если на позициях с 13 по 24 есть белые шашки, смотрим на расположение последней из них относительно черных
        шашек. Можем двигать черные шашки только если их позиция меньше последней белой
        Применительно только к шашкам, являющимся единственными в ячейке"""

        punishment = {13: -11, 14: -10, 15: -9, 16: -8, 17: -7, 18: -6,
                      19: -5, 20: -4, 21: -3, 22: -2, 23: -1, 24: 0}

        encouragement = {19: 5, 20: 4, 21: 3, 22: 2, 23: 1, 24: 0}

        last_white_checker_position = self.get_last_white_checker_position()

        if last_white_checker_position is not None and old_position in punishment and old_position > last_white_checker_position:
            return punishment[old_position]

        if old_position in encouragement:
            return encouragement[old_position]

        return 0

    def distance_assessment(self, new_position):
        """Оценка расстояния от ближайшей сзади фишки. Применяется только в фазах 3, 4, 5."""

        previous_checker = None

        sorted_checker_list = sorted(self.black_checkers, key=lambda x: x.position)
        for checker in sorted_checker_list:
            if checker.position > new_position:
                break
            elif checker.position < new_position:
                previous_checker = checker

        if previous_checker:
            return new_position - previous_checker.position

        return 0

    def punishment_and_encouragement(self, old_position=None, new_position=None):
        """Штрафы за освобождение позиций и поощрения за занятия позиций в зависимости от фазы и от позиции.
        Использование при переходе на позицию, где еще нет стека и освобождении позиций с одной шашкой"""

        phase_of_game = self.get_phase_of_game()

        if phase_of_game == 1:
            if old_position is not None and 1 <= old_position <= 6:
                # punishment = {2: -1, 3: -1, 4: -1, 5: -1, 6: -1}
                return -phase_of_game

            if new_position is not None and 2 <= new_position <= 7:
                # encouragement = {2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}
                return phase_of_game

        if phase_of_game == 2:
            if old_position is not None and 13 <= old_position <= 18:
                return -phase_of_game

            if new_position is not None and 13 <= new_position <= 18:
                return phase_of_game

        if phase_of_game == 3:
            if old_position is not None and 7 <= old_position <= 12:
                return -phase_of_game

            if new_position is not None and 7 <= new_position <= 13:
                return phase_of_game

        return 0

    def is_first_checker_in_another_yard(self, line_color):
        """Функция должна проверять, есть ли во дворе шашка противника"""

        enemy_color = 'white' if line_color == 'black' else 'black'
        my_structure = self.field.white_yard if enemy_color == 'black' else self.field.black_yard

        enemy_checker_in_my_yard = self.field.get_sum_of_structure(my_structure, enemy_color) > 0

        if enemy_checker_in_my_yard:  # можно выстраивать линию длиной >= 6
            return True
        return False

    def is_six_checkers_in_line(self, my_color):
        """Функция должна проверять, что до того, как в зоне выброса появится шашка противника, мы не можем выстроить
        6 и более шашек в своем доме и дворе"""

        my_checkers = (x for x in (self.black_checkers if my_color == 'black' else self.white_checkers)
                       if 1 <= x.position <= 12)

        my_first_checker_position = sorted(my_checkers, key=lambda x: x.position)[0].position

        # пройтись от этой шашки вперед по структурам и найти (если есть) пустые ячейки или шашки другого цвета,
        # если счетчик меньше 6, то дальше будем проходить от позиции, следующей за найденной (если следующая позиция)
        # занята шашкой моего цвета
        # и так до 12-й позиции
        # если насчитали 6, возвращаем на переход
        # либо что всё нормально

    def move(self, color, dice, recursion=False, checkers=None):
        if recursion:
            checkers_list = checkers
        else:
            checkers_list = self.get_possible_checker_list(color)

        checker_weight = self.get_from(color)
        cell_weight = self.get_to(color)

        main_mark = None
        marks = None

        if checkers_list:

            for checker_value in checkers_list:
                if self.is_checker_from_head(checker_value):
                    if not self.head_reset:
                        continue

                cell_value = checker_value.position + dice
                if cell_value > 24:
                    continue

                old_position, position = self.get_position(color, checker_value.position)
                old_position = old_position.data[position]

                new_position, position = self.get_position(color, cell_value)
                new_position = new_position.data[position]

                if isinstance(new_position, MyStack) and new_position.color != color:
                    continue

                count = cell_weight[cell_value] + checker_weight[checker_value.position]

                if self.get_phase_of_game() > 2:
                    count -= self.distance_assessment(cell_value)

                if isinstance(old_position, MyStack):
                    if old_position.count > 1:
                        if checker_value.position != 1:
                            count += self.get_plus_ratio(old_position.count)

                        else:
                            count += self.get_head_ratio(old_position.count)

                    elif old_position.count == 1:
                        if self.get_phase_of_game() in (4, 5):
                            count += self.manage_the_last_quarter(checker_value.position)

                        count += self.punishment_and_encouragement(old_position=checker_value.position)

                        if recursion:
                            count -= self.punishment(self.get_phase_of_game(), checker_value.position)

                if isinstance(new_position, MyStack):
                    count -= self.get_minus_ratio(new_position.count)

                else:
                    count += self.punishment_and_encouragement(new_position=cell_value)

                    if recursion:
                        count += self.encouragement(self.get_phase_of_game(), cell_value)

                if main_mark is None or main_mark < count:
                    marks = None
                    main_mark = count
                    main_checker = checker_value
                elif count == main_mark:
                    if marks is None:
                        marks = dict()
                        marks[main_mark] = (main_checker, checker_value)
                    else:
                        marks[main_mark] += (checker_value,)

        if marks is not None:
            if recursion:
                main_mark = list(marks.keys())[0]
                main_checker = random.choice(list(marks.values())[0])
                return None, main_checker, main_mark

            _, main_checker, main_mark = self.move(color, dice, recursion=True, checkers=list(marks.values())[0])
            self.is_success_move(main_checker, dice)
            return True, main_checker, main_mark

        if main_mark is not None:
            if not recursion:
                self.is_success_move(main_checker, dice)
            return True, main_checker, main_mark

        return False, None, None  # ход не удался


g = Game()

g.play_the_game()
