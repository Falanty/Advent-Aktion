class LoopingIterator:
    def __init__(self, start, *restart):
        self.start = start
        self.restart = restart[0] if restart else None

    def __iter__(self):
        self.i = self.start
        return self

    def __next__(self):
        x = self.i
        if self.i is self.restart:
            self.i = self.start
        else:
            self.i += 1
        return x


class SimpleIterator:
    def __init__(self, start, *step):
        self.start = start
        self.step = step[0] if step else 1

    def __iter__(self):
        self.i = self.start
        return self

    def __next__(self):
        x = self.i
        self.i += self.step
        return x
