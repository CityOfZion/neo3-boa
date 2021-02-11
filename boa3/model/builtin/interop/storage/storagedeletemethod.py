from typing import Any, Dict, Iterable, List, Sized, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StorageDeleteMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'delete'
        syscall = 'System.Storage.Delete'
        # TODO: refactor to accept StorageContext as argument
        args: Dict[str, Variable] = {'key': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.none)

    def validate_parameters(self, *params: IExpression) -> bool:
        if any(not isinstance(param, IExpression) for param in params):
            return False

        args: List[IType] = [arg.type for arg in self.args.values()]
        # TODO: refactor when default arguments are implemented
        if len(params) != len(args):
            return False

        return self._validate_key_type(params[0].type)

    def _validate_key_type(self, key_type: IType):
        # TODO: refactor when `Union` type is implemented
        from boa3.model.type.type import Type
        return Type.str.is_type_of(key_type) or Type.bytes.is_type_of(key_type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        return Interop.StorageGetContext.opcode + super().opcode

    @property
    def storage_context_hash(self) -> bytes:
        # TODO: refactor when default arguments are implemented
        return self._method_hash(self._storage_context)

    @property
    def key_arg(self) -> Variable:
        return self.args['key']

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
        key_type: IType = exp[0].type
        if not method.key_arg.type.is_type_of(key_type):
            method = StorageDeleteMethod()
            method.args['key'] = Variable(key_type)
        return method
