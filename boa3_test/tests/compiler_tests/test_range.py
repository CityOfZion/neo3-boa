from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase
from boa3_test.tests.boatestcase import FaultException


class TestRange(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/range_test'

    RANGE_ERROR_MESSAGE = String('range() arg 3 must not be zero').to_bytes()

    def test_range_given_length_compile(self):
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

        output, _ = self.assertCompile('RangeGivenLen.py')
        self.assertEqual(expected_output, output)

    async def test_range_given_length(self):
        await self.set_up_contract('RangeGivenLen.py')

        result, _ = await self.call('range_example', [5], return_type=list)
        self.assertEqual(list(range(5)), result)
        result, _ = await self.call('range_example', [10], return_type=list)
        self.assertEqual(list(range(10)), result)
        result, _ = await self.call('range_example', [0], return_type=list)
        self.assertEqual(list(range(0)), result)

    def test_range_given_start_compile(self):
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

        output, _ = self.assertCompile('RangeGivenStart.py')
        self.assertEqual(expected_output, output)

    async def test_range_given_start(self):
        await self.set_up_contract('RangeGivenStart.py')

        result, _ = await self.call('range_example', [2, 6], return_type=list)
        self.assertEqual(list(range(2, 6)), result)
        result, _ = await self.call('range_example', [-10, 0], return_type=list)
        self.assertEqual(list(range(-10, 0)), result)

    def test_range_given_step_compile(self):
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

        output, _ = self.assertCompile('RangeGivenStep.py')
        self.assertEqual(expected_output, output)

    async def test_range_given_step(self):
        await self.set_up_contract('RangeGivenStep.py')

        result, _ = await self.call('range_example', [2, 10, 3], return_type=list)
        self.assertEqual(list(range(2, 10, 3)), result)
        result, _ = await self.call('range_example', [-2, 10, 3], return_type=list)
        self.assertEqual(list(range(-2, 10, 3)), result)

    def test_range_parameter_mismatched_type(self):
        path = self.get_contract_path('RangeParameterMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_range_as_sequence_compile(self):
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

        output, _ = self.assertCompile('RangeExpectedSequence.py')
        self.assertEqual(expected_output, output)

    async def test_range_as_sequence(self):
        await self.set_up_contract('RangeExpectedSequence.py')

        result, _ = await self.call('range_example', [2, 6], return_type=list)
        self.assertEqual(list(range(2, 6)), result)
        result, _ = await self.call('range_example', [-10, 0], return_type=list)
        self.assertEqual(list(range(-10, 0)), result)

    def test_range_mismatched_type(self):
        path = self.get_contract_path('RangeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_range_too_few_parameters(self):
        path = self.get_contract_path('RangeTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_range_too_many_parameters(self):
        path = self.get_contract_path('RangeTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_range_get_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('RangeGetValue.py')
        self.assertEqual(expected_output, output)

    async def test_range_get_value(self):
        await self.set_up_contract('RangeGetValue.py')

        result, _ = await self.call('Main', [[1, 2, 3, 4]], return_type=int)
        self.assertEqual(1, result)
        result, _ = await self.call('Main', [[5, 3, 2]], return_type=int)
        self.assertEqual(5, result)

        with self.assertRaises(FaultException) as context:
            await self.call('Main', [[]], return_type=int)

        self.assertRegex(str(context.exception), r'The value \d+ is out of range.')

    def test_range_set_value(self):
        path = self.get_contract_path('RangeSetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    async def test_range_slicing(self):
        await self.set_up_contract('RangeSlicingLiteralValues.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([2], result)

    async def test_range_slicing_start_larger_than_ending(self):
        await self.set_up_contract('RangeSlicingStartLargerThanEnding.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([], result)

    async def test_range_slicing_with_variables(self):
        await self.set_up_contract('RangeSlicingVariableValues.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([2], result)

    async def test_range_slicing_negative_start(self):
        await self.set_up_contract('RangeSlicingNegativeStart.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([2, 3, 4, 5], result)

    async def test_range_slicing_negative_end(self):
        await self.set_up_contract('RangeSlicingNegativeEnd.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([0, 1], result)

    async def test_range_slicing_start_omitted(self):
        await self.set_up_contract('RangeSlicingStartOmitted.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([0, 1, 2], result)

    async def test_range_slicing_omitted(self):
        await self.set_up_contract('RangeSlicingOmitted.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([0, 1, 2, 3, 4, 5], result)

    async def test_range_slicing_end_omitted(self):
        await self.set_up_contract('RangeSlicingEndOmitted.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([2, 3, 4, 5], result)

    async def test_range_slicing_with_stride(self):
        await self.set_up_contract('RangeSlicingWithStride.py')

        a = range(6)
        expected_result = a[2:5:2]
        result, _ = await self.call('literal_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[2:5:2]
        result, _ = await self.call('literal_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6:5:2]
        result, _ = await self.call('negative_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:-1:2]
        result, _ = await self.call('negative_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6:-1:2]
        result, _ = await self.call('negative_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999:5:2]
        result, _ = await self.call('negative_really_low_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:-999:2]
        result, _ = await self.call('negative_really_low_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999:-999:2]
        result, _ = await self.call('negative_really_low_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999:5:2]
        result, _ = await self.call('really_high_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:999:2]
        result, _ = await self.call('really_high_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999:999:2]
        result, _ = await self.call('really_high_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

    async def test_range_slicing_with_negative_stride(self):
        await self.set_up_contract('RangeSlicingWithNegativeStride.py')

        a = range(6)
        expected_result = a[2:5:-1]
        result, _ = await self.call('literal_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6:5:-1]
        result, _ = await self.call('negative_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:-1:-1]
        result, _ = await self.call('negative_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6:-1:-1]
        result, _ = await self.call('negative_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999:5:-1]
        result, _ = await self.call('negative_really_low_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:-999:-1]
        result, _ = await self.call('negative_really_low_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999:-999:-1]
        result, _ = await self.call('negative_really_low_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999:5:-1]
        result, _ = await self.call('really_high_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[0:999:-1]
        result, _ = await self.call('really_high_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999:999:-1]
        result, _ = await self.call('really_high_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

    async def test_range_slicing_omitted_with_stride(self):
        await self.set_up_contract('RangeSlicingOmittedWithStride.py')

        a = range(6)
        expected_result = a[::2]
        result, _ = await self.call('omitted_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:5:2]
        result, _ = await self.call('omitted_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[2::2]
        result, _ = await self.call('omitted_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6::2]
        result, _ = await self.call('negative_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:-1:2]
        result, _ = await self.call('negative_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999::2]
        result, _ = await self.call('negative_really_low_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:-999:2]
        result, _ = await self.call('negative_really_low_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999::2]
        result, _ = await self.call('really_high_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:999:2]
        result, _ = await self.call('really_high_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

    async def test_range_slicing_omitted_with_negative_stride(self):
        await self.set_up_contract('RangeSlicingOmittedWithNegativeStride.py')

        a = range(6)
        expected_result = a[::-2]
        result, _ = await self.call('omitted_values', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:5:-2]
        result, _ = await self.call('omitted_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[2::-2]
        result, _ = await self.call('omitted_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-6::-2]
        result, _ = await self.call('negative_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:-1:-2]
        result, _ = await self.call('negative_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[-999::-2]
        result, _ = await self.call('negative_really_low_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:-999:-2]
        result, _ = await self.call('negative_really_low_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[999::-2]
        result, _ = await self.call('really_high_start', [], return_type=list)
        self.assertEqual(list(expected_result), result)

        a = range(6)
        expected_result = a[:999:-2]
        result, _ = await self.call('really_high_end', [], return_type=list)
        self.assertEqual(list(expected_result), result)

    async def test_boa2_range_test(self):
        await self.set_up_contract('RangeBoa2Test.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(list(range(100, 120)), result)

    def test_range_index(self):
        path = self.get_contract_path('IndexRange.py')
        # TODO: change when index() with only one argument is implemented for range #2kq1y13
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)
