from boa3.internal.model.builtin.decorator.builtindecorator import IBuiltinDecorator


class InstanceMethodDecorator(IBuiltinDecorator):
    def __init__(self):
        identifier = '-instancemethod'  # MUST NOT be used from smart contracts
        super().__init__(identifier)

    @property
    def has_cls_or_self(self) -> bool:
        return True
