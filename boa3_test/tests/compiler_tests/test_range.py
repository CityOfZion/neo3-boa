from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestRange(BoaTest):

    default_folder: str = 'test_sc/range_test'

    RANGE_ERROR_MESSAGE = String('range() arg 3 must not be zero').to_bytes()

    def test_range_given_length(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.PUSH1      # range(arg0)
            + Opcode.PUSH0
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = self.get_contract_path('RangeGivenLen.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'range_example', 5)
        self.assertEqual([0, 1, 2, 3, 4], result)
        result = self.run_smart_contract(engine, path, 'range_example', 10)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], result)
        result = self.run_smart_contract(engine, path, 'range_example', 0)
        self.assertEqual([], result)

    def test_range_given_start(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH1      # range(arg0, arg1)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = self.get_contract_path('RangeGivenStart.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'range_example', 2, 6)
        self.assertEqual([2, 3, 4, 5], result)
        result = self.run_smart_contract(engine, path, 'range_example', -10, 0)
        self.assertEqual([-10, -9, -8, -7, -6, -5, -4, -3, -2, -1], result)

    def test_range_given_step(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG2     # range(arg0, arg1, arg2)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = self.get_contract_path('RangeGivenStep.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'range_example', 2, 10, 3)
        self.assertEqual([2, 5, 8], result)
        result = self.run_smart_contract(engine, path, 'range_example', -2, 10, 3)
        self.assertEqual([-2, 1, 4, 7], result)

    def test_range_parameter_mismatched_type(self):
        path = self.get_contract_path('RangeParameterMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_range_as_sequence(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH1      # range(arg0, arg1)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = self.get_contract_path('RangeExpectedSequence.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'range_example', 2, 6)
        self.assertEqual([2, 3, 4, 5], result)
        result = self.run_smart_contract(engine, path, 'range_example', -10, 0)
        self.assertEqual([-10, -9, -8, -7, -6, -5, -4, -3, -2, -1], result)

    def test_range_mismatched_type(self):
        path = self.get_contract_path('RangeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_range_too_few_parameters(self):
        path = self.get_contract_path('RangeTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_range_too_many_parameters(self):
        path = self.get_contract_path('RangeTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_range_get_value(self):
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

        path = self.get_contract_path('GetValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3, 4])
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', [5, 3, 2])
        self.assertEqual(5, result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', [])

    def test_range_set_value(self):
        path = self.get_contract_path('SetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_range_slicing(self):
        path = self.get_contract_path('RangeSlicingLiteralValues.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2], result)

    def test_range_slicing_start_larger_than_ending(self):
        path = self.get_contract_path('RangeSlicingStartLargerThanEnding.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_range_slicing_with_variables(self):
        path = self.get_contract_path('RangeSlicingVariableValues.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2], result)

    def test_range_slicing_negative_start(self):
        path = self.get_contract_path('RangeSlicingNegativeStart.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2, 3, 4, 5], result)

    def test_range_slicing_negative_end(self):
        path = self.get_contract_path('RangeSlicingNegativeEnd.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1], result)

    def test_range_slicing_start_omitted(self):
        path = self.get_contract_path('RangeSlicingStartOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1, 2], result)

    def test_range_slicing_omitted(self):
        path = self.get_contract_path('RangeSlicingOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1, 2, 3, 4, 5], result)

    def test_range_slicing_end_omitted(self):
        path = self.get_contract_path('RangeSlicingEndOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2, 3, 4, 5], result)

    def test_range_slicing_with_stride(self):
        path = self.get_contract_path('RangeSlicingWithStride.py')
        engine = TestEngine()

        a = range(6)
        expected_result = a[2:5:2]
        result = self.run_smart_contract(engine, path, 'literal_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[2:5:2]
        result = self.run_smart_contract(engine, path, 'literal_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6:5:2]
        result = self.run_smart_contract(engine, path, 'negative_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999:5:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999:5:2]
        result = self.run_smart_contract(engine, path, 'really_high_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_values')
        self.assertEqual(list(expected_result), result)

    def test_range_slicing_with_negative_stride(self):
        path = self.get_contract_path('RangeSlicingWithNegativeStride.py')
        engine = TestEngine()

        a = range(6)
        expected_result = a[2:5:-1]
        result = self.run_smart_contract(engine, path, 'literal_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6:5:-1]
        result = self.run_smart_contract(engine, path, 'negative_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:-1:-1]
        result = self.run_smart_contract(engine, path, 'negative_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6:-1:-1]
        result = self.run_smart_contract(engine, path, 'negative_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999:5:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:-999:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999:-999:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999:5:-1]
        result = self.run_smart_contract(engine, path, 'really_high_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:999:-1]
        result = self.run_smart_contract(engine, path, 'really_high_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999:999:-1]
        result = self.run_smart_contract(engine, path, 'really_high_values')
        self.assertEqual(list(expected_result), result)

    def test_range_slicing_omitted_with_stride(self):
        path = self.get_contract_path('RangeSlicingOmittedWithStride.py')
        engine = TestEngine()

        a = range(6)
        expected_result = a[::2]
        result = self.run_smart_contract(engine, path, 'omitted_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:5:2]
        result = self.run_smart_contract(engine, path, 'omitted_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[2::2]
        result = self.run_smart_contract(engine, path, 'omitted_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6::2]
        result = self.run_smart_contract(engine, path, 'negative_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999::2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999::2]
        result = self.run_smart_contract(engine, path, 'really_high_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_end')
        self.assertEqual(list(expected_result), result)

    def test_range_slicing_omitted_with_negative_stride(self):
        path = self.get_contract_path('RangeSlicingOmittedWithNegativeStride.py')
        engine = TestEngine()

        a = range(6)
        expected_result = a[::-2]
        result = self.run_smart_contract(engine, path, 'omitted_values')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:5:-2]
        result = self.run_smart_contract(engine, path, 'omitted_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[2::-2]
        result = self.run_smart_contract(engine, path, 'omitted_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6::-2]
        result = self.run_smart_contract(engine, path, 'negative_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:-1:-2]
        result = self.run_smart_contract(engine, path, 'negative_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999::-2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:-999:-2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999::-2]
        result = self.run_smart_contract(engine, path, 'really_high_start')
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:999:-2]
        result = self.run_smart_contract(engine, path, 'really_high_end')
        self.assertEqual(list(expected_result), result)

    def test_boa2_range_test(self):
        path = self.get_contract_path('RangeBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(list(range(100, 120)), result)
