class MyStack:
    def __init__(self):
        self.top = None
        self.color = None

        # attributes for elements:
        # prev_element
        # next_element

    def is_empty(self):
        return self.top is None

    def add_element(self, element):
        if self.is_empty():
            self.top = element
            self.color = element.color
        else:
            self.top.next_element = element
            self.top = element

    def pop_element(self):
        if not self.is_empty():
            if self.top.prev_element is not None:
                self.top = self.top.prev_element
                self.top.next_element = None
            else:
                self.top = None
                self.color = None


class MyList(list):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __getitem__(self, item):
        if isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            modify_slice = slice((start - 1 if start not in (len(self) - 1, 0) else None),
                                 (stop - 1 if stop not in (len(self), -1) else None),
                                 step)
            return super().__getitem__(modify_slice)
        if item > 0:
            if item - 1 in range(len(self)):
                return super().__getitem__(item - 1)
        else:
            if abs(item) in range(1, len(self) + 1):
                return super().__getitem__(item)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            modify_slice = slice((start - 1 if start not in (len(self) - 1, 0) else None),
                                 (stop - 1 if stop not in (len(self), -1) else None),
                                 step)
            super().__setitem__(modify_slice, value)
        else:
            if key > 0:
                if key - 1 in range(len(self)):
                    super().__setitem__(key - 1, value)
            else:
                if abs(key) in range(1, len(self) + 1):
                    super().__setitem__(key, value)


class FieldStructure:
    def __init__(self, data):
        self.data = data
        self.next_element = None
        self.previous_element = None

    def connect_elements(self, next_element=None, previous_element=None):
        if next_element:
            self.next_element = next_element
        if previous_element:
            self.previous_element = previous_element
