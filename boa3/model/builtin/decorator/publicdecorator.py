from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator


class PublicDecorator(IBuiltinDecorator):
    def __init__(self):
        identifier = 'public'
        super().__init__(identifier)
