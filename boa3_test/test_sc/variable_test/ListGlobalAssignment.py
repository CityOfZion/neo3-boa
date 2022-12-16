from typing import List

from boa3.builtin.compile_time import public

a = [1, 2, 3, 4]


class Test:
    @classmethod
    def get_global(cls) -> List[int]:
        return a


@public
def append_to_global(value: int):
    a.append(value)


@public
def get_from_global() -> List[int]:
    return a


@public
def get_from_class() -> List[int]:
    return Test.get_global()


@public
def get_from_class_without_assigning() -> List[int]:
    Test.get_global()
    return []
