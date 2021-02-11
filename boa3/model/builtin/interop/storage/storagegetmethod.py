from typing import Any, Dict, Iterable, List, Sized, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StorageGetMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'get'
        syscall = 'System.Storage.Get'
        # TODO: refactor to accept StorageContext as argument
        args: Dict[str, Variable] = {'key': Variable(Type.union.build([Type.bytes,
                                                                       Type.str
                                                                       ]))}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)

    def validate_parameters(self, *params: IExpression) -> bool:
        if any(not isinstance(param, IExpression) for param in params):
            return False

        args: List[IType] = [arg.type for arg in self.args.values()]
        # TODO: refactor when default arguments are implemented
        if len(params) != len(args):
            return False

        return self.key_arg.type.is_type_of(params[0].type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        from boa3.model.type.type import Type
        from boa3.neo.vm.type.Integer import Integer

        opcodes = Interop.StorageGetContext.opcode + super().opcode
        opcodes.extend([
            (Opcode.DUP, b''),
            (Opcode.ISNULL, b''),
            (Opcode.JMPIFNOT, Integer(7).to_byte_array(signed=True, min_length=1)),
            (Opcode.DROP, b''),
            (Opcode.PUSHDATA1, b'\x00'),
            (Opcode.CONVERT, Type.bytes.stack_item),
        ])
        return opcodes

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
            method = StorageGetMethod()
            method.args['key'] = Variable(key_type)
        return method
