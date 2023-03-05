def second_priority(self, color, dice, counter_value=1):
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
                        # здесь нужно физически перенести шашку на новое место
                        return True
            if others_checkers:
                for checker in others_checkers:
                    if checker.position + dice in another_cells_numbers:
                        checker.position += dice
                        # здесь нужно физически перенести шашку на новое место
                        return True

        else:
            tower += 1
            if tower > 15:
                return False
            continue
