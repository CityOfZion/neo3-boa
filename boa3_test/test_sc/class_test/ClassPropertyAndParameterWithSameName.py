from boa3.builtin.compile_time import public


class Example:
    def __init__(self, arg: str):
        self._internal_value = arg

    @property
    def same_name(self) -> str:
        return self._internal_value


@public
def main(same_name: str) -> str:
    obj = Example(same_name)
    return obj.same_name
