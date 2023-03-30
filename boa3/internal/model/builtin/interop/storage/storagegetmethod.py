import ast
from typing import Any, Dict, Iterable, List, Sized, Tuple

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StorageGetMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import StorageContextType
        from boa3.internal.model.type.primitive.bytestringtype import ByteStringType

        identifier = 'get'
        syscall = 'System.Storage.Get'
        context_type = StorageContextType.build()
        byte_string_type = ByteStringType.build()

        args: Dict[str, Variable] = {'key': Variable(byte_string_type),
                                     'context': Variable(context_type)}

        from boa3.internal.model.builtin.interop.storage.storagegetcontextmethod import StorageGetContextMethod
        default_id = StorageGetContextMethod(context_type).identifier
        context_default = set_internal_call(ast.parse("{0}()".format(default_id)
                                                      ).body[0].value)
        super().__init__(identifier, syscall, args, defaults=[context_default], return_type=Type.bytes)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.type.Integer import Integer

        opcodes = super()._opcode
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
    def generation_order(self) -> List[int]:
        """
        Gets the indexes order that need to be used during code generation.
        If the order for generation is the same as inputted in code, returns reversed(range(0,len_args))

        :return: Index order for code generation
        """
        indexes = super().generation_order
        context_index = list(self.args).index('context')

        if indexes[-1] != context_index:
            # context must be the last generated argument
            indexes.remove(context_index)
            indexes.append(context_index)

        return indexes

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
