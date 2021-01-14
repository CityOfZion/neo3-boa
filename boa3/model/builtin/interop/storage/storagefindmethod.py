from typing import Any, Dict, Iterable, List, Sized, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StorageFindMethod(InteropMethod):

    def __init__(self, prefix_type: IType = None):
        from boa3.model.type.type import Type
        identifier = 'find'
        syscall = 'System.Storage.Find'
        # TODO: refactor to accept StorageContext as argument

        if prefix_type is None:
            prefix_type = Type.union.build([Type.bytes,
                                            Type.str
                                            ])
        args: Dict[str, Variable] = {'prefix': Variable(prefix_type)}

        from boa3.model.builtin.interop.iterator import IteratorType
        return_type = IteratorType.build(Type.dict.build([prefix_type,  # return an Iterator[prefix, bytes]
                                                          Type.bytes]))
        super().__init__(identifier, syscall, args, return_type=return_type)

    @property
    def identifier(self) -> str:
        return '-{0}_{1}'.format(self._identifier, self.prefix_arg.type.identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if any(not isinstance(param, IExpression) for param in params):
            return False

        args: List[IType] = [arg.type for arg in self.args.values()]
        # TODO: refactor when default arguments are implemented
        if len(params) != len(args):
            return False

        return self.prefix_arg.type.is_type_of(params[0].type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        return Interop.StorageGetContext.opcode + super().opcode

    @property
    def prefix_arg(self) -> Variable:
        return self.args['prefix']

    def build(self, value: Any) -> IBuiltinMethod:
        exp: List[IExpression] = []
        if isinstance(value, Sized):
            if len(value) > 1 or not isinstance(value, Iterable):
                return self
            exp = [exp if isinstance(exp, IExpression) else Variable(exp)
                   for exp in value if isinstance(exp, (IExpression, IType))]

        elif isinstance(exp, (IExpression, IType)):
            exp = [value if isinstance(value, IExpression) else Variable(value)]
        else:
            return self

        if not self.validate_parameters(*exp):
            return self

        method = self
        prefix_type: IType = exp[0].type
        if type(method.prefix_arg.type) != type(prefix_type):
            method = StorageFindMethod(prefix_type)
        return method