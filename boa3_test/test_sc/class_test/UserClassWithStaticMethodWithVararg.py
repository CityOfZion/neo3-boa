from typing import List

from boa3.builtin.compile_time import public


class Example:
    @staticmethod
    def some_method(*args: int) -> int:
        if len(args) > 0:
            return args[0]
        return 42


@public
def call_by_class_name(arg: List[int]) -> int:
    return Example.some_method(*arg)
