import unittest

from boa3.boa3 import Boa3
from boa3.exception import CompilerError, CompilerWarning
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBytes(BoaTest):

    default_folder: str = 'test_sc/bytes_test'

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
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_bytes_to_int_with_builtin(self):
        path = self.get_contract_path('BytesToIntWithBuiltin.py')
        output = Boa3.compile(path)

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
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x00')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x01')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x02')
        self.assertEqual(True, result)

    def test_bytes_to_bool_with_builtin(self):
        path = self.get_contract_path('BytesToBoolWithBuiltin.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x00')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x01')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x02')
        self.assertEqual(True, result)

    def test_bytes_to_bool_with_builtin_hard_coded_false(self):
        path = self.get_contract_path('BytesToBoolWithBuiltinHardCodedFalse.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_bool', expected_result_type=bool)
        self.assertEqual(False, result)

    def test_bytes_to_bool_with_builtin_hard_coded_true(self):
        path = self.get_contract_path('BytesToBoolWithBuiltinHardCodedTrue.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_bool')
        self.assertEqual(True, result)

    def test_bytes_to_bool_mismatched_types(self):
        path = self.get_contract_path('BytesToBoolWithBuiltinMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_to_str(self):
        path = self.get_contract_path('BytesToStr.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_str')
        self.assertEqual('abc', result)

    def test_bytes_to_str_with_builtin(self):
        path = self.get_contract_path('BytesToStrWithBuiltin.py')
        output = Boa3.compile(path)

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

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'main', bytearray())

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

    @unittest.skip("bytestring setitem is not working yet")
    def test_byte_array_set_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0] = 0x01
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
            + Opcode.LDARG0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearraySetValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', b'123')
        self.assertEqual(b'\x0123', result)
        result = self.run_smart_contract(engine, path, 'Main', b'0')
        self.assertEqual(b'\x01', result)

    @unittest.skip("bytestring setitem is not working yet")
    def test_byte_array_set_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[-1] = 0x01
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
            + Opcode.LDARG0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearraySetValueNegativeIndex.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', b'123')
        self.assertEqual(b'12\x01', result)
        result = self.run_smart_contract(engine, path, 'Main', b'0')
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

    def test_byte_array_from_literal_bytes(self):
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
            + Opcode.STLOC1
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayFromVariableBytes.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_string(self):
        path = self.get_contract_path('BytearrayFromString.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_byte_array_append(self):
        path = self.get_contract_path('BytearrayAppend.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_append_with_builtin(self):
        path = self.get_contract_path('BytearrayAppendWithBuiltin.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_append_mutable_sequence_with_builtin(self):
        path = self.get_contract_path('BytearrayAppendWithMutableSequence.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_clear(self):
        path = self.get_contract_path('BytearrayClear.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'', result)

    @unittest.skip("reverse items doesn't work with bytestring")
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
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_byte_array_to_int_with_builtin(self):
        path = self.get_contract_path('BytearrayToIntWithBuiltin.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_byte_array_to_int_with_bytes_builtin(self):
        path = self.get_contract_path('BytearrayToIntWithBytesBuiltin.py')
        output = Boa3.compile(path)

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
        self.compile_and_save(path)
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
