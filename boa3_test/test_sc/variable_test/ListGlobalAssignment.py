from boa3.sc.compiletime import public

a = [1, 2, 3, 4]


class Test:
    @classmethod
    def get_global(cls) -> list[int]:
        return a


@public
def append_to_global(value: int):
    a.append(value)


@public
def get_from_global() -> list[int]:
    return a


@public
def get_from_class() -> list[int]:
    return Test.get_global()


@public
def get_from_class_without_assigning() -> list[int]:
    Test.get_global()
    return []
