from typing import Any, Dict, List, Optional, Union

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IsInstanceMethod(IBuiltinMethod):

    def __init__(self, target_type: IType = None):
        from boa3.internal.model.type.type import Type
        identifier = 'isinstance'

        args: Dict[str, Variable] = {
            'x': Variable(Type.any),
            'A_tuple': None
        }

        super().__init__(identifier, args, return_type=Type.bool)

        from boa3.internal.model.type.collection.sequence.tupletype import TupleType
        from boa3.internal.model.type.annotation.metatype import MetaType
        from boa3.internal.model.type.annotation.uniontype import UnionType

        if not isinstance(target_type, IType):
            instances = [Type.none]
        elif isinstance(target_type, TupleType) and isinstance(target_type.item_type, UnionType):
            instances = [typ.meta_type if isinstance(typ, MetaType) else typ
                         for typ in target_type.item_type.union_types]
        else:
            instances = [target_type.meta_type if isinstance(target_type, MetaType) else target_type]

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
        from boa3.internal.model.type.type import Type
        if (len(self._instances_type) == 0
                or (len(self._instances_type) == 1 and self._instances_type[0] in (None, Type.none))
            ):
            return self._identifier

        types = list({tpe.raw_identifier for tpe in self._instances_type})
        types.sort()
        return '-{0}_of_{1}'.format(self._identifier, '_or_'.join(types))

    def args_to_be_generated(self) -> List[int]:
        args = [name for name, symbol in self.args.items() if isinstance(symbol, Variable)]
        return [list(self.args).index(key) for key in args]

    @property
    def is_supported(self) -> bool:
        from boa3.internal.model.type.classes.classtype import ClassType
        return not any(isinstance(param, ClassType) and len(param.is_instance_opcodes()) == 0
                       for param in self._instances_type)

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

    def generate_internal_opcodes(self, code_generator):
        if len(self._instances_type) == 0:
            code_generator.insert_type_check(None)
            return

        ifs = []
        types = self._instances_type.copy()
        for type_to_check in types[:-1]:
            code_generator.duplicate_stack_top_item()
            type_to_check.generate_is_instance_type_check(code_generator)

            if_is_instance = code_generator.convert_begin_if()
            code_generator.change_jump(if_is_instance, Opcode.JMPIF)

            ifs.append(if_is_instance)

        types[-1].generate_is_instance_type_check(code_generator)
        if len(types) > 1:
            last_if = code_generator.convert_begin_if()
            code_generator.change_jump(last_if, Opcode.JMP)

        for begin_if in ifs:
            code_generator.convert_end_if(begin_if, is_internal=True)

        if len(types) > 1:
            code_generator.remove_stack_top_item()
            code_generator.convert_literal(True)
            code_generator.convert_end_if(last_if, is_internal=True)

    @property
    def _args_on_stack(self) -> int:
        return 1

    @property
    def generation_order(self) -> List[int]:
        # type should not be converted
        indexes = super().generation_order
        typ_index = list(self.args).index('A_tuple')

        if typ_index in indexes:
            indexes.remove(typ_index)

        return indexes

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and self.validate_parameters(*value):
            return IsInstanceMethod(value[-1])
        return super().build(value)
