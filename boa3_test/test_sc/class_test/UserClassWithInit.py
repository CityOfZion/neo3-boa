from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        pass


@public
def build_example_object() -> Example:
    return Example()
