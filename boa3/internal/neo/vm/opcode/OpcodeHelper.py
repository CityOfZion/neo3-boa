from __future__ import annotations

from typing import Dict, Optional, Tuple, Union

from boa3.internal.constants import FOUR_BYTES_MAX_VALUE
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String


def get_pushdata_and_data(bytestring: Union[str, bytes]) -> Tuple[Opcode, bytes]:
    """
    Gets the push opcode and data to the respective str ot bytes value

    :param bytestring: value that will be pushed
    :return: the respective opcode and its required data
    :rtype: Tuple[Opcode, bytes]
    """
    if isinstance(bytestring, str):
        bytestring = String(bytestring).to_bytes()

    bytes_size = Integer(len(bytestring)).to_byte_array(min_length=1)
    if len(bytes_size) == 1:
        opcode = Opcode.PUSHDATA1
    elif len(bytes_size) == 2:
        opcode = Opcode.PUSHDATA2
    else:
        if len(bytes_size) > 4:
            bytestring = bytestring[:FOUR_BYTES_MAX_VALUE]
        bytes_size = Integer(len(bytestring)).to_byte_array(min_length=4)
        opcode = Opcode.PUSHDATA4

    data = bytes_size + bytestring
    return opcode, data


def get_pushdata_and_data_from_size(data_size: int) -> Tuple[Opcode, bytes]:
    bytes_size = Integer(data_size).to_byte_array(min_length=1)
    if len(bytes_size) == 1:
        opcode = Opcode.PUSHDATA1
    elif len(bytes_size) == 2:
        opcode = Opcode.PUSHDATA2
    else:
        bytes_size = FOUR_BYTES_MAX_VALUE
        opcode = Opcode.PUSHDATA4

    return opcode, bytes_size


def get_literal_push(integer: int) -> Optional[Opcode]:
    """
    Gets the push opcode to the respective integer

    :param integer: value that will be pushed
    :return: the respective opcode
    :rtype: Opcode or None
    """
    if -1 <= integer <= 16:
        opcode_value: int = Integer.from_bytes(Opcode.PUSH0) + integer
        return Opcode(Integer(opcode_value).to_byte_array())
    else:
        return None


def get_push_and_data(integer: int) -> Tuple[Opcode, bytes]:
    """
    Gets the push opcode and data to the respective integer

    :param integer: value that will be pushed
    :return: the respective opcode and its required data
    :rtype: Tuple[Opcode, bytes]
    """
    opcode = get_literal_push(integer)
    if isinstance(opcode, Opcode):
        return opcode, b''
    else:
        data = Integer(integer).to_byte_array(signed=True, min_length=1)
        if len(data) == 1:
            opcode = Opcode.PUSHINT8
        elif len(data) == 2:
            opcode = Opcode.PUSHINT16
        elif len(data) <= 4:
            data = Integer(integer).to_byte_array(signed=True, min_length=4)
            opcode = Opcode.PUSHINT32
        elif len(data) <= 8:
            data = Integer(integer).to_byte_array(signed=True, min_length=8)
            opcode = Opcode.PUSHINT64
        elif len(data) <= 16:
            data = Integer(integer).to_byte_array(signed=True, min_length=16)
            opcode = Opcode.PUSHINT128
        else:
            data = data[:32]
            opcode = Opcode.PUSHINT256

        return opcode, data


def has_larger_opcode(opcode: Opcode) -> bool:
    return opcode in _larger_opcode


def get_larger_opcode(opcode: Opcode):
    """
    Gets the large opcode to the standard opcode

    :return: the respective opcode
    :rtype: Opcode or None
    """
    if opcode in _larger_opcode:
        return _larger_opcode[opcode]
    elif opcode in _larger_opcode.values():
        return opcode
    else:
        return None


