from boa3.builtin.compile_time import public


class Example:
    def __init__(self, arg0: int, arg1: str):
        pass


@public
def build_example_object() -> Example:
    return Example(42, '42')
