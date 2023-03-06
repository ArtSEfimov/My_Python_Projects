import random
from Accessory_module import MyList, MyStack, FieldStructure


class Checker:

    def __init__(self, color):
        self.color = color.lower()
        self.__position = 1

        self.prev_element = None
        self.next_element = None

        self.is_up = False
        self.is_single = False

    def get_position(self):
        return self.__position

    def set_position(self, value):
        self.__position = value

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

    def computer_step(self):  # black checkers
        self.first_dice, self.second_dice = self.throw_dices()

        # флаг первого хода (пригодится, когда надо будет снимать с головы две шашки)
        if self.first_step_flag:
            self.first_step_flag = False

        for dice in (self.first_dice, self.second_dice):
            if not self.first_priority('black', dice):  # если приоритетная попытка хода не удалась
                if not self.second_priority('black', dice):  # если и вторая попытка хода не удалась
                    print('Пропуск хода')

        self.field.show_field()

    def new_place_for_checker(self, checker: Checker):
        position = checker.position
        color = checker.color

        # определим, в какой части поля находится клетка, которая уже записана в свойство шашки
        quarters = {
            (1 if color == 'white' else 3): self.field.white_home,
            (2 if color == 'white' else 4): self.field.white_yard,
            (3 if color == 'white' else 1): self.field.black_home,
            (4 if color == 'white' else 2): self.field.black_yard
        }
        position_in_mylist = position % 6
        position_in_mylist = position_in_mylist if position_in_mylist else 6
        new_home = quarters[((position - 1) // 6) + 1].data[position_in_mylist]

        if new_home == 0:  # это значит,что там ноль, а не стэк, значит стэк нужно создавать заново
            new_home = MyStack()
        # это значит что там уже стэк
        new_home.add_element(checker)

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
                        checker.position += dice
                        # НУЖНО УБРАТЬ ШАШКУ СО СТАРОЙ ПОЗИЦИИ
                        self.new_place_for_checker(checker)
                        # здесь нужно убрать пустые стеки (превратить в нули)
                        # и изменить свойства верзним шашкам (top стеков)
                        return True

            if others_checkers:
                for checker in others_checkers:
                    if checker.position + dice in priority_cells_numbers:
                        checker.position += dice
                        # НУЖНО УБРАТЬ ШАШКУ СО СТАРОЙ ПОЗИЦИИ
                        self.new_place_for_checker(checker)
                        # здесь нужно убрать пустые стеки (превратить в нули)
                        # и изменить свойства верзним шашкам (top стеков)
                        return True

        return False  # ход не удался

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
                            checker.position += dice
                            # НУЖНО УБРАТЬ ШАШКУ СО СТАРОЙ ПОЗИЦИИ
                            self.new_place_for_checker(checker)
                            # здесь нужно убрать пустые стеки (превратить в нули)
                            # и изменить свойства верзним шашкам (top стеков)
                            return True
                if others_checkers:
                    for checker in others_checkers:
                        if checker.position + dice in another_cells_numbers:
                            checker.position += dice
                            # НУЖНО УБРАТЬ ШАШКУ СО СТАРОЙ ПОЗИЦИИ
                            self.new_place_for_checker(checker)
                            # здесь нужно убрать пустые стеки (превратить в нули)
                            # и изменить свойства верзним шашкам (top стеков)
                            return True

            else:
                tower += 1
                if tower > 15:
                    return False
                continue


g = Game()
g.computer_step()
