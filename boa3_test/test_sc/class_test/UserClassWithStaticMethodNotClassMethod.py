from boa3.sc.compiletime import public


class Example:
    @staticmethod
    def some_method(cls: int) -> int:
        return cls


@public
def call_by_class_name(arg: int) -> int:
    return Example.some_method(arg)
