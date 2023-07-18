from boa3.builtin.compile_time import public


class Example:
    def __init__(self, string_: str):
        self._string = string_

    @property
    def string_prop(self) -> str:
        return self._string


@public
def main(string: str, start: int, end: int) -> str:
    obj = Example(string)
    return obj.string_prop[start:end]
