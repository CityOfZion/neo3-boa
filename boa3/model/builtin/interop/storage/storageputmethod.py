from typing import Any, Dict, Iterable, List, Sized, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StoragePutMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'put'
        syscall = 'System.Storage.Put'
        # TODO: refactor to accept StorageContext as argument
        args: Dict[str, Variable] = {'key': Variable(Type.union.build([Type.bytes,
                                                                       Type.str
                                                                       ])),
                                     'value': Variable(Type.union.build([Type.bytes,
                                                                         Type.str,
                                                                         Type.int
                                                                         ]))
                                     }
        super().__init__(identifier, syscall, args, return_type=Type.none)

    def validate_parameters(self, *params: IExpression) -> bool:
        if any(not isinstance(param, IExpression) for param in params):
            return False

        args: List[IType] = [arg.type for arg in self.args.values()]
        # TODO: refactor when default arguments are implemented
        if len(params) != len(args):
            return False

        return (self.key_arg.type.is_type_of(params[0].type)
                and self.value_arg.type.is_type_of(params[1].type))

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        return Interop.StorageGetContext.opcode + super().opcode

    @property
    def key_arg(self) -> Variable:
        return self.args['key']

    @property
    def value_arg(self) -> Variable:
        return self.args['value']

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, (Sized, Iterable)):
            return self
        num_args: int = len(self.args)
        if len(value) != num_args or any(not isinstance(exp, (IExpression, IType)) for exp in value[:num_args]):
            return self

        exp = [exp if isinstance(exp, IExpression) else Variable(exp) for exp in value]
        if not self.validate_parameters(*exp):
            return self

        key_type: IType = exp[0].type
        value_type: IType = exp[1].type
        if self.key_arg.type.is_type_of(key_type) and self.value_arg.type.is_type_of(value_type):
            return self

        method: InteropMethod = StoragePutMethod()
        method.args['key'] = Variable(key_type)
        method.args['value'] = Variable(value_type)
        return method
