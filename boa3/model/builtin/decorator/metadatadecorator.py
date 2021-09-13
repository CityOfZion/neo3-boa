from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator


class MetadataDecorator(IBuiltinDecorator):
    def __init__(self):
        identifier = 'metadata'
        super().__init__(identifier)
