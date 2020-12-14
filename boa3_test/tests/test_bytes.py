import unittest

from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation, UnresolvedOperation
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBytes(BoaTest):

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
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/bytes_test/BytesLiteral.py' % self.dirname
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

        path = '%s/boa3_test/test_sc/bytes_test/BytesGetValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/test_sc/bytes_test/BytesGetValueNegativeIndex.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', bytes([1, 2, 3]))
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'Main', b'0')
        self.assertEqual(48, result)

    def test_bytes_set_value(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesSetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_bytes_clear(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesClear.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_bytes_reverse(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesReverse.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_bytes_to_int(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToInt.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_bytes_to_int_with_builtin(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToIntWithBuiltin.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_bytes_to_int_mismatched_types(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToIntWithBuiltinMismatchedTypes.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_bytes_to_int_with_byte_array_builtin(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToIntWithBytearrayBuiltin.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_bytes_to_bool(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToBool.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x00')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x01')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x02')
        self.assertEqual(True, result)

    def test_bytes_to_bool_with_builtin(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToBoolWithBuiltin.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x00')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x01')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'bytes_to_bool', b'\x02')
        self.assertEqual(True, result)

    @unittest.skip("It is converting hardcoded b'\x00' to b''")
    def test_bytes_to_bool_with_builtin_hard_coded_false(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToBoolWithBuiltinHardCodedFalse.py' % self.dirname
        output = Boa3.compile(path)
        # TODO: Instead of converting to b'\x00', it is converting to b''. Change this test when it is fixed.

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_bool')
        self.assertEqual(False, result)

    def test_bytes_to_bool_with_builtin_hard_coded_true(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToBoolWithBuiltinHardCodedTrue.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_bool')
        self.assertEqual(True, result)

    def test_bytes_to_bool_mismatched_types(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToBoolWithBuiltinMismatchedTypes.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_bytes_to_str(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToStr.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_str')
        self.assertEqual('abc', result)

    def test_bytes_to_str_with_builtin(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToStrWithBuiltin.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_str')
        self.assertEqual('123', result)

    def test_bytes_to_str_mismatched_types(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytesToStrWithBuiltinMismatchedTypes.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

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
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/bytes_test/BytesFromBytearray.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_assign_with_slice(self):
        path = '%s/boa3_test/test_sc/bytes_test/AssignSlice.py' % self.dirname

        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/test_sc/bytes_test/BytearrayGetValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/test_sc/bytes_test/BytearrayGetValueNegativeIndex.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/test_sc/bytes_test/BytearraySetValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/test_sc/bytes_test/BytearraySetValueNegativeIndex.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', b'123')
        self.assertEqual(b'12\x01', result)
        result = self.run_smart_contract(engine, path, 'Main', b'0')
        self.assertEqual(b'\x01', result)

    def test_byte_array_literal_value(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayLiteral.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

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
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/bytes_test/BytearrayFromLiteralBytes.py' % self.dirname
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
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/bytes_test/BytearrayFromVariableBytes.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_string(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayFromString.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_byte_array_append(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayAppend.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_append_with_builtin(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayAppendWithBuiltin.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_append_mutable_sequence_with_builtin(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayAppendWithMutableSequence.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(b'\x01\x02\x03\x04', result)

    def test_byte_array_clear(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayClear.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(b'', result)

    def test_byte_array_reverse(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayReverse.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(b'\x03\x02\x01', result)

    def test_byte_array_extend(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayExtend.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_byte_array_to_int(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayToInt.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_byte_array_to_int_with_builtin(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayToIntWithBuiltin.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)

    def test_byte_array_to_int_with_bytes_builtin(self):
        path = '%s/boa3_test/test_sc/bytes_test/BytearrayToIntWithBytesBuiltin.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'bytes_to_int')
        self.assertEqual(513, result)
