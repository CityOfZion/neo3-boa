from neo3.core import types

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3_test.tests import boatestcase


class TestBytes(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/bytes_test'

    SUBSEQUENCE_NOT_FOUND_MSG = 'subsequence of bytes not found'

    def test_bytes_literal_value(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytesLiteral.py')
        self.assertEqual(expected_output, output)

    def test_bytes_get_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytesGetValue.py')
        self.assertEqual(expected_output, output)

    async def test_bytes_get_value_run(self):
        await self.set_up_contract('BytesGetValue.py')

        result, _ = await self.call('Main', [bytes([1, 2, 3])], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('Main', [b'0'], return_type=int)
        self.assertEqual(48, result)

    def test_bytes_get_value_negative_index_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSHM1
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytesGetValueNegativeIndex.py')
        self.assertEqual(expected_output, output)

    async def test_bytes_get_value_negative_index_run(self):
        await self.set_up_contract('BytesGetValueNegativeIndex.py')

        result, _ = await self.call('Main', [bytes([1, 2, 3])], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('Main', [b'0'], return_type=int)
        self.assertEqual(48, result)

    def test_bytes_set_value(self):
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, 'BytesSetValue.py')

    def test_bytes_clear(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'BytesClear.py')

    def test_bytes_reverse(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'BytesReverse.py')

    async def test_bytes_to_int(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'BytesToInt.py')
        await self.set_up_contract('BytesToInt.py')

        result, _ = await self.call('bytes_to_int', return_type=int)
        self.assertEqual(int.from_bytes(b'\x01\x02', "little", signed=True), result)

    async def test_bytes_to_int_default_args(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'BytesToIntDefaultArgs.py')
        await self.set_up_contract('BytesToIntDefaultArgs.py')

        for x in range(0, 256):
            bytes_value = x.to_bytes()
            result, _ = await self.call('main', [bytes_value], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, "little", signed=True), result)

        for x in range(256, 0x10000, 100):
            bytes_value = x.to_bytes(2)
            result, _ = await self.call('main', [bytes_value], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, "little", signed=True), result)

        for x in range(0, 0x100000, 1000):
            bytes_value = x.to_bytes(3)

            result, _ = await self.call('main', [bytes_value], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, "little", signed=True), result)

    async def test_bytes_to_int_big_endian_args(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'BytesToIntBigEndianArgs.py')
        await self.set_up_contract('BytesToIntBigEndianArgs.py')

        for x in range(0, 0x100000, 1000):
            bytes_value = x.to_bytes(3)

            result, _ = await self.call('main', [bytes_value, True], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, 'big', signed=True), result)

            result, _ = await self.call('main', [bytes_value, False], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, 'little', signed=True), result)

    async def test_bytes_to_int_big_endian_signed_args(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'BytesToIntBigEndianSignedArgs.py')
        await self.set_up_contract('BytesToIntBigEndianSignedArgs.py')

        for x in range(0, 0x100000, 1000):
            bytes_value = x.to_bytes(3)

            result, _ = await self.call('main', [bytes_value, True, True], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, 'big', signed=True), result)

            result, _ = await self.call('main', [bytes_value, False, True], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, 'little', signed=True), result)

            result, _ = await self.call('main', [bytes_value, True, False], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, 'big', signed=False), result)

            result, _ = await self.call('main', [bytes_value, False, False], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, 'little', signed=False), result)

        big_bytes_value = b'abcdef1234567890'
        result, _ = await self.call('main', [big_bytes_value, True, True], return_type=int)
        self.assertEqual(int.from_bytes(big_bytes_value, 'big', signed=True), result)

        result, _ = await self.call('main', [big_bytes_value, False, True], return_type=int)
        self.assertEqual(int.from_bytes(big_bytes_value, 'little', signed=True), result)

        result, _ = await self.call('main', [big_bytes_value, True, False], return_type=int)
        self.assertEqual(int.from_bytes(big_bytes_value, 'big', signed=False), result)

        result, _ = await self.call('main', [big_bytes_value, False, False], return_type=int)
        self.assertEqual(int.from_bytes(big_bytes_value, 'little', signed=False), result)

    async def test_bytes_to_int_negative_numbers(self):
        self.assertCompilerLogs(CompilerWarning.MethodWarning, 'BytesToIntBigEndianSignedArgs.py')
        await self.set_up_contract('BytesToIntBigEndianSignedArgs.py')

        min_num_len2 = 2 ** 16 // 2 * -1
        max_num_len2 = 2 ** 16 // 2 - 1
        for x in range(min_num_len2, max_num_len2 + 1, 200):
            bytes_value = x.to_bytes(2, signed=True)

            result, _ = await self.call('main', [bytes_value, True, True], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, 'big', signed=True), result)

            result, _ = await self.call('main', [bytes_value, False, True], return_type=int)
            self.assertEqual(int.from_bytes(bytes_value, 'little', signed=True), result)

    def test_bytes_to_int_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'BytesToIntWithBuiltin.py')

    async def test_bytes_to_bool(self):
        await self.set_up_contract('BytesToBool.py')

        result, _ = await self.call('bytes_to_bool', [b'\x00'], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('bytes_to_bool', [b'\x01'], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('bytes_to_bool', [b'\x02'], return_type=bool)
        self.assertEqual(True, result)

    def test_bytes_to_bool_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'BytesToBoolWithBuiltin.py')

    async def test_bytes_to_str(self):
        await self.set_up_contract('BytesToStr.py')

        result, _ = await self.call('bytes_to_str', return_type=str)
        self.assertEqual('abc', result)

    def test_bytes_to_str_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'BytesToStrWithBuiltin.py')

    def test_bytes_from_byte_array(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a
            + Opcode.STLOC1
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytesFromBytearray.py')
        self.assertEqual(expected_output, output)

    async def test_assign_with_slice(self):
        await self.set_up_contract('AssignSlice.py')

        arg = b'unittest'
        result, _ = await self.call('main', [arg], return_type=bytearray)
        self.assertEqual(arg[1:2], result)

        arg = b'123'
        result, _ = await self.call('main', [arg], return_type=bytearray)
        self.assertEqual(arg[1:2], result)

        arg = bytearray()
        result, _ = await self.call('main', [arg], return_type=bytearray)
        self.assertEqual(arg[1:2], result)

    async def test_slice_with_cast(self):
        await self.set_up_contract('SliceWithCast.py')

        result, _ = await self.call('main', [b'unittest'], return_type=bytes)
        self.assertEqual(b'unittest'[1:2], result)

        result, _ = await self.call('main', ['123'], return_type=bytes)
        self.assertEqual(b'123'[1:2], result)

        result, _ = await self.call('main', [12345], return_type=bytes)
        self.assertEqual(Integer(12345).to_byte_array()[1:2], result)

        result, _ = await self.call('main', [bytearray()], return_type=bytes)
        self.assertEqual(bytearray()[1:2], result)

    async def test_slice_with_stride(self):
        await self.set_up_contract('SliceWithStride.py')

        a = b'unit_test'
        expected_result = a[2:5:2]
        result, _ = await self.call('literal_values', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6:5:2]
        result, _ = await self.call('negative_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:-1:2]
        result, _ = await self.call('negative_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6:-1:2]
        result, _ = await self.call('negative_values', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999:5:2]
        result, _ = await self.call('negative_really_low_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:-999:2]
        result, _ = await self.call('negative_really_low_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999:-999:2]
        result, _ = await self.call('negative_really_low_values', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999:5:2]
        result, _ = await self.call('really_high_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:999:2]
        result, _ = await self.call('really_high_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999:999:2]
        result, _ = await self.call('really_high_values', return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_slice_with_negative_stride(self):
        await self.set_up_contract('SliceWithNegativeStride.py')

        a = b'unit_test'
        expected_result = a[2:5:-1]
        result, _ = await self.call('literal_values', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6:5:-1]
        result, _ = await self.call('negative_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:-1:-1]
        result, _ = await self.call('negative_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6:-1:-1]
        result, _ = await self.call('negative_values', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999:5:-1]
        result, _ = await self.call('negative_really_low_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:-999:-1]
        result, _ = await self.call('negative_really_low_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999:-999:-1]
        result, _ = await self.call('negative_really_low_values', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999:5:-1]
        result, _ = await self.call('really_high_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:999:-1]
        result, _ = await self.call('really_high_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999:999:-1]
        result, _ = await self.call('really_high_values', return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_slice_omitted_with_stride(self):
        await self.set_up_contract('SliceOmittedWithStride.py')

        a = b'unit_test'
        expected_result = a[::2]
        result, _ = await self.call('omitted_values', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:5:2]
        result, _ = await self.call('omitted_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[2::2]
        result, _ = await self.call('omitted_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6::2]
        result, _ = await self.call('negative_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:-1:2]
        result, _ = await self.call('negative_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999::2]
        result, _ = await self.call('negative_really_low_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:-999:2]
        result, _ = await self.call('negative_really_low_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999::2]
        result, _ = await self.call('really_high_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:999:2]
        result, _ = await self.call('really_high_end', return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_slice_omitted_with_negative_stride(self):
        await self.set_up_contract('SliceOmittedWithNegativeStride.py')

        a = b'unit_test'
        expected_result = a[::-2]
        result, _ = await self.call('omitted_values', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:5:-2]
        result, _ = await self.call('omitted_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[2::-2]
        result, _ = await self.call('omitted_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6::-2]
        result, _ = await self.call('negative_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:-1:-2]
        result, _ = await self.call('negative_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999::-2]
        result, _ = await self.call('negative_really_low_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:-999:-2]
        result, _ = await self.call('negative_really_low_end', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999::-2]
        result, _ = await self.call('really_high_start', return_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:999:-2]
        result, _ = await self.call('really_high_end', return_type=bytes)
        self.assertEqual(expected_result, result)

    def test_byte_array_get_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytearrayGetValue.py')
        self.assertEqual(expected_output, output)

    async def test_byte_array_get_value_run(self):
        await self.set_up_contract('BytearrayGetValue.py')

        result, _ = await self.call('Main', [bytes([1, 2, 3])], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('Main', [b'0'], return_type=int)
        self.assertEqual(48, result)

    def test_byte_array_get_value_negative_index_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSHM1
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytearrayGetValueNegativeIndex.py')
        self.assertEqual(expected_output, output)

    async def test_byte_array_get_value_negative_index_run(self):
        await self.set_up_contract('BytearrayGetValueNegativeIndex.py')

        result, _ = await self.call('Main', [bytes([1, 2, 3])], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('Main', [b'0'], return_type=int)
        self.assertEqual(48, result)

    def test_byte_array_set_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC0
            + Opcode.LDLOC0     # var[0] = 0x01
            + Opcode.PUSH0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.LDLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytearraySetValue.py')
        self.assertEqual(expected_output, output)

    async def test_byte_array_set_value_run(self):
        await self.set_up_contract('BytearraySetValue.py')

        result, _ = await self.call('Main', [b'123'], return_type=bytes)
        self.assertEqual(b'\x0123', result)

        result, _ = await self.call('Main', [b'0'], return_type=bytes)
        self.assertEqual(b'\x01', result)

    def test_byte_array_set_value_negative_index_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC0
            + Opcode.LDLOC0     # var[-1] = 0x01
            + Opcode.PUSHM1
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.LDLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytearraySetValueNegativeIndex.py')
        self.assertEqual(expected_output, output)

    async def test_byte_array_set_value_negative_index_run(self):
        await self.set_up_contract('BytearraySetValueNegativeIndex.py')

        result, _ = await self.call('Main', [b'123'], return_type=bytes)
        self.assertEqual(b'12\x01', result)

        result, _ = await self.call('Main', [b'0'], return_type=bytes)
        self.assertEqual(b'\x01', result)

    def test_byte_array_literal_value(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'BytearrayLiteral.py')

    def test_byte_array_default_compile(self):
        expected_output = (
            Opcode.PUSH0      # bytearray()
            + Opcode.NEWBUFFER
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytearrayDefault.py')
        self.assertEqual(expected_output, output)

    async def test_byte_array_default_run(self):
        await self.set_up_contract('BytearrayDefault.py')

        result, _ = await self.call('create_bytearray', return_type=bytearray)
        self.assertEqual(bytearray(), result)

    def test_byte_array_from_literal_bytes(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytearrayFromLiteralBytes.py')
        self.assertEqual(expected_output, output)

    def test_byte_array_from_variable_bytes(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # b = bytearray(a)
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC1
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytearrayFromVariableBytes.py')
        self.assertEqual(expected_output, output)

    def test_byte_array_from_size_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # bytearray(size)
            + Opcode.NEWBUFFER
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BytearrayFromSize.py')
        self.assertEqual(expected_output, output)

    async def test_byte_array_from_size_run(self):
        await self.set_up_contract('BytearrayFromSize.py')

        result, _ = await self.call('create_bytearray', [10], return_type=bytearray)
        self.assertEqual(bytearray(10), result)

        result, _ = await self.call('create_bytearray', [0], return_type=bytearray)
        self.assertEqual(bytearray(0), result)

        with self.assertRaises(Exception) as context:
            await self.call('create_bytearray', [-10], return_type=bytearray)
        self.assertRegex(context.exception.__str__(), 'invalid size')

    def test_byte_array_from_list_of_int(self):
        compiler_error_message = self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'BytearrayFromListOfInt.py')

        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.type.type import Type
        arg_type = Type.list.build([Type.int])
        expected_error = CompilerError.NotSupportedOperation(0, 0, f'{Builtin.ByteArray.identifier}({arg_type.identifier})')
        self.assertEqual(expected_error._error_message, compiler_error_message)

    async def test_byte_array_string(self):
        await self.set_up_contract('BytearrayFromString.py')

        # Neo3-boa's bytearray only converts with utf-8 encoding
        string = 'string value'
        expected = bytearray(string, 'utf-8')
        result, _ = await self.call('main', [string], return_type=bytearray)
        self.assertEqual(expected, result)

        string = 'áãõ😀'
        expected = bytearray(string, 'utf-8')
        result, _ = await self.call('main', [string], return_type=bytearray)
        self.assertEqual(expected, result)

    def test_byte_array_string_with_encoding(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'BytearrayFromStringWithEncoding.py')

    async def test_byte_array_append(self):
        await self.set_up_contract('BytearrayAppend.py')

        expected = bytearray(b'\x01\x02\x03')
        expected.append(4)
        result, _ = await self.call('Main', return_type=bytearray)
        self.assertEqual(expected, result)

    async def test_byte_array_append_with_builtin(self):
        await self.set_up_contract('BytearrayAppendWithBuiltin.py')

        expected = bytearray(b'\x01\x02\x03')
        expected.append(4)
        result, _ = await self.call('Main', return_type=bytearray)
        self.assertEqual(expected, result)

    async def test_byte_array_append_mutable_sequence_with_builtin(self):
        await self.set_up_contract('BytearrayAppendWithMutableSequence.py')

        expected = bytearray(b'\x01\x02\x03')
        expected.append(4)
        result, _ = await self.call('Main', return_type=bytearray)
        self.assertEqual(expected, result)

    async def test_byte_array_clear(self):
        await self.set_up_contract('BytearrayClear.py')

        expected = bytearray()
        result, _ = await self.call('Main', return_type=bytearray)
        self.assertEqual(expected, result)

    async def test_byte_array_reverse(self):
        await self.set_up_contract('BytearrayReverse.py')

        expected = bytearray(b'\x01\x02\x03')
        expected.reverse()
        result, _ = await self.call('Main', return_type=bytearray)
        self.assertEqual(expected, result)

    async def test_byte_array_extend(self):
        await self.set_up_contract('BytearrayExtend.py')

        expected = bytearray(b'\x01\x02\x03')
        expected.extend(b'\x04\x05\x06')
        result, _ = await self.call('Main', return_type=bytearray)
        self.assertEqual(expected, result)

    async def test_byte_array_extend_with_builtin(self):
        await self.set_up_contract('BytearrayExtendWithBuiltin.py')

        expected = bytearray(b'\x01\x02\x03')
        expected.extend(b'\x04\x05\x06')
        result, _ = await self.call('Main', return_type=bytearray)
        self.assertEqual(expected, result)

    async def test_byte_array_to_int(self):
        await self.set_up_contract('BytearrayToInt.py')

        result, _ = await self.call('bytes_to_int', return_type=int)
        self.assertEqual(int.from_bytes(bytearray(b'\x01\x02'), "little", signed=True), result)

    def test_byte_array_to_int_with_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'BytearrayToIntWithBuiltin.py')

    def test_byte_array_to_int_with_bytes_builtin(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'BytearrayToIntWithBytesBuiltin.py')

    async def test_boa2_byte_array_test(self):
        await self.set_up_contract('BytearrayBoa2Test.py')

        result, _ = await self.call('main', return_type=bytes)
        self.assertEqual(b'\t\x01\x02', result)

    def test_boa2_byte_array_test2(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'BytearrayBoa2Test2.py')

    async def test_boa2_byte_array_test3(self):
        await self.set_up_contract('BytearrayBoa2Test3.py')

        result, _ = await self.call('main', return_type=bytes)
        self.assertEqual(b'\x01\x02\xaa\xfe', result)

    async def test_boa2_slice_test(self):
        await self.set_up_contract('SliceBoa2Test.py')

        expected = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08')[:4]
        result, _ = await self.call('main', return_type=bytearray)
        self.assertEqual(expected, result)

    async def test_boa2_slice_test2(self):
        await self.set_up_contract('SliceBoa2Test2.py')

        result, _ = await self.call('main', return_type=bytes)
        self.assertEqual(b'\x02\x03\x04\x02\x03\x04\x05\x06\x01\x02\x03\x04\x03\x04', result)

    async def test_uint160_bytes(self):
        await self.set_up_contract('UInt160Bytes.py')

        expected = types.UInt160(b'0123456789abcdefghij')
        result, _ = await self.call('main', return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_uint160_int(self):
        await self.set_up_contract('UInt160Int.py')

        expected = types.UInt160((160).to_bytes(2, 'little') + bytes(18))
        result, _ = await self.call('main', return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_uint256_bytes(self):
        await self.set_up_contract('UInt256Bytes.py')

        expected = types.UInt256(b'0123456789abcdefghijklmnopqrstuv')
        result, _ = await self.call('main', return_type=types.UInt256)
        self.assertEqual(expected, result)

    async def test_uint256_int(self):
        await self.set_up_contract('UInt256Int.py')

        expected = types.UInt256((256).to_bytes(2, 'little') + bytes(30))
        result, _ = await self.call('main', return_type=types.UInt256)
        self.assertEqual(expected, result)

    async def test_bytes_upper(self):
        await self.set_up_contract('UpperBytesMethod.py')

        bytes_value = b'abcdefghijklmnopqrstuvwxyz'
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.upper(), result)

        bytes_value = b'a1b123y3z'
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.upper(), result)

        bytes_value = b'!@#$%123*-/'
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.upper(), result)

    async def test_bytes_lower(self):
        await self.set_up_contract('LowerBytesMethod.py')

        bytes_value = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.lower(), result)

        bytes_value = b'A1B123Y3Z'
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.lower(), result)

        bytes_value = b'!@#$%123*-/'
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.lower(), result)

    async def test_bytes_startswith_method(self):
        await self.set_up_contract('StartswithBytesMethod.py')

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 0
        end = len(bytes_value)
        result, _ = await self.call('main', [bytes_value, subbytes_value, start, end], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 2
        end = 6
        result, _ = await self.call('main', [bytes_value, subbytes_value, start, end], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        end = 6
        result, _ = await self.call('main', [bytes_value, subbytes_value, start, end], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        end = 3
        result, _ = await self.call('main', [bytes_value, subbytes_value, start, end], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_tes'
        start = -99
        end = -1
        result, _ = await self.call('main', [bytes_value, subbytes_value, start, end], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 0
        end = 0
        result, _ = await self.call('main', [bytes_value, subbytes_value, start, end], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        start = 0
        end = 99
        result, _ = await self.call('main', [bytes_value, subbytes_value, start, end], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

    async def test_bytes_startswith_method_default_end(self):
        await self.set_up_contract('StartswithBytesMethodDefaultEnd.py')

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 0
        result, _ = await self.call('main', [bytes_value, subbytes_value, start], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 2
        result, _ = await self.call('main', [bytes_value, subbytes_value, start], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        result, _ = await self.call('main', [bytes_value, subbytes_value, start], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 3
        result, _ = await self.call('main', [bytes_value, subbytes_value, start], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_tes'
        start = -99
        result, _ = await self.call('main', [bytes_value, subbytes_value, start], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 0
        result, _ = await self.call('main', [bytes_value, subbytes_value, start], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 99
        result, _ = await self.call('main', [bytes_value, subbytes_value, start], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        start = 0
        result, _ = await self.call('main', [bytes_value, subbytes_value, start], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

    async def test_bytes_startswith_method_defaults(self):
        await self.set_up_contract('StartswithBytesMethodDefaults.py')

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        result, _ = await self.call('main', [bytes_value, subbytes_value], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        result, _ = await self.call('main', [bytes_value, subbytes_value], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

        bytes_value = b'unit_test'
        subbytes_value = b''
        result, _ = await self.call('main', [bytes_value, subbytes_value], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

        bytes_value = b'unit_test'
        subbytes_value = b'12345'
        result, _ = await self.call('main', [bytes_value, subbytes_value], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

        bytes_value = b'unit_test'
        subbytes_value = b'bigger subbytes_value'
        result, _ = await self.call('main', [bytes_value, subbytes_value], return_type=bool)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

    async def test_bytes_strip(self):
        await self.set_up_contract('StripBytesMethod.py')

        bytes_value = b'abcdefghijklmnopqrstuvwxyz'
        sub_bytes = b'abcxyz'
        result, _ = await self.call('main', [bytes_value, sub_bytes], return_type=bytes)
        self.assertEqual(bytes_value.strip(sub_bytes), result)

        bytes_value = b'abcdefghijklmnopqrsvwxyz unit test abcdefghijklmnopqrsvwxyz'
        sub_bytes = b'abcdefghijklmnopqrsvwxyz '
        result, _ = await self.call('main', [bytes_value, sub_bytes], return_type=bytes)
        self.assertEqual(bytes_value.strip(sub_bytes), result)

        bytes_value = b'0123456789hello world987654310'
        sub_bytes = b'0987654321'
        result, _ = await self.call('main', [bytes_value, sub_bytes], return_type=bytes)
        self.assertEqual(bytes_value.strip(sub_bytes), result)

    async def test_bytes_strip_default(self):
        await self.set_up_contract('StripBytesMethodDefault.py')

        bytes_value = b'     unit test    '
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.strip(), result)

        bytes_value = b'unit test    '
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.strip(), result)

        bytes_value = b'    unit test'
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.strip(), result)

        bytes_value = b' \t\n\r\f\vunit test \t\n\r\f\v'
        result, _ = await self.call('main', [bytes_value], return_type=bytes)
        self.assertEqual(bytes_value.strip(), result)

    async def test_isdigit_method(self):
        await self.set_up_contract('BytesIsdigitMethod.py')

        bytes_value = b'0123456789'
        result, _ = await self.call('main', [bytes_value], return_type=bool)
        self.assertEqual(bytes_value.isdigit(), result)

        bytes_value = b'23mixed01'
        result, _ = await self.call('main', [bytes_value], return_type=bool)
        self.assertEqual(bytes_value.isdigit(), result)

        bytes_value = b'no digits here'
        result, _ = await self.call('main', [bytes_value], return_type=bool)
        self.assertEqual(bytes_value.isdigit(), result)

        bytes_value = b''
        result, _ = await self.call('main', [bytes_value], return_type=bool)
        self.assertEqual(bytes_value.isdigit(), result)

    async def test_bytes_join_with_sequence(self):
        await self.set_up_contract('JoinBytesMethodWithSequence.py')

        bytes_value = b' '
        sequence = [b"Unit", b"Test", b"Neo3-boa"]
        result, _ = await self.call('main', [bytes_value, sequence], return_type=bytes)
        self.assertEqual(bytes_value.join(sequence), result)

        bytes_value = b' '
        sequence = []
        result, _ = await self.call('main', [bytes_value, sequence], return_type=bytes)
        self.assertEqual(bytes_value.join(sequence), result)

        bytes_value = b' '
        sequence = [b"UnitTest"]
        result, _ = await self.call('main', [bytes_value, sequence], return_type=bytes)
        self.assertEqual(bytes_value.join(sequence), result)

    async def test_bytes_join_with_dictionary(self):
        await self.set_up_contract('JoinBytesMethodWithDictionary.py')

        bytes_value = b' '
        dictionary = {b"Unit": 1, b"Test": 2, b"Neo3-boa": 3}
        result, _ = await self.call('main', [bytes_value, dictionary], return_type=bytes)
        self.assertEqual(bytes_value.join(dictionary), result)

        bytes_value = b' '
        dictionary = {}
        result, _ = await self.call('main', [bytes_value, dictionary], return_type=bytes)
        self.assertEqual(bytes_value.join(dictionary), result)

        bytes_value = b' '
        dictionary = {b"UnitTest": 1}
        result, _ = await self.call('main', [bytes_value, dictionary], return_type=bytes)
        self.assertEqual(bytes_value.join(dictionary), result)

    async def test_bytes_index(self):
        await self.set_up_contract('IndexBytes.py')

        bytes_ = b'unit test'
        subsequence = b'i'
        start = 0
        end = 4
        result, _ = await self.call('main', [bytes_, subsequence, start, end], return_type=int)
        self.assertEqual(bytes_.index(subsequence, start, end), result)

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = 2
        end = 4
        result, _ = await self.call('main', [bytes_, bytes_sequence, start, end], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence, start, end), result)

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = 0
        end = -1
        result, _ = await self.call('main', [bytes_, bytes_sequence, start, end], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence, start, end), result)

        bytes_ = b'unit test'
        bytes_sequence = b'n'
        start = 0
        end = 99
        result, _ = await self.call('main', [bytes_, bytes_sequence, start, end], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence, start, end), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['unit test', 'i', 3, 4], return_type=int)
        self.assertRegex(str(context.exception), f'{self.SUBSEQUENCE_NOT_FOUND_MSG}')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['unit test', 'i', 4, -1], return_type=int)
        self.assertRegex(str(context.exception), f'{self.SUBSEQUENCE_NOT_FOUND_MSG}')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['unit test', 'i', 0, -99], return_type=int)
        self.assertRegex(str(context.exception), f'{self.SUBSEQUENCE_NOT_FOUND_MSG}')

    async def test_bytes_index_end_default(self):
        await self.set_up_contract('IndexBytesEndDefault.py')

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 0
        result, _ = await self.call('main', [bytes_, bytes_sequence, start], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence, start), result)

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 4
        result, _ = await self.call('main', [bytes_, bytes_sequence, start], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence, start), result)

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 6
        result, _ = await self.call('main', [bytes_, bytes_sequence, start], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence, start), result)

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = -10
        result, _ = await self.call('main', [bytes_, bytes_sequence, start], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence, start), result)

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = 99
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [bytes_, bytes_sequence, start], return_type=int)
        self.assertRegex(str(context.exception), f'{self.SUBSEQUENCE_NOT_FOUND_MSG}')

        bytes_ = b'unit test'
        bytes_sequence = b's'
        start = -1
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [bytes_, bytes_sequence, start], return_type=int)
        self.assertRegex(str(context.exception), f'{self.SUBSEQUENCE_NOT_FOUND_MSG}')

    async def test_bytes_index_defaults(self):
        await self.set_up_contract('IndexBytesDefaults.py')

        bytes_ = b'unit test'
        bytes_sequence = b'u'
        result, _ = await self.call('main', [bytes_, bytes_sequence], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence), result)

        bytes_ = b'unit test'
        bytes_sequence = b't'
        result, _ = await self.call('main', [bytes_, bytes_sequence], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence), result)

        bytes_ = b'unit test'
        bytes_sequence = b' '
        result, _ = await self.call('main', [bytes_, bytes_sequence], return_type=int)
        self.assertEqual(bytes_.index(bytes_sequence), result)

    def test_bytes_index_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'IndexBytesMismatchedType.py')

    async def test_bytes_property_slicing(self):
        await self.set_up_contract('BytesPropertySlicing.py')

        bytes_value = b'unit test'
        start = 0
        end = len(bytes_value)
        result, _ = await self.call('main', [bytes_value, start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

        start = 2
        end = len(bytes_value) - 1
        result, _ = await self.call('main', [bytes_value, start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

        start = len(bytes_value)
        end = 0
        result, _ = await self.call('main', [bytes_value, start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

    async def test_bytes_instance_variable_slicing(self):
        await self.set_up_contract('BytesInstanceVariableSlicing.py')

        bytes_value = b'unit test'
        start = 0
        end = len(bytes_value)
        result, _ = await self.call('main', [bytes_value, start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

        start = 2
        end = len(bytes_value) - 1
        result, _ = await self.call('main', [bytes_value, start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

        start = len(bytes_value)
        end = 0
        result, _ = await self.call('main', [bytes_value, start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

    async def test_bytes_class_variable_slicing(self):
        await self.set_up_contract('BytesClassVariableSlicing.py')

        bytes_value = b'unit test'
        start = 0
        end = len(bytes_value)
        result, _ = await self.call('main', [start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

        start = 2
        end = len(bytes_value) - 1
        result, _ = await self.call('main', [start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

        start = len(bytes_value)
        end = 0
        result, _ = await self.call('main', [start, end], return_type=bytes)
        self.assertEqual(bytes_value[start:end], result)

    async def test_bytes_replace(self):
        await self.set_up_contract('ReplaceBytesMethod.py')

        string = b'banana'
        old = b'an'
        new = b'o'
        count = -1
        result, _ = await self.call('main', [string, old, new, count], return_type=bytes)
        self.assertEqual(string.replace(old, new, count), result)

        old = b'a'
        new = b'o'
        count = -1
        result, _ = await self.call('main', [string, old, new, count], return_type=bytes)
        self.assertEqual(string.replace(old, new, count), result)

        old = b'a'
        new = b'oo'
        count = -1
        result, _ = await self.call('main', [string, old, new, count], return_type=bytes)
        self.assertEqual(string.replace(old, new, count), result)

        string = b'banana'
        old = b'an'
        new = b'o'
        count = 1
        result, _ = await self.call('main', [string, old, new, count], return_type=bytes)
        self.assertEqual(string.replace(old, new, count), result)

        string = b'banana'
        old = b'an'
        new = b'o'
        count = 2
        result, _ = await self.call('main', [string, old, new, count], return_type=bytes)
        self.assertEqual(string.replace(old, new, count), result)

        string = b'banana'
        old = b'an'
        new = b'o'
        count = 3
        result, _ = await self.call('main', [string, old, new, count], return_type=bytes)
        self.assertEqual(string.replace(old, new, count), result)

        string = b'banana'
        old = b'an'
        new = b'o'
        result, _ = await self.call('main_default_count', [string, old, new], return_type=bytes)
        self.assertEqual(string.replace(old, new), result)

    def test_bytes_replace_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ReplaceBytesMethodMismatchedType.py')

    def test_bytes_replace_too_many_arguments(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ReplaceBytesMethodTooManyArguments.py')

    def test_bytes_replace_too_few_arguments(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ReplaceBytesMethodTooFewArguments.py')