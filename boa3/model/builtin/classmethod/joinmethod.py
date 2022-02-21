from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.type.collection.mapping.mutable.dicttype import DictType
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.primitive.ibytestringtype import IByteStringType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class JoinMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None, iterable_type: Union[SequenceType, DictType] = None):
        from boa3.model.type.type import Type

        if not isinstance(self_type, IByteStringType):
            from boa3.model.type.primitive.bytestringtype import ByteStringType
            self_type = ByteStringType.build()

        if not isinstance(iterable_type, (SequenceType, DictType)):
            iterable_type = Type.sequence.build_collection([self_type])

        identifier = 'join'
        args: Dict[str, Variable] = {
            'self': Variable(self_type),
            'iterable': Variable(iterable_type),
        }

        super().__init__(identifier, args, return_type=self_type)

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type

        if Type.dict.is_type_of(self._arg_iterable.type):
            return '-{0}_{1}'.format(self._identifier, Type.dict.identifier)

        return self._identifier  # JoinMethod default value for self

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def _arg_iterable(self) -> Variable:
        return self.args['iterable']

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count

        jmp_place_holder = (Opcode.JMP, b'\x01')

        # Receives: string, iterable
        verify_empty_string = [         # verify if string is empty
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),         # iterable_size = len(iterable)
            (Opcode.PUSH0, b''),        # index = 0
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            jmp_place_holder            # if iterable_size is less than or equals to 0, return empty string
        ]

        initialize_string = [           # initializes the return value
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),     # joined = iterable[0]
            (Opcode.SWAP, b''),
            (Opcode.INC, b''),          # index++
            (Opcode.SWAP, b''),
        ]

        from boa3.model.type.type import Type
        if Type.dict.is_type_of(self._arg_iterable.type):
            get_dict_keys = [           # get dictionary keys as an array
                (Opcode.REVERSE3, b''),
                (Opcode.KEYS, b''),
                (Opcode.REVERSE3, b''),
            ]
            initialize_string = get_dict_keys + initialize_string

        verify_index = [                # verify if all items on the iterable were visited
            (Opcode.OVER, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            jmp_place_holder            # jump to remove_extra_values if every item was already visited
        ]

        concat_strings = [              # concatenate the items inside de interable
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.CAT, b''),          # joined = joined + string
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PICKITEM, b''),
            (Opcode.CAT, b''),          # joined = joined + iterable[index]
            (Opcode.SWAP, b''),
            (Opcode.INC, b''),          # index++
            (Opcode.SWAP, b''),
            # jump back to verify_index
        ]

        jmp_back_to_verify = Opcode.get_jump_and_data(Opcode.JMP, -get_bytes_count(verify_index +
                                                                                   concat_strings))
        concat_strings.append(jmp_back_to_verify)

        jmp_concatenation = Opcode.get_jump_and_data(Opcode.JMPLE, get_bytes_count(initialize_string +
                                                                                   verify_index +
                                                                                   concat_strings), True)
        verify_empty_string[-1] = jmp_concatenation

        add_empty_string = [            # add a empty string at the top of the stack
            (Opcode.PUSHDATA1, b'\x00')
        ]

        jmp_concatenation = Opcode.get_jump_and_data(Opcode.JMPGE, get_bytes_count(concat_strings +
                                                                                   add_empty_string), True)
        verify_index[-1] = jmp_concatenation

        remove_extra_values = [         # remove all values from stack except the joined string
            (Opcode.NIP, b''),
            (Opcode.NIP, b''),
            (Opcode.NIP, b''),
            (Opcode.NIP, b''),
        ]

        return (
            verify_empty_string +
            initialize_string +
            verify_index +
            concat_strings +
            add_empty_string +
            remove_extra_values
        )

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, Iterable):
            value = [value]
        if isinstance(value, list) and len(value) <= 2:
            self_type = self._arg_self.type
            if len(value) < 2:
                value.append(None)
            if isinstance(value[0], type(self_type)) and isinstance(value[1], SequenceType):
                return self
            else:
                return JoinMethod(value[0], value[1])

        return super().build(value)
