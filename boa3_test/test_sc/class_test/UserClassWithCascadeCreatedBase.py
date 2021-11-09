from boa3.builtin import public


class Foo:
    def bar(self) -> int:
        return 42


class Zubs(Foo):
    pass


class Example(Zubs):
    pass


@public
def implemented_method() -> int:
    return Zubs().bar()


@public
def inherited_method() -> int:
    return Example().bar()
