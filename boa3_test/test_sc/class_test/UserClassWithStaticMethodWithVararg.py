from boa3.sc.compiletime import public


class Example:
    @staticmethod
    def some_method(*args: int) -> int:
        if len(args) > 0:
            return args[0]
        return 42


@public
def call_by_class_name(arg: list[int]) -> int:
    return Example.some_method(*arg)
