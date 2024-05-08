from boa3.internal.model.method import Method
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class StandardMethod(Method):
    def __init__(self,
                 display_name: str,
                 args: dict[str, IType] = None,
                 return_type: IType = Type.none,
                 safe: bool = False,
                 literal_implementation: bool = True,
                 deprecated: bool = False
                 ):
        if not isinstance(args, dict):
            args = {}
        method_args = {key: Variable(value) for key, value in args.items()}
        super().__init__(
            args=method_args,
            return_type=return_type,
            is_public=True,
            external_name=display_name,
            is_safe=safe,
            deprecated=deprecated
        )

        self.literal_implementation = literal_implementation
