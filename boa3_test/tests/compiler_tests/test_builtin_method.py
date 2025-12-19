import json

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


def minimal_signed_bytes(n: int) -> int:
    length = 1
    while True:
        try:
            return len(n.to_bytes(length, signed=True))
        except OverflowError:
            length += 1

class TestBuiltinMethod(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/built_in_methods_test'
    FORGOT_SIGNED_ARG_MSG = 'did you call to_bytes on a negative integer without setting signed=True?'
    LENGTH_ARG_TOO_SMALL_MSG = 'try raising the value of the length argument'

    # region len test

    def test_len_of_tuple_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3      # a = (1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = len(a)
            + Opcode.SIZE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )

        output, _ = self.assertCompile('LenTuple.py')
        self.assertEqual(expected_output, output)

    async def test_len_of_tuple_run(self):
        await self.set_up_contract('LenTuple.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(3, result)

    def test_len_of_list_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = len(a)
            + Opcode.SIZE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )

        output, _ = self.assertCompile('LenList.py')
        self.assertEqual(expected_output, output)

    async def test_len_of_list_run(self):
        await self.set_up_contract('LenList.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(3, result)

    def test_len_of_str_compile(self):
        input = 'just a test'
        byte_input = String(input).to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        output, _ = self.assertCompile('LenString.py')
        self.assertEqual(expected_output, output)

    async def test_len_of_str_run(self):
        await self.set_up_contract('LenString.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(11, result)

    async def test_len_of_bytes(self):
        await self.set_up_contract('LenBytes.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(3, result)

    def test_len_of_no_collection(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'LenMismatchedType.py')

    def test_len_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'LenTooManyParameters.py')

    def test_len_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'LenTooFewParameters.py')

    # endregion

    # region append test

    def test_append_tuple(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'AppendTuple.py')

    def test_append_sequence(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'AppendSequence.py')

    def test_append_mutable_sequence_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.append(4)
            + Opcode.PUSH4
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AppendMutableSequence.py')
        self.assertEqual(expected_output, output)

    async def test_append_mutable_sequence_run(self):
        await self.set_up_contract('AppendMutableSequence.py')

        result, _ = await self.call('append_example', [], return_type=list)
        self.assertEqual([1, 2, 3, 4], result)

    def test_append_mutable_sequence_with_builtin_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.append(4)
            + Opcode.PUSH4
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AppendMutableSequenceBuiltinCall.py')
        self.assertEqual(expected_output, output)

    async def test_append_mutable_sequence_with_builtin_run(self):
        await self.set_up_contract('AppendMutableSequenceBuiltinCall.py')

        result, _ = await self.call('append_example', [], return_type=list)
        self.assertEqual([1, 2, 3, 4], result)

    def test_append_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'AppendTooManyParameters.py')

    def test_append_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'AppendTooFewParameters.py')

    # endregion

    # region clear test

    def test_clear_tuple(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ClearTuple.py')

    def test_clear_mutable_sequence_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.clear()
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(9).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSHDATA1
            + Integer(0).to_byte_array(min_length=1)
            + Opcode.CONVERT
            + Type.bytearray.stack_item
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CLEARITEMS
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output, _ = self.assertCompile('ClearMutableSequence.py')
        self.assertEqual(expected_output, output)

    async def test_clear_mutable_sequence_run(self):
        await self.set_up_contract('ClearMutableSequence.py')

        result, _ = await self.call('clear_example', [], return_type=list)
        self.assertEqual([], result)

    def test_clear_mutable_sequence_with_builtin_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # MutableSequence.clear(a)
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(9).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSHDATA1
            + Integer(0).to_byte_array(min_length=1)
            + Opcode.CONVERT
            + Type.bytearray.stack_item
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CLEARITEMS
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output, _ = self.assertCompile('ClearMutableSequenceBuiltinCall.py')
        self.assertEqual(expected_output, output)

    async def test_clear_mutable_sequence_with_builtin_run(self):
        await self.set_up_contract('ClearMutableSequenceBuiltinCall.py')

        result, _ = await self.call('clear_example', [], return_type=list)
        self.assertEqual([], result)

    def test_clear_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ClearTooManyParameters.py')

    def test_clear_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ClearTooFewParameters.py')

    # endregion

    # region reverse test

    def test_reverse_tuple(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ReverseTuple.py')

    def test_reverse_mutable_sequence_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.reverse()
            + Opcode.REVERSEITEMS
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output, _ = self.assertCompile('ReverseMutableSequence.py')
        self.assertEqual(expected_output, output)

    async def test_reverse_mutable_sequence_run(self):
        await self.set_up_contract('ReverseMutableSequence.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([3, 2, 1], result)

    async def test_reverse_mutable_sequence_with_builtin(self):
        await self.set_up_contract('ReverseMutableSequenceBuiltinCall.py')

        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(b'\x03\x02\x01', result)

    def test_reverse_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ReverseTooManyParameters.py')

    def test_reverse_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ReverseTooFewParameters.py')

    # endregion

    # region extend test

    def test_extend_tuple(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ExtendTuple.py')

    def test_extend_sequence(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ExtendSequence.py')

    async def test_extend_mutable_sequence(self):
        await self.set_up_contract('ExtendMutableSequence.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    async def test_extend_mutable_sequence_with_builtin(self):
        await self.set_up_contract('ExtendMutableSequenceBuiltinCall.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_extend_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ExtendTooManyParameters.py')

    def test_extend_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ExtendTooFewParameters.py')

    # endregion

    # region to_script_hash test

    async def test_script_hash_int(self):
        await self.set_up_contract('ScriptHashInt.py')

        from boa3.internal.neo import to_script_hash
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(to_script_hash(Integer(123).to_byte_array()), result)

    def test_script_hash_int_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'ScriptHashIntBuiltinCall.py')

    async def test_script_hash_str(self):
        await self.set_up_contract('ScriptHashStr.py')

        from boa3.internal.neo import to_script_hash
        expected_result = to_script_hash(String('NUnLWXALK2G6gYa7RadPLRiQYunZHnncxg').to_bytes())
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = to_script_hash(String('123').to_bytes())
        result, _ = await self.call('Main2', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    def test_script_hash_str_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'ScriptHashStrBuiltinCall.py')

    async def test_script_hash_variable(self):
        await self.set_up_contract('ScriptHashVariable.py')

        from boa3.internal.neo import to_script_hash
        from base58 import b58encode
        value = b58encode(Integer(123).to_byte_array())
        if isinstance(value, int):
            value = Integer(value).to_byte_array()

        result, _ = await self.call('Main', [value], return_type=bytes)
        self.assertEqual(to_script_hash(value), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [123], return_type=bytes)

        self.assertRegex(str(context.exception), 'invalid base58 digit')

    def test_script_hash_variable_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'ScriptHashVariableBuiltinCall.py')

    def test_script_hash_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ScriptHashTooManyParameters.py')

    def test_script_hash_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ScriptHashTooFewParameters.py')

    def test_script_hash_mismatched_types(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ScriptHashMismatchedType.py')

    def test_script_hash_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'ScriptHashBuiltinWrongUsage.py')

    # endregion

    # region to_hex_str test

    async def test_to_hex_str(self):
        await self.set_up_contract('HexStr.py')

        from boa3.internal.neo import to_hex_str
        expected_result = to_hex_str(b'abcdefghijklmnopqrstuvwxyz0123456789'
                                     ).replace('0x', '', 1)
        expected_result = expected_result.replace('0x', '', 1)
        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual(expected_result, result)

        expected_result = to_hex_str(b'123'
                                     ).replace('0x', '', 1)
        result, _ = await self.call('Main2', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_hex_str_variable(self):
        await self.set_up_contract('HexStrVariable.py')

        value = b''
        result, _ = await self.call('Main', [value], return_type=str)
        self.assertEqual('', result)

        from boa3.internal.neo import to_hex_str
        from base58 import b58encode
        value = b58encode(Integer(123).to_byte_array())
        if isinstance(value, int):
            value = Integer(value).to_byte_array()

        hex_str = to_hex_str(value
                             ).replace('0x', '', 1)

        result, _ = await self.call('Main', [value], return_type=str)
        self.assertEqual(hex_str, result)

    def test_hex_str_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'HexStrTooManyParameters.py')

    def test_hex_str_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'HexStrTooFewParameters.py')

    def test_hex_str_mismatched_types(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'HexStrMismatchedType.py')

    # endregion

    # region to_bytes test

    async def test_int_to_bytes(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytes.py')
        await self.set_up_contract('IntToBytes.py')

        value = Integer(123).to_byte_array()
        result, _ = await self.call('int_to_bytes', [], return_type=bytes)
        self.assertEqual(value, result)

    async def test_int_zero_to_bytes(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntZeroToBytes.py')
        await self.set_up_contract('IntZeroToBytes.py')

        value = Integer(0).to_byte_array(min_length=1)
        result, _ = await self.call('int_to_bytes', [], return_type=bytes)
        self.assertEqual(value, result)

    async def test_int_to_bytes_default_args(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesDefaultArgs.py')
        await self.set_up_contract('IntToBytesDefaultArgs.py')

        for value in range(128):
            result, _ = await self.call('main', [value], return_type=bytes)
            self.assertEqual(value.to_bytes(byteorder='little', signed=True), result)

        for value in range(-128, 0, -1):
            result, _ = await self.call('main', [value], return_type=bytes)
            self.assertEqual(value.to_bytes(byteorder='little', signed=True), result)

        value = 128
        result, _ = await self.call('main', [value], return_type=bytes)
        self.assertEqual(value.to_bytes(2, byteorder='little', signed=True), result)
        value = 1234
        result, _ = await self.call('main', [value], return_type=bytes)
        self.assertEqual(value.to_bytes(2, byteorder='little', signed=True), result)
        value = -129
        result, _ = await self.call('main', [value], return_type=bytes)
        self.assertEqual(value.to_bytes(2, byteorder='little', signed=True), result)

    async def test_int_to_bytes_length_args(self):
        with self.assertRaises(AssertionError) as context:
            self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesLengthArgs.py')
        self.assertRegex(str(context.exception), 'MethodWarning not logged')

        await self.set_up_contract('IntToBytesLengthArgs.py')

        min_value_len2 = 2 ** (8 * 2) // 2 * -1
        max_value_len2 = 2 ** (8 * 2) // 2 - 1
        for value in range(min_value_len2, max_value_len2 + 1, 200):
            length = 2
            result, _ = await self.call('main', [value, length], return_type=bytes)
            self.assertEqual(value.to_bytes(length, byteorder='little', signed=True), result)

        value = max_value_len2
        length = 2
        result, _ = await self.call('main', [value, length], return_type=bytes)
        self.assertEqual(value.to_bytes(length, byteorder='little', signed=True), result)

        value = min_value_len2
        length = 2
        result, _ = await self.call('main', [value, length], return_type=bytes)
        self.assertEqual(value.to_bytes(length, byteorder='little', signed=True), result)

        value = 123
        length = 10
        result, _ = await self.call('main', [value, length], return_type=bytes)
        self.assertEqual(value.to_bytes(length, byteorder='little', signed=True), result)

        value = 1234
        length = 10
        result, _ = await self.call('main', [value, length], return_type=bytes)
        self.assertEqual(value.to_bytes(length, byteorder='little', signed=True), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [1234, 1], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [max_value_len2 + 1, 2], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [min_value_len2 - 1, 2], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)

    async def test_int_to_bytes_length_big_endian_args(self):
        with self.assertRaises(AssertionError) as context:
            self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesLengthBigEndianArgs.py')
        self.assertRegex(str(context.exception), 'MethodWarning not logged')

        await self.set_up_contract('IntToBytesLengthBigEndianArgs.py')

        for value in range(-100000, 100000, 200):
            length = 5
            big_endian = True
            result, _ = await self.call('main', [value, length, big_endian], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'big', signed=True), result)

            big_endian = False
            result, _ = await self.call('main', [value, length, big_endian], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'little', signed=True), result)

        value = 123
        length = 10
        big_endian = True
        result, _ = await self.call('main', [value, length, big_endian], return_type=bytes)
        self.assertEqual(value.to_bytes(length, 'big'), result)

        value = 123
        length = 10
        big_endian = False
        result, _ = await self.call('main', [value, length, big_endian], return_type=bytes)
        self.assertEqual(value.to_bytes(length, 'little'), result)

        value = 1234
        length = 10
        big_endian = True
        result, _ = await self.call('main', [value, length, big_endian], return_type=bytes)
        self.assertEqual(value.to_bytes(length, 'big'), result)

        value = 1234
        length = 10
        big_endian = False
        result, _ = await self.call('main', [value, length, big_endian], return_type=bytes)
        self.assertEqual(value.to_bytes(length, 'little'), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [1234, 1, False], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [1234, 1, True], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)

    async def test_int_to_bytes_length_big_endian_signed_args(self):
        with self.assertRaises(AssertionError) as context:
            self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesLengthBigEndianSignedArgs.py')
        self.assertRegex(str(context.exception), 'MethodWarning not logged')

        await self.set_up_contract('IntToBytesLengthBigEndianSignedArgs.py')

        for value in range(-30000, 30000, 200):
            length = 5
            big_endian = True
            signed = True
            result, _ = await self.call('main', [value, length, big_endian, signed], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'big', signed=signed), result)

            big_endian = False
            signed = True
            result, _ = await self.call('main', [value, length, big_endian, signed], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'little', signed=signed), result)

        min_value_len2_unsigned = 0
        max_value_len2_unsigned = 2 ** 16 - 1
        for value in range(min_value_len2_unsigned, max_value_len2_unsigned + 1, 200):
            length = 2
            big_endian = True
            signed = False
            result, _ = await self.call('main', [value, length, big_endian, signed], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'big', signed=signed), result)

            big_endian = False
            signed = False
            result, _ = await self.call('main', [value, length, big_endian, signed], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'little', signed=signed), result)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [min_value_len2_unsigned - 1, 2, True, False], return_type=bytes)
        self.assertRegex(str(context.exception), self.FORGOT_SIGNED_ARG_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [min_value_len2_unsigned - 1, 2, False, False], return_type=bytes)
        self.assertRegex(str(context.exception), self.FORGOT_SIGNED_ARG_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [max_value_len2_unsigned + 1, 2, True, False], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [max_value_len2_unsigned + 1, 2, False, False], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)

        min_value_len2_signed = 2 ** (8 * 2) // 2 * -1
        max_value_len2_signed = 2 ** (8 * 2) // 2 - 1
        for value in range(min_value_len2_signed, max_value_len2_signed + 1, 200):
            length = 2
            big_endian = True
            signed = True
            result, _ = await self.call('main', [value, length, big_endian, signed], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'big', signed=signed), result)

            big_endian = False
            signed = True
            result, _ = await self.call('main', [value, length, big_endian, signed], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'little', signed=signed), result)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [min_value_len2_signed - 1, 2, True, True], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [min_value_len2_signed - 1, 2, False, True], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [max_value_len2_signed + 1, 2, True, True], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [max_value_len2_signed + 1, 2, False, True], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)

        max_int_length1 = (1 << 7) - 1
        length = 5
        big_endian = True
        signed = True
        result, _ = await self.call('main', [max_int_length1, length, big_endian, signed], return_type=bytes)
        self.assertEqual(max_int_length1.to_bytes(length, 'big', signed=signed), result)
        big_endian = False
        signed = True
        result, _ = await self.call('main', [max_int_length1, length, big_endian, signed], return_type=bytes)
        self.assertEqual(max_int_length1.to_bytes(length, 'little', signed=signed), result)

        min_int_length1 = -(1 << 7)
        length = 5
        big_endian = True
        signed = True
        result, _ = await self.call('main', [min_int_length1, length, big_endian, signed], return_type=bytes)
        self.assertEqual(min_int_length1.to_bytes(length, 'big', signed=signed), result)
        big_endian = False
        signed = True
        result, _ = await self.call('main', [min_int_length1, length, big_endian, signed], return_type=bytes)
        self.assertEqual(min_int_length1.to_bytes(length, 'little', signed=signed), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [max_int_length1 + 1, 1, True, True], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [min_int_length1 - 1, 1, True, True], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [-1, 1, True, False], return_type=bytes)
        self.assertRegex(str(context.exception), self.FORGOT_SIGNED_ARG_MSG)

    def test_int_to_bytes_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'IntToBytesWithBuiltin.py')

    async def test_int_to_bytes_as_parameter(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesAsParameter.py')
        await self.set_up_contract('IntToBytesAsParameter.py')

        result, _ = await self.call('int_to_bytes', [111], return_type=None)
        # return is Void, checking to see if there is no error
        self.assertIsNone(result)

    async def test_int_to_bytes_constant_big_endian_true(self):
        with self.assertRaises(AssertionError) as context:
            self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesConstantBigEndianTrue.py')
        self.assertRegex(str(context.exception), 'MethodWarning not logged')

        await self.set_up_contract('IntToBytesConstantBigEndianTrue.py')

        for value in range(-40000, 40000, 100):
            length = minimal_signed_bytes(value)
            result, _ = await self.call('main', [value], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'big', signed=True), result)

    async def test_int_to_bytes_constant_signed_false(self):
        with self.assertRaises(AssertionError) as context:
            self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesConstantSignedFalse.py')
        self.assertRegex(str(context.exception), 'MethodWarning not logged')

        await self.set_up_contract('IntToBytesConstantSignedFalse.py')

        for value in range(0, 40000, 100):
            length = minimal_signed_bytes(value)
            result, _ = await self.call('main', [value], return_type=bytes)
            self.assertEqual(value.to_bytes(length, 'little', signed=False), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [-1], return_type=bytes)
        self.assertRegex(str(context.exception), self.FORGOT_SIGNED_ARG_MSG)

    async def test_int_to_bytes_constant_length(self):
        with self.assertRaises(AssertionError) as context:
            self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesConstantLength.py')
        self.assertRegex(str(context.exception), 'MethodWarning not logged')

        await self.set_up_contract('IntToBytesConstantLength.py')

        for value in range(-128, 128):
            result, _ = await self.call('len_1', [value], return_type=bytes)
            self.assertEqual(value.to_bytes(1, 'little', signed=True), result)

        for value in range(-32768, 32768, 100):
            result, _ = await self.call('len_2', [value], return_type=bytes)
            self.assertEqual(value.to_bytes(2, 'little', signed=True), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('len_1', [128], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('len_2', [32768], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)

    async def test_int_to_bytes_constant_length_class(self):
        with self.assertRaises(AssertionError) as context:
            self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesConstantLengthClass.py')
        self.assertRegex(str(context.exception), 'MethodWarning not logged')

        await self.set_up_contract('IntToBytesConstantLengthClass.py')

        for value in range(-128, 128):
            result, _ = await self.call('len_1', [value], return_type=bytes)
            self.assertEqual(value.to_bytes(1, 'little', signed=True), result)

        for value in range(-32768, 32768, 100):
            result, _ = await self.call('len_2', [value], return_type=bytes)
            self.assertEqual(value.to_bytes(2, 'little', signed=True), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('len_1', [128], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('len_2', [32768], return_type=bytes)
        self.assertRegex(str(context.exception), self.LENGTH_ARG_TOO_SMALL_MSG)

    async def test_int_to_bytes_kwargs(self):
        with self.assertRaises(AssertionError) as context:
            self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesKwargs.py')
        self.assertRegex(str(context.exception), 'MethodWarning not logged')

    async def test_int_to_bytes_as_args_inside_class_instance_method(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'IntToBytesAsArgInsideClassInstanceMethod.py')
        await self.set_up_contract('IntToBytesAsArgInsideClassInstanceMethod.py')

        value = Integer(30).to_byte_array()
        result, _ = await self.call('int_to_bytes', [], return_type=bytes)
        self.assertEqual(value, result)

        value = Integer(10).to_byte_array() + Integer(20).to_byte_array()
        result, _ = await self.call('int_to_bytes2', [], return_type=bytes)
        self.assertEqual(value, result)

    def test_str_to_bytes_compile(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1        # '123'.to_bytes()
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.RET
        )

        output, _ = self.assertCompile('StrToBytes.py')
        self.assertEqual(expected_output, output)

    async def test_str_to_bytes_run(self):
        await self.set_up_contract('StrToBytes.py')

        result, _ = await self.call('str_to_bytes', [], return_type=bytes)
        self.assertEqual(String('123').to_bytes(), result)

    def test_str_to_bytes_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'StrToBytesTooManyParameters.py')

    def test_str_to_bytes_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'StrToBytesWithBuiltin.py')

    def test_to_bytes_mismatched_types(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ToBytesMismatchedType.py')

    # endregion

    # region print test

    async def test_print_int(self):
        await self.set_up_contract('PrintInt.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        runtime_logs = self.get_runtime_logs(self.contract_hash)
        self.assertEqual(1, len(runtime_logs))
        self.assertEqual('42', runtime_logs[0].msg)

    async def test_print_str(self):
        await self.set_up_contract('PrintStr.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        runtime_logs = self.get_runtime_logs(self.contract_hash)
        self.assertEqual(1, len(runtime_logs))
        self.assertEqual('str', runtime_logs[0].msg)

    async def test_print_bytes(self):
        await self.set_up_contract('PrintBytes.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        runtime_logs = self.get_runtime_logs(self.contract_hash)
        self.assertEqual(1, len(runtime_logs))
        self.assertEqual(b'\x01\x02\x03'.decode('utf-8'), runtime_logs[0].msg)

    async def test_print_bool(self):
        await self.set_up_contract('PrintBool.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        runtime_logs = self.get_runtime_logs(self.contract_hash)
        self.assertEqual(1, len(runtime_logs))
        self.assertEqual('true', runtime_logs[0].msg)

    async def test_print_list(self):
        await self.set_up_contract('PrintList.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        expected_print = json.dumps([1, 2, 3, 4], separators=(',', ':'))

        runtime_logs = self.get_runtime_logs(self.contract_hash)
        self.assertEqual(1, len(runtime_logs))
        self.assertEqual(expected_print, runtime_logs[0].msg)

    async def test_print_user_class(self):
        await self.set_up_contract('PrintClass.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        expected_print = json.dumps({
            'val1': 1,
            'val2': 2
        }, separators=(',', ':'))

        runtime_logs = self.get_runtime_logs(self.contract_hash)
        self.assertEqual(1, len(runtime_logs))
        self.assertEqual(expected_print, runtime_logs[0].msg)

    async def test_print_many_values(self):
        await self.set_up_contract('PrintManyValues.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        runtime_logs = self.get_runtime_logs(self.contract_hash)
        self.assertEqual(4, len(runtime_logs))
        for index in range(4):
            self.assertEqual(str(index + 1), runtime_logs[index].msg)

    async def test_print_no_args(self):
        await self.set_up_contract('PrintNoArgs.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        runtime_logs = self.get_runtime_logs(self.contract_hash)
        self.assertEqual(0, len(runtime_logs))

    def test_print_missing_outer_function_return(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'PrintIntMissingFunctionReturn.py')

    # endregion

    # region isinstance test

    async def test_isinstance_int_literal(self):
        await self.set_up_contract('IsInstanceIntLiteral.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_int_variable(self):
        await self.set_up_contract('IsInstanceIntVariable.py')

        result, _ = await self.call('Main', [10], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [False], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', ['string'], return_type=bool)
        self.assertEqual(False, result)

    async def test_isinstance_bool_literal(self):
        await self.set_up_contract('IsInstanceBoolLiteral.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(False, result)

    async def test_isinstance_bool_variable(self):
        await self.set_up_contract('IsInstanceBoolVariable.py')

        result, _ = await self.call('Main', [10], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [False], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', ['string'], return_type=bool)
        self.assertEqual(False, result)

    async def test_isinstance_str_literal(self):
        await self.set_up_contract('IsInstanceStrLiteral.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_str_variable(self):
        await self.set_up_contract('IsInstanceStrVariable.py')

        result, _ = await self.call('Main', [10], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [False], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', ['string'], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_list_literal(self):
        await self.set_up_contract('IsInstanceListLiteral.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_tuple_literal(self):
        await self.set_up_contract('IsInstanceTupleLiteral.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_tuple_variable(self):
        await self.set_up_contract('IsInstanceTupleVariable.py')

        result, _ = await self.call('Main', [10], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [False], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', ['string'], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [[]], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_many_types(self):
        await self.set_up_contract('IsInstanceManyTypes.py')

        result, _ = await self.call('Main', [10], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [False], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', ['string'], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [{}], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_many_types_with_class(self):
        await self.set_up_contract('IsInstanceManyTypesWithClass.py')

        result, _ = await self.call('Main', [42], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [[]], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', ['some string'], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [bytes(20)], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [None], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [{1: 2, 2: 4}], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_uint160(self):
        await self.set_up_contract('IsInstanceUInt160.py')

        result, _ = await self.call('Main', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [bytes(20)], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [bytes(30)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [42], return_type=bool)
        self.assertEqual(False, result)

    async def test_isinstance_uint256(self):
        await self.set_up_contract('IsInstanceUInt256.py')

        result, _ = await self.call('main', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [bytes(20)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [bytes(30)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [bytes(32)], return_type=bool)
        self.assertEqual(True, result)

    # endregion

    # region exit test

    async def test_exit(self):
        await self.set_up_contract('Exit.py')

        result, _ = await self.call('main', [False], return_type=int)
        self.assertEqual(123, result)

        with self.assertRaises(boatestcase.AbortException):
            await self.call('main', [True], return_type=int)

    # endregion

    # region max test

    async def test_max_int(self):
        await self.set_up_contract('MaxInt.py')

        value1 = 10
        value2 = 999
        result, _ = await self.call('main', [value1, value2], return_type=int)
        self.assertEqual(max(value1, value2), result)

    async def test_max_int_more_arguments(self):
        await self.set_up_contract('MaxIntMoreArguments.py')

        numbers = 4, 1, 16, 8, 2
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(max(numbers), result)

    async def test_max_str(self):
        await self.set_up_contract('MaxStr.py')

        value1 = 'foo'
        value2 = 'bar'
        result, _ = await self.call('main', [value1, value2], return_type=str)
        self.assertEqual(max(value1, value2), result)

        result, _ = await self.call('main', [value2, value1], return_type=str)
        self.assertEqual(max(value2, value1), result)

        value1 = 'alg'
        value2 = 'al'
        result, _ = await self.call('main', [value1, value2], return_type=str)
        self.assertEqual(max(value1, value2), result)

        value = 'some string'
        result, _ = await self.call('main', [value, value], return_type=str)
        self.assertEqual(max(value, value), result)

    async def test_max_str_more_arguments(self):
        await self.set_up_contract('MaxStrMoreArguments.py')

        values = 'Lorem', 'ipsum', 'dolor', 'sit', 'amet'
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(max(values), result)

    async def test_max_bytes(self):
        await self.set_up_contract('MaxBytes.py')

        value1 = b'foo'
        value2 = b'bar'
        result, _ = await self.call('main', [value1, value2], return_type=bytes)
        self.assertEqual(max(value1, value2), result)

        result, _ = await self.call('main', [value2, value1], return_type=bytes)
        self.assertEqual(max(value2, value1), result)

        value1 = b'alg'
        value2 = b'al'
        result, _ = await self.call('main', [value1, value2], return_type=bytes)
        self.assertEqual(max(value1, value2), result)

        value = b'some string'
        result, _ = await self.call('main', [value, value], return_type=bytes)
        self.assertEqual(max(value, value), result)

    async def test_max_bytes_more_arguments(self):
        await self.set_up_contract('MaxBytesMoreArguments.py')

        values = b'Lorem', b'ipsum', b'dolor', b'sit', b'amet'
        result, _ = await self.call('main', [], return_type=bytes)
        self.assertEqual(max(values), result)

    def test_max_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'MaxTooFewParameters.py')

    def test_max_mismatched_types(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MaxMismatchedTypes.py')

    # endregion

    # region min test

    async def test_min_int(self):
        await self.set_up_contract('MinInt.py')

        val1 = 50
        val2 = 1
        result, _ = await self.call('main', [val1, val2], return_type=int)
        self.assertEqual(min(val1, val2), result)

    async def test_min_int_more_arguments(self):
        await self.set_up_contract('MinIntMoreArguments.py')

        numbers = 2, 8, 1, 4, 16
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(min(numbers), result)

    async def test_min_str(self):
        await self.set_up_contract('MinStr.py')

        value1 = 'foo'
        value2 = 'bar'
        result, _ = await self.call('main', [value1, value2], return_type=str)
        self.assertEqual(min(value1, value2), result)

        result, _ = await self.call('main', [value2, value1], return_type=str)
        self.assertEqual(min(value2, value1), result)

        value1 = 'alg'
        value2 = 'al'
        result, _ = await self.call('main', [value1, value2], return_type=str)
        self.assertEqual(min(value1, value2), result)

        value = 'some string'
        result, _ = await self.call('main', [value, value], return_type=str)
        self.assertEqual(min(value, value), result)

    async def test_min_str_more_arguments(self):
        await self.set_up_contract('MinStrMoreArguments.py')

        values = 'Lorem', 'ipsum', 'dolor', 'sit', 'amet'
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(min(values), result)

    async def test_min_bytes(self):
        await self.set_up_contract('MinBytes.py')

        value1 = b'foo'
        value2 = b'bar'
        result, _ = await self.call('main', [value1, value2], return_type=bytes)
        self.assertEqual(min(value1, value2), result)

        result, _ = await self.call('main', [value2, value1], return_type=bytes)
        self.assertEqual(min(value2, value1), result)

        value1 = b'alg'
        value2 = b'al'
        result, _ = await self.call('main', [value1, value2], return_type=bytes)
        self.assertEqual(min(value1, value2), result)

        value = b'some string'
        result, _ = await self.call('main', [value, value], return_type=bytes)
        self.assertEqual(min(value, value), result)

    async def test_min_bytes_more_arguments(self):
        await self.set_up_contract('MinBytesMoreArguments.py')

        values = b'Lorem', b'ipsum', b'dolor', b'sit', b'amet'
        result, _ = await self.call('main', [], return_type=bytes)
        self.assertEqual(min(values), result)

    def test_min_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'MinTooFewParameters.py')

    def test_min_mismatched_types(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MinMismatchedTypes.py')

    # endregion

    # region abs test

    async def test_abs(self):
        await self.set_up_contract('Abs.py')

        val = 10
        result, _ = await self.call('main', [val], return_type=int)
        self.assertEqual(abs(val), result)

        result, _ = await self.call('main', [-1], return_type=int)
        self.assertEqual(abs(-1), result)

        result, _ = await self.call('main', [1], return_type=int)
        self.assertEqual(abs(1), result)

    def test_abs_bytes(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'AbsMismatchedTypesBytes.py')

    def test_abs_string(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'AbsMismatchedTypesString.py')

    def test_abs_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'AbsTooFewParameters.py')

    def test_abs_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'AbsTooManyParameters.py')

    # endregion

    # region sum test

    async def test_sum(self):
        await self.set_up_contract('Sum.py')

        val = [1, 2, 3, 4]
        result, _ = await self.call('main', [val], return_type=int)
        self.assertEqual(sum(val), result)

        val = list(range(10, 20, 2))
        result, _ = await self.call('main', [val], return_type=int)
        self.assertEqual(sum(val), result)

    async def test_sum_with_start(self):
        await self.set_up_contract('SumWithStart.py')

        val = [1, 2, 3, 4]
        result, _ = await self.call('main', [val, 10], return_type=int)
        self.assertEqual(sum(val, 10), result)

        val = list(range(10, 20, 2))
        result, _ = await self.call('main', [val, 20], return_type=int)
        self.assertEqual(sum(val, 20), result)

    def test_sum_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'SumMismatchedTypes.py')

    def test_sum_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'SumTooFewParameters.py')

    def test_sum_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'SumTooManyParameters.py')

    # endregion

    # region str split test

    async def test_str_split_opcodes(self):
        expected_output_start = (
                Opcode.INITSLOT
                + b'\x00'
                + b'\x03'
                + Opcode.LDARG1
                + Opcode.LDARG2
                + Opcode.LDARG0
                + Opcode.PUSH2
                + Opcode.PICK
                + Opcode.SWAP
                + Opcode.CALLT + b'\x00\x00'
                + Opcode.OVER
                + Opcode.PUSH0
                + Opcode.JMPLT
                + Integer(25).to_byte_array(signed=True, min_length=1)
        )

        output, _ = self.assertCompile('StrSplit.py')
        self.assertStartsWith(output, expected_output_start)

    async def test_str_split(self):
        await self.set_up_contract('StrSplit.py')

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 2
        expected_result = string.split(separator, maxsplit)
        result, _ = await self.call('main', [string, separator, maxsplit], return_type=list)
        self.assertEqual(expected_result, result)

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 1
        expected_result = string.split(separator, maxsplit)
        result, _ = await self.call('main', [string, separator, maxsplit], return_type=list)
        self.assertEqual(expected_result, result)

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 0
        expected_result = string.split(separator, maxsplit)
        result, _ = await self.call('main', [string, separator, maxsplit], return_type=list)
        self.assertEqual(expected_result, result)

        string = 'unit123test123str123split'
        separator = '123'
        maxsplit = 1
        expected_result = string.split(separator, maxsplit)
        result, _ = await self.call('main', [string, separator, maxsplit], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_str_split_maxsplit_default_opcodes(self):
        expected_output = (
                Opcode.INITSLOT
                + b'\x00'
                + b'\x02'
                + Opcode.LDARG1
                + Opcode.LDARG0
                + Opcode.CALLT + b'\x00\x00'
                + Opcode.RET
        )

        output, _ = self.assertCompile('StrSplitMaxsplitDefault.py')
        self.assertEqual(expected_output, output)

    async def test_str_split_maxsplit_default(self):
        await self.set_up_contract('StrSplitMaxsplitDefault.py')

        string = '1#2#3#4'
        separator = '#'
        expected_result = string.split(separator)
        result, _ = await self.call('main', [string, separator], return_type=list)
        self.assertEqual(expected_result, result)

        string = 'unit123test123str123split'
        separator = '123'
        expected_result = string.split(separator)
        result, _ = await self.call('main', [string, separator], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_str_split_default_opcodes(self):
        default_separator = String(' ').to_bytes()
        expected_output = (
                Opcode.INITSLOT
                + b'\x00'
                + b'\x01'
                + Opcode.PUSHDATA1
                + Integer(len(default_separator)).to_byte_array(min_length=1)
                + default_separator
                + Opcode.LDARG0
                + Opcode.CALLT + b'\x00\x00'
                + Opcode.RET
        )

        output, _ = self.assertCompile('StrSplitSeparatorDefault.py')
        self.assertEqual(expected_output, output)

    async def test_str_split_default(self):
        await self.set_up_contract('StrSplitSeparatorDefault.py')

        string = '1 2 3 4'
        expected_result = string.split()
        result, _ = await self.call('main', [string], return_type=list)
        self.assertEqual(expected_result, result)

    # endregion

    # region count test

    async def test_count_list_int(self):
        await self.set_up_contract('CountListInt.py')

        list_ = [1, 2, 3, 4, 1, 1, 0]
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(list_.count(1), result)

    async def test_count_list_str(self):
        await self.set_up_contract('CountListStr.py')

        list_ = ['unit', 'test', 'unit', 'unit', 'random', 'string']
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(list_.count('unit'), result)

    async def test_count_list_bytes(self):
        await self.set_up_contract('CountListBytes.py')

        list_ = [b'unit', b'test', b'unit', b'unit', b'random', b'string']
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(list_.count(b'unit'), result)

    async def test_count_list_different_primitive_types(self):
        await self.set_up_contract('CountListDifferentPrimitiveTypes.py')

        list_ = [b'unit', 'test', b'unit', b'unit', 123, 123, True, False]
        expected_result = [list_.count(b'unit'), list_.count('test'), list_.count(123)]
        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_count_list_different_any_types(self):
        await self.set_up_contract('CountListAnyType.py')

        mixed_list = [[b'unit', b'unit'], [123, 123], [True, False], [True, False], [b'unit', 'test'], 'not list']

        count1 = mixed_list.count([b'unit', 'test'])
        count2 = mixed_list.count([123, 123])
        count3 = mixed_list.count([True, False])
        count4 = mixed_list.count(['random value', 'random value', 'random value'])
        expected_result = [count1, count2, count3, count4]

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_count_list_only_sequences(self):
        await self.set_up_contract('CountListOnlySequences.py')

        mixed_list = [[b'unit', b'unit'], [123, 123], [True, False], [True, False], [b'unit', 'test']]

        count1 = mixed_list.count([b'unit', 'test'])
        count2 = mixed_list.count([123, 123])
        count3 = mixed_list.count([True, False])
        count4 = mixed_list.count(['random value', 'random value', 'random value'])
        expected_result = [count1, count2, count3, count4]

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_count_list_empty(self):
        await self.set_up_contract('CountListEmpty.py')

        list_ = []
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(list_.count(1), result)

    async def test_count_tuple_int(self):
        await self.set_up_contract('CountTupleInt.py')

        tuple_ = (1, 2, 3, 4, 1, 1, 0)
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(tuple_.count(1), result)

    async def test_count_tuple_str(self):
        await self.set_up_contract('CountTupleStr.py')

        tuple_ = ('unit', 'test', 'unit', 'unit', 'random', 'string')
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(tuple_.count('unit'), result)

    async def test_count_tuple_bytes(self):
        await self.set_up_contract('CountTupleBytes.py')

        tuple_ = (b'unit', b'test', b'unit', b'unit', b'random', b'string')
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(tuple_.count(b'unit'), result)

    async def test_count_tuple_different_types(self):
        await self.set_up_contract('CountTupleDifferentTypes.py')

        tuple_ = (b'unit', 'test', b'unit', b'unit', 123, 123, True, False)
        expected_result = [tuple_.count(b'unit'), tuple_.count('test'), tuple_.count(123)]
        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_count_tuple_different_non_primitive_types(self):
        await self.set_up_contract('CountTupleDifferentNonPrimitiveTypes.py')

        mixed_tuple = ([b'unit', 'test'], [b'unit', b'unit'], [123, 123], [True, False], [True, False])

        count1 = mixed_tuple.count([b'unit', 'test'])
        count2 = mixed_tuple.count([123, 123])
        count3 = mixed_tuple.count([True, False])
        expected_result = [count1, count2, count3]

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_count_tuple_empty(self):
        await self.set_up_contract('CountTupleEmpty.py')

        tuple_ = ()
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(tuple_.count(1), result)

    async def test_count_range(self):
        await self.set_up_contract('CountRange.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(range(10).count(1), result)

    def test_count_sequence_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'CountSequenceTooManyArguments.py')

    def test_count_sequence_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'CountSequenceTooFewArguments.py')

    async def test_count_str(self):
        await self.set_up_contract('CountStr.py')

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = 43
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = 1000
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = -1000
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = -4
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 23
        end = 43
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = -11
        end = 43
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = -1000
        end = 43
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 1000
        end = 43
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 0
        end = 43
        expected_result = str_.count(substr, start, end)
        result, _ = await self.call('main', [str_, substr, start, end], return_type=int)
        self.assertEqual(expected_result, result)

    async def test_count_str_end_default(self):
        await self.set_up_contract('CountStrEndDefault.py')

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 0
        expected_result = str_.count(substr, start)
        result, _ = await self.call('main', [str_, substr, start], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 4
        expected_result = str_.count(substr, start)
        result, _ = await self.call('main', [str_, substr, start], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        start = 0
        expected_result = str_.count(substr, start)
        result, _ = await self.call('main', [str_, substr, start], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        start = 5
        expected_result = str_.count(substr, start)
        result, _ = await self.call('main', [str_, substr, start], return_type=int)
        self.assertEqual(expected_result, result)

    async def test_count_str_default(self):
        await self.set_up_contract('CountStrDefault.py')

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        expected_result = str_.count(substr)
        result, _ = await self.call('main', [str_, substr], return_type=int)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        expected_result = str_.count(substr)
        result, _ = await self.call('main', [str_, substr], return_type=int)
        self.assertEqual(expected_result, result)

    def test_count_str_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'CountStrTooManyArguments.py')

    def test_count_str_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'CountStrTooFewArguments.py')

    # endregion

    # region super test

    def test_super_with_args(self):
        # TODO: Change when super with args is implemented #2kq1rw4
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'SuperWithArgs.py')

    async def test_super_call_method(self):
        await self.set_up_contract('SuperCallMethod.py')

        super_method_expected_result = -20
        arg = 20
        result, _ = await self.call('example_method', [arg], return_type=int)
        self.assertEqual(arg, result)

        arg = 30
        result, _ = await self.call('example_method', [arg], return_type=int)
        self.assertEqual(arg, result)

        arg = 40
        result, _ = await self.call('example_method', [arg], return_type=int)
        self.assertEqual(super_method_expected_result, result)

    # endregion

    # region int test

    async def test_int_str(self):
        await self.set_up_contract('IntStr.py')

        value = '0b101'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0B101'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0b101'
        base = 2
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0B101'
        base = 2
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0o123'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0O123'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0o123'
        base = 8
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0O123'
        base = 8
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        with self.assertRaises(boatestcase.AssertException):
            value = '0x123'
            base = 8
            await self.call('main', [value, base], return_type=int)

        with self.assertRaises(ValueError):
            int(value, base)

        value = '0x123'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0X123'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0x123'
        base = 16
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '0X123'
        base = 16
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = '123'
        base = 16
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = 'abcdef'
        base = 16
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        with self.assertRaises(boatestcase.AssertException):
            value = 'abcdefg'
            base = 16
            await self.call('main', [value, base], return_type=int)

        with self.assertRaises(ValueError):
            int(value, base)

        value = '11'
        base = 11
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

    async def test_int_bytes(self):
        await self.set_up_contract('IntBytes.py')

        value = b'0b101'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0B101'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0b101'
        base = 2
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0B101'
        base = 2
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0o123'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0O123'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0o123'
        base = 8
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0O123'
        base = 8
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        with self.assertRaises(boatestcase.AssertException):
            value = b'0x123'
            base = 8
            await self.call('main', [value, base], return_type=int)

        with self.assertRaises(ValueError):
            int(value, base)

        value = b'0x123'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0X123'
        base = 0
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0x123'
        base = 16
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'0X123'
        base = 16
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'123'
        base = 16
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        value = b'abcdef'
        base = 16
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

        with self.assertRaises(boatestcase.AssertException):
            value = b'abcdefg'
            base = 16
            await self.call('main', [value, base], return_type=int)

        with self.assertRaises(ValueError):
            int(value, base)

        value = b'11'
        base = 11
        result, _ = await self.call('main', [value, base], return_type=int)
        self.assertEqual(int(value, base), result)

    async def test_int_int(self):
        await self.set_up_contract('IntInt.py')

        value = 10
        result, _ = await self.call('main', [value], return_type=int)
        self.assertEqual(int(value), result)

        value = -10
        result, _ = await self.call('main', [value], return_type=int)
        self.assertEqual(int(value), result)

    def test_int_int_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'IntIntTooManyParameters.py')

    async def test_int_no_parameters(self):
        await self.set_up_contract('IntNoParameters.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(int(), result)

    # endregion

    # region bool test

    async def test_bool(self):
        await self.set_up_contract('Bool.py')

        val = 1
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = 'test'
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = b'test'
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = [1, 2, 3]
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = {'1': 2}
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

    async def test_bool_bytes(self):
        await self.set_up_contract('BoolBytes.py')

        val = b'123'
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = b''
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

    async def test_bool_class(self):
        await self.set_up_contract('BoolClass.py')

        # dunder methods are not supported in neo3-boa
        class Example:
            def __init__(self):
                self.test = 123

        result, _ = await self.call('main', [], return_type=bool)
        self.assertEqual(bool(Example()), result)

    async def test_bool_dict(self):
        await self.set_up_contract('BoolDict.py')

        val = {}
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = {'a': 123, 'b': 56, 'c': 1}
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

    async def test_bool_int(self):
        await self.set_up_contract('BoolInt.py')

        val = -1
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = 0
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = 1
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

    async def test_bool_list(self):
        await self.set_up_contract('BoolList.py')

        val = []
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = [1, 2, 3, 4, 5]
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

    async def test_bool_range(self):
        await self.set_up_contract('BoolRange.py')

        result, _ = await self.call('range_0', [], return_type=bool)
        self.assertEqual(bool(range(0)), result)

        result, _ = await self.call('range_not_0', [], return_type=bool)
        self.assertEqual(bool(range(10)), result)

    async def test_bool_str(self):
        await self.set_up_contract('BoolStr.py')

        val = 'unit test'
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

        val = ''
        result, _ = await self.call('main', [val], return_type=bool)
        self.assertEqual(bool(val), result)

    # endregion

    # region list test

    async def test_list_any(self):
        await self.set_up_contract('ListAny.py')

        val = [1, 2, 3, 4]
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

        val = {'a': 1, 'b': '2', 'c': True, 'd': b'01', '12e12e12e12': 123}
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

        val = 'unit test'
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(bytes(val, 'utf-8')), result)

        val = b'unit test'
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

        with self.assertRaises(boatestcase.FaultException):
            val = 123
            await self.call('main', [val], return_type=list)

    async def test_list_default(self):
        await self.set_up_contract('ListDefault.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(list(), result)

    async def test_list_sequence(self):
        await self.set_up_contract('ListSequence.py')

        val = [1, 2, 3, 4]
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

        val = (1, 2, 3, 4)
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

        val = range(0, 10)
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

        val = [1, 2, 3, 4]
        result, _ = await self.call('verify_list_unchanged', [val], return_type=list)
        new_list = list(val)
        val[0] = val[1]
        self.assertEqual(new_list, result)

    def test_list_sequence_mismatched_return_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ListSequenceMismatchedReturnType.py')

    async def test_list_mapping(self):
        await self.set_up_contract('ListMapping.py')

        val = {'a': 1, 'b': 2, 'c': 3, 'd': 0, '12e12e12e12': 123}
        result, _ = await self.call('main', [val], return_type=list)
        # result should be a list of all the keys used in the dictionary, in insertion order
        self.assertEqual(list(val), result)

        val = {'a': 1, 'b': '2', 'c': True, 'd': b'01', '12e12e12e12': 123}
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

        val = {1: 0, 23: 12, -10: 412, 25: '123'}
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

        val = {b'123': 123, b'test': 'test', b'unit': 'unit'}
        expected_result = [String.from_bytes(item) for item in val]
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(expected_result, result)

        val = {'a': 1, 'b': '2', 'c': True, 1: 0, 23: 12, 25: 'value'}
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

    def test_list_mapping_mismatched_return_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ListMappingMismatchedReturnType.py')

    async def test_list_bytes(self):
        await self.set_up_contract('ListBytes.py')

        val = b'unit test'
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

    def test_list_bytes_mismatched_return_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ListBytesMismatchedReturnType.py')

    async def test_list_str(self):
        await self.set_up_contract('ListString.py')

        val = 'unit test'
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

    def test_list_str_mismatched_return_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ListStringMismatchedReturnType.py')

    async def test_list_bytes_str(self):
        await self.set_up_contract('ListBytesString.py')

        # If the compiler doesn't have a type hint to know if it's a bytes or str value it will consider it as bytes
        val = 'unit test'
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(bytes(val, 'utf-8')), result)

        val = b'unit test'
        result, _ = await self.call('main', [val], return_type=list)
        self.assertEqual(list(val), result)

    # endregion

    # region str test

    async def test_str_bytes_str(self):
        await self.set_up_contract('StrByteString.py')

        value = 'test'
        result, _ = await self.call('str_parameter', [value], return_type=str)
        self.assertEqual(str(value), result)

        value = b'test'
        result, _ = await self.call('bytes_parameter', [value], return_type=str)
        # since bytes and string is the same thing internally it will return 'test' instead of the "b'test'"
        self.assertEqual('test', result)

        result, _ = await self.call('empty_parameter', [], return_type=str)
        self.assertEqual(str(), result)

    async def test_str_int(self):
        await self.set_up_contract('StrInt.py')

        value = 1234567890
        result, _ = await self.call('main', [value], return_type=str)
        self.assertEqual(str(value), result)

        value = -1234567890
        result, _ = await self.call('main', [value], return_type=str)
        self.assertEqual(str(value), result)

    async def test_str_bool(self):
        await self.set_up_contract('StrBool.py')

        value = True
        result, _ = await self.call('main', [value], return_type=str)
        self.assertEqual(str(value), result)

        value = False
        result, _ = await self.call('main', [value], return_type=str)
        self.assertEqual(str(value), result)

    def test_str_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'StrTooManyParameters.py')

    # endregion
