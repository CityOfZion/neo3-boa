from boa3.sc.compiletime import public


class SomeClass:
    def __init__(self):
        self._some_list: list[int] = [1, 2, 3]

    @property
    def inner_list(self) -> list[int]:
        return self._some_list

    def append(self, value: int) -> bool:
        self._some_list.append(value)
        return True


@public
def main() -> list:
    a = SomeClass()
    a.append(4)
    return a.inner_list
