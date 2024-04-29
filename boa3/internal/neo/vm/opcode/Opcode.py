from enum import Enum


class Opcode(bytes, Enum):
    """
    Opcodes are similar to instructions in assembly language.
    """

    # region Constants

    PUSHINT8 = b'\x00'
    """
    Pushes a 1-byte signed integer onto the stack.

    :meta hide-value:
    """
    PUSHINT16 = b'\x01'
    """
    Pushes a 2-byte signed integer onto the stack.

    :meta hide-value:
    """
    PUSHINT32 = b'\x02'
    """
    Pushes a 4-byte signed integer onto the stack.

    :meta hide-value:
    """
    PUSHINT64 = b'\x03'
    """
    Pushes a 8-byte signed integer onto the stack.

    :meta hide-value:
    """
    PUSHINT128 = b'\x04'
    """
    Pushes a 16-byte signed integer onto the stack.

    :meta hide-value:
    """
    PUSHINT256 = b'\x05'
    """
    Pushes a 32-byte signed integer onto the stack.

    :meta hide-value:
    """

    PUSHT = b'\x08'
    """
    Pushes the boolean value True onto the stack.

    :meta hide-value:
    """
    PUSHF = b'\x09'
    """
    Pushes the boolean value False onto the stack.

    :meta hide-value:
    """
    PUSHA = b'\x0A'
    """
    Converts the 4-bytes offset to a Pointer, and pushes it onto the stack.

    :meta hide-value:
    """
    PUSHNULL = b'\x0B'
    """
    The item null is pushed onto the stack.

    :meta hide-value:
    """
    PUSHDATA1 = b'\x0C'
    """
    The next byte contains the number of bytes to be pushed onto the stack.

    :meta hide-value:
    """
    PUSHDATA2 = b'\x0D'
    """
    The next two bytes contain the number of bytes to be pushed onto the stack.

    :meta hide-value:
    """
    PUSHDATA4 = b'\x0E'
    """
    The next four bytes contain the number of bytes to be pushed onto the stack.

    :meta hide-value:
    """

    PUSHM1 = b'\x0F'
    """
    The number -1 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH0 = b'\x10'
    """
    The number 0 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH1 = b'\x11'
    """
    The number 1 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH2 = b'\x12'
    """
    The number 2 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH3 = b'\x13'
    """
    The number 3 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH4 = b'\x14'
    """
    The number 4 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH5 = b'\x15'
    """
    The number 5 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH6 = b'\x16'
    """
    The number 6 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH7 = b'\x17'
    """
    The number 7 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH8 = b'\x18'
    """
    The number 8 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH9 = b'\x19'
    """
    The number 9 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH10 = b'\x1A'
    """
    The number 10 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH11 = b'\x1B'
    """
    The number 11 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH12 = b'\x1C'
    """
    The number 12 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH13 = b'\x1D'
    """
    The number 13 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH14 = b'\x1E'
    """
    The number 14 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH15 = b'\x1F'
    """
    The number 15 is pushed onto the stack.

    :meta hide-value:
    """
    PUSH16 = b'\x20'
    """
    The number 16 is pushed onto the stack.

    :meta hide-value:
    """

    # endregion

    # region Flow control

    NOP = b'\x21'
    """
    The NOP operation does nothing. It is intended to fill in space if opcodes are patched.

    :meta hide-value:
    """
    JMP = b'\x22'
    """
    Unconditionally transfers control to a target instruction. The target instruction is represented as a 1-byte
    signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMP_L = b'\x23'
    """
    Unconditionally transfers control to a target instruction. The target instruction is represented as a 4-bytes
    signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPIF = b'\x24'
    """
    Transfers control to a target instruction if the value is True, not null, or non-zero. The target instruction
    is represented as a 1-byte signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPIF_L = b'\x25'
    """
    Transfers control to a target instruction if the value is True, not null, or non-zero. The target instruction
    is represented as a 4-bytes signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPIFNOT = b'\x26'
    """
    Transfers control to a target instruction if the value is False, a null reference,
    or zero. The target instruction is represented as a 1-byte signed offset from the beginning of the current
    instruction.

    :meta hide-value:
    """
    JMPIFNOT_L = b'\x27'
    """
    Transfers control to a target instruction if the value is False, a null reference,
    or zero. The target instruction is represented as a 4-bytes signed offset from the beginning of the current
    instruction.

    :meta hide-value:
    """
    JMPEQ = b'\x28'
    """
    Transfers control to a target instruction if two values are equal. The target instruction is represented as a
    1-byte signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPEQ_L = b'\x29'
    """
    Transfers control to a target instruction if two values are equal. The target instruction is represented as a
    4-bytes signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPNE = b'\x2A'
    """
    Transfers control to a target instruction when two values are not equal. The target instruction is represented
    as a 1-byte signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPNE_L = b'\x2B'
    """
    Transfers control to a target instruction when two values are not equal. The target instruction is represented
    as a 4-bytes signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPGT = b'\x2C'
    """
    Transfers control to a target instruction if the first value is greater than the second value. The target
    instruction is represented as a 1-byte signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPGT_L = b'\x2D'
    """
    Transfers control to a target instruction if the first value is greater than the second value. The target
    instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPGE = b'\x2E'
    """
    Transfers control to a target instruction if the first value is greater than or equal to the second value. The
    target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPGE_L = b'\x2F'
    """
    Transfers control to a target instruction if the first value is greater than or equal to the second value. The
    target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPLT = b'\x30'
    """
    Transfers control to a target instruction if the first value is less than the second value. The target
    instruction is represented as a 1-byte signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPLT_L = b'\x31'
    """
    Transfers control to a target instruction if the first value is less than the second value. The target
    instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPLE = b'\x32'
    """
    Transfers control to a target instruction if the first value is less than or equal to the second value. The
    target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.

    :meta hide-value:
    """
    JMPLE_L = b'\x33'
    """
    Transfers control to a target instruction if the first value is less than or equal to the second value. The
    target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.

    :meta hide-value:
    """

    CALL = b'\x34'
    """
    Calls the function at the target address which is represented as a 1-byte signed offset from the beginning of
    the current instruction.

    :meta hide-value:
    """
    CALL_L = b'\x35'
    """
    Calls the function at the target address which is represented as a 4-bytes signed offset from the beginning of
    the current instruction.

    :meta hide-value:
    """
    CALLA = b'\x36'
    """
    Pop the address of a function from the stack, and call the function.

    :meta hide-value:
    """
    CALLT = b'\x37'
    """
    Calls the function which is described by the token.

    :meta hide-value:
    """
    ABORT = b'\x38'
    """
    It turns the vm state to FAULT immediately, and cannot be caught.

    :meta hide-value:
    """
    ASSERT = b'\x39'
    """
    Pop the top value of the stack, if it false, then exit vm execution and set vm state to FAULT.

    :meta hide-value:
    """
    THROW = b'\x3A'
    """
    Pop the top value of the stack, and throw it.

    :meta hide-value:
    """
    TRY = b'\x3B'
    """
    TRY CatchOffset(sbyte) FinallyOffset(sbyte). If there's no catch body, set CatchOffset 0. If there's no finally
    body, set FinallyOffset 0.

    :meta hide-value:
    """
    TRY_L = b'\x3C'
    """
    TRY_L CatchOffset(int) FinallyOffset(int). If there's no catch body, set CatchOffset 0. If there's no finally
    body, set FinallyOffset 0.

    :meta hide-value:
    """
    ENDTRY = b'\x3D'
    """
    Ensures that the appropriate surrounding finally blocks are executed. And then unconditionally transfers
    control to the specific target instruction, represented as a 1-byte signed offset from the beginning of the
    current instruction.

    :meta hide-value:
    """
    ENDTRY_L = b'\x3E'
    """
    Ensures that the appropriate surrounding finally blocks are executed. And then unconditionally transfers
    control to the specific target instruction, represented as a 4-byte signed offset from the beginning of the
    current instruction.

    :meta hide-value:
    """
    ENDFINALLY = b'\x3F'
    """
    End finally, If no exception happen or be catched, vm will jump to the target instruction of ENDTRY/ENDTRY_L.
    Otherwise vm will rethrow the exception to upper layer.

    :meta hide-value:
    """
    RET = b'\x40'
    """
    Returns from the current method.

    :meta hide-value:
    """
    SYSCALL = b'\x41'
    """
    Calls to an interop service.

    :meta hide-value:
    """

    # endregion

    # region Stack

    DEPTH = b'\x43'
    """
    Puts the number of stack items onto the stack.

    :meta hide-value:
    """
    DROP = b'\x45'
    """
    Removes the top stack item.

    :meta hide-value:
    """
    NIP = b'\x46'
    """
    Removes the second-to-top stack item.

    :meta hide-value:
    """
    XDROP = b'\x48'
    """
    The item n back in the main stack is removed.

    :meta hide-value:
    """
    CLEAR = b'\x49'
    """
    Clear the stack

    :meta hide-value:
    """

    DUP = b'\x4A'
    """
    Duplicates the top stack item.

    :meta hide-value:
    """
    OVER = b'\x4B'
    """
    Copies the second-to-top stack item to the top.

    :meta hide-value:
    """
    PICK = b'\x4D'
    """
    The item n back in the stack is copied to the top.

    :meta hide-value:
    """

    TUCK = b'\x4E'
    """
    The item at the top of the stack is copied and inserted before the second-to-top item.

    :meta hide-value:
    """
    SWAP = b'\x50'
    """
    The top two items on the stack are swapped.

    :meta hide-value:
    """
    ROT = b'\x51'
    """
    The top three items on the stack are rotated to the left.

    :meta hide-value:
    """
    ROLL = b'\x52'
    """
    The item n back in the stack is moved to the top.

    :meta hide-value:
    """
    REVERSE3 = b'\x53'
    """
    Reverse the order of the top 3 items on the stack.

    :meta hide-value:
    """
    REVERSE4 = b'\x54'
    """
    Reverse the order of the top 4 items on the stack.

    :meta hide-value:
    """
    REVERSEN = b'\x55'
    """
    Pop the number N on the stack, and reverse the order of the top N items on the stack.

    :meta hide-value:
    """

    # endregion

    # region Slot

    INITSSLOT = b'\x56'
    """
    Initialize the static field list for the current execution context.

    :meta hide-value:
    """
    INITSLOT = b'\x57'
    """
    Initialize the argument slot and the local variable list for the current execution context.

    :meta hide-value:
    """

    LDSFLD0 = b'\x58'
    """
    Loads the static field at index 0 onto the evaluation stack.

    :meta hide-value:
    """
    LDSFLD1 = b'\x59'
    """
    Loads the static field at index 1 onto the evaluation stack.

    :meta hide-value:
    """
    LDSFLD2 = b'\x5A'
    """
    Loads the static field at index 2 onto the evaluation stack.

    :meta hide-value:
    """
    LDSFLD3 = b'\x5B'
    """
    Loads the static field at index 3 onto the evaluation stack.

    :meta hide-value:
    """
    LDSFLD4 = b'\x5C'
    """
    Loads the static field at index 4 onto the evaluation stack.

    :meta hide-value:
    """
    LDSFLD5 = b'\x5D'
    """
    Loads the static field at index 5 onto the evaluation stack.

    :meta hide-value:
    """
    LDSFLD6 = b'\x5E'
    """
    Loads the static field at index 6 onto the evaluation stack.

    :meta hide-value:
    """
    LDSFLD = b'\x5F'
    """
    Loads the static field at a specified index onto the evaluation stack. The index is represented as a 1-byte
    unsigned integer.

    :meta hide-value:
    """
    STSFLD0 = b'\x60'
    """
    Stores the value on top of the evaluation stack in the static field list at index 0.

    :meta hide-value:
    """
    STSFLD1 = b'\x61'
    """
    Stores the value on top of the evaluation stack in the static field list at index 1.

    :meta hide-value:
    """
    STSFLD2 = b'\x62'
    """
    Stores the value on top of the evaluation stack in the static field list at index 2.

    :meta hide-value:
    """
    STSFLD3 = b'\x63'
    """
    Stores the value on top of the evaluation stack in the static field list at index 3.

    :meta hide-value:
    """
    STSFLD4 = b'\x64'
    """
    Stores the value on top of the evaluation stack in the static field list at index 4.

    :meta hide-value:
    """
    STSFLD5 = b'\x65'
    """
    Stores the value on top of the evaluation stack in the static field list at index 5.

    :meta hide-value:
    """
    STSFLD6 = b'\x66'
    """
    Stores the value on top of the evaluation stack in the static field list at index 6.

    :meta hide-value:
    """
    STSFLD = b'\x67'
    """
    Stores the value on top of the evaluation stack in the static field list at a specified index. The index is
    represented as a 1-byte unsigned integer.

    :meta hide-value:
    """
    LDLOC0 = b'\x68'
    """
    Loads the local variable at index 0 onto the evaluation stack.

    :meta hide-value:
    """
    LDLOC1 = b'\x69'
    """
    Loads the local variable at index 1 onto the evaluation stack.

    :meta hide-value:
    """
    LDLOC2 = b'\x6A'
    """
    Loads the local variable at index 2 onto the evaluation stack.

    :meta hide-value:
    """
    LDLOC3 = b'\x6B'
    """
    Loads the local variable at index 3 onto the evaluation stack.

    :meta hide-value:
    """
    LDLOC4 = b'\x6C'
    """
    Loads the local variable at index 4 onto the evaluation stack.

    :meta hide-value:
    """
    LDLOC5 = b'\x6D'
    """
    Loads the local variable at index 5 onto the evaluation stack.

    :meta hide-value:
    """
    LDLOC6 = b'\x6E'
    """
    Loads the local variable at index 6 onto the evaluation stack.

    :meta hide-value:
    """
    LDLOC = b'\x6F'
    """
    Loads the local variable at a specified index onto the evaluation stack. The index is represented as a 1-byte
    unsigned integer.

    :meta hide-value:
    """
    STLOC0 = b'\x70'
    """
    Stores the value on top of the evaluation stack in the local variable list at index 0.

    :meta hide-value:
    """
    STLOC1 = b'\x71'
    """
    Stores the value on top of the evaluation stack in the local variable list at index 1.

    :meta hide-value:
    """
    STLOC2 = b'\x72'
    """
    Stores the value on top of the evaluation stack in the local variable list at index 2.

    :meta hide-value:
    """
    STLOC3 = b'\x73'
    """
    Stores the value on top of the evaluation stack in the local variable list at index 3.

    :meta hide-value:
    """
    STLOC4 = b'\x74'
    """
    Stores the value on top of the evaluation stack in the local variable list at index 4.

    :meta hide-value:
    """
    STLOC5 = b'\x75'
    """
    Stores the value on top of the evaluation stack in the local variable list at index 5.

    :meta hide-value:
    """
    STLOC6 = b'\x76'
    """
    Stores the value on top of the evaluation stack in the local variable list at index 6.

    :meta hide-value:
    """
    STLOC = b'\x77'
    """
    Stores the value on top of the evaluation stack in the local variable list at a specified index. The index is
    represented as a 1-byte unsigned integer.

    :meta hide-value:
    """
    LDARG0 = b'\x78'
    """
    Loads the argument at index 0 onto the evaluation stack.

    :meta hide-value:
    """
    LDARG1 = b'\x79'
    """
    Loads the argument at index 1 onto the evaluation stack.

    :meta hide-value:
    """
    LDARG2 = b'\x7A'
    """
    Loads the argument at index 2 onto the evaluation stack.

    :meta hide-value:
    """
    LDARG3 = b'\x7B'
    """
    Loads the argument at index 3 onto the evaluation stack.

    :meta hide-value:
    """
    LDARG4 = b'\x7C'
    """
    Loads the argument at index 4 onto the evaluation stack.

    :meta hide-value:
    """
    LDARG5 = b'\x7D'
    """
    Loads the argument at index 5 onto the evaluation stack.

    :meta hide-value:
    """
    LDARG6 = b'\x7E'
    """
    Loads the argument at index 6 onto the evaluation stack.

    :meta hide-value:
    """
    LDARG = b'\x7F'
    """
    Loads the argument at a specified index onto the evaluation stack. The index is represented as a 1-byte
    unsigned integer.

    :meta hide-value:
    """
    STARG0 = b'\x80'
    """
    Stores the value on top of the evaluation stack in the argument slot at index 0.

    :meta hide-value:
    """
    STARG1 = b'\x81'
    """
    Stores the value on top of the evaluation stack in the argument slot at index 1.

    :meta hide-value:
    """
    STARG2 = b'\x82'
    """
    Stores the value on top of the evaluation stack in the argument slot at index 2.

    :meta hide-value:
    """
    STARG3 = b'\x83'
    """
    Stores the value on top of the evaluation stack in the argument slot at index 3.

    :meta hide-value:
    """
    STARG4 = b'\x84'
    """
    Stores the value on top of the evaluation stack in the argument slot at index 4.

    :meta hide-value:
    """
    STARG5 = b'\x85'
    """
    Stores the value on top of the evaluation stack in the argument slot at index 5.

    :meta hide-value:
    """
    STARG6 = b'\x86'
    """
    Stores the value on top of the evaluation stack in the argument slot at index 6.

    :meta hide-value:
    """
    STARG = b'\x87'
    """
    Stores the value on top of the evaluation stack in the argument slot at a specified index. The index is
    represented as a 1-byte unsigned integer.

    :meta hide-value:
    """

    # endregion

    # region Splice

    NEWBUFFER = b'\x88'
    """
    Creates a new Buffer and pushes it onto the stack.

    :meta hide-value:
    """
    MEMCPY = b'\x89'
    """
    Copies a range of bytes from one Buffer to another.

    :meta hide-value:
    """
    CAT = b'\x8B'
    """
    Concatenates two strings.

    :meta hide-value:
    """
    SUBSTR = b'\x8C'
    """
    Returns a section of a string.

    :meta hide-value:
    """
    LEFT = b'\x8D'
    """
    Keeps only characters left of the specified point in a string.

    :meta hide-value:
    """
    RIGHT = b'\x8E'
    """
    Keeps only characters right of the specified point in a string.

    :meta hide-value:
    """

    # endregion

    # region Bitwise logic

    INVERT = b'\x90'
    """
    Flips all of the bits in the input.

    :meta hide-value:
    """
    AND = b'\x91'
    """
    Boolean and between each bit in the inputs.

    :meta hide-value:
    """
    OR = b'\x92'
    """
    Boolean or between each bit in the inputs.

    :meta hide-value:
    """
    XOR = b'\x93'
    """
    Boolean exclusive or between each bit in the inputs.

    :meta hide-value:
    """
    EQUAL = b'\x97'
    """
    Returns 1 if the inputs are exactly equal, 0 otherwise.

    :meta hide-value:
    """
    NOTEQUAL = b'\x98'
    """
    Returns 1 if the inputs are not equal, 0 otherwise.

    :meta hide-value:
    """

    # endregion

    # region Arithmetic

    SIGN = b'\x99'
    """
    Puts the sign of top stack item on top of the main stack. If value is negative, put -1; if positive,
    put 1; if value is zero, put 0.

    :meta hide-value:
    """
    ABS = b'\x9A'
    """
    The input is made positive.

    :meta hide-value:
    """
    NEGATE = b'\x9B'
    """
    The sign of the input is flipped.

    :meta hide-value:
    """
    INC = b'\x9C'
    """
    1 is added to the input.

    :meta hide-value:
    """
    DEC = b'\x9D'
    """
    1 is subtracted from the input.

    :meta hide-value:
    """
    ADD = b'\x9E'
    """
    a is added to b.

    :meta hide-value:
    """
    SUB = b'\x9F'
    """
    b is subtracted from a.

    :meta hide-value:
    """
    MUL = b'\xA0'
    """
    a is multiplied by b.

    :meta hide-value:
    """
    DIV = b'\xA1'
    """
    a is divided by b.

    :meta hide-value:
    """
    MOD = b'\xA2'
    """
    Returns the remainder after dividing a by b.

    :meta hide-value:
    """
    POW = b'\xA3'
    """
    The result of raising value to the exponent power.

    :meta hide-value:
    """
    SQRT = b'\xA4'
    """
    Returns the square root of a specified number.

    :meta hide-value:
    """
    MODMUL = b'\xA5'
    """
    Performs modulus division on a number multiplied by another number.

    :meta hide-value:
    """
    MODPOW = b'\xA6'
    """
    Performs modulus division on a number raised to the power of another number.
    If the exponent is -1, it will have the calculation of the modular inverse.

    :meta hide-value:
    """
    SHL = b'\xA8'
    """
    Shifts a left b bits, preserving sign.

    :meta hide-value:
    """
    SHR = b'\xA9'
    """
    Shifts a right b bits, preserving sign.

    :meta hide-value:
    """
    NOT = b'\xAA'
    """
    If the input is 0 or 1, it is flipped. Otherwise the output will be 0.

    :meta hide-value:
    """
    BOOLAND = b'\xAB'
    """
    If both a and b are not 0, the output is 1. Otherwise 0.

    :meta hide-value:
    """
    BOOLOR = b'\xAC'
    """
    If a or b is not 0, the output is 1. Otherwise 0.

    :meta hide-value:
    """
    NZ = b'\xB1'
    """
    Returns 0 if the input is 0. 1 otherwise.

    :meta hide-value:
    """
    NUMEQUAL = b'\xB3'
    """
    Returns 1 if the numbers are equal, 0 otherwise.

    :meta hide-value:
    """
    NUMNOTEQUAL = b'\xB4'
    """
    Returns 1 if the numbers are not equal, 0 otherwise.

    :meta hide-value:
    """
    LT = b'\xB5'
    """
    Returns 1 if a is less than b, 0 otherwise.

    :meta hide-value:
    """
    LE = b'\xB6'
    """
    Returns 1 if a is less than or equal to b, 0 otherwise.

    :meta hide-value:
    """
    GT = b'\xB7'
    """
    Returns 1 if a is greater than b, 0 otherwise.

    :meta hide-value:
    """
    GE = b'\xB8'
    """
    Returns 1 if a is greater than or equal to b, 0 otherwise.

    :meta hide-value:
    """
    MIN = b'\xB9'
    """
    Returns the smaller of a and b.

    :meta hide-value:
    """
    MAX = b'\xBA'
    """
    Returns the larger of a and b.

    :meta hide-value:
    """
    WITHIN = b'\xBB'
    """
    Returns 1 if x is within the specified range (left-inclusive), 0 otherwise.

    :meta hide-value:
    """

    # endregion

    # region Compound-type

    PACKMAP = b'\xBE'
    """
    A value n is taken from top of main stack. The next n*2 items on main stack are removed, put inside n-sized map
    and this map is put on top of the main stack.

    :meta hide-value:
    """
    PACKSTRUCT = b'\xBF'
    """
    A value n is taken from top of main stack. The next n items on main stack are removed, put inside n-sized
    struct and this struct is put on top of the main stack.

    :meta hide-value:
    """
    PACK = b'\xC0'
    """
    A value n is taken from top of main stack. The next n items on main stack are removed, put inside n-sized array
    and this array is put on top of the main stack.

    :meta hide-value:
    """
    UNPACK = b'\xC1'
    """
    A collection is removed from top of the main stack. Its elements are put on top of the main stack (in reverse order) and the collection size is also put on main stack.

    :meta hide-value:
    """
    NEWARRAY0 = b'\xC2'
    """
    An empty array (with size 0) is put on top of the main stack.

    :meta hide-value:
    """
    NEWARRAY = b'\xC3'
    """
    A value n is taken from top of main stack. A null-filled array with size n is put on top of the main stack.

    :meta hide-value:
    """
    NEWARRAY_T = b'\xC4'
    """
    A value n is taken from top of main stack. An array of type T with size n is put on top of the main stack.

    :meta hide-value:
    """
    NEWSTRUCT0 = b'\xC5'
    """
    An empty struct (with size 0) is put on top of the main stack.

    :meta hide-value:
    """
    NEWSTRUCT = b'\xC6'
    """
    A value n is taken from top of main stack. A zero-filled struct with size n is put on top of the main stack.

    :meta hide-value:
    """
    NEWMAP = b'\xC8'
    """
    A Map is created and put on top of the main stack.

    :meta hide-value:
    """
    SIZE = b'\xCA'
    """
    An array is removed from top of the main stack. Its size is put on top of the main stack.

    :meta hide-value:
    """
    HASKEY = b'\xCB'
    """
    An input index n (or key) and an array (or map) are removed from the top of the main stack. Puts True on top of
    main stack if array[n] (or map[n]) exist, and False otherwise.

    :meta hide-value:
    """
    KEYS = b'\xCC'
    """
    A map is taken from top of the main stack. The keys of this map are put on top of the main stack.

    :meta hide-value:
    """
    VALUES = b'\xCD'
    """
    A map is taken from top of the main stack. The values of this map are put on top of the main stack.

    :meta hide-value:
    """
    PICKITEM = b'\xCE'
    """
    An input index n (or key) and an array (or map) are taken from main stack. Element array[n] (or map[n]) is put
    on top of the main stack.

    :meta hide-value:
    """
    APPEND = b'\xCF'
    """
    The item on top of main stack is removed and appended to the second item on top of the main stack.

    :meta hide-value:
    """
    SETITEM = b'\xD0'
    """
    A value v, index n (or key) and an array (or map) are taken from main stack. Attribution array[n]=v
    (or map[n]=v) is performed.

    :meta hide-value:
    """
    REVERSEITEMS = b'\xD1'
    """
    An array is removed from the top of the main stack and its elements are reversed.

    :meta hide-value:
    """
    REMOVE = b'\xD2'
    """
    An input index n (or key) and an array (or map) are removed from the top of the main stack. Element array[n]
    (or map[n]) is removed.

    :meta hide-value:
    """
    CLEARITEMS = b'\xD3'
    """
    Remove all the items from the compound-type.

    :meta hide-value:
    """
    POPITEM = b'\xD4'
    """
    Remove the last element from an array, and push it onto the stack.

    :meta hide-value:
    """

    # endregion

    # region Types

    ISNULL = b'\xD8'
    """
    Returns true if the input is null;

    :meta hide-value:
    """
    ISTYPE = b'\xD9'
    """
    Returns true if the top item of the stack is of the specified type;

    :meta hide-value:
    """
    CONVERT = b'\xDB'
    """
    Returns true if the input is null;

    :meta hide-value:
    """

    # endregion

    # region Extensions

    ABORTMSG = b'\xE0'
    """
    Turns the vm state to FAULT immediately, and cannot be caught. Includes a reason.

    :meta hide-value:
    """

    ASSERTMSG = b'\xE1'
    """
    Pop the top value of the stack, if it false, then exit vm execution and set vm state to FAULT. Includes a reason.

    :meta hide-value:
    """

    # endregion

    def __repr__(self) -> str:
        return str(self)
