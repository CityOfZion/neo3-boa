from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator


class StaticMethodDecorator(IBuiltinDecorator):
    def __init__(self):
        identifier = 'staticmethod'
        super().__init__(identifier)
