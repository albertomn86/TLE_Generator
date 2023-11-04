class Tle(object):
    def __init__(self, title: str, l1: str, l2: str):
        self.object_name = title.decode().strip()
        self.object_id = l2.decode().split()[1]
        self._title_line = title
        self._line_1 = l1
        self._line_2 = l2

    def __str__(self):
        return f'{self._title_line}\n{self._line_1}\n{self._line_2}'

    def getLines(self) -> list:
        return [self._title_line, self._line_1, self._line_2]
