from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.model.expression import IExpression


class MetadataDecorator(IBuiltinDecorator):
    def __init__(self):
        identifier = 'metadata'
        super().__init__(identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == len(self.args)
