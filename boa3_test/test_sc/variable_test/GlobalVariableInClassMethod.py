from boa3.builtin import public

GLOBAL_TEST = 42


class Example:
    val1 = 1

    def __init__(self):
        self.val2 = 2

    def export(self) -> dict:
        return {
            'val1': self.val1,
            'val2': self.val2,
            'bar': GLOBAL_TEST  # without this, it works
        }

    def get_constant(self) -> int:
        return GLOBAL_TEST  # this works as expected


@public
def use_variable_in_map() -> dict:
    return Example().export()


@public
def use_variable_in_func() -> int:
    return Example().get_constant()
