from boa3.sc.compiletime import public


class Example:
    def __init__(self):
        pass


@public
def build_example_object() -> Example:
    return Example()
