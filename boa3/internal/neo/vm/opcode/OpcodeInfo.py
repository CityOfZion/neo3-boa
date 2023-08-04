from typing import Optional

from boa3.internal import constants
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.opcode.OpcodeInformation import OpcodeInformation


class OpcodeInfo:
    @classmethod
    def get_info(cls, opcode: Opcode) -> Optional[OpcodeInformation]:
        """
        Gets a binary operation given the operator.

        :param opcode: Neo VM opcode
        :return: The opcode info if it exists. None otherwise
        :rtype: OpcodeInformation or None
        """
        for id, op in vars(cls).items():
            if isinstance(op, OpcodeInformation) and op.opcode is opcode:
                return op

    # region Constants

    PUSHINT8 = OpcodeInformation(Opcode.PUSHINT8, 1)
    PUSHINT16 = OpcodeInformation(Opcode.PUSHINT16, 2)
    PUSHINT32 = OpcodeInformation(Opcode.PUSHINT32, 4)
    PUSHINT64 = OpcodeInformation(Opcode.PUSHINT64, 8)
    PUSHINT128 = OpcodeInformation(Opcode.PUSHINT128, 16)
    PUSHINT256 = OpcodeInformation(Opcode.PUSHINT256, 32)

    # Pushes the boolean value True onto the stack.
    PUSHT = OpcodeInformation(Opcode.PUSHT)
    # Pushes the boolean value False onto the stack.
    PUSHF = OpcodeInformation(Opcode.PUSHF)
    # Convert the next four bytes to an address, and push the address onto the stack.
    PUSHA = OpcodeInformation(Opcode.PUSHA, 4)
    # The item null is pushed onto the stack.
    PUSHNULL = OpcodeInformation(Opcode.PUSHNULL)
    # The next byte contains the number of bytes to be pushed onto the stack.
    PUSHDATA1 = OpcodeInformation(Opcode.PUSHDATA1, 1, constants.ONE_BYTE_MAX_VALUE)
    # The next two bytes contain the number of bytes to be pushed onto the stack.
    PUSHDATA2 = OpcodeInformation(Opcode.PUSHDATA2, 2, constants.TWO_BYTES_MAX_VALUE)
    # The next four bytes contain the number of bytes to be pushed onto the stack.
    PUSHDATA4 = OpcodeInformation(Opcode.PUSHDATA4, 4, constants.FOUR_BYTES_MAX_VALUE)

    # The number -1 is pushed onto the stack.
    PUSHM1 = OpcodeInformation(Opcode.PUSHM1)
    # The number 0 is pushed onto the stack.
    PUSH0 = OpcodeInformation(Opcode.PUSH0)
    # The number 1 is pushed onto the stack.
    PUSH1 = OpcodeInformation(Opcode.PUSH1)
    # The number 2 is pushed onto the stack.
    PUSH2 = OpcodeInformation(Opcode.PUSH2)
    # The number 3 is pushed onto the stack.
    PUSH3 = OpcodeInformation(Opcode.PUSH3)
    # The number 4 is pushed onto the stack.
    PUSH4 = OpcodeInformation(Opcode.PUSH4)
    # The number 5 is pushed onto the stack.
    PUSH5 = OpcodeInformation(Opcode.PUSH5)
    # The number 6 is pushed onto the stack.
    PUSH6 = OpcodeInformation(Opcode.PUSH6)
    # The number 7 is pushed onto the stack.
    PUSH7 = OpcodeInformation(Opcode.PUSH7)
    # The number 8 is pushed onto the stack.
    PUSH8 = OpcodeInformation(Opcode.PUSH8)
    # The number 9 is pushed onto the stack.
    PUSH9 = OpcodeInformation(Opcode.PUSH9)
    # The number 10 is pushed onto the stack.
    PUSH10 = OpcodeInformation(Opcode.PUSH10)
    # The number 11 is pushed onto the stack.
    PUSH11 = OpcodeInformation(Opcode.PUSH11)
    # The number 12 is pushed onto the stack.
    PUSH12 = OpcodeInformation(Opcode.PUSH12)
    # The number 13 is pushed onto the stack.
    PUSH13 = OpcodeInformation(Opcode.PUSH13)
    # The number 14 is pushed onto the stack.
    PUSH14 = OpcodeInformation(Opcode.PUSH14)
    # The number 15 is pushed onto the stack.
    PUSH15 = OpcodeInformation(Opcode.PUSH15)
    # The number 16 is pushed onto the stack.
    PUSH16 = OpcodeInformation(Opcode.PUSH16)

    # endregion

    # region Flow control

    # The NOP operation does nothing. It is intended to fill in space if opcodes are patched.
    NOP = OpcodeInformation(Opcode.NOP)
    # Unconditionally transfers control to a target instruction. The target instruction is represented as a 1-byte
    # signed offset from the beginning of the current instruction.
    JMP = OpcodeInformation(Opcode.JMP, 1)
    # Unconditionally transfers control to a target instruction. The target instruction is represented as a 4-bytes
    # signed offset from the beginning of the current instruction.
    JMP_L = OpcodeInformation(Opcode.JMP_L, 4)
    # Transfers control to a target instruction if the value is True, not null, or non-zero. The target instruction
    # is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPIF = OpcodeInformation(Opcode.JMPIF, 1, stack_items=1)
    # Transfers control to a target instruction if the value is True, not null, or non-zero. The target instruction
    # is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPIF_L = OpcodeInformation(Opcode.JMPIF_L, 4, stack_items=1)
    # Transfers control to a target instruction if the value is False, a null reference,
    # or zero. The target instruction is represented as a 1-byte signed offset from the beginning of the current
    # instruction.
    JMPIFNOT = OpcodeInformation(Opcode.JMPIFNOT, 1, stack_items=1)
    # Transfers control to a target instruction if the value is False, a null reference,
    # or zero. The target instruction is represented as a 4-bytes signed offset from the beginning of the current
    # instruction.
    JMPIFNOT_L = OpcodeInformation(Opcode.JMPIFNOT_L, 4, stack_items=1)
    # Transfers control to a target instruction if two values are equal. The target instruction is represented as a
    # 1-byte signed offset from the beginning of the current instruction.
    JMPEQ = OpcodeInformation(Opcode.JMPEQ, 1, stack_items=2)
    # Transfers control to a target instruction if two values are equal. The target instruction is represented as a
    # 4-bytes signed offset from the beginning of the current instruction.
    JMPEQ_L = OpcodeInformation(Opcode.JMPEQ_L, 4, stack_items=2)
    # Transfers control to a target instruction when two values are not equal. The target instruction is represented
    # as a 1-byte signed offset from the beginning of the current instruction.
    JMPNE = OpcodeInformation(Opcode.JMPNE, 1, stack_items=2)
    # Transfers control to a target instruction when two values are not equal. The target instruction is represented
    # as a 4-bytes signed offset from the beginning of the current instruction.
    JMPNE_L = OpcodeInformation(Opcode.JMPNE_L, 4, stack_items=2)
    # Transfers control to a target instruction if the first value is greater than the second value. The target
    # instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPGT = OpcodeInformation(Opcode.JMPGT, 1, stack_items=2)
    # Transfers control to a target instruction if the first value is greater than the second value. The target
    # instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPGT_L = OpcodeInformation(Opcode.JMPGT_L, 4, stack_items=2)
    # Transfers control to a target instruction if the first value is greater than or equal to the second value. The
    # target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPGE = OpcodeInformation(Opcode.JMPGE, 1, stack_items=2)
    # Transfers control to a target instruction if the first value is greater than or equal to the second value. The
    # target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPGE_L = OpcodeInformation(Opcode.JMPGE_L, 4, stack_items=2)
    # Transfers control to a target instruction if the first value is less than the second value. The target
    # instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPLT = OpcodeInformation(Opcode.JMPLT, 1, stack_items=2)
    # Transfers control to a target instruction if the first value is less than the second value. The target
    # instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPLT_L = OpcodeInformation(Opcode.JMPLT_L, 4, stack_items=2)
    # Transfers control to a target instruction if the first value is less than or equal to the second value. The
    # target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
    JMPLE = OpcodeInformation(Opcode.JMPLE, 1, stack_items=2)
    # Transfers control to a target instruction if the first value is less than or equal to the second value. The
    # target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
    JMPLE_L = OpcodeInformation(Opcode.JMPLE_L, 4, stack_items=2)
    # Calls the function at the target address which is represented as a 1-byte signed offset from the beginning of
    # the current instruction.
    CALL = OpcodeInformation(Opcode.CALL, 1)
    # Calls the function at the target address which is represented as a 4-bytes signed offset from the beginning of
    # the current instruction.
    CALL_L = OpcodeInformation(Opcode.CALL_L, 4)
    # Pop the address of a function from the stack, and call the function.
    CALLA = OpcodeInformation(Opcode.CALLA)
    # Calls the function which is described by the token.
    CALLT = OpcodeInformation(Opcode.CALLT, 2)
    # It turns the vm state to FAULT immediately, and cannot be caught.
    ABORT = OpcodeInformation(Opcode.ABORT)
    # Pop the top value of the stack, if it false, then exit vm execution and set vm state to FAULT.
    ASSERT = OpcodeInformation(Opcode.ASSERT)
    # Pop the top value of the stack, and throw it.
    THROW = OpcodeInformation(Opcode.THROW)
    # TRY CatchOffset(sbyte) FinallyOffset(sbyte). If there's no catch body, set CatchOffset 0. If there's no finally
    # body, set FinallyOffset 0.
    TRY = OpcodeInformation(Opcode.TRY, 2)
    # TRY_L CatchOffset(int) FinallyOffset(int). If there's no catch body, set CatchOffset 0. If there's no finally
    # body, set FinallyOffset 0.
    TRY_L = OpcodeInformation(Opcode.TRY_L, 8)
    # Ensures that the appropriate surrounding finally blocks are executed. And then unconditionally transfers
    # control to the specific target instruction, represented as a 1-byte signed offset from the beginning of the
    # current instruction.
    ENDTRY = OpcodeInformation(Opcode.ENDTRY, 1)
    # Ensures that the appropriate surrounding finally blocks are executed. And then unconditionally transfers
    # control to the specific target instruction, represented as a 4-byte signed offset from the beginning of the
    # current instruction.
    ENDTRY_L = OpcodeInformation(Opcode.ENDTRY_L, 4)
    # End finally, If no exception happen or be catched, vm will jump to the target instruction of ENDTRY/ENDTRY_L.
    # Otherwise vm will rethrow the exception to upper layer.
    ENDFINALLY = OpcodeInformation(Opcode.ENDFINALLY)
    # Returns from the current method.
    RET = OpcodeInformation(Opcode.RET)
    # Calls to an interop service.
    SYSCALL = OpcodeInformation(Opcode.SYSCALL, min_data_len=4)

    # endregion

    # region Stack

    # Puts the number of stack items onto the stack.
    DEPTH = OpcodeInformation(Opcode.DEPTH)
    # Removes the top stack item.
    DROP = OpcodeInformation(Opcode.DROP)
    # Removes the second-to-top stack item.
    NIP = OpcodeInformation(Opcode.NIP)
    # The item n back in the main stack is removed.
    XDROP = OpcodeInformation(Opcode.XDROP, stack_items=1)
    # Clear the stack
    CLEAR = OpcodeInformation(Opcode.CLEAR)
    # Duplicates the top stack item.
    DUP = OpcodeInformation(Opcode.DUP)
    # Copies the second-to-top stack item to the top.
    OVER = OpcodeInformation(Opcode.OVER)
    # The item n back in the stack is copied to the top.
    PICK = OpcodeInformation(Opcode.PICK, stack_items=1)
    # The item at the top of the stack is copied and inserted before the second-to-top item.
    TUCK = OpcodeInformation(Opcode.TUCK)
    # The top two items on the stack are swapped.
    SWAP = OpcodeInformation(Opcode.SWAP)
    # The top three items on the stack are rotated to the left.
    ROT = OpcodeInformation(Opcode.ROT)
    # The item n back in the stack is moved to the top.
    ROLL = OpcodeInformation(Opcode.ROLL)
    # Reverse the order of the top 3 items on the stack.
    REVERSE3 = OpcodeInformation(Opcode.REVERSE3)
    # Reverse the order of the top 4 items on the stack.
    REVERSE4 = OpcodeInformation(Opcode.REVERSE4)
    # Pop the number N on the stack, and reverse the order of the top N items on the stack.
    REVERSEN = OpcodeInformation(Opcode.REVERSEN, stack_items=1)

    # endregion

    # region Slot

    # Initialize the static field list for the current execution context.
    INITSSLOT = OpcodeInformation(Opcode.INITSSLOT, 1)
    # Initialize the argument slot and the local variable list for the current execution context.
    INITSLOT = OpcodeInformation(Opcode.INITSLOT, 2)
    # Loads the static field at index 0 onto the evaluation stack.
    LDSFLD0 = OpcodeInformation(Opcode.LDSFLD0)
    # Loads the static field at index 1 onto the evaluation stack.
    LDSFLD1 = OpcodeInformation(Opcode.LDSFLD1)
    # Loads the static field at index 2 onto the evaluation stack.
    LDSFLD2 = OpcodeInformation(Opcode.LDSFLD2)
    # Loads the static field at index 3 onto the evaluation stack.
    LDSFLD3 = OpcodeInformation(Opcode.LDSFLD3)
    # Loads the static field at index 4 onto the evaluation stack.
    LDSFLD4 = OpcodeInformation(Opcode.LDSFLD4)
    # Loads the static field at index 5 onto the evaluation stack.
    LDSFLD5 = OpcodeInformation(Opcode.LDSFLD5)
    # Loads the static field at index 6 onto the evaluation stack.
    LDSFLD6 = OpcodeInformation(Opcode.LDSFLD6)
    # Loads the static field at a specified index onto the evaluation stack. The index is represented as a 1-byte
    # unsigned integer.
    LDSFLD = OpcodeInformation(Opcode.LDSFLD, 1)
    # Stores the value on top of the evaluation stack in the static field list at index 0.
    STSFLD0 = OpcodeInformation(Opcode.STSFLD0)
    # Stores the value on top of the evaluation stack in the static field list at index 1.
    STSFLD1 = OpcodeInformation(Opcode.STSFLD1)
    # Stores the value on top of the evaluation stack in the static field list at index 2.
    STSFLD2 = OpcodeInformation(Opcode.STSFLD2)
    # Stores the value on top of the evaluation stack in the static field list at index 3.
    STSFLD3 = OpcodeInformation(Opcode.STSFLD3)
    # Stores the value on top of the evaluation stack in the static field list at index 4.
    STSFLD4 = OpcodeInformation(Opcode.STSFLD4)
    # Stores the value on top of the evaluation stack in the static field list at index 5.
    STSFLD5 = OpcodeInformation(Opcode.STSFLD5)
    # Stores the value on top of the evaluation stack in the static field list at index 6.
    STSFLD6 = OpcodeInformation(Opcode.STSFLD6)
    # Stores the value on top of the evaluation stack in the static field list at a specified index. The index is
    # represented as a 1-byte unsigned integer.
    STSFLD = OpcodeInformation(Opcode.STSFLD, 1)
    # Loads the local variable at index 0 onto the evaluation stack.
    LDLOC0 = OpcodeInformation(Opcode.LDLOC0)
    # Loads the local variable at index 1 onto the evaluation stack.
    LDLOC1 = OpcodeInformation(Opcode.LDLOC1)
    # Loads the local variable at index 2 onto the evaluation stack.
    LDLOC2 = OpcodeInformation(Opcode.LDLOC2)
    # Loads the local variable at index 3 onto the evaluation stack.
    LDLOC3 = OpcodeInformation(Opcode.LDLOC3)
    # Loads the local variable at index 4 onto the evaluation stack.
    LDLOC4 = OpcodeInformation(Opcode.LDLOC4)
    # Loads the local variable at index 5 onto the evaluation stack.
    LDLOC5 = OpcodeInformation(Opcode.LDLOC5)
    # Loads the local variable at index 6 onto the evaluation stack.
    LDLOC6 = OpcodeInformation(Opcode.LDLOC6)
    # Loads the local variable at a specified index onto the evaluation stack. The index is represented as a 1-byte
    # unsigned integer.
    LDLOC = OpcodeInformation(Opcode.LDLOC, 1)
    # Stores the value on top of the evaluation stack in the local variable list at index 0.
    STLOC0 = OpcodeInformation(Opcode.STLOC0)
    # Stores the value on top of the evaluation stack in the local variable list at index 1.
    STLOC1 = OpcodeInformation(Opcode.STLOC1)
    # Stores the value on top of the evaluation stack in the local variable list at index 2.
    STLOC2 = OpcodeInformation(Opcode.STLOC2)
    # Stores the value on top of the evaluation stack in the local variable list at index 3.
    STLOC3 = OpcodeInformation(Opcode.STLOC3)
    # Stores the value on top of the evaluation stack in the local variable list at index 4.
    STLOC4 = OpcodeInformation(Opcode.STLOC4)
    # Stores the value on top of the evaluation stack in the local variable list at index 5.
    STLOC5 = OpcodeInformation(Opcode.STLOC5)
    # Stores the value on top of the evaluation stack in the local variable list at index 6.
    STLOC6 = OpcodeInformation(Opcode.STLOC6)
    # Stores the value on top of the evaluation stack in the local variable list at a specified index. The index is
    # represented as a 1-byte unsigned integer.
    STLOC = OpcodeInformation(Opcode.STLOC, 1)
    # Loads the argument at index 0 onto the evaluation stack.
    LDARG0 = OpcodeInformation(Opcode.LDARG0)
    # Loads the argument at index 1 onto the evaluation stack.
    LDARG1 = OpcodeInformation(Opcode.LDARG1)
    # Loads the argument at index 2 onto the evaluation stack.
    LDARG2 = OpcodeInformation(Opcode.LDARG2)
    # Loads the argument at index 3 onto the evaluation stack.
    LDARG3 = OpcodeInformation(Opcode.LDARG3)
    # Loads the argument at index 4 onto the evaluation stack.
    LDARG4 = OpcodeInformation(Opcode.LDARG4)
    # Loads the argument at index 5 onto the evaluation stack.
    LDARG5 = OpcodeInformation(Opcode.LDARG5)
    # Loads the argument at index 6 onto the evaluation stack.
    LDARG6 = OpcodeInformation(Opcode.LDARG6)
    # Loads the argument at a specified index onto the evaluation stack. The index is represented as a 1-byte
    # unsigned integer.
    LDARG = OpcodeInformation(Opcode.LDARG, 1)
    # Stores the value on top of the evaluation stack in the argument slot at index 0.
    STARG0 = OpcodeInformation(Opcode.STARG0)
    # Stores the value on top of the evaluation stack in the argument slot at index 1.
    STARG1 = OpcodeInformation(Opcode.STARG1)
    # Stores the value on top of the evaluation stack in the argument slot at index 2.
    STARG2 = OpcodeInformation(Opcode.STARG2)
    # Stores the value on top of the evaluation stack in the argument slot at index 3.
    STARG3 = OpcodeInformation(Opcode.STARG3)
    # Stores the value on top of the evaluation stack in the argument slot at index 4.
    STARG4 = OpcodeInformation(Opcode.STARG4)
    # Stores the value on top of the evaluation stack in the argument slot at index 5.
    STARG5 = OpcodeInformation(Opcode.STARG5)
    # Stores the value on top of the evaluation stack in the argument slot at index 6.
    STARG6 = OpcodeInformation(Opcode.STARG6)
    # Stores the value on top of the evaluation stack in the argument slot at a specified index. The index is
    # represented as a 1-byte unsigned integer.
    STARG = OpcodeInformation(Opcode.STARG, 1)

    # endregion

    # region Splice

    NEWBUFFER = OpcodeInformation(Opcode.NEWBUFFER)
    MEMCPY = OpcodeInformation(Opcode.MEMCPY)
    # Concatenates two strings.
    CAT = OpcodeInformation(Opcode.CAT)
    # Returns a section of a string.
    SUBSTR = OpcodeInformation(Opcode.SUBSTR)
    # Keeps only characters left of the specified point in a string.
    LEFT = OpcodeInformation(Opcode.LEFT, stack_items=2)
    # Keeps only characters right of the specified point in a string.
    RIGHT = OpcodeInformation(Opcode.RIGHT, stack_items=2)

    # endregion

    # region Bitwise logic

    # Flips all of the bits in the input.
    INVERT = OpcodeInformation(Opcode.INVERT)
    # Boolean and between each bit in the inputs.
    AND = OpcodeInformation(Opcode.AND)
    # Boolean or between each bit in the inputs.
    OR = OpcodeInformation(Opcode.OR)
    # Boolean exclusive or between each bit in the inputs.
    XOR = OpcodeInformation(Opcode.XOR)
    # Returns 1 if the inputs are exactly equal, 0 otherwise.
    EQUAL = OpcodeInformation(Opcode.EQUAL)
    # Returns 1 if the inputs are not equal, 0 otherwise.
    NOTEQUAL = OpcodeInformation(Opcode.NOTEQUAL)

    # endregion

    # region Arithmetic

    # Puts the sign of top stack item on top of the main stack. If value is negative, put -1; if positive,
    # put 1; if value is zero, put 0.
    SIGN = OpcodeInformation(Opcode.SIGN)
    # The input is made positive.
    ABS = OpcodeInformation(Opcode.ABS)
    # The sign of the input is flipped.
    NEGATE = OpcodeInformation(Opcode.NEGATE)
    # 1 is added to the input.
    INC = OpcodeInformation(Opcode.INC)
    # 1 is subtracted from the input.
    DEC = OpcodeInformation(Opcode.DEC)
    # a is added to b.
    ADD = OpcodeInformation(Opcode.ADD)
    # b is subtracted from a.
    SUB = OpcodeInformation(Opcode.SUB)
    # a is multiplied by b.
    MUL = OpcodeInformation(Opcode.MUL)
    # a is divided by b.
    DIV = OpcodeInformation(Opcode.DIV)
    # Returns the remainder after dividing a by b.
    MOD = OpcodeInformation(Opcode.MOD)
    # The result of raising value to the exponent power.
    POW = OpcodeInformation(Opcode.POW)
    # Returns the square root of a specified number.
    SQRT = OpcodeInformation(Opcode.SQRT)
    # Performs modulus division on a number multiplied by another number.
    MODMUL = OpcodeInformation(Opcode.MODMUL)
    # Performs modulus division on a number raised to the power of another number.
    # If the exponent is -1, it will have the calculation of the modular inverse.
    MODPOW = OpcodeInformation(Opcode.MODPOW)
    # Shifts a left b bits, preserving sign.
    SHL = OpcodeInformation(Opcode.SHL)
    # Shifts a right b bits, preserving sign.
    SHR = OpcodeInformation(Opcode.SHR)
    # If the input is 0 or 1, it is flipped. Otherwise the output will be 0.
    NOT = OpcodeInformation(Opcode.NOT)
    # If both a and b are not 0, the output is 1. Otherwise 0.
    BOOLAND = OpcodeInformation(Opcode.BOOLAND)
    # If a or b is not 0, the output is 1. Otherwise 0.
    BOOLOR = OpcodeInformation(Opcode.BOOLOR)
    # Returns 0 if the input is 0. 1 otherwise.
    NZ = OpcodeInformation(Opcode.NZ)
    # Returns 1 if the numbers are equal, 0 otherwise.
    NUMEQUAL = OpcodeInformation(Opcode.NUMEQUAL)
    # Returns 1 if the numbers are not equal, 0 otherwise.
    NUMNOTEQUAL = OpcodeInformation(Opcode.NUMNOTEQUAL)
    # Returns 1 if a is less than b, 0 otherwise.
    LT = OpcodeInformation(Opcode.LT)
    # Returns 1 if a is less than or equal to b, 0 otherwise.
    LE = OpcodeInformation(Opcode.LE)
    # Returns 1 if a is greater than b, 0 otherwise.
    GT = OpcodeInformation(Opcode.GT)
    # Returns 1 if a is greater than or equal to b, 0 otherwise.
    GE = OpcodeInformation(Opcode.GE)
    # Returns the smaller of a and b.
    MIN = OpcodeInformation(Opcode.MIN, stack_items=2)
    # Returns the larger of a and b.
    MAX = OpcodeInformation(Opcode.MAX)
    # Returns 1 if x is within the specified range (left-inclusive), 0 otherwise.
    WITHIN = OpcodeInformation(Opcode.WITHIN)

    # endregion

    # region Compound-type

    # A value n is taken from top of main stack. The next n*2 items on main stack are removed, put inside n-sized map
    # and this map is put on top of the main stack.
    PACKMAP = OpcodeInformation(Opcode.PACKMAP)
    # A value n is taken from top of main stack. The next n items on main stack are removed, put inside n-sized
    # struct and this struct is put on top of the main stack.
    PACKSTRUCT = OpcodeInformation(Opcode.PACKSTRUCT)
    # A value n is taken from top of main stack. The next n items on main stack are removed, put inside n-sized array
    # and this array is put on top of the main stack.
    PACK = OpcodeInformation(Opcode.PACK)
    # A collection is removed from top of the main stack. Its elements are put on top of the main stack (in reverse
    # order) and the collection size is also put on main stack.
    UNPACK = OpcodeInformation(Opcode.UNPACK)
    # An empty array (with size 0) is put on top of the main stack.
    NEWARRAY0 = OpcodeInformation(Opcode.NEWARRAY0)
    # A value n is taken from top of main stack. A null-filled array with size n is put on top of the main stack.
    NEWARRAY = OpcodeInformation(Opcode.NEWARRAY)
    # A value n is taken from top of main stack. An array of type T with size n is put on top of the main stack.
    NEWARRAY_T = OpcodeInformation(Opcode.NEWARRAY_T, 1)
    # An empty struct (with size 0) is put on top of the main stack.
    NEWSTRUCT0 = OpcodeInformation(Opcode.NEWSTRUCT0)
    # A value n is taken from top of main stack. A zero-filled struct with size n is put on top of the main stack.
    NEWSTRUCT = OpcodeInformation(Opcode.NEWSTRUCT)
    # A Map is created and put on top of the main stack.
    NEWMAP = OpcodeInformation(Opcode.NEWMAP)
    # An array is removed from top of the main stack. Its size is put on top of the main stack.
    SIZE = OpcodeInformation(Opcode.SIZE)
    # An input index n (or key) and an array (or map) are removed from the top of the main stack. Puts True on top of
    # main stack if array[n] (or map[n]) exist, and False otherwise.
    HASKEY = OpcodeInformation(Opcode.HASKEY, stack_items=2)
    # A map is taken from top of the main stack. The keys of this map are put on top of the main stack.
    KEYS = OpcodeInformation(Opcode.KEYS)
    # A map is taken from top of the main stack. The values of this map are put on top of the main stack.
    VALUES = OpcodeInformation(Opcode.VALUES)
    # An input index n (or key) and an array (or map) are taken from main stack. Element array[n] (or map[n]) is put
    # on top of the main stack.
    PICKITEM = OpcodeInformation(Opcode.PICKITEM)
    # The item on top of main stack is removed and appended to the second item on top of the main stack.
    APPEND = OpcodeInformation(Opcode.APPEND)
    # A value v, index n (or key) and an array (or map) are taken from main stack. Attribution array[n]=v
    # (or map[n]=v) is performed.
    SETITEM = OpcodeInformation(Opcode.SETITEM)
    # An array is removed from the top of the main stack and its elements are reversed.
    REVERSEITEMS = OpcodeInformation(Opcode.REVERSEITEMS)
    # An input index n (or key) and an array (or map) are removed from the top of the main stack. Element array[n]
    # (or map[n]) is removed.
    REMOVE = OpcodeInformation(Opcode.REMOVE)
    # Remove all the items from the compound-type.
    CLEARITEMS = OpcodeInformation(Opcode.CLEARITEMS, stack_items=1)
    # Remove the last element from an array, and push it onto the stack.
    POPITEM = OpcodeInformation(Opcode.POPITEM, stack_items=1)

    # endregion

    # region Types

    # Returns true if the input is null. Returns false otherwise.
    ISNULL = OpcodeInformation(Opcode.ISNULL)
    # Returns true if the top item is of the specified type.
    ISTYPE = OpcodeInformation(Opcode.ISTYPE, 1)
    # Converts the top item to the specified type.
    CONVERT = OpcodeInformation(Opcode.CONVERT, 1)

    # endregion

    # region Extensions

    # Turns the vm state to FAULT immediately, and cannot be caught. Includes a reason.
    ABORTMSG = OpcodeInformation(Opcode.ABORTMSG)

    # Pop the top value of the stack, if it false, then exit vm execution and set vm state to FAULT. Includes a reason.
    ASSERTMSG = OpcodeInformation(Opcode.ASSERTMSG)

    # endregion
