from boa3.boa3 import Boa3
from boa3.exception.CompilerError import InternalError, UnresolvedOperation
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestString(BoaTest):

    default_folder: str = 'test_sc/string_test'

    def test_string_get_value(self):
        path = self.get_contract_path('GetValue.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'unit')
        self.assertEqual('u', result)
        result = self.run_smart_contract(engine, path, 'Main', '123')
        self.assertEqual('1', result)

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', '')

    def test_string_get_value_to_variable(self):
        path = self.get_contract_path('GetValueToVariable.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'unit')
        self.assertEqual('u', result)
        result = self.run_smart_contract(engine, path, 'Main', '123')
        self.assertEqual('1', result)

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', '')

    def test_string_set_value(self):
        path = self.get_contract_path('SetValue.py')
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_string_slicing(self):
        path = self.get_contract_path('StringSlicingLiteralValues.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('i', result)

    def test_string_slicing_start_larger_than_ending(self):
        path = self.get_contract_path('StringSlicingStartLargerThanEnding.py')
        self.compile_and_save(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('', result)

    def test_string_slicing_with_variables(self):
        path = self.get_contract_path('StringSlicingVariableValues.py')

        engine = TestEngine()
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
        path = self.get_contract_path('StringSlicingNegativeStart.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'unit_', result)

    def test_string_slicing_negative_end_omitted(self):
        path = self.get_contract_path('StringSlicingNegativeEndOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('test', result)

    def test_string_slicing_start_omitted(self):
        path = self.get_contract_path('StringSlicingStartOmitted.py')

        engine = TestEngine()
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
        path = self.get_contract_path('StringSlicingOmitted.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('unit_test', result)

    def test_string_slicing_end_omitted(self):
        path = self.get_contract_path('StringSlicingEndOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'it_test', result)

    def test_string_slicing_omitted_stride(self):
        path = self.get_contract_path('StringSlicingWithStride.py')
        self.assertCompilerLogs(InternalError, path)

    def test_string_slicing_omitted_with_stride(self):
        path = self.get_contract_path('StringSlicingOmittedWithStride.py')
        self.assertCompilerLogs(InternalError, path)

    def test_string_simple_concat(self):
        path = self.get_contract_path('StringSimpleConcat.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual('bye worldhi', result)

    def test_boa2_string_concat_test(self):
        path = self.get_contract_path('ConcatBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual('helloworld', result)

    def test_boa2_string_concat_test2(self):
        path = self.get_contract_path('ConcatBoa2Test2.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['hello', 'world'])
        self.assertEqual('helloworld', result)

        result = self.run_smart_contract(engine, path, 'main', 'blah', ['hello', 'world'])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['blah'])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['hello', 'world', 'third'])
        self.assertEqual('helloworld', result)

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['1', 'neo'])
        self.assertEqual('1neo', result)

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['', 'neo'])
        self.assertEqual('neo', result)
