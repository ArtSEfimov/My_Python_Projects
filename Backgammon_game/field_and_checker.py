from data_structures import FieldStructure, MyList, MyStack
from collections import deque


class Checker:

    def __init__(self, color):
        self.color = color.lower()
        self.__position = 1
        self.__backup_position = deque()

        self.prev_element = None
        self.next_element = None

        self.is_up = None
        self.is_single = None

    def get_position(self):
        return self.__position

    def set_position(self, value):
        self.backup_position = self.__position
        self.__position = value

    def get_backup_position(self):
        return self.__backup_position.pop()

    def set_backup_position(self, value):
        self.__backup_position.append(value)

    backup_position = property(get_backup_position, set_backup_position)
    position = property(get_position, set_position)

    def __repr__(self):
        return f'{self.position}'


class Field:
    def __init__(self):
        self.white_home = FieldStructure(MyList([0] * 6))
        self.black_home = FieldStructure(MyList([0] * 6))
        self.white_yard = FieldStructure(MyList([0] * 6))
        self.black_yard = FieldStructure(MyList([0] * 6))

    @staticmethod
    def get_sum_of_structure(structure, color):
        return sum(
            (element.count
             for element in structure.data
             if isinstance(element, MyStack)
             and element.color == color
             )
        )

    @staticmethod
    def get_occupied_of_structure(structure, color):
        summa = 0
        for element in structure.data:
            if isinstance(element, MyStack):
                if element.color == color:
                    summa += 1
        return summa

    @staticmethod
    def get_count_of_free_cells(structure):
        count = 0
        for element in structure.data:
            if not isinstance(element, MyStack):
                count += 1
        return count

    def init_field_and_create_field_structure(self):
        self.white_home.connect_elements(next_element=self.white_yard)
        self.white_yard.connect_elements(previous_element=self.white_home, next_element=self.black_home)
        self.black_home.connect_elements(next_element=self.black_yard)
        self.black_yard.connect_elements(previous_element=self.black_home, next_element=self.white_home)

    def show_field(self):
        print(f'\n{15 * "="}\n')
        count = 1
        start = self.white_home
        for e in range(4):
            tmp_data = start.data
            for element in tmp_data:
                # на случай модификации функции вывода в консоль
                # if type(element) == MyStack:
                #     print(*element)
                # /на случай модификации функции вывода в консоль

                print(f'{count:2d}|\t {element}')
                count += 1
            if e < 3:
                print()

            start = start.next_element
        print(f'\n{15 * "="}\n')
