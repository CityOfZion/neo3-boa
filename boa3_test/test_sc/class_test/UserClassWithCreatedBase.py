from boa3.sc.compiletime import public


class Foo:
    def bar(self) -> int:
        return 42


class Example(Foo):
    pass


@public
def implemented_method() -> int:
    return Foo().bar()


@public
def inherited_method() -> int:
    return Example().bar()
