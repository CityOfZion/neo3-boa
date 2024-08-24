from boa3.sc.compiletime import public


class Example:
    @property
    def some_property() -> int:
        return 1


@public
def get_property() -> int:
    return Example().some_property
