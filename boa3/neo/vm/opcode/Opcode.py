from __future__ import annotations

from enum import Enum
from typing import Dict, Optional, Tuple, Union

from boa3.constants import FOUR_BYTES_MAX_VALUE
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String


class Opcode(bytes, Enum):
    # region Constants

    # Pushes a 1-byte signed integer onto the stack.
    PUSHINT8 = b'\x00'
    # Pushes a 2-byte signed integer onto the stack.
    PUSHINT16 = b'\x01'
    # Pushes a 4-byte signed integer onto the stack.
    PUSHINT32 = b'\x02'
    # Pushes a 8-byte signed integer onto the stack.
    PUSHINT64 = b'\x03'
    # Pushes a 16-byte signed integer onto the stack.
    PUSHINT128 = b'\x04'
    # Pushes a 32-byte signed integer onto the stack.
    PUSHINT256 = b'\x05'

    # Converts the 4-bytes offset to a Pointer, and pushes it onto the stack.
    PUSHA = b'\x0A'
    # The item null is pushed onto the stack.
    PUSHNULL = b'\x0B'
    # The next byte contains the number of bytes to be pushed onto the stack.
    PUSHDATA1 = b'\x0C'
    # The next two bytes contain the number of bytes to be pushed onto the stack.
    PUSHDATA2 = b'\x0D'
    # The next four bytes contain the number of bytes to be pushed onto the stack.
    PUSHDATA4 = b'\x0E'

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_push_and_data(integer: int) -> Tuple[Opcode, bytes]:
        """
        Gets the push opcode and data to the respective integer

        :param integer: value that will be pushed
        :return: the respective opcode and its required data
        :rtype: Tuple[Opcode, bytes]
        """
        opcode = Opcode.get_literal_push(integer)
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

    # The number -1 is pushed onto the stack.
    PUSHM1 = b'\x0F'
    # The number 0 is pushed onto the stack.
    PUSH0 = b'\x10'
    # The number 1 is pushed onto the stack.
    PUSH1 = b'\x11'
    # The number 2 is pushed onto the stack.
    PUSH2 = b'\x12'
    # The number 3 is pushed onto the stack.
    PUSH3 = b'\x13'
    # The number 4 is pushed onto the stack.
    PUSH4 = b'\x14'
    # The number 5 is pushed onto the stack.
    PUSH5 = b'\x15'
    # The number 6 is pushed onto the stack.
    PUSH6 = b'\x16'
    # The number 7 is pushed onto the stack.
    PUSH7 = b'\x17'
    # The number 8 is pushed onto the stack.
    PUSH8 = b'\x18'
    # The number 9 is pushed onto the stack.
    PUSH9 = b'\x19'
    # The number 10 is pushed onto the stack.
    PUSH10 = b'\x1A'
    # The number 11 is pushed onto the stack.
    PUSH11 = b'\x1B'
    # The number 12 is pushed onto the stack.
    PUSH12 = b'\x1C'
    # The number 13 is pushed onto the stack.
    PUSH13 = b'\x1D'
    # The number 14 is pushed onto the stack.
    PUSH14 = b'\x1E'
    # The number 15 is pushed onto the stack.
    PUSH15 = b'\x1F'
    # The number 16 is pushed onto the stack.
    PUSH16 = b'\x20'

    # endregion

    # region Flow control

    def has_larger_opcode(self) -> bool:
        return self in self.__larger_opcode

    def get_larger_opcode(self):
        """
        Gets the large opcode to the standard opcode

        :return: the respective opcode
        :rtype: Opcode or None
        """
        opcode_map = self.__larger_opcode
        if self in opcode_map:
            return opcode_map[self]
        elif self in opcode_map.values():
            return self
        else:
            return None

    @property
    def __larger_opcode(self) -> Dict[Opcode, Opcode]:
        """
        A map of each opcode with its larger equivalent

        :return: a dictionary that maps each opcode to its larger equivalent.
        """
        opcodes = {
            self.JMP: self.JMP_L,
            self.JMPIF: self.JMPIF_L,
            self.JMPIFNOT: self.JMPIFNOT_L,
            self.JMPEQ: self.JMPEQ_L,
            self.JMPNE: self.JMPNE_L,
            self.JMPGT: self.JMPGT_L,
            self.JMPGE: self.JMPGE_L,
            self.JMPLT: self.JMPLT_L,
            self.JMPLE: self.JMPLE_L,
            self.CALL: self.CALL_L,
            self.TRY: self.TRY_L,
            self.ENDTRY: self.ENDTRY_L
        }
        return opcodes

    # The NOP operation does nothing. It is intended to fill in space if opcodes are patched.
    NOP = b'\x21'
    # Unconditionally transfers control to a target instruction. The target instruction is represented as a 1-byte
    # signed offset from the beginning of the current instruction.
    JMP = b'\x22'
    # Unconditionally transfers control to a target instruction. The target instruction is represented as a 4-bytes
    # signed offset from the beginning of the current instruction.
    JMP_L = b'\x23'
    # Transfers control to a target instruction if the value is True, not null, or non-zero. The target instruction
    # is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPIF = b'\x24'
    # Transfers control to a target instruction if the value is True, not null, or non-zero. The target instruction
    # is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPIF_L = b'\x25'
    # Transfers control to a target instruction if the value is False, a null reference,
    # or zero. The target instruction is represented as a 1-byte signed offset from the beginning of the current
    # instruction.
    JMPIFNOT = b'\x26'
    # Transfers control to a target instruction if the value is False, a null reference,
    # or zero. The target instruction is represented as a 4-bytes signed offset from the beginning of the current
    # instruction.
    JMPIFNOT_L = b'\x27'
    # Transfers control to a target instruction if two values are equal. The target instruction is represented as a
    # 1-byte signed offset from the beginning of the current instruction.
    JMPEQ = b'\x28'
    # Transfers control to a target instruction if two values are equal. The target instruction is represented as a
    # 4-bytes signed offset from the beginning of the current instruction.
    JMPEQ_L = b'\x29'
    # Transfers control to a target instruction when two values are not equal. The target instruction is represented
    # as a 1-byte signed offset from the beginning of the current instruction.
    JMPNE = b'\x2A'
    # Transfers control to a target instruction when two values are not equal. The target instruction is represented
    # as a 4-bytes signed offset from the beginning of the current instruction.
    JMPNE_L = b'\x2B'
    # Transfers control to a target instruction if the first value is greater than the second value. The target
    # instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPGT = b'\x2C'
    # Transfers control to a target instruction if the first value is greater than the second value. The target
    # instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPGT_L = b'\x2D'
    # Transfers control to a target instruction if the first value is greater than or equal to the second value. The
    # target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPGE = b'\x2E'
    # Transfers control to a target instruction if the first value is greater than or equal to the second value. The
    # target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPGE_L = b'\x2F'
    # Transfers control to a target instruction if the first value is less than the second value. The target
    # instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPLT = b'\x30'
    # Transfers control to a target instruction if the first value is less than the second value. The target
    # instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPLT_L = b'\x31'
    # Transfers control to a target instruction if the first value is less than or equal to the second value. The
    # target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPLE = b'\x32'
    # Transfers control to a target instruction if the first value is less than or equal to the second value. The
    # target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPLE_L = b'\x33'

    @property
    def is_jump(self) -> bool:
        return self.JMP <= self <= self.JMPLE_L

    @staticmethod
    def get_jump_and_data(opcode: Opcode, integer: int, jump_through: bool = False) -> Tuple[Opcode, bytes]:
        """
        Gets the jump opcode and data to the respective integer

        :param opcode: which jump will be used
        :param integer: number of bytes that'll be jumped
        :param jump_through: whether it should go over the instructions or not
        :return: the respective opcode and its required data
        :rtype: Tuple[Opcode, bytes]
        """
        if not opcode.is_jump:
            opcode = Opcode.JMP

        from boa3.neo.vm.opcode.OpcodeInfo import OpcodeInfo
        opcode_info = OpcodeInfo.get_info(opcode)
        arg_size = opcode_info.data_len
        jmp_arg = Integer(arg_size + integer + jump_through).to_byte_array(min_length=arg_size) if integer > 0 \
            else Integer(integer).to_byte_array(min_length=arg_size)

        if len(jmp_arg) > opcode_info.max_data_len and opcode.has_larger_opcode():
            opcode = opcode.get_larger_opcode()
            opcode_info = OpcodeInfo.get_info(opcode)
            arg_size = opcode_info.data_len
            jmp_arg = Integer(arg_size + integer + jump_through).to_byte_array(min_length=arg_size) if integer > 0 \
                else Integer(integer).to_byte_array(min_length=arg_size)
            jmp_opcode = opcode
        else:
            jmp_opcode = opcode

        jmp_arg = jmp_arg[-arg_size:]

        return jmp_opcode, jmp_arg

    # Calls the function at the target address which is represented as a 1-byte signed offset from the beginning of
    # the current instruction.
    CALL = b'\x34'
    # Calls the function at the target address which is represented as a 4-bytes signed offset from the beginning of
    # the current instruction.
    CALL_L = b'\x35'
    # Pop the address of a function from the stack, and call the function.
    CALLA = b'\x36'
    # Calls the function which is described by the token.
    CALLT = b'\x37'
    # It turns the vm state to FAULT immediately, and cannot be caught.
    ABORT = b'\x38'
    # Pop the top value of the stack, if it false, then exit vm execution and set vm state to FAULT.
    ASSERT = b'\x39'
    # Pop the top value of the stack, and throw it.
    THROW = b'\x3A'
    # TRY CatchOffset(sbyte) FinallyOffset(sbyte). If there's no catch body, set CatchOffset 0. If there's no finally
    # body, set FinallyOffset 0.
    TRY = b'\x3B'
    # TRY_L CatchOffset(int) FinallyOffset(int). If there's no catch body, set CatchOffset 0. If there's no finally
    # body, set FinallyOffset 0.
    TRY_L = b'\x3C'
    # Ensures that the appropriate surrounding finally blocks are executed. And then unconditionally transfers
    # control to the specific target instruction, represented as a 1-byte signed offset from the beginning of the
    # current instruction.
    ENDTRY = b'\x3D'
    # Ensures that the appropriate surrounding finally blocks are executed. And then unconditionally transfers
    # control to the specific target instruction, represented as a 4-byte signed offset from the beginning of the
    # current instruction.
    ENDTRY_L = b'\x3E'
    # End finally, If no exception happen or be catched, vm will jump to the target instruction of ENDTRY/ENDTRY_L.
    # Otherwise vm will rethrow the exception to upper layer.
    ENDFINALLY = b'\x3F'
    # Returns from the current method.
    RET = b'\x40'
    # Calls to an interop service.
    SYSCALL = b'\x41'

    def has_target(self) -> bool:
        return self.JMP <= self <= self.CALL_L or self.TRY <= self < self.ENDFINALLY

    # endregion

    # region Stack

    # Puts the number of stack items onto the stack.
    DEPTH = b'\x43'
    # Removes the top stack item.
    DROP = b'\x45'
    # Removes the second-to-top stack item.
    NIP = b'\x46'
    # The item n back in the main stack is removed.
    XDROP = b'\x48'
    # Clear the stack
    CLEAR = b'\x49'

    @staticmethod
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

    # Duplicates the top stack item.
    DUP = b'\x4A'
    # Copies the second-to-top stack item to the top.
    OVER = b'\x4B'
    # The item n back in the stack is copied to the top.
    PICK = b'\x4D'

    @staticmethod
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

    # The item at the top of the stack is copied and inserted before the second-to-top item.
    TUCK = b'\x4E'
    # The top two items on the stack are swapped.
    SWAP = b'\x50'
    # The top three items on the stack are rotated to the left.
    ROT = b'\x51'
    # The item n back in the stack is moved to the top.
    ROLL = b'\x52'
    # Reverse the order of the top 3 items on the stack.
    REVERSE3 = b'\x53'
    # Reverse the order of the top 4 items on the stack.
    REVERSE4 = b'\x54'
    # Pop the number N on the stack, and reverse the order of the top N items on the stack.
    REVERSEN = b'\x55'

    @staticmethod
    def get_reverse(no_stack_items: int) -> Optional[Opcode]:
        """
        Gets the opcode to reverse n items on the stack

        :param no_stack_items: index of the variable
        :return: the respective opcode
        :rtype: Opcode
        """
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

    # endregion

    # region Slot

    # Initialize the static field list for the current execution context.
    INITSSLOT = b'\x56'
    # Initialize the argument slot and the local variable list for the current execution context.
    INITSLOT = b'\x57'

    @staticmethod
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

    @staticmethod
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

    @property
    def is_load_slot(self) -> bool:
        return (self.LDSFLD0 <= self <= self.LDSFLD
                or self.LDLOC0 <= self <= self.LDLOC
                or self.LDARG0 <= self <= self.LDARG)

    @staticmethod
    def get_store_from_load(load_opcode) -> Optional[Opcode]:
        """
        Gets the store slot opcode equivalent to the given load slot opcode.

        :param load_opcode: load opcode
        :type load_opcode: Opcode
        :return: equivalent store opcode if the given opcode is a load slot. Otherwise, returns None
        :rtype: Opcode or None
        """
        if load_opcode.is_load_slot:
            opcode_value: int = Integer.from_bytes(load_opcode) + 8
            return Opcode(Integer(opcode_value).to_byte_array())

    # Loads the static field at index 0 onto the evaluation stack.
    LDSFLD0 = b'\x58'
    # Loads the static field at index 1 onto the evaluation stack.
    LDSFLD1 = b'\x59'
    # Loads the static field at index 2 onto the evaluation stack.
    LDSFLD2 = b'\x5A'
    # Loads the static field at index 3 onto the evaluation stack.
    LDSFLD3 = b'\x5B'
    # Loads the static field at index 4 onto the evaluation stack.
    LDSFLD4 = b'\x5C'
    # Loads the static field at index 5 onto the evaluation stack.
    LDSFLD5 = b'\x5D'
    # Loads the static field at index 6 onto the evaluation stack.
    LDSFLD6 = b'\x5E'
    # Loads the static field at a specified index onto the evaluation stack. The index is represented as a 1-byte
    # unsigned integer.
    LDSFLD = b'\x5F'
    # Stores the value on top of the evaluation stack in the static field list at index 0.
    STSFLD0 = b'\x60'
    # Stores the value on top of the evaluation stack in the static field list at index 1.
    STSFLD1 = b'\x61'
    # Stores the value on top of the evaluation stack in the static field list at index 2.
    STSFLD2 = b'\x62'
    # Stores the value on top of the evaluation stack in the static field list at index 3.
    STSFLD3 = b'\x63'
    # Stores the value on top of the evaluation stack in the static field list at index 4.
    STSFLD4 = b'\x64'
    # Stores the value on top of the evaluation stack in the static field list at index 5.
    STSFLD5 = b'\x65'
    # Stores the value on top of the evaluation stack in the static field list at index 6.
    STSFLD6 = b'\x66'
    # Stores the value on top of the evaluation stack in the static field list at a specified index. The index is
    # represented as a 1-byte unsigned integer.
    STSFLD = b'\x67'
    # Loads the local variable at index 0 onto the evaluation stack.
    LDLOC0 = b'\x68'
    # Loads the local variable at index 1 onto the evaluation stack.
    LDLOC1 = b'\x69'
    # Loads the local variable at index 2 onto the evaluation stack.
    LDLOC2 = b'\x6A'
    # Loads the local variable at index 3 onto the evaluation stack.
    LDLOC3 = b'\x6B'
    # Loads the local variable at index 4 onto the evaluation stack.
    LDLOC4 = b'\x6C'
    # Loads the local variable at index 5 onto the evaluation stack.
    LDLOC5 = b'\x6D'
    # Loads the local variable at index 6 onto the evaluation stack.
    LDLOC6 = b'\x6E'
    # Loads the local variable at a specified index onto the evaluation stack. The index is represented as a 1-byte
    # unsigned integer.
    LDLOC = b'\x6F'
    # Stores the value on top of the evaluation stack in the local variable list at index 0.
    STLOC0 = b'\x70'
    # Stores the value on top of the evaluation stack in the local variable list at index 1.
    STLOC1 = b'\x71'
    # Stores the value on top of the evaluation stack in the local variable list at index 2.
    STLOC2 = b'\x72'
    # Stores the value on top of the evaluation stack in the local variable list at index 3.
    STLOC3 = b'\x73'
    # Stores the value on top of the evaluation stack in the local variable list at index 4.
    STLOC4 = b'\x74'
    # Stores the value on top of the evaluation stack in the local variable list at index 5.
    STLOC5 = b'\x75'
    # Stores the value on top of the evaluation stack in the local variable list at index 6.
    STLOC6 = b'\x76'
    # Stores the value on top of the evaluation stack in the local variable list at a specified index. The index is
    # represented as a 1-byte unsigned integer.
    STLOC = b'\x77'
    # Loads the argument at index 0 onto the evaluation stack.
    LDARG0 = b'\x78'
    # Loads the argument at index 1 onto the evaluation stack.
    LDARG1 = b'\x79'
    # Loads the argument at index 2 onto the evaluation stack.
    LDARG2 = b'\x7A'
    # Loads the argument at index 3 onto the evaluation stack.
    LDARG3 = b'\x7B'
    # Loads the argument at index 4 onto the evaluation stack.
    LDARG4 = b'\x7C'
    # Loads the argument at index 5 onto the evaluation stack.
    LDARG5 = b'\x7D'
    # Loads the argument at index 6 onto the evaluation stack.
    LDARG6 = b'\x7E'
    # Loads the argument at a specified index onto the evaluation stack. The index is represented as a 1-byte
    # unsigned integer.
    LDARG = b'\x7F'
    # Stores the value on top of the evaluation stack in the argument slot at index 0.
    STARG0 = b'\x80'
    # Stores the value on top of the evaluation stack in the argument slot at index 1.
    STARG1 = b'\x81'
    # Stores the value on top of the evaluation stack in the argument slot at index 2.
    STARG2 = b'\x82'
    # Stores the value on top of the evaluation stack in the argument slot at index 3.
    STARG3 = b'\x83'
    # Stores the value on top of the evaluation stack in the argument slot at index 4.
    STARG4 = b'\x84'
    # Stores the value on top of the evaluation stack in the argument slot at index 5.
    STARG5 = b'\x85'
    # Stores the value on top of the evaluation stack in the argument slot at index 6.
    STARG6 = b'\x86'
    # Stores the value on top of the evaluation stack in the argument slot at a specified index. The index is
    # represented as a 1-byte unsigned integer.
    STARG = b'\x87'

    # endregion

    # region Splice

    # Creates a new Buffer and pushes it onto the stack.
    NEWBUFFER = b'\x88'
    # Copies a range of bytes from one Buffer to another.
    MEMCPY = b'\x89'
    # Concatenates two strings.
    CAT = b'\x8B'
    # Returns a section of a string.
    SUBSTR = b'\x8C'
    # Keeps only characters left of the specified point in a string.
    LEFT = b'\x8D'
    # Keeps only characters right of the specified point in a string.
    RIGHT = b'\x8E'

    # endregion

    # region Bitwise logic

    # Flips all of the bits in the input.
    INVERT = b'\x90'
    # Boolean and between each bit in the inputs.
    AND = b'\x91'
    # Boolean or between each bit in the inputs.
    OR = b'\x92'
    # Boolean exclusive or between each bit in the inputs.
    XOR = b'\x93'
    # Returns 1 if the inputs are exactly equal, 0 otherwise.
    EQUAL = b'\x97'
    # Returns 1 if the inputs are not equal, 0 otherwise.
    NOTEQUAL = b'\x98'

    # endregion

    # region Arithmetic

    # Puts the sign of top stack item on top of the main stack. If value is negative, put -1; if positive,
    # put 1; if value is zero, put 0.
    SIGN = b'\x99'
    # The input is made positive.
    ABS = b'\x9A'
    # The sign of the input is flipped.
    NEGATE = b'\x9B'
    # 1 is added to the input.
    INC = b'\x9C'
    # 1 is subtracted from the input.
    DEC = b'\x9D'
    # a is added to b.
    ADD = b'\x9E'
    # b is subtracted from a.
    SUB = b'\x9F'
    # a is multiplied by b.
    MUL = b'\xA0'
    # a is divided by b.
    DIV = b'\xA1'
    # Returns the remainder after dividing a by b.
    MOD = b'\xA2'
    # The result of raising value to the exponent power.
    POW = b'\xA3'
    # Returns the square root of a specified number.
    SQRT = b'\xA4'
    # Performs modulus division on a number multiplied by another number.
    MODMUL = b'\xA5'
    # Performs modulus division on a number raised to the power of another number.
    # If the exponent is -1, it will have the calculation of the modular inverse.
    MODPOW = b'\xA6'
    # Shifts a left b bits, preserving sign.
    SHL = b'\xA8'
    # Shifts a right b bits, preserving sign.
    SHR = b'\xA9'
    # If the input is 0 or 1, it is flipped. Otherwise the output will be 0.
    NOT = b'\xAA'
    # If both a and b are not 0, the output is 1. Otherwise 0.
    BOOLAND = b'\xAB'
    # If a or b is not 0, the output is 1. Otherwise 0.
    BOOLOR = b'\xAC'
    # Returns 0 if the input is 0. 1 otherwise.
    NZ = b'\xB1'
    # Returns 1 if the numbers are equal, 0 otherwise.
    NUMEQUAL = b'\xB3'
    # Returns 1 if the numbers are not equal, 0 otherwise.
    NUMNOTEQUAL = b'\xB4'
    # Returns 1 if a is less than b, 0 otherwise.
    LT = b'\xB5'
    # Returns 1 if a is less than or equal to b, 0 otherwise.
    LE = b'\xB6'
    # Returns 1 if a is greater than b, 0 otherwise.
    GT = b'\xB7'
    # Returns 1 if a is greater than or equal to b, 0 otherwise.
    GE = b'\xB8'
    # Returns the smaller of a and b.
    MIN = b'\xB9'
    # Returns the larger of a and b.
    MAX = b'\xBA'
    # Returns 1 if x is within the specified range (left-inclusive), 0 otherwise.
    WITHIN = b'\xBB'

    # endregion

    # region Compound-type

    # A value n is taken from top of main stack. The next n*2 items on main stack are removed, put inside n-sized map
    # and this map is put on top of the main stack.
    PACKMAP = b'\xBE'
    # A value n is taken from top of main stack. The next n items on main stack are removed, put inside n-sized
    # struct and this struct is put on top of the main stack.
    PACKSTRUCT = b'\xBF'
    # A value n is taken from top of main stack. The next n items on main stack are removed, put inside n-sized array
    # and this array is put on top of the main stack.
    PACK = b'\xC0'
    # A collection is removed from top of the main stack. Its elements are put on top of the main stack (in reverse order) and the collection size is also put on main stack.
    UNPACK = b'\xC1'
    # An empty array (with size 0) is put on top of the main stack.
    NEWARRAY0 = b'\xC2'
    # A value n is taken from top of main stack. A null-filled array with size n is put on top of the main stack.
    NEWARRAY = b'\xC3'
    # A value n is taken from top of main stack. An array of type T with size n is put on top of the main stack.
    NEWARRAY_T = b'\xC4'
    # An empty struct (with size 0) is put on top of the main stack.
    NEWSTRUCT0 = b'\xC5'
    # A value n is taken from top of main stack. A zero-filled struct with size n is put on top of the main stack.
    NEWSTRUCT = b'\xC6'
    # A Map is created and put on top of the main stack.
    NEWMAP = b'\xC8'
    # An array is removed from top of the main stack. Its size is put on top of the main stack.
    SIZE = b'\xCA'
    # An input index n (or key) and an array (or map) are removed from the top of the main stack. Puts True on top of
    # main stack if array[n] (or map[n]) exist, and False otherwise.
    HASKEY = b'\xCB'
    # A map is taken from top of the main stack. The keys of this map are put on top of the main stack.
    KEYS = b'\xCC'
    # A map is taken from top of the main stack. The values of this map are put on top of the main stack.
    VALUES = b'\xCD'
    # An input index n (or key) and an array (or map) are taken from main stack. Element array[n] (or map[n]) is put
    # on top of the main stack.
    PICKITEM = b'\xCE'
    # The item on top of main stack is removed and appended to the second item on top of the main stack.
    APPEND = b'\xCF'
    # A value v, index n (or key) and an array (or map) are taken from main stack. Attribution array[n]=v
    # (or map[n]=v) is performed.
    SETITEM = b'\xD0'
    # An array is removed from the top of the main stack and its elements are reversed.
    REVERSEITEMS = b'\xD1'
    # An input index n (or key) and an array (or map) are removed from the top of the main stack. Element array[n]
    # (or map[n]) is removed.
    REMOVE = b'\xD2'
    # Remove all the items from the compound-type.
    CLEARITEMS = b'\xD3'
    # Remove the last element from an array, and push it onto the stack.
    POPITEM = b'\xD4'

    # endregion

    # region Types

    # Returns true if the input is null;
    ISNULL = b'\xD8'
    # Returns true if the top item of the stack is of the specified type;
    ISTYPE = b'\xD9'
    # Returns true if the input is null;
    CONVERT = b'\xDB'

    # endregion

    def __repr__(self) -> str:
        return str(self)
