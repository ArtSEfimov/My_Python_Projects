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
        if self.field.get_sum_of_structure(self.field.black_home, 'black') >= 6 \
                and self.field.get_occupied_of_structure(self.field.black_home, 'black') \
                + self.get_position_color(7) <= 4 or \
                (self.black_head.count > 2 and
                 self.field.get_occupied_of_structure(self.field.black_home, 'black') < 4):
            return 1
        if self.field.get_count_of_free_cells(self.field.white_home) != 0 \
                and self.field.get_occupied_of_structure(self.field.white_home, 'black') < 4:
            return 2
        if self.field.get_occupied_of_structure(self.field.black_yard, 'black') < 4:
            return 3
        return 4

    # Обязательно нужно добавить условие при котором может не быть свободных мест и тогда придется
    # выбирать другую фазу

    # ДОБАВИТЬ дополнительную фазу, где учесть, что есть "забытые" дома шашки, когда все уже "убежали" вперед

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
                1: 13, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,

                7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12,
                # 7: 9, 8: 10, 9: 11, 10: 12, 11: 13, 12: 14, # trying

                13: -5, 14: -4, 15: -3, 16: -2, 17: -1, 18: 0,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0
            }

        if current_phase == 2:
            return {
                1: 13, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,

                # 7: 7, 8: 12, 9: 11, 10: 10, 11: 9, 12: 8,  # trying_1

                # 7: 7, 8: 14, 9: 13, 10: 12, 11: 11, 12: 10, # original

                7: 7, 8: 16, 9: 15, 10: 14, 11: 13, 12: 12,  # trying_2

                13: -5, 14: -4, 15: -3, 16: -2, 17: -1, 18: 0,

                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0
            }

        if current_phase == 3:
            return {
                # 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2,
                # 7: 1, 8: 12, 9: 11, 10: 10, 11: 9, 12: 8,

                1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1,
                8: 4, 9: 3, 10: 2, 11: 1, 12: 0,

                13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0
            }

        if current_phase == 4:
            return {
                1: 25, 2: 22, 3: 19, 4: 16, 5: 13, 6: 10,
                7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2,
                13: 5, 14: 4, 15: 3, 16: 2, 17: 1, 18: 0,
                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0
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
                8: 12, 9: 13, 10: 14, 11: 15, 12: 16,
                13: 13, 14: 12, 15: 11, 16: 10, 17: 9, 18: 8,

                # 13: 11, 14: 10, 15: 9, 16: 8, 17: 7, 18: 6,  # trying_3

                # 13: 7, 14: 6, 15: 5, 16: 4, 17: 3, 18: 2,  # trying_1

                # 13: 9, 14: 8, 15: 7, 16: 6, 17: 5, 18: 4,  # trying_2

                19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
            }

        if current_phase == 4:
            return {
                2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
                7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12,

                # 7: 15, 8: 16, 9: 17, 10: 18, 11: 19, 12: 20,
                # 13: 13, 14: 12, 15: 11, 16: 10, 17: 9, 18: 8,

                13: 7, 14: 8, 15: 9, 16: 10, 17: 11, 18: 12,
                19: 1, 20: 2, 21: 3, 22: 4, 23: 5, 24: 6
            }

    def compare_counts(self, tuple_12, tuple_21):
        if all(map(lambda x: x is not None, tuple_12)) and all(map(lambda x: x is not None, tuple_21)):
            tuple_12 = sum(tuple_12)
            tuple_21 = sum(tuple_21)
            if tuple_21 < tuple_12:  # если True, то прямой порядок хода (первый, второй)
                return self.first_dice, self.second_dice
            if tuple_21 > tuple_12:
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
            if tuple_21 < tuple_12:  # если True, то прямой порядок хода (первый, второй)
                return self.first_dice, None
            if tuple_21 > tuple_12:
                return self.second_dice, None
            return random.choice((self.first_dice, self.second_dice)), None
            # return self.first_dice, None  # ДЛЯ ОТЛАДКИ (ЧТОБЫ БЫЛО ОДНОЗНАЧНО)

        if any(map(lambda x: x is not None, tuple_12)):
            return self.first_dice, None
        return self.second_dice, None

    def checking_move(self):

        result_1, checker_1, count_1 = self.move('black', self.first_dice)
        result_2, checker_2, count_2 = self.move('black', self.second_dice)

        count_12 = (count_1, count_2)

        print(count_12)

        if result_2:
            self.remove_checker_from_old_position(checker_2)
            self.move_checker_to_new_position(checker_2, reverse_flag=True)

        if result_1:
            self.remove_checker_from_old_position(checker_1)
            self.move_checker_to_new_position(checker_1, reverse_flag=True)

        result_2, checker_2, count_2 = self.move('black', self.second_dice)
        result_1, checker_1, count_1 = self.move('black', self.first_dice)

        count_21 = (count_2, count_1)

        print(count_21)

        if result_1:
            self.remove_checker_from_old_position(checker_1)
            self.move_checker_to_new_position(checker_1, reverse_flag=True)

        if result_2:
            self.remove_checker_from_old_position(checker_2)
            self.move_checker_to_new_position(checker_2, reverse_flag=True)

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

    @staticmethod
    def get_ratio(count):
        # return 6 if count < 6 else (3 if count < 11 else 2) # ORIGINAL
        # return 3 if count < 6 else (4 if count < 11 else 5) # trying_1
        ratios = {
            1: 12, 2: 14, 3: 16, 4: 18, 5: 20,
            6: 22, 7: 24, 8: 26, 9: 28, 10: 30,
            11: 32, 12: 34, 13: 36, 14: 38, 15: 40
        }

        # ratios = {
        #     1: 10, 2: 12, 3: 15, 4: 18, 5: 20,
        #     6: 21, 7: 22, 8: 23, 9: 24, 10: 25,
        #     11: 26, 12: 27, 13: 28, 14: 29, 15: 30
        # }

        return ratios[count]  # trying_2

    @staticmethod
    def get_low_ratio(count):
        # return 2 if count < 6 else (3 if count < 11 else 4) # trying_1
        # return 4.5 if count == 2 else (4.8 if count < 6 else (2.4 if count < 11 else 1.6)) # Original

        ratios = {
            1: 5, 2: 7, 3: 9, 4: 11, 5: 13,
            6: 15, 7: 17, 8: 19, 9: 21, 10: 23,
            11: 25, 12: 27, 13: 29, 14: 31, 15: 33
        }

        # ratios = {
        #     1: 5, 2: 7, 3: 8, 4: 9, 5: 10,
        #     6: 11, 7: 12, 8: 13, 9: 14, 10: 15,
        #     11: 16, 12: 17, 13: 18, 14: 19, 15: 20
        # }

        return ratios[count]  # trying_2

    def move(self, color, dice):
        checkers_list = self.get_possible_checker_list(color)
        checker_weight = self.get_from(color)
        cell_weight = self.get_to(color)

        counts = dict()

        if checkers_list:

            for checker_value in checkers_list:
                if self.is_checker_from_head(checker_value):
                    if not self.head_reset:
                        continue

                cell_value = checker_value.position + dice

                old_position, position = self.get_position(color, checker_value.position)
                old_position = old_position.data[position]

                new_position, position = self.get_position(color, cell_value)
                new_position = new_position.data[position]

                if isinstance(new_position, MyStack) and new_position.color != color:
                    continue

                count = cell_weight[cell_value] + checker_weight[checker_value.position]

                if isinstance(old_position, MyStack):
                    if old_position.count > 1:
                        if checker_value.position != 1:

                            count += self.get_ratio(old_position.count)
                        else:

                            count += self.get_low_ratio(old_position.count)

                    elif old_position.count == 1:
                        count -= 0  # в зависимости от четверти и фазы игры (
                    # например надо приоритетнее снять в 3-й четверти во второй фазе)

                if isinstance(new_position, MyStack):

                    count -= self.get_ratio(new_position.count)

                else:
                    count += 0  # в зависимости от четверти и фазы игры (
                    # например надо приоритетнее снять в 3-й четверти во второй фазе)

                counts[checker_value] = count

        if counts:
            sorted_counts = sorted(counts, key=lambda c: counts[c], reverse=True)
            checker = sorted_counts[0]
            count = counts[checker]

            self.is_success_move(checker, dice)
            return True, checker, count

        return False, None, None  # ход не удался


g = Game()

g.play_the_game()
