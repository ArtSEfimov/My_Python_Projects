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

    def try_to_step(self, first_dice, second_dice):
        result, checker_1, count_1 = self.ranking_by_priority('black', first_dice)
        if result:  # ЕСТЬ успех с ПЕРВЫМ КУБИКОМ
            result, checker_2, _ = self.ranking_by_priority('black', second_dice)
            if result:  # ЕСТЬ успех с ПЕРВЫМ КУБИКОМ и со ВТОРЫМ КУБИКОМ
                return True  # ход удался

            # ЕСТЬ успех с ПЕРВЫМ КУБИКОМ, но НЕТ успеха со ВТОРЫМ КУБИКОМ
            # значит нужно попробовать походить наоборот
            # сначала возвращаем на старое место шашку первого хода

            self.remove_checker_from_old_position(checker_1)
            self.move_checker_to_new_position(checker_1, reverse_flag=True)

            # затем меняем местами порядок хода
        result, checker_2, count_2 = self.ranking_by_priority('black', second_dice)
        if result:  # ЕСТЬ успех со ВТОРЫМ кубиком
            result, checker_1, _ = self.ranking_by_priority('black', first_dice)
            if result:  # ЕСТЬ успех со ВТОРЫМ кубиком и с ПЕРВЫМ кубиком
                return True  # ход удался

            self.remove_checker_from_old_position(checker_2)
            self.move_checker_to_new_position(checker_2, reverse_flag=True)

            if count_2 > count_1:
                self.ranking_by_priority('black', first_dice)
                return first_dice
            else:
                self.ranking_by_priority('black', second_dice)
                return second_dice
        
        return False

    def finished(self, color):
        if color == 'black':
            return self.field.get_sum_of_structure(self.field.white_yard, color) == 15
        return self.field.get_sum_of_structure(self.field.black_yard, color) == 15

    def play_the_game(self):
        color = 'black' if self.who_steps == 'computer' else 'white'
        while not self.finished(color):
            self.head_reset = True
            self.computer_step()
            time.sleep(0)

    def computer_step(self):  # black checkers
        self.first_dice, self.second_dice = self.throw_dices()

        # флаг первого хода (пригодится, когда надо будет снимать с головы две шашки)
        if self.first_step_flag:
            self.first_step_flag = False
        step_result = self.try_to_step(self.first_priority, first_dice=self.first_dice, second_dice=self.second_dice)
        if isinstance(step_result, bool):
            if step_result:
                self.who_steps = 'human'  # ход удался, ходит следующий игрок
            else:
                step_result = self.try_to_step(self.second_priority,
                                               first_dice=self.first_dice,
                                               second_dice=self.second_dice)  # надо запустить функцию низшего приоритета с обоими значениями кубиков
                if isinstance(step_result, bool):
                    self.who_steps = 'human'  # ход удался (или нет), ходит следующий игрок
                else:
                    self.second_priority('black', step_result)
        # step_result = значению кубика, с которым надо запустить функцию низшего приоритета
        else:
            self.second_priority('black', step_result)
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
        position = checker.position
        color = checker.color
        new_home, position_in_mylist = self.get_position(color, position)
        new_home = new_home.data

        if new_home[position_in_mylist] == 0:  # это значит,что там ноль, а не стэк, значит стэк нужно создавать заново
            new_home[position_in_mylist] = MyStack()
        # это значит что там уже стэк
        new_home[position_in_mylist].add_element(checker)

    def is_not_head_checker(self, checker):
        if checker is self.black_head.top or checker is self.white_head.top:
            if self.head_reset:
                self.head_reset = False
                return True
            return False
        return True

    def get_possible_checker_list(self, color):
        return [checker
                for checker in (self.white_checkers if color == 'white' else self.black_checkers)
                if checker.is_up and self.is_not_head_checker(checker)]

    def get_phase_of_game(self):
        if self.field.get_sum_of_structure(self.field.black_home, 'black') >= 12:
            return 1
        if self.field.black_home.data.count(0) < 3:
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
        not_singles_checkers = list(
            filter(
                lambda c: not c.is_single, possible_checker_list
            )
        )
        # список ОСТАЛЬНЫХ шашек (которые не одиночные, но всё ещё наверху и могут "ходить")
        others_checkers = list(
            filter(
                lambda c: c.is_single, possible_checker_list
            )
        )
        checker_list = list()
        checker_list.extend(not_singles_checkers)
        checker_list.extend(others_checkers)
        if current_phase == 1:
            return checker_list

    def get_to(self, color):

        def generate_list(left_border, right_border, empty_flag=True):
            if empty_flag:
                return [k
                        for k in range(left_border, right_border)
                        if field_map[k] == 0
                        ]

            def generate_another_list():
                tower = 1
                another_list = list()
                while tower < 16:
                    tmp_list = [k for k in range(left_border, right_border)
                                if isinstance(field_map[k], MyStack)
                                and field_map[k].color == color
                                and len(field_map[k]) == tower]
                    if tmp_list:
                        another_list.extend(tmp_list)
                    else:
                        break
                    tower += 1
                return another_list

            return generate_another_list()

        current_phase = self.get_phase_of_game()
        field_map = self.get_field_map(color)
        cells_list = list()
        if current_phase == 1:
            borders = (
                (2, 7), (13, 19), (2, 13), (2, 19), (2, 25)
            )
            for left, right in borders:
                cells_list.extend(generate_list(left, right))
            for left, right in borders:
                cells_list.extend(generate_list(left, right, empty_flag=False))
            return cells_list

    def ranking_by_priority(self, color, dice):
        count = 0
        checker_list = self.get_from(color)
        if not checker_list:
            return False, None
        cells_list = self.get_to(color)

        for cell in cells_list:
            for checker in checker_list:
                count += 1
                if checker.position + dice == cell:
                    # убираем шашку со старой позиции)
                    self.remove_checker_from_old_position(checker)
                    # присваеваем ей ноувю позицию
                    checker.position += dice
                    # размещаем ее на новой позиции
                    self.move_checker_to_new_position(checker)

                    return True, checker, count

        return False, None, None  # ход не удался


g = Game()
print(g.get_field_map('black'))
print(g.get_to('black')
      )
