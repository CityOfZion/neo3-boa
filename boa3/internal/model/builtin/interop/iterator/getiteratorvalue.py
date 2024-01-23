from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.internal.model.variable import Variable


class GetIteratorValue(InteropMethod):
    def __init__(self, iterator: IteratorType):
        syscall = 'System.Iterator.Value'
        identifier = '-get_iterator_value'
        args: dict[str, Variable] = {'self': Variable(iterator)}

        result_type = iterator.item_type
        from boa3.internal.model.type.collection.mapping.mappingtype import MappingType
        if isinstance(iterator._origin_collection, MappingType):
            from boa3.internal.model.type.type import Type
            result_type = Type.tuple.build((iterator.key_type, iterator.item_type))
        super().__init__(identifier, syscall, args, return_type=result_type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def self_arg(self) -> Variable:
        return self.args['self']

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        super().generate_internal_opcodes(code_generator)

        # if result is not Struct
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.Struct)
        is_struct = code_generator.convert_begin_if()

        #   cast(result, list)
        code_generator.convert_cast(Type.list, is_internal=True)

        code_generator.convert_end_if(is_struct, is_internal=True)


class IteratorValueProperty(IBuiltinProperty):
    def __init__(self, iterator: IteratorType):
        identifier = 'iterator_value'
        getter = GetIteratorValue(iterator)
        super().__init__(identifier, getter)
