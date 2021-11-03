class Foo:
    def foo_method(self) -> int:
        return 42


class Bar:
    def bar_method(self) -> int:
        return -42


class Example(Foo, Bar):
    pass