_larger_opcode: Dict[Opcode, Opcode] = {
    Opcode.JMP: Opcode.JMP_L,
    Opcode.JMPIF: Opcode.JMPIF_L,
    Opcode.JMPIFNOT: Opcode.JMPIFNOT_L,
    Opcode.JMPEQ: Opcode.JMPEQ_L,
    Opcode.JMPNE: Opcode.JMPNE_L,
    Opcode.JMPGT: Opcode.JMPGT_L,
    Opcode.JMPGE: Opcode.JMPGE_L,
    Opcode.JMPLT: Opcode.JMPLT_L,
    Opcode.JMPLE: Opcode.JMPLE_L,
    Opcode.CALL: Opcode.CALL_L,
    Opcode.TRY: Opcode.TRY_L,
    Opcode.ENDTRY: Opcode.ENDTRY_L
}


def is_jump(opcode: Opcode) -> bool:
    return Opcode.JMP <= opcode <= Opcode.JMPLE_L


def get_try_and_data(except_target: int, finally_target: int = 0, jump_through: bool = False) -> Tuple[Opcode, bytes]:
    """
    Gets the try opcode and data to the respective targets
    """
    jmp_placeholder = Opcode.JMP
    jmp_to_except_placeholder = get_jump_and_data(jmp_placeholder, except_target + jump_through, jump_through)
    jmp_to_finally_placeholder = get_jump_and_data(jmp_placeholder, finally_target, jump_through and finally_target > 0)

    if jmp_to_except_placeholder[0] == jmp_placeholder and jmp_to_finally_placeholder[0] == jmp_placeholder:
        opcode = Opcode.TRY
    else:
        opcode = Opcode.TRY_L

    from boa3.internal.neo.vm.opcode.OpcodeInfo import OpcodeInfo
    opcode_info = OpcodeInfo.get_info(opcode)
    each_arg_len = opcode_info.data_len // 2

    return (opcode,
            jmp_to_except_placeholder[1].rjust(each_arg_len, b'\x00')
            + jmp_to_finally_placeholder[1].rjust(each_arg_len, b'\x00'))


def get_jump_and_data(opcode: Opcode, integer: int, jump_through: bool = False) -> Tuple[Opcode, bytes]:
    """
    Gets the jump opcode and data to the respective integer

    :param opcode: which jump will be used
    :param integer: number of bytes that'll be jumped
    :param jump_through: whether it should go over the instructions or not
    :return: the respective opcode and its required data
    :rtype: Tuple[Opcode, bytes]
    """
    if not has_target(opcode):
        opcode = Opcode.JMP

    from boa3.internal.neo.vm.opcode.OpcodeInfo import OpcodeInfo
    opcode_info = OpcodeInfo.get_info(opcode)
    arg_size = opcode_info.data_len
    jmp_arg = Integer(arg_size + integer + jump_through).to_byte_array(min_length=arg_size) if integer > 0 \
        else Integer(integer).to_byte_array(min_length=arg_size)

    if len(jmp_arg) > opcode_info.max_data_len and has_larger_opcode(opcode):
        opcode = get_larger_opcode(opcode)
        opcode_info = OpcodeInfo.get_info(opcode)
        arg_size = opcode_info.data_len
        jmp_arg = Integer(arg_size + integer + jump_through).to_byte_array(min_length=arg_size) if integer > 0 \
            else Integer(integer).to_byte_array(min_length=arg_size)
        jmp_opcode = opcode
    else:
        jmp_opcode = opcode

    jmp_arg = jmp_arg[-arg_size:]

    return jmp_opcode, jmp_arg


def has_target(opcode: Opcode) -> bool:
    return Opcode.JMP <= opcode <= Opcode.CALL_L or Opcode.TRY <= opcode < Opcode.ENDFINALLY


def get_drop(position: int) -> Optional[Opcode]:
    """
    Gets the opcode to remove the item n back in the stack

    :param position: index of the variable
    :return: the respective opcode
    :rtype: Opcode
    """
    duplicate_item = {
        1: Opcode.DROP,
        2: Opcode.NIP
    }

    if position > 0:
        if position in duplicate_item:
            return duplicate_item[position]
        else:
            return Opcode.XDROP


