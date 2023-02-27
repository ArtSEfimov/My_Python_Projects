class MyList(list):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __getitem__(self, item):
        if item - 1 in range(len(self)):
            return super().__getitem__(item - 1)
        return None

    def __setitem__(self, key, value):
        if key - 1 in range(len(self)):
            super(MyList, self).__setitem__(key - 1, value)
        return None


class Field:
    def __init__(self):
        self.white_home = []
        self.black_home = []
        self.white_yard = []
        self.black_yard = []

    def init_field(self):
        pass
