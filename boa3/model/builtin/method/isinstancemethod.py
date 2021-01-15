from typing import Any, Dict, List, Optional, Tuple, Union

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class IsInstanceMethod(IBuiltinMethod):

    def __init__(self, target_type: IType = None):
        from boa3.model.type.type import Type
        identifier = 'isinstance'

        args: Dict[str, Variable] = {
            'x': Variable(Type.any),
            'A_tuple': None
        }

        super().__init__(identifier, args, return_type=Type.bool)

        from boa3.model.type.collection.sequence.tupletype import TupleType
        from boa3.model.type.annotation.uniontype import UnionType
        if not isinstance(target_type, IType):
            instances = [Type.none]
        elif isinstance(target_type, TupleType) and isinstance(target_type.item_type, UnionType):
            instances = target_type.item_type.union_types
        else:
            instances = [target_type]

        self._instances_type: List[IType] = instances

    def set_instance_type(self, value: List[IType]):
        new_list = []
        for tpe in value:
            if isinstance(tpe, IType):
                if not any(tpe.raw_identifier == other.raw_identifier for other in new_list):
                    new_list.append(tpe)

        self._instances_type = new_list

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type
        if (len(self._instances_type) == 0
                or (len(self._instances_type) == 1 and self._instances_type[0] in (None, Type.none))
            ):
            return self._identifier

        types = list({tpe.raw_identifier for tpe in self._instances_type})
        types.sort()
        return '-{0}_of_{1}'.format(self._identifier, '_or_'.join(types))

    @property
    def is_supported(self) -> bool:
        from boa3.model.type.classtype import ClassType
        return not any(isinstance(param, ClassType) for param in self._instances_type)

    def not_supported_str(self, callable_id: str) -> str:
        types = (self._instances_type[0].identifier if len(self._instances_type) == 1
                 else '({0})'.format(', '.join([arg.identifier for arg in self._instances_type])))

        return '{0}({1}, {2})'.format(callable_id, self.arg_x, types)

    @property
    def arg_x(self) -> Variable:
        return self.args['x']

    def validate_parameters(self, *params: Union[IExpression, IType]) -> bool:
        if len(params) != 2:
            return False

        return not any(not isinstance(param, (IExpression, IType)) for param in params)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        if len(self._instances_type) == 0:
            return [
                (Opcode.ISNULL, b'')
            ]
        else:
            opcodes = []
            from boa3.model.type.type import Type
            types = self._instances_type.copy()

            code, data = self._type_opcode(types[-1])
            size = len(code + data)
            opcodes.append((code, data))

            from boa3.neo.vm.type.Integer import Integer

            for instance_type in reversed(types[:-1]):
                jmp_if_true_body = [
                    (Opcode.DUP, b''),
                    self._type_opcode(instance_type),
                    (Opcode.JMPIF, Integer(size + 4).to_byte_array(min_length=1, signed=True))
                ]

                for opcode, code_data in jmp_if_true_body:
                    size += len(opcode + code_data)

                opcodes = jmp_if_true_body + opcodes

            if len(types) > 1:
                opcodes.extend([
                    (Opcode.JMP, Integer(4).to_byte_array(min_length=1, signed=True)),
                    (Opcode.DROP, b''),
                    (Opcode.PUSH1, b''),
                ])

            return opcodes

    def _type_opcode(self, instance_type: Optional[IType]) -> Tuple[Opcode, bytes]:
        from boa3.model.type.type import Type
        if instance_type in (None, Type.none):
            return Opcode.ISNULL, b''
        else:
            return Opcode.ISTYPE, instance_type.stack_item

    @property
    def _args_on_stack(self) -> int:
        return 1

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and self.validate_parameters(*value):
            return IsInstanceMethod(value[-1])
        return super().build(value)