def get_dup(position: int) -> Optional[Opcode]:
    """
    Gets the opcode to duplicate the item n back in the stack

    :param position: index of the variable
    :return: the respective opcode
    :rtype: Opcode
    """
    duplicate_item = {
        1: Opcode.DUP,
        2: Opcode.OVER
    }

    if position >= 0:
        if position in duplicate_item:
            return duplicate_item[position]
        else:
            return Opcode.PICK


def get_reverse(no_stack_items: int, rotate: bool = False) -> Optional[Opcode]:
    """
    Gets the opcode to reverse n items on the stack

    :param no_stack_items: index of the variable
    :param rotate: whether the stack should be reversed or rotated
    :return: the respective opcode
    :rtype: Opcode
    """
    if no_stack_items == 3 and rotate:
        return Opcode.ROT

    reverse_stack = {
        2: Opcode.SWAP,
        3: Opcode.REVERSE3,
        4: Opcode.REVERSE4
    }

    if no_stack_items >= 0:
        if no_stack_items in reverse_stack:
            return reverse_stack[no_stack_items]
        else:
            return Opcode.REVERSEN


def get_store(index: int, local: bool, is_arg: bool = False) -> Opcode:
    """
    Gets the opcode to store the variable

    :param index: index of the variable
    :param local: identifies if the variable is local or global
    :param is_arg: identifies if the variable is an argument of a function. False if local is False.
    :return: the respective opcode
    :rtype: Opcode
    """
    if not local:
        is_arg = False

    if 0 <= index <= 6:
        if is_arg:
            opcode_value: int = Integer.from_bytes(Opcode.STARG0) + index
        elif local:
            opcode_value: int = Integer.from_bytes(Opcode.STLOC0) + index
        else:
            opcode_value: int = Integer.from_bytes(Opcode.STSFLD0) + index
        return Opcode(Integer(opcode_value).to_byte_array())
    else:
        if is_arg:
            return Opcode.STARG
        elif local:
            return Opcode.STLOC
        else:
            return Opcode.STSFLD


def get_load(index: int, local: bool, is_arg: bool = False) -> Opcode:
    """
    Gets the opcode to load the variable

    :param index: index of the variable
    :param local: identifies if the variable is local or global
    :param is_arg: identifies if the variable is an argument of a function. False if local is False.
    :return: the respective opcode
    :rtype: Opcode
    """
    if not local:
        is_arg = False

    if 0 <= index <= 6:
        if is_arg:
            opcode_value: int = Integer.from_bytes(Opcode.LDARG0) + index
        elif local:
            opcode_value: int = Integer.from_bytes(Opcode.LDLOC0) + index
        else:
            opcode_value: int = Integer.from_bytes(Opcode.LDSFLD0) + index
        return Opcode(Integer(opcode_value).to_byte_array())
    else:
        if is_arg:
            return Opcode.LDARG
        elif local:
            return Opcode.LDLOC
        else:
            return Opcode.LDSFLD


def is_load_slot(opcode: Opcode) -> bool:
    return (Opcode.LDSFLD0 <= opcode <= Opcode.LDSFLD
            or Opcode.LDLOC0 <= opcode <= Opcode.LDLOC
            or Opcode.LDARG0 <= opcode <= Opcode.LDARG)


def get_store_from_load(load_opcode) -> Optional[Opcode]:
    """
    Gets the store slot opcode equivalent to the given load slot opcode.

    :param load_opcode: load opcode
    :type load_opcode: Opcode
    :return: equivalent store opcode if the given opcode is a load slot. Otherwise, returns None
    :rtype: Opcode or None
    """
    if is_load_slot(load_opcode):
        opcode_value: int = Integer.from_bytes(load_opcode) + 8
        return Opcode(Integer(opcode_value).to_byte_array())
