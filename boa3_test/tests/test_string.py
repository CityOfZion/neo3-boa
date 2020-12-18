import unittest

from boa3.boa3 import Boa3
from boa3.exception.CompilerError import InternalError, UnresolvedOperation
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestString(BoaTest):

    def test_string_get_value(self):
        path = '%s/boa3_test/test_sc/string_test/GetValue.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'unit')
        self.assertEqual('u', result)
        result = self.run_smart_contract(engine, path, 'Main', '123')
        self.assertEqual('1', result)

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', '')

    def test_string_get_value_to_variable(self):
        path = '%s/boa3_test/test_sc/string_test/GetValueToVariable.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'unit')
        self.assertEqual('u', result)
        result = self.run_smart_contract(engine, path, 'Main', '123')
        self.assertEqual('1', result)

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', '')

    def test_string_set_value(self):
        path = '%s/boa3_test/test_sc/string_test/SetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_string_slicing(self):
        path = '%s/boa3_test/test_sc/string_test/StringSlicingLiteralValues.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('i', result)

    def test_string_slicing_with_variables(self):
        path = '%s/boa3_test/test_sc/string_test/StringSlicingVariableValues.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('i', result)

    def test_string_slicing_negative_start(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # return a[:-4]
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.PUSH4            # size of the substring: len(a) - 4
            + Opcode.NEGATE
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.LEFT
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingNegativeStart.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'unit_', result)

    @unittest.skip("slicing with negative arg is wrong")
    def test_string_slicing_negative_end(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # return a[-4:]
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.DUP            # size of the substring: len(a) - (len(a) - 4) = 4
            + Opcode.SIZE
            + Opcode.PUSH4
            + Opcode.NEGATE
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.SUB
            + Opcode.RIGHT
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingNegativeEnd.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(b'test', result)

    def test_string_slicing_start_omitted(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # return a[:3]
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.PUSH3            # size of the substring: 3
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.LEFT
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingStartOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'uni', result)

    def test_string_slicing_omitted(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # return a[:3]
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('unit_test', result)

    def test_string_slicing_end_omitted(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # return a[2:]
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.DUP            # size of the substring: len(a) - 2
            + Opcode.SIZE
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.SUB
            + Opcode.RIGHT
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingEndOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'it_test', result)

    def test_string_slicing_omitted_stride(self):
        path = '%s/boa3_test/test_sc/string_test/StringSlicingWithStride.py' % self.dirname
        self.assertCompilerLogs(InternalError, path)

    def test_string_slicing_omitted_with_stride(self):
        path = '%s/boa3_test/test_sc/string_test/StringSlicingOmittedWithStride.py' % self.dirname
        self.assertCompilerLogs(InternalError, path)
