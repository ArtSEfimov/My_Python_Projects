import random
from data_structures import MyStack
from field_and_checker import Checker, Field


class Game:
    def __init__(self):
        self.field = Field()
        self.field.init_field_and_create_field_structure()

        self.white_checkers = [Checker('white') for _ in range(15)]
        self.black_checkers = [Checker('black') for _ in range(15)]

        self.first_step_flag = True

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
        result_list = list()

        for dice in (first_dice, second_dice):
            result = self.first_priority('black', dice)
            result_list.append((dice, result))

        return not all(
            map(
                lambda e: e[1], result_list
            )
        )

    # НУЖНО НАУЧИТЬСЯ ВОЗВРАЩАТЬ ШАШКУ НА МЕСТО, ЧТОБЫ ПРОБОВАТЬ РАЗНЫЕ КОМБИНАЦИИ ХОДОВ
    # В ПРИОРИТЕТЕ ПРИОРИТЕТНЫЙ ШАГ, ДАЖЕ ЕСЛИ ПРИДЕТСЯ РАЗМЕНИВАТЬ МЕСТАМИ КУБИКИ

    def computer_step(self):  # black checkers
        self.first_dice, self.second_dice = self.throw_dices()

        # флаг первого хода (пригодится, когда надо будет снимать с головы две шашки)
        if self.first_step_flag:
            self.first_step_flag = False

        result, checker = self.first_priority('black', self.first_dice)
        if not result:
            result, checker = self.first_priority('black', self.second_dice)
            if not result:
                pass
            else:
                
        else:
            result, checker = self.first_priority('black', self.second_dice)

        if not self.second_priority('black', dice):  # если и вторая попытка хода не удалась
            print('Пропуск хода')

        # надо подумать, если не получилось походить в этом порядке очков кубиков, может получится в обратном порядке
        # еще надо подумать над снятием шашки с "головы" (чтобы делать это один раз за ход)

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

    def remove_checker_from_old_position(self, checker: Checker, reverse_flag=False):
        old_position = checker.position if not reverse_flag else checker.backup_position
        color = checker.color
        old_home, position_in_mylist = self.get_position(color, old_position)
        old_home = old_home.data
        old_home[position_in_mylist].pop_element()
        if old_home[position_in_mylist].is_empty():
            old_home[position_in_mylist] = 0

    def move_checker_to_new_position(self, checker: Checker, reverse_flag=False):
        position = checker.position if not reverse_flag else checker.backup_position
        color = checker.color
        new_home, position_in_mylist = self.get_position(color, position)
        new_home = new_home.data

        if new_home[position_in_mylist] == 0:  # это значит,что там ноль, а не стэк, значит стэк нужно создавать заново
            new_home[position_in_mylist] = MyStack()
        # это значит что там уже стэк
        new_home[position_in_mylist].add_element(checker)

    def first_priority(self, color, dice):
        # формируем список шашек, которые находятся наверху и могут "ходить"
        possible_checker_list = [checker
                                 for checker in (self.white_checkers if color == 'white' else self.black_checkers)
                                 if checker.is_up]

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

        # вспомогательный словарь (для каждого игрока будет свой, но формируется на основании общего поля)
        # -------------------------------------------------------------------------------------------------
        field_map = dict()
        current_field_element = self.field.white_home if color == 'white' else self.field.black_home
        start_for_next_part = 0
        for _ in range(4):
            field_map.update({i + start_for_next_part: current_field_element.data[i] for i in range(1, 7)})
            current_field_element = current_field_element.next_element
            start_for_next_part = max(field_map.keys())

        # -------------------------------------------------------------------------------------------------

        # функции для создания приоритетного списка полей, куда можно походить в первую очередь
        # здесь делаем поля, которые не заняты (значения равны 0, а не списку с шашками)
        def make_priority_cells_list(head=None):
            if head:
                return [k for k in range(2, 19) if field_map[k] == 0]
            return [k for k in range(13, 25) if field_map[k] == 0]

        priority_cells_numbers = make_priority_cells_list(
            head=(self.white_head if color == 'white' else self.black_head)
        )

        if priority_cells_numbers:  # если есть поля с нулевыми значениями
            if not_singles_checkers:  # если есть неодиночные шашки (убираем "верхние этажи")
                for checker in not_singles_checkers:
                    if checker.position + dice in priority_cells_numbers:
                        # убираем шашку со старой позиции
                        self.remove_checker_from_old_position(checker)
                        # присваеваем ей ноувю позицию
                        checker.position += dice
                        # размещаем ее на новой позиции
                        self.move_checker_to_new_position(checker)

                        return True, checker

            if others_checkers:
                for checker in others_checkers:
                    if checker.position + dice in priority_cells_numbers:
                        # убираем шашку со старой позиции
                        self.remove_checker_from_old_position(checker)
                        # присваеваем ей ноувю позицию
                        checker.position += dice
                        # размещаем ее на новой позиции
                        self.move_checker_to_new_position(checker)

                        return True, checker

        return False,  # ход не удался

    def second_priority(self, color, dice):
        # формируем список шашек, которые находятся наверху и могут "ходить"
        possible_checker_list = [checker
                                 for checker in (self.white_checkers if color == 'white' else self.black_checkers)
                                 if checker.is_up]

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

        # вспомогательный словарь (для каждого игрока будет свой, но формируется на основании общего поля)
        # -------------------------------------------------------------------------------------------------
        field_map = dict()
        current_field_element = self.field.white_home if color == 'white' else self.field.black_home
        start_for_next_part = 0
        for _ in range(4):
            field_map.update({i + start_for_next_part: current_field_element.data[i] for i in range(1, 7)})
            current_field_element = current_field_element.next_element
            start_for_next_part = max(field_map.keys())

        # -------------------------------------------------------------------------------------------------

        # функция для формирования полей, куда можно походить (от наименьшей башни к наибольшей)
        # приоритет - создать башни наименьшего размера
        def make_another_cells_list(current_color, head=None, tower_length=1):
            if head:
                return [k
                        for k in range(2, 19)
                        if len(field_map[k]) <= tower_length and field_map[k].color == current_color]
            return [k
                    for k in range(13, 25)
                    if len(field_map[k]) <= tower_length and field_map[k].color == current_color]

        # остальные поля (без нулей)
        while True:
            tower = 1
            another_cells_numbers = make_another_cells_list(
                color,
                head=(self.white_head if color == 'white' else self.black_head),
                tower_length=tower
            )
            if another_cells_numbers:
                if not_singles_checkers:
                    for checker in not_singles_checkers:
                        if checker.position + dice in another_cells_numbers:
                            # убираем шашку со старой позиции
                            self.remove_checker_from_old_position(checker)
                            # присваеваем ей ноувю позицию
                            checker.position += dice
                            # размещаем ее на новой позиции
                            self.move_checker_to_new_position(checker)

                            return True, checker

                if others_checkers:
                    for checker in others_checkers:
                        if checker.position + dice in another_cells_numbers:
                            # убираем шашку со старой позиции
                            self.remove_checker_from_old_position(checker)
                            # присваеваем ей ноувю позицию
                            checker.position += dice
                            # размещаем ее на новой позиции
                            self.move_checker_to_new_position(checker)

                            return True, checker

            else:
                tower += 1
                if tower > 15:
                    return False,
                continue


g = Game()
g.computer_step()