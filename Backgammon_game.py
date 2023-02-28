class MyList(list):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, slice):
            print(item.indices(len(self)))
            start, stop, step = item.indices(len(self))
            modify_slice = slice((start - 1 if start not in (len(self) - 1, 0) else None),
                                 (stop - 1 if stop not in (len(self), -1) else None),
                                 step)
            print(modify_slice)
            return super().__getitem__(modify_slice)
        if item - 1 in range(len(self)):
            return super().__getitem__(item - 1)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            modify_slice = slice((start - 1 if start not in (len(self) - 1, 0) else None),
                                 (stop - 1 if stop not in (len(self), -1) else None),
                                 step)
            super().__setitem__(modify_slice, value)
        if key - 1 in range(len(self)):
            super(MyList, self).__setitem__(key - 1, value)


ml = MyList([i for i in range(1, 11)])
ml[1:5] = [2, 2, 2, 2]
print(ml)


class Field:
    def __init__(self):
        self.white_home = MyList([0] * 15)
        self.black_home = MyList([0] * 15)
        self.white_yard = MyList([0] * 15)
        self.black_yard = MyList([0] * 15)

        self.field = MyList()

    def init_field(self):
        self.white_home[1] = 'X' * 15
        self.black_home[1] = 'X' * 15
        self.field.append(self.white_home)
        self.field.append(self.black_home)
        self.field.append(self.white_yard)
        self.field.append(self.black_yard)

#     def show_field(self):
#         for row in self.field:
#             print(row[::-1])
#             # row = row[::-1]
#             # for element in row:
#             #     print(element)
#
#
# f = Field()
#
# f.init_field()
#
# f.show_field()
