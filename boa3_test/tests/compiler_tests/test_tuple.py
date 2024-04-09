from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestTuple(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/tuple_test'

    VALUE_OUT_OF_RANGE_ERROR = r'The value \d+ is out of range'
    VALUE_NOT_IN_SEQUENCE_ERROR = r'\w+ not in sequence'

    def test_tuple_int_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = (1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('IntTuple.py')
        self.assertEqual(expected_output, output)

    def test_tuple_string_values(self):
        byte_input0 = String('1').to_bytes()
        byte_input1 = String('2').to_bytes()
        byte_input2 = String('3').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = ('1', '2', '3')
            + Integer(len(byte_input2)).to_byte_array()
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array()
            + byte_input0
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('StrTuple.py')
        self.assertEqual(expected_output, output)

    def test_tuple_bool_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHF      # a = (True, True, False)
            + Opcode.PUSHT
            + Opcode.PUSHT
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BoolTuple.py')
        self.assertEqual(expected_output, output)

    def test_tuple_variable_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH1      # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2      # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH3      # c = 3
            + Opcode.STLOC2
            + Opcode.PUSH3      # d = (a, b, c)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('VariableTuple.py')
        self.assertEqual(expected_output, output)

    def test_tuple_assign_empty_tuple(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.NEWARRAY0
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('EmptyTupleAssignment.py')
        self.assertEqual(expected_output, output)

    def test_tuple_get_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('TupleGetValue.py')
        self.assertEqual(expected_output, output)

    async def test_tuple_get_value_run(self):
        await self.set_up_contract('TupleGetValue.py')

        result, _ = await self.call('Main', [(1, 2, 3, 4)], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('Main', [(5, 3, 2)], return_type=int)
        self.assertEqual(5, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [()], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_OUT_OF_RANGE_ERROR)

    def test_non_sequence_get_value(self):
        path = self.get_contract_path('TupleGetValueMismatchedType.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_tuple_set_value(self):
        path = self.get_contract_path('TupleSetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_non_sequence_set_value(self):
        path = self.get_contract_path('SetValueMismatchedType.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_tuple_get_value_typed_tuple_compile(self):
        ok = String('ok').to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # x = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # x[1]
            + Opcode.PUSH1
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('TupleGetValueTypedTuple.py')
        self.assertEqual(expected_output, output)

    async def test_tuple_get_value_typed_tuple_run(self):
        await self.set_up_contract('TupleGetValueTypedTuple.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(1, result)

    def test_tuple_index_mismatched_type(self):
        path = self.get_contract_path('TupleIndexMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_tuple_of_tuple_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0][0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('TupleOfTuple.py')
        self.assertEqual(expected_output, output)

    async def test_tuple_of_tuple_run(self):
        await self.set_up_contract('TupleOfTuple.py')

        result, _ = await self.call('Main', [((1, 2), (3, 4))], return_type=int)
        self.assertEqual(1, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [()], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_OUT_OF_RANGE_ERROR)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [((), (1, 2), (3, 4))], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_OUT_OF_RANGE_ERROR)

    async def test_tuple_slicing(self):
        await self.set_up_contract('TupleSlicingLiteralValues.py')

        result, _ = await self.call('Main', [], return_type=tuple)
        self.assertEqual((2,), result)

    async def test_tuple_slicing_start_larger_than_ending(self):
        await self.set_up_contract('TupleSlicingStartLargerThanEnding.py')

        result, _ = await self.call('Main', [], return_type=tuple)
        self.assertEqual((), result)

    async def test_tuple_slicing_with_variables(self):
        await self.set_up_contract('TupleSlicingVariableValues.py')

        result, _ = await self.call('Main', [], return_type=tuple)
        self.assertEqual((2,), result)

    async def test_tuple_slicing_negative_start(self):
        await self.set_up_contract('TupleSlicingNegativeStart.py')

        result, _ = await self.call('Main', [], return_type=tuple)
        self.assertEqual((2, 3, 4, 5), result)

    async def test_tuple_slicing_negative_end(self):
        await self.set_up_contract('TupleSlicingNegativeEnd.py')

        result, _ = await self.call('Main', [], return_type=tuple)
        self.assertEqual((0, 1), result)

    async def test_tuple_slicing_start_omitted(self):
        await self.set_up_contract('TupleSlicingStartOmitted.py')

        result, _ = await self.call('Main', [], return_type=tuple)
        self.assertEqual((0, 1, 2), result)

    def test_tuple_slicing_omitted_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5      # a = (0, 1, 2, 3, 4, 5)
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:]
            + Opcode.UNPACK
            + Opcode.PACK
            + Opcode.RET        # return
        )
        output, _ = self.assertCompile('TupleSlicingOmitted.py')
        self.assertEqual(expected_output, output)

    async def test_tuple_slicing_omitted_run(self):
        await self.set_up_contract('TupleSlicingOmitted.py')

        result, _ = await self.call('Main', [], return_type=tuple)
        self.assertEqual((0, 1, 2, 3, 4, 5), result)

    async def test_tuple_slicing_end_omitted(self):
        await self.set_up_contract('TupleSlicingEndOmitted.py')

        result, _ = await self.call('Main', [], return_type=tuple)
        self.assertEqual((2, 3, 4, 5), result)

    async def test_tuple_slicing_with_stride(self):
        await self.set_up_contract('TupleSlicingWithStride.py')

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[2:5:2]
        result, _ = await self.call('literal_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6:5:2]
        result, _ = await self.call('negative_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:-1:2]
        result, _ = await self.call('negative_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6:-1:2]
        result, _ = await self.call('negative_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999:5:2]
        result, _ = await self.call('negative_really_low_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:-999:2]
        result, _ = await self.call('negative_really_low_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999:-999:2]
        result, _ = await self.call('negative_really_low_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999:5:2]
        result, _ = await self.call('really_high_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:999:2]
        result, _ = await self.call('really_high_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999:999:2]
        result, _ = await self.call('really_high_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

    async def test_tuple_slicing_with_negative_stride(self):
        await self.set_up_contract('TupleSlicingWithNegativeStride.py')

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[2:5:-1]
        result, _ = await self.call('literal_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6:5:-1]
        result, _ = await self.call('negative_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:-1:-1]
        result, _ = await self.call('negative_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6:-1:-1]
        result, _ = await self.call('negative_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999:5:-1]
        result, _ = await self.call('negative_really_low_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:-999:-1]
        result, _ = await self.call('negative_really_low_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999:-999:-1]
        result, _ = await self.call('negative_really_low_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999:5:-1]
        result, _ = await self.call('really_high_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:999:-1]
        result, _ = await self.call('really_high_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999:999:-1]
        result, _ = await self.call('really_high_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

    async def test_tuple_slicing_omitted_with_stride_run(self):
        await self.set_up_contract('TupleSlicingOmittedWithStride.py')

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[::2]
        result, _ = await self.call('omitted_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:5:2]
        result, _ = await self.call('omitted_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[2::2]
        result, _ = await self.call('omitted_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6::2]
        result, _ = await self.call('negative_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:-1:2]
        result, _ = await self.call('negative_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999::2]
        result, _ = await self.call('negative_really_low_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:-999:2]
        result, _ = await self.call('negative_really_low_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999::2]
        result, _ = await self.call('really_high_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:999:2]
        result, _ = await self.call('really_high_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

    async def test_tuple_slicing_omitted_with_negative_stride(self):
        await self.set_up_contract('TupleSlicingOmittedWithNegativeStride.py')

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[::-2]
        result, _ = await self.call('omitted_values', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:5:-2]
        result, _ = await self.call('omitted_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[2::-2]
        result, _ = await self.call('omitted_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6::-2]
        result, _ = await self.call('negative_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:-1:-2]
        result, _ = await self.call('negative_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999::-2]
        result, _ = await self.call('negative_really_low_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:-999:-2]
        result, _ = await self.call('negative_really_low_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999::-2]
        result, _ = await self.call('really_high_start', [], return_type=tuple)
        self.assertEqual(expected_result, result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:999:-2]
        result, _ = await self.call('really_high_end', [], return_type=tuple)
        self.assertEqual(expected_result, result)

    async def test_tuple_index(self):
        await self.set_up_contract('IndexTuple.py')

        tuple_ = (1, 2, 3, 4)
        value = 3
        start = 0
        end = 4
        result, _ = await self.call('main', [tuple_, value, start, end], return_type=int)
        self.assertEqual(tuple_.index(value, start, end), result)

        tuple_ = (1, 2, 3, 4)
        value = 3
        start = 2
        end = 4
        result, _ = await self.call('main', [tuple_, value, start, end], return_type=int)
        self.assertEqual(tuple_.index(value, start, end), result)

        tuple_ = (1, 2, 3, 4)
        value = 3
        start = 0
        end = -1
        result, _ = await self.call('main', [tuple_, value, start, end], return_type=int)
        self.assertEqual(tuple_.index(value, start, end), result)

        tuple_ = (1, 2, 3, 4)
        value = 2
        start = 0
        end = 99
        result, _ = await self.call('main', [tuple_, value, start, end], return_type=int)
        self.assertEqual(tuple_.index(value, start, end), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [(1, 2, 3, 4), 3, 3, 4], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_NOT_IN_SEQUENCE_ERROR)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [(1, 2, 3, 4), 3, 4, -1], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_NOT_IN_SEQUENCE_ERROR)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [(1, 2, 3, 4), 3, 0, -99], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_NOT_IN_SEQUENCE_ERROR)

    async def test_tuple_index_end_default(self):
        await self.set_up_contract('IndexTupleEndDefault.py')

        tuple_ = (1, 2, 3, 4)
        value = 3
        start = 0
        result, _ = await self.call('main', [tuple_, value, start], return_type=int)
        self.assertEqual(tuple_.index(value, start), result)

        tuple_ = (1, 2, 3, 4)
        value = 2
        start = -10
        result, _ = await self.call('main', [tuple_, value, start], return_type=int)
        self.assertEqual(tuple_.index(value, start), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [(1, 2, 3, 4), 2, 99], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_NOT_IN_SEQUENCE_ERROR)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [(1, 2, 3, 4), 4, -1], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_NOT_IN_SEQUENCE_ERROR)

    async def test_tuple_index_defaults(self):
        await self.set_up_contract('IndexTupleDefaults.py')

        tuple_ = (1, 2, 3, 4)
        value = 3
        result, _ = await self.call('main', [tuple_, value], return_type=int)
        self.assertEqual(tuple_.index(value), result)

        tuple_ = (1, 2, 3, 4)
        value = 1
        result, _ = await self.call('main', [tuple_, value], return_type=int)
        self.assertEqual(tuple_.index(value), result)
