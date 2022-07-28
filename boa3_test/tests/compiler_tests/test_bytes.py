from boa3.boa3 import Boa3
from boa3.exception import CompilerError, CompilerWarning
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.StackItem import StackItemType
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBytes(BoaTest):
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

        path = self.get_contract_path('BytesLiteral.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_bytes_get_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytesGetValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', bytes([1, 2, 3]))
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', b'0')
        self.assertEqual(48, result)

    def test_bytes_get_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSHM1
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytesGetValueNegativeIndex.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', bytes([1, 2, 3]))
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'Main', b'0')
        self.assertEqual(48, result)

    def test_bytes_set_value(self):
        path = self.get_contract_path('BytesSetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_bytes_clear(self):
        path = self.get_contract_path('BytesClear.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_reverse(self):
        path = self.get_contract_path('BytesReverse.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_to_int(self):
        path = self.get_contract_path('BytesToInt.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_bytes_to_int_with_builtin(self):
        path = self.get_contract_path('BytesToIntWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_bytes_to_int_mismatched_types(self):
        path = self.get_contract_path('BytesToIntWithBuiltinMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_to_int_with_byte_array_builtin(self):
        path = self.get_contract_path('BytesToIntWithBytearrayBuiltin.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_to_bool(self):
        path = self.get_contract_path('BytesToBool.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x00')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x01')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x02')
        self.assertEqual(True, result)

    def test_bytes_to_bool_with_builtin(self):
        path = self.get_contract_path('BytesToBoolWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x00')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x01')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x02')
        self.assertEqual(True, result)

    def test_bytes_to_bool_with_builtin_hard_coded_false(self):
        path = self.get_contract_path('BytesToBoolWithBuiltinHardCodedFalse.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_bool')
        self.assertEqual(False, result)

    def test_bytes_to_bool_with_builtin_hard_coded_true(self):
        path = self.get_contract_path('BytesToBoolWithBuiltinHardCodedTrue.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_bool')
        self.assertEqual(True, result)

    def test_bytes_to_bool_mismatched_types(self):
        path = self.get_contract_path('BytesToBoolWithBuiltinMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_to_str(self):
        path = self.get_contract_path('BytesToStr.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_str')
        self.assertEqual('abc', result)

    def test_bytes_to_str_with_builtin(self):
        path = self.get_contract_path('BytesToStrWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_str')
        self.assertEqual('123', result)

    def test_bytes_to_str_mismatched_types(self):
        path = self.get_contract_path('BytesToStrWithBuiltinMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

        path = self.get_contract_path('BytesFromBytearray.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_assign_with_slice(self):
        path = self.get_contract_path('AssignSlice.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', b'unittest',
                                         expected_result_type=bytearray)
        self.assertEqual(b'unittest'[1:2], result)

        result = self.run_smart_contract(engine, path, 'main', b'123',
                                         expected_result_type=bytearray)
        self.assertEqual(b'123'[1:2], result)

        result = self.run_smart_contract(engine, path, 'main', bytearray(),
                                         expected_result_type=bytearray)
        self.assertEqual(bytearray()[1:2], result)

    def test_slice_with_cast(self):
        path = self.get_contract_path('SliceWithCast.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', b'unittest',
                                         expected_result_type=bytes)
        self.assertEqual(b'unittest'[1:2], result)

        result = self.run_smart_contract(engine, path, 'main', '123',
                                         expected_result_type=bytes)
        self.assertEqual(b'123'[1:2], result)

        result = self.run_smart_contract(engine, path, 'main', bytearray(),
                                         expected_result_type=bytearray)
        self.assertEqual(bytearray()[1:2], result)

        result = self.run_smart_contract(engine, path, 'main', 12345,
                                         expected_result_type=bytes)
        self.assertEqual(Integer(12345).to_byte_array()[1:2], result)

    def test_slice_with_stride(self):
        path = self.get_contract_path('SliceWithStride.py')
        engine = TestEngine()

        a = b'unit_test'
        expected_result = a[2:5:2]
        result = self.run_smart_contract(engine, path, 'literal_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6:5:2]
        result = self.run_smart_contract(engine, path, 'negative_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999:5:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999:5:2]
        result = self.run_smart_contract(engine, path, 'really_high_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_slice_with_negative_stride(self):
        path = self.get_contract_path('SliceWithNegativeStride.py')
        engine = TestEngine()

        a = b'unit_test'
        expected_result = a[2:5:-1]
        result = self.run_smart_contract(engine, path, 'literal_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6:5:-1]
        result = self.run_smart_contract(engine, path, 'negative_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:-1:-1]
        result = self.run_smart_contract(engine, path, 'negative_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6:-1:-1]
        result = self.run_smart_contract(engine, path, 'negative_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999:5:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:-999:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999:-999:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999:5:-1]
        result = self.run_smart_contract(engine, path, 'really_high_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[0:999:-1]
        result = self.run_smart_contract(engine, path, 'really_high_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999:999:-1]
        result = self.run_smart_contract(engine, path, 'really_high_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_slice_omitted_with_stride(self):
        path = self.get_contract_path('SliceOmittedWithStride.py')
        engine = TestEngine()

        a = b'unit_test'
        expected_result = a[::2]
        result = self.run_smart_contract(engine, path, 'omitted_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:5:2]
        result = self.run_smart_contract(engine, path, 'omitted_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[2::2]
        result = self.run_smart_contract(engine, path, 'omitted_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6::2]
        result = self.run_smart_contract(engine, path, 'negative_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999::2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999::2]
        result = self.run_smart_contract(engine, path, 'really_high_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_slice_omitted_with_negative_stride(self):
        path = self.get_contract_path('SliceOmittedWithNegativeStride.py')
        engine = TestEngine()

        a = b'unit_test'
        expected_result = a[::-2]
        result = self.run_smart_contract(engine, path, 'omitted_values',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:5:-2]
        result = self.run_smart_contract(engine, path, 'omitted_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[2::-2]
        result = self.run_smart_contract(engine, path, 'omitted_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-6::-2]
        result = self.run_smart_contract(engine, path, 'negative_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:-1:-2]
        result = self.run_smart_contract(engine, path, 'negative_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[-999::-2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:-999:-2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[999::-2]
        result = self.run_smart_contract(engine, path, 'really_high_start',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        a = b'unit_test'
        expected_result = a[:999:-2]
        result = self.run_smart_contract(engine, path, 'really_high_end',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_byte_array_get_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayGetValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', bytes([1, 2, 3]))
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', b'0')
        self.assertEqual(48, result)

    def test_byte_array_get_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSHM1
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayGetValueNegativeIndex.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', bytes([1, 2, 3]))
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'Main', b'0')
        self.assertEqual(48, result)

    def test_byte_array_set_value(self):
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

        path = self.get_contract_path('BytearraySetValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', b'123',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x0123', result)
        result = self.run_smart_contract(engine, path, 'Main', b'0',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01', result)

    def test_byte_array_set_value_negative_index(self):
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

        path = self.get_contract_path('BytearraySetValueNegativeIndex.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', b'123',
                                         expected_result_type=bytes)
        self.assertEqual(b'12\x01', result)
        result = self.run_smart_contract(engine, path, 'Main', b'0',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01', result)

    def test_byte_array_literal_value(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayLiteral.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_byte_array_default(self):
        expected_output = (
            Opcode.PUSH0      # bytearray()
            + Opcode.NEWBUFFER
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayDefault.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'create_bytearray',
                                         expected_result_type=bytearray)
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

        path = self.get_contract_path('BytearrayFromLiteralBytes.py')
        output = Boa3.compile(path)
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

        path = self.get_contract_path('BytearrayFromVariableBytes.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_from_size(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # bytearray(size)
            + Opcode.NEWBUFFER
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayFromSize.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'create_bytearray', 10,
                                         expected_result_type=bytearray)
        self.assertEqual(bytearray(10), result)

        result = self.run_smart_contract(engine, path, 'create_bytearray', 0,
                                         expected_result_type=bytearray)
        self.assertEqual(bytearray(0), result)

        # cannot build with negative size
        with self.assertRaisesRegex(TestExecutionException, f'^{self.MAX_ITEM_SIZE_EXCEED_MSG_PREFIX}'):
            result = self.run_smart_contract(engine, path, 'create_bytearray', -10,
                                             expected_result_type=bytes)

    def test_byte_array_from_list_of_int(self):
        path = self.get_contract_path('BytearrayFromListOfInt.py')
        compiler_error_message = self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

        from boa3.model.builtin.builtin import Builtin
        from boa3.model.type.type import Type
        arg_type = Type.list.build([Type.int])
        expected_error = CompilerError.NotSupportedOperation(0, 0, f'{Builtin.ByteArray.identifier}({arg_type.identifier})')
        self.assertEqual(expected_error._error_message, compiler_error_message)

    def test_byte_array_string(self):
        path = self.get_contract_path('BytearrayFromString.py')
        engine = TestEngine()

        # Neo3-boa's bytearray only converts with utf-8 encoding
        string = 'string value'
        result = self.run_smart_contract(engine, path, 'main', string, expected_result_type=bytearray)
        self.assertEqual(bytearray(string, 'utf-8'), result)

        string = 'áãõ😀'
        result = self.run_smart_contract(engine, path, 'main', string, expected_result_type=bytearray)
        self.assertEqual(bytearray(string, 'utf-8'), result)

    def test_byte_array_string_with_encoding(self):
        path = self.get_contract_path('BytearrayFromStringWithEncoding.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_byte_array_append(self):
        path = self.get_contract_path('BytearrayAppend.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_append_with_builtin(self):
        path = self.get_contract_path('BytearrayAppendWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_append_mutable_sequence_with_builtin(self):
        path = self.get_contract_path('BytearrayAppendWithMutableSequence.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_clear(self):
        path = self.get_contract_path('BytearrayClear.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'', result)

    def test_byte_array_reverse(self):
        path = self.get_contract_path('BytearrayReverse.py')
        Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x03\x02\x01', result)

    def test_byte_array_extend(self):
        path = self.get_contract_path('BytearrayExtend.py')
        Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04\x05\x06', result)

    def test_byte_array_extend_with_builtin(self):
        path = self.get_contract_path('BytearrayExtendWithBuiltin.py')
        Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04\x05\x06', result)

    def test_byte_array_to_int(self):
        path = self.get_contract_path('BytearrayToInt.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_byte_array_to_int_with_builtin(self):
        path = self.get_contract_path('BytearrayToIntWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_byte_array_to_int_with_bytes_builtin(self):
        path = self.get_contract_path('BytearrayToIntWithBytesBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_boa2_byte_array_test(self):
        path = self.get_contract_path('BytearrayBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\t\x01\x02', result)

    def test_boa2_byte_array_test2(self):
        path = self.get_contract_path('BytearrayBoa2Test2.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_boa2_byte_array_test3(self):
        path = self.get_contract_path('BytearrayBoa2Test3.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(b'\x01\x02\xaa\xfe', result)

    def test_boa2_slice_test(self):
        path = self.get_contract_path('SliceBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_boa2_slice_test2(self):
        path = self.get_contract_path('SliceBoa2Test2.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x02\x03\x04\x02\x03\x04\x05\x06\x01\x02\x03\x04\x03\x04', result)

    def test_uint160_bytes(self):
        path = self.get_contract_path('UInt160Bytes.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        if isinstance(result, str):
            from boa3.neo.vm.type.String import String
            result = String(result).to_bytes()
        self.assertEqual(b'0123456789abcdefghij', result)

    def test_uint160_int(self):
        path = self.get_contract_path('UInt160Int.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        if isinstance(result, str):
            from boa3.neo.vm.type.String import String
            result = String(result).to_bytes()
        self.assertEqual((160).to_bytes(2, 'little') + bytes(18), result)

    def test_uint256_bytes(self):
        path = self.get_contract_path('UInt256Bytes.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(b'0123456789abcdefghijklmnopqrstuv', result)

    def test_uint256_int(self):
        path = self.get_contract_path('UInt256Int.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual((256).to_bytes(2, 'little') + bytes(30), result)

    def test_bytes_upper(self):
        path = self.get_contract_path('UpperBytesMethod.py')
        engine = TestEngine()

        bytes_value = b'abcdefghijklmnopqrstuvwxyz'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, expected_result_type=bytes)
        self.assertEqual(bytes_value.upper(), result)

        bytes_value = b'a1b123y3z'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, expected_result_type=bytes)
        self.assertEqual(bytes_value.upper(), result)

        bytes_value = b'!@#$%123*-/'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, expected_result_type=bytes)
        self.assertEqual(bytes_value.upper(), result)

    def test_bytes_lower(self):
        path = self.get_contract_path('LowerBytesMethod.py')
        engine = TestEngine()

        bytes_value = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, expected_result_type=bytes)
        self.assertEqual(bytes_value.lower(), result)

        bytes_value = b'A1B123Y3Z'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, expected_result_type=bytes)
        self.assertEqual(bytes_value.lower(), result)

        bytes_value = b'!@#$%123*-/'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, expected_result_type=bytes)
        self.assertEqual(bytes_value.lower(), result)

    def test_bytes_startswith_method(self):
        path = self.get_contract_path('StartswithBytesMethod.py')
        engine = TestEngine()

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 0
        end = len(bytes_value)
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start, end)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 2
        end = 6
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start, end)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        end = 6
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start, end)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        end = 3
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start, end)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_tes'
        start = -99
        end = -1
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start, end)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 0
        end = 0
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start, end)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        start = 0
        end = 99
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start, end)
        self.assertEqual(bytes_value.startswith(subbytes_value, start, end), result)

    def test_bytes_startswith_method_default_end(self):
        path = self.get_contract_path('StartswithBytesMethodDefaultEnd.py')
        engine = TestEngine()

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 0
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 2
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 3
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_tes'
        start = -99
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 0
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 99
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        start = 0
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value, start)
        self.assertEqual(bytes_value.startswith(subbytes_value, start), result)

    def test_bytes_startswith_method_defaults(self):
        path = self.get_contract_path('StartswithBytesMethodDefaults.py')
        engine = TestEngine()

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

        bytes_value = b'unit_test'
        subbytes_value = b''
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

        bytes_value = b'unit_test'
        subbytes_value = b'12345'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

        bytes_value = b'unit_test'
        subbytes_value = b'bigger subbytes_value'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, subbytes_value)
        self.assertEqual(bytes_value.startswith(subbytes_value), result)

    def test_bytes_strip(self):
        path = self.get_contract_path('StripBytesMethod.py')
        engine = TestEngine()

        bytes_value = b'abcdefghijklmnopqrstuvwxyz'
        sub_bytes = b'abcxyz'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, sub_bytes,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.strip(sub_bytes), result)

        bytes_value = b'abcdefghijklmnopqrsvwxyz unit test abcdefghijklmnopqrsvwxyz'
        sub_bytes = b'abcdefghijklmnopqrsvwxyz '
        result = self.run_smart_contract(engine, path, 'main', bytes_value, sub_bytes,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.strip(sub_bytes), result)

        bytes_value = b'0123456789hello world987654310'
        sub_bytes = b'0987654321'
        result = self.run_smart_contract(engine, path, 'main', bytes_value, sub_bytes,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.strip(sub_bytes), result)

    def test_bytes_strip_default(self):
        path = self.get_contract_path('StripBytesMethodDefault.py')
        engine = TestEngine()

        bytes_value = b'     unit test    '
        result = self.run_smart_contract(engine, path, 'main', bytes_value,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.strip(), result)

        bytes_value = b'unit test    '
        result = self.run_smart_contract(engine, path, 'main', bytes_value,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.strip(), result)

        bytes_value = b'    unit test'
        result = self.run_smart_contract(engine, path, 'main', bytes_value,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.strip(), result)

        bytes_value = b' \t\n\r\f\vunit test \t\n\r\f\v'
        result = self.run_smart_contract(engine, path, 'main', bytes_value,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.strip(), result)

    def test_isdigit_method(self):
        path = self.get_contract_path('IsdigitMethod.py')
        engine = TestEngine()

        bytes_value = b'0123456789'
        result = self.run_smart_contract(engine, path, 'main', bytes_value)
        self.assertEqual(bytes_value.isdigit(), result)

        bytes_value = b'23mixed01'
        result = self.run_smart_contract(engine, path, 'main', bytes_value)
        self.assertEqual(bytes_value.isdigit(), result)

        bytes_value = b'no digits here'
        result = self.run_smart_contract(engine, path, 'main', bytes_value)
        self.assertEqual(bytes_value.isdigit(), result)

        bytes_value = b''
        result = self.run_smart_contract(engine, path, 'main', bytes_value)
        self.assertEqual(bytes_value.isdigit(), result)

    def test_bytes_join_with_sequence(self):
        path = self.get_contract_path('JoinBytesMethodWithSequence.py')
        engine = TestEngine()

        bytes_value = b' '
        sequence = [b"Unit", b"Test", b"Neo3-boa"]
        result = self.run_smart_contract(engine, path, 'main', bytes_value, sequence,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.join(sequence), result)

        bytes_value = b' '
        sequence = []
        result = self.run_smart_contract(engine, path, 'main', bytes_value, sequence,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.join(sequence), result)

        bytes_value = b' '
        sequence = [b"UnitTest"]
        result = self.run_smart_contract(engine, path, 'main', bytes_value, sequence,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.join(sequence), result)

    def test_bytes_join_with_dictionary(self):
        path = self.get_contract_path('JoinBytesMethodWithDictionary.py')
        engine = TestEngine()

        bytes_value = b' '
        dictionary = {b"Unit": 1, b"Test": 2, b"Neo3-boa": 3}
        result = self.run_smart_contract(engine, path, 'main', bytes_value, dictionary,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.join(dictionary), result)

        bytes_value = b' '
        dictionary = {}
        result = self.run_smart_contract(engine, path, 'main', bytes_value, dictionary,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.join(dictionary), result)

        bytes_value = b' '
        dictionary = {b"UnitTest": 1}
        result = self.run_smart_contract(engine, path, 'main', bytes_value, dictionary,
                                         expected_result_type=bytes)
        self.assertEqual(bytes_value.join(dictionary), result)

    def test_bytes_index(self):
        path = self.get_contract_path('IndexBytes.py')
        engine = TestEngine()

        bytes_ = b'unit test'
        subsequence = b'i'
        start = 0
        end = 4
        result = self.run_smart_contract(engine, path, 'main', bytes_, subsequence, start, end)
        self.assertEqual(bytes_.index(subsequence, start, end), result)

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = 2
        end = 4
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence, start, end)
        self.assertEqual(bytes_.index(bytes_sequence, start, end), result)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 'i', 3, 4)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 'i', 4, -1)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 'i', 0, -99)

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = 0
        end = -1
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence, start, end)
        self.assertEqual(bytes_.index(bytes_sequence, start, end), result)

        bytes_ = b'unit test'
        bytes_sequence = b'n'
        start = 0
        end = 99
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence, start, end)
        self.assertEqual(bytes_.index(bytes_sequence, start, end), result)

    def test_bytes_index_end_default(self):
        path = self.get_contract_path('IndexBytesEndDefault.py')
        engine = TestEngine()

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 0
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence, start)
        self.assertEqual(bytes_.index(bytes_sequence, start), result)

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 4
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence, start)
        self.assertEqual(bytes_.index(bytes_sequence, start), result)

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 6
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence, start)
        self.assertEqual(bytes_.index(bytes_sequence, start), result)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 'i', 99)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 't', -1)

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = -10
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence, start)
        self.assertEqual(bytes_.index(bytes_sequence, start), result)

    def test_bytes_index_defaults(self):
        path = self.get_contract_path('IndexBytesDefaults.py')
        engine = TestEngine()

        bytes_ = b'unit test'
        bytes_sequence = b'u'
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence)
        self.assertEqual(bytes_.index(bytes_sequence), result)

        bytes_ = b'unit test'
        bytes_sequence = b't'
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence)
        self.assertEqual(bytes_.index(bytes_sequence), result)

        bytes_ = b'unit test'
        bytes_sequence = b' '
        result = self.run_smart_contract(engine, path, 'main', bytes_, bytes_sequence)
        self.assertEqual(bytes_.index(bytes_sequence), result)

    def test_bytes_index_mismatched_type(self):
        path = self.get_contract_path('IndexBytesMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
