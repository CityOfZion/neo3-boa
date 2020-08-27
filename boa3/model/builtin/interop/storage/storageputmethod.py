from typing import Any, Dict, Iterable, List, Sized, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.expression import IExpression
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StoragePutMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'put'
        syscall = 'System.Storage.Put'
        self._storage_context = 'System.Storage.GetContext'  # TODO: refactor when default arguments are implemented
        args: Dict[str, Variable] = {'key': Variable(Type.bytes), 'value': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.none)

    @property
    def requires_storage(self) -> bool:
        return True

    def validate_parameters(self, *params: IExpression) -> bool:
        if any(not isinstance(param, IExpression) for param in params):
            return False

        args: List[IType] = [arg.type for arg in self.args.values()]
        # TODO: refactor when default arguments are implemented
        if len(params) != len(args):
            return False

        return (self._validate_key_type(params[0].type)
                and self._validate_value_type(params[1].type))

    def _validate_key_type(self, key_type: IType):
        # TODO: refactor when `Union` type is implemented
        from boa3.model.type.type import Type
        return Type.str.is_type_of(key_type) or Type.bytes.is_type_of(key_type)

    def _validate_value_type(self, key_type: IType):
        # TODO: refactor when `Union` type is implemented
        from boa3.model.type.type import Type
        return (Type.str.is_type_of(key_type)
                or Type.int.is_type_of(key_type)
                or Type.bytes.is_type_of(key_type))

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        opcodes = [(Opcode.SYSCALL, self.storage_context_hash)]
        opcodes.extend(super().opcode)
        return opcodes

    @property
    def storage_context_hash(self) -> bytes:
        # TODO: refactor when default arguments are implemented
        return self._method_hash(self._storage_context)

    @property
    def key_arg(self) -> Variable:
        return self.args['key']

    @property
    def value_arg(self) -> Variable:
        return self.args['value']

    def build(self, value: Any):
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
