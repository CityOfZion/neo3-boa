from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests import boatestcase
from boa3_test.tests.boatestcase import FaultException
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestList(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/list_test'

    VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX = r'The value \-?\d+ is out of range.'
    INVALID_INDEX_MSG = 'invalid index'

    def test_list_int_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('IntList.py')
        self.assertEqual(expected_output, output)

    def test_list_string_values(self):
        byte_input0 = String('1').to_bytes()
        byte_input1 = String('2').to_bytes()
        byte_input2 = String('3').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = ['1', '2', '3']
            + Integer(len(byte_input2)).to_byte_array()  # '3'
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array()  # '2'
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array()  # '1'
            + byte_input0
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('StrList.py')
        self.assertEqual(expected_output, output)

    def test_list_bool_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHF      # a = [True, True, False]
            + Opcode.PUSHT
            + Opcode.PUSHT
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('BoolList.py')
        self.assertEqual(expected_output, output)

    def test_list_variable_values(self):
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
            + Opcode.PUSH3      # d = [a, b, c]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('VariableList.py')
        self.assertEqual(expected_output, output)

    def test_list_empty_dict(self):
        expected_output = (
            Opcode.NEWMAP      # return [{}]
            + Opcode.PUSH1      # array length
            + Opcode.PACK
            + Opcode.RET
        )

        output, _ = self.assertCompile('ListWithEmptyTypedDict.py')
        self.assertEqual(expected_output, output)

    def test_non_sequence_get_value(self):
        path = self.get_contract_path('MismatchedTypeListGetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_list_get_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('ListGetValue.py')
        self.assertEqual(expected_output, output)

    async def test_list_get_value(self):
        await self.set_up_contract('ListGetValue.py')

        result, _ = await self.call('Main', [[1, 2, 3, 4]], return_type=int)
        self.assertEqual(1, result)
        result, _ = await self.call('Main', [[5, 3, 2]], return_type=int)
        self.assertEqual(5, result)

        with self.assertRaises(FaultException) as context:
            await self.call('Main', [[]], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_list_get_value_with_negative_index_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[-1]
            + Opcode.PUSHM1

            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('ListGetValueNegativeIndex.py')
        self.assertEqual(expected_output, output)

    async def test_list_get_value_with_negative_index(self):
        await self.set_up_contract('ListGetValueNegativeIndex.py')

        result, _ = await self.call('Main', [[1, 2, 3, 4]], return_type=int)
        self.assertEqual(4, result)
        result, _ = await self.call('Main', [[5, 3, 2]], return_type=int)
        self.assertEqual(2, result)

        with self.assertRaises(FaultException) as context:
            await self.call('Main', [[]], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_list_get_value_with_variable_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK
            + Opcode.LDARG0     # [0, 1, 2, 3, 4, 5][arg]

            + Opcode.DUP        # will check if number is negative
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

        output, _ = self.assertCompile('ListGetValueWithVariable.py')
        self.assertEqual(expected_output, output)

    async def test_list_get_value_with_variable(self):
        await self.set_up_contract('ListGetValueWithVariable.py')

        result, _ = await self.call('main', [0], return_type=int)
        self.assertEqual(0, result)
        result, _ = await self.call('main', [2], return_type=int)
        self.assertEqual(2, result)

    def test_list_type_hint(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # list length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('ListTypeHintAssignment.py')
        self.assertEqual(expected_output, output)

    def test_list_assign_empty_list(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.NEWARRAY0
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('EmptyListAssignment.py')
        self.assertEqual(expected_output, output)

    def test_list_set_into_list_slice(self):
        path = self.get_contract_path('SetListIntoListSlice.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_list_set_value_compile(self):
        path = self.get_contract_path('ListSetValue.py')
        self.assertCompilerNotLogs(CompilerWarning.NameShadowing, path)

    async def test_list_set_value(self):
        await self.set_up_contract('ListSetValue.py')

        result, _ = await self.call('Main', [[1, 2, 3, 4]], return_type=list)
        self.assertEqual([1, 2, 3, 4], result)
        result, _ = await self.call('Main', [[5, 3, 2]], return_type=list)
        self.assertEqual([1, 3, 2], result)

        with self.assertRaises(FaultException) as context:
            await self.call('Main', [[]], return_type=list)

        self.assertRegex(str(context.exception), self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_list_set_value_with_negative_index_compile(self):
        path = self.get_contract_path('ListSetValueNegativeIndex.py')
        self.assertCompilerNotLogs(CompilerWarning.NameShadowing, path)

    async def test_list_set_value_with_negative_index(self):
        await self.set_up_contract('ListSetValueNegativeIndex.py')

        result, _ = await self.call('Main', [[1, 2, 3, 4]], return_type=list)
        self.assertEqual([1, 2, 3, 1], result)
        result, _ = await self.call('Main', [[5, 3, 2]], return_type=list)
        self.assertEqual([5, 3, 1], result)

        with self.assertRaises(FaultException) as context:
            await self.call('Main', [[]], return_type=list)

        self.assertRegex(str(context.exception), self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_non_sequence_set_value(self):
        path = self.get_contract_path('MismatchedTypeListSetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_list_index_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeListIndex.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_array_boa2_test1(self):
        await self.set_up_contract('ArrayBoa2Test1.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_boa2_array_test(self):
        await self.set_up_contract('ArrayBoa2Test.py')

        result, _ = await self.call('main', [0], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', [1], return_type=int)
        self.assertEqual(6, result)

        result, _ = await self.call('main', [2], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [4], return_type=int)
        self.assertEqual(8, result)

        result, _ = await self.call('main', [8], return_type=int)
        self.assertEqual(9, result)

    async def test_boa2_array_test2(self):
        await self.set_up_contract('ArrayBoa2Test2.py')

        result, _ = await self.call('main', [], return_type=bytes)
        self.assertEqual(b'\xa0', result)

    async def test_boa2_array_test3(self):
        await self.set_up_contract('ArrayBoa2Test3.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual([1, 2, 3], result)

    def test_list_of_list_compile(self):
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

        output, _ = self.assertCompile('ListOfList.py')
        self.assertEqual(expected_output, output)

    async def test_list_of_list(self):
        await self.set_up_contract('ListOfList.py')

        result, _ = await self.call('Main', [[[1, 2], [3, 4]]], return_type=int)
        self.assertEqual(1, result)

        with self.assertRaises(FaultException) as context:
            await self.call('Main', [[]], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

        with self.assertRaises(FaultException) as context:
            await self.call('Main', [[[], [1, 2], [3, 4]]], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    async def test_boa2_demo1(self):
        await self.set_up_contract('Demo1Boa2.py')

        result, _ = await self.call('main', ['add', 1, 3], return_type=int)
        self.assertEqual(7, result)

        result, _ = await self.call('main', ['add', 2, 3], return_type=int)
        self.assertEqual(8, result)

    # region TestSlicing

    async def test_list_slicing(self):
        await self.set_up_contract('ListSlicingLiteralValues.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([2], result)

    async def test_list_slicing_start_larger_than_ending(self):
        await self.set_up_contract('ListSlicingStartLargerThanEnding.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([], result)

    async def test_list_slicing_with_variables(self):
        await self.set_up_contract('ListSlicingVariableValues.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([2], result)

    async def test_list_slicing_negative_start(self):
        await self.set_up_contract('ListSlicingNegativeStart.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([2, 3, 4, 5], result)

    async def test_list_slicing_negative_end(self):
        await self.set_up_contract('ListSlicingNegativeEnd.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([0, 1], result)

    async def test_list_slicing_start_omitted(self):
        await self.set_up_contract('ListSlicingStartOmitted.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([0, 1, 2], result)

    async def test_list_slicing_omitted(self):
        await self.set_up_contract('ListSlicingOmitted.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([0, 1, 2, 3, 4, 5], result)

    async def test_list_slicing_end_omitted(self):
        await self.set_up_contract('ListSlicingEndOmitted.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([2, 3, 4, 5], result)

    def test_list_slicing_positive_index_opcode(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK  # [0, 1, 2, 3, 4, 5]
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.PUSH2  # lower index

            + Opcode.DUP  # checks if lower index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.PUSH3  # upper index

            + Opcode.OVER  # checks if upper index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.SWAP
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.SWAP
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.NEWARRAY0  # starts getting the subarray

        )
        path = self.get_contract_path('ListSlicingLiteralValues.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    def test_list_slicing_negative_lower_index_opcode(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK  # [0, 1, 2, 3, 4, 5]
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.PUSH4
            + Opcode.NEGATE  # lower index

            + Opcode.OVER   # fix negative index
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.DUP  # checks if lower index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.OVER
            + Opcode.SIZE  # upper index

            + Opcode.NEWARRAY0  # starts getting the subarray
        )
        path = self.get_contract_path('ListSlicingNegativeStart.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    def test_list_slicing_negative_upper_index_opcode(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK  # [0, 1, 2, 3, 4, 5]
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.PUSH4
            + Opcode.NEGATE  # upper index

            + Opcode.OVER  # fix negative index
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.DUP  # checks if upper index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.PUSH0  # lower index
            + Opcode.SWAP

            + Opcode.NEWARRAY0  # starts getting the subarray
        )
        path = self.get_contract_path('ListSlicingNegativeEnd.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    def test_list_slicing_variable_index_opcode(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK  # [0, 1, 2, 3, 4, 5]
            + Opcode.LDARG0  # lower index

            + Opcode.DUP     # checks if variable is negative
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)

            + Opcode.OVER  # fix negative index
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.DUP  # checks if lower index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.LDARG1  # upper index

            + Opcode.DUP  # checks if variable is negative
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(6).to_byte_array(min_length=1)

            + Opcode.PUSH2  # fix negative index
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.OVER  # checks if upper index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.SWAP
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.SWAP
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.NEWARRAY0  # starts getting the subarray
        )
        path = self.get_contract_path('ListSlicingWithVariables.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    async def test_list_slicing_with_stride(self):
        await self.set_up_contract('ListSlicingWithStride.py')

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[2:5:2]
        result, _ = await self.call('literal_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6:5:2]
        result, _ = await self.call('negative_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:-1:2]
        result, _ = await self.call('negative_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6:-1:2]
        result, _ = await self.call('negative_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999:5:2]
        result, _ = await self.call('negative_really_low_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:-999:2]
        result, _ = await self.call('negative_really_low_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999:-999:2]
        result, _ = await self.call('negative_really_low_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999:5:2]
        result, _ = await self.call('really_high_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:999:2]
        result, _ = await self.call('really_high_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999:999:2]
        result, _ = await self.call('really_high_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        x = 2
        y = 4
        expected_result = a[x:y:2]
        result, _ = await self.call('with_variables', [x, y], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_list_slicing_with_negative_stride(self):
        await self.set_up_contract('ListSlicingWithNegativeStride.py')

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[2:5:-1]
        result, _ = await self.call('literal_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6:5:-1]
        result, _ = await self.call('negative_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:-1:-1]
        result, _ = await self.call('negative_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6:-1:-1]
        result, _ = await self.call('negative_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999:5:-1]
        result, _ = await self.call('negative_really_low_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:-999:-1]
        result, _ = await self.call('negative_really_low_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999:-999:-1]
        result, _ = await self.call('negative_really_low_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999:5:-1]
        result, _ = await self.call('really_high_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:999:-1]
        result, _ = await self.call('really_high_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999:999:-1]
        result, _ = await self.call('really_high_values', [], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_list_slicing_omitted_with_stride(self):
        await self.set_up_contract('ListSlicingOmittedWithStride.py')

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[::2]
        result, _ = await self.call('omitted_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:5:2]
        result, _ = await self.call('omitted_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5, 6]
        expected_result = a[2::2]
        result, _ = await self.call('omitted_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6::2]
        result, _ = await self.call('negative_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:-1:2]
        result, _ = await self.call('negative_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999::2]
        result, _ = await self.call('negative_really_low_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:-999:2]
        result, _ = await self.call('negative_really_low_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999::2]
        result, _ = await self.call('really_high_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:999:2]
        result, _ = await self.call('really_high_end', [], return_type=list)
        self.assertEqual(expected_result, result)

    async def test_list_slicing_omitted_with_negative_stride(self):
        await self.set_up_contract('ListSlicingOmittedWithNegativeStride.py')

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[::-2]
        result, _ = await self.call('omitted_values', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:5:-2]
        result, _ = await self.call('omitted_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5, 6]
        expected_result = a[2::-2]
        result, _ = await self.call('omitted_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6::-2]
        result, _ = await self.call('negative_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:-1:-2]
        result, _ = await self.call('negative_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999::-2]
        result, _ = await self.call('negative_really_low_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:-999:-2]
        result, _ = await self.call('negative_really_low_end', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999::-2]
        result, _ = await self.call('really_high_start', [], return_type=list)
        self.assertEqual(expected_result, result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:999:-2]
        result, _ = await self.call('really_high_end', [], return_type=list)
        self.assertEqual(expected_result, result)

    # endregion

    # region TestAppend

    def test_list_append_int_value_compile(self):
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

        output, _ = self.assertCompile('ListAppendIntValue.py')
        self.assertEqual(expected_output, output)

    async def test_list_append_int_value(self):
        await self.set_up_contract('ListAppendIntValue.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3, 4], result)

    def test_list_append_any_value_compile(self):
        four = String('4').to_bytes(min_length=1)

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
            + Opcode.PUSHDATA1
            + Integer(len(four)).to_byte_array()
            + four
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

        output, _ = self.assertCompile('ListAppendAnyValue.py')
        self.assertEqual(expected_output, output)

    async def test_list_append_any_value(self):
        await self.set_up_contract('ListAppendAnyValue.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3, '4'], result)

    def test_list_append_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeListAppendValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_append_with_builtin_compile(self):
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
            + Opcode.LDLOC0     # list.append(a, 4)
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

        output, _ = self.assertCompile('ListAppendIntWithBuiltin.py')
        self.assertEqual(expected_output, output)

    async def test_list_append_with_builtin(self):
        await self.set_up_contract('ListAppendIntWithBuiltin.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3, 4], result)

    def test_list_append_with_builtin_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeListAppendWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_boa2_list_append_test(self):
        await self.set_up_contract('ListAppendBoa2Test.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual([6, 7], result)

    async def test_list_append_in_class_variable(self):
        await self.set_up_contract('ListAppendInClassVariable.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual([1, 2, 3, 4], result)

    # endregion

    # region TestClear

    def test_list_clear(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x02'
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

        output, _ = self.assertCompile('ClearList.py')
        self.assertEqual(expected_output, output)

    def test_list_reverse(self):
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

        output, _ = self.assertCompile('ReverseList.py')
        self.assertEqual(expected_output, output)

    async def test_boa2_list_reverse_test(self):
        await self.set_up_contract('ReverseBoa2Test.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(['blah', 4, 2, 1], result)

    # endregion

    # region TestExtend

    async def test_list_extend_tuple_value(self):
        await self.set_up_contract('ListExtendTupleValue.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    async def test_list_extend_any_value(self):
        await self.set_up_contract('ListExtendAnyValue.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3, '4', 5, 1], result)

    def test_list_extend_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeListExtendValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_extend_mismatched_iterable_value_type(self):
        path = self.get_contract_path('MismatchedTypeListExtendTupleValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_list_extend_with_builtin(self):
        await self.set_up_contract('ListExtendWithBuiltin.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_list_extend_with_builtin_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeListExtendWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region TestPop

    def test_list_pop_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop()
            + Opcode.PUSHM1
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        output, _ = self.assertCompile('PopList.py')
        self.assertEqual(expected_output, output)

    def test_list_pop(self):
        path, _ = self.get_deploy_file_paths('PopList.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = (runner.call_contract(path, 'pop_test'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual([1, 2, 3, 4, 5].pop(), invoke.result)

    def test_list_pop_without_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop()
            + Opcode.PUSHM1
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output, _ = self.assertCompile('PopListWithoutAssignment.py')
        self.assertEqual(expected_output, output)

    def test_list_pop_without_assignment(self):
        path, _ = self.get_deploy_file_paths('PopListWithoutAssignment.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = (runner.call_contract(path, 'pop_test'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        list_ = [1, 2, 3, 4, 5]
        list_.pop()
        self.assertEqual(list_, invoke.result)

    def test_list_pop_literal_argument_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop(2)
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        output, _ = self.assertCompile('PopListLiteralArgument.py')
        self.assertEqual(expected_output, output)

    def test_list_pop_literal_argument(self):
        path, _ = self.get_deploy_file_paths('PopListLiteralArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = (runner.call_contract(path, 'pop_test'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual([1, 2, 3, 4, 5].pop(2), invoke.result)

    def test_list_pop_literal_negative_argument_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop(-2)
            + Opcode.PUSH2
            + Opcode.NEGATE
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        output, _ = self.assertCompile('PopListLiteralNegativeArgument.py')
        self.assertEqual(expected_output, output)

    def test_list_pop_literal_negative_argument(self):
        path, _ = self.get_deploy_file_paths('PopListLiteralNegativeArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = (runner.call_contract(path, 'pop_test'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual([1, 2, 3, 4, 5].pop(-2), invoke.result)

    def test_list_pop_literal_variable_argument_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x01'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop(arg0)
            + Opcode.LDARG0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        output, _ = self.assertCompile('PopListVariableArgument.py')
        self.assertEqual(expected_output, output)

    async def test_list_pop_literal_variable_argument(self):
        await self.set_up_contract('PopListVariableArgument.py')

        list_ = [1, 2, 3, 4, 5]
        index = 0
        result, _ = await self.call('pop_test', [index], return_type=int)
        self.assertEqual(list_.pop(index), result)

        list_ = [1, 2, 3, 4, 5]
        index = len(list_) - 1
        result, _ = await self.call('pop_test', [index], return_type=int)
        self.assertEqual(list_.pop(index), result)

        list_ = [1, 2, 3, 4, 5]
        index = -len(list_)
        result, _ = await self.call('pop_test', [index], return_type=int)
        self.assertEqual(list_.pop(index), result)

        list_ = [1, 2, 3, 4, 5]
        index = 99999
        with self.assertRaises(FaultException) as context:
            await self.call('pop_test', [index], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)
        self.assertRaises(IndexError, list_.pop, index)

        list_ = [1, 2, 3, 4, 5]
        index = -99999
        with self.assertRaises(FaultException) as context:
            await self.call('pop_test', [index], return_type=int)

        self.assertRegex(str(context.exception), self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)
        self.assertRaises(IndexError, list_.pop, index)

    def test_list_pop_mismatched_type_argument(self):
        path = self.get_contract_path('PopListMismatchedTypeArgument.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_pop_mismatched_type_result_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop(2)
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = self.get_contract_path('PopListMismatchedTypeResult.py')
        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    async def test_list_pop_mismatched_type_result(self):
        await self.set_up_contract('PopListMismatchedTypeResult.py')

        result, _ = await self.call('pop_test', [], return_type=int)
        self.assertEqual(3, result)

    def test_list_pop_too_many_arguments(self):
        path = self.get_contract_path('PopListTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_boa2_list_remove_test(self):
        await self.set_up_contract('ListRemoveBoa2Test.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual([16, 3, 4], result)

    # endregion

    # region TestInsert

    async def test_list_insert_int_value(self):
        await self.set_up_contract('ListInsertIntValue.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 4, 3], result)

    async def test_list_insert_any_value(self):
        await self.set_up_contract('ListInsertAnyValue.py')

        list_ = [1, 2, 3]
        pos = 0
        value = '0'
        result, _ = await self.call('Main', [list_, pos, value], return_type=list)
        list_.insert(pos, value)
        self.assertEqual(list_, result)

        list_ = [1, 2, 3]
        pos = 1
        value = '1'
        result, _ = await self.call('Main', [list_, pos, value], return_type=list)
        list_.insert(pos, value)
        self.assertEqual(list_, result)

        list_ = [1, 2, 3]
        pos = 3
        value = '4'
        result, _ = await self.call('Main', [list_, pos, value], return_type=list)
        list_.insert(pos, value)
        self.assertEqual(list_, result)

    async def test_list_insert_int_negative_index(self):
        await self.set_up_contract('ListInsertIntNegativeIndex.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 4, 2, 3], result)

    async def test_list_insert_int_with_builtin(self):
        await self.set_up_contract('ListInsertIntWithBuiltin.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 4, 3], result)

    # endregion

    # region TestRemove

    async def test_list_remove_value(self):
        await self.set_up_contract('ListRemoveValue.py')

        result, _ = await self.call('Main', [[1, 2, 3, 4], 3], return_type=list)
        self.assertEqual([1, 2, 4], result)

        result, _ = await self.call('Main', [[1, 2, 3, 2, 3], 3], return_type=list)
        self.assertEqual([1, 2, 2, 3], result)

        with self.assertRaises(FaultException) as context:
            await self.call('Main', [[1, 2, 3, 4], 6], return_type=list)

        self.assertRegex(str(context.exception), self.INVALID_INDEX_MSG)

    async def test_list_remove_int_value(self):
        await self.set_up_contract('ListRemoveIntValue.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([10, 30], result)

    async def test_list_remove_int_with_builtin(self):
        await self.set_up_contract('ListRemoveIntWithBuiltin.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([10, 20], result)

    # endregion

    # region TestCopy

    async def test_list_copy(self):
        await self.set_up_contract('ListCopy.py')

        result, _ = await self.call('copy_list', [[1, 2, 3, 4], 5], return_type=list)
        self.assertEqual([[1, 2, 3, 4], [1, 2, 3, 4, 5]], result)

        result, _ = await self.call('copy_list', [['list', 'unit', 'test'], 'copy'], return_type=list)
        self.assertEqual([['list', 'unit', 'test'], ['list', 'unit', 'test', 'copy']], result)

        result, _ = await self.call('copy_list', [[True, False], True], return_type=list)
        self.assertEqual([[True, False], [True, False, True]], result)

        result, _ = await self.call('attribution', [[1, 2, 3, 4], 5], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('attribution', [['list', 'unit', 'test'], 'copy'], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('attribution', [[True, False], True], return_type=bool)
        self.assertEqual(False, result)

    async def test_int_list_copy(self):
        await self.set_up_contract('ListCopyInt.py')

        result, _ = await self.call('copy_int_list', [[1, 2, 3, 4], 5], return_type=list)
        self.assertEqual([[1, 2, 3, 4], [1, 2, 3, 4, 5]], result)

    async def test_str_list_copy(self):
        await self.set_up_contract('ListCopyStr.py')

        result, _ = await self.call('copy_str_list', [['list', 'unit', 'test'], 'copy'], return_type=list)
        self.assertEqual([['list', 'unit', 'test'], ['list', 'unit', 'test', 'copy']], result)

    async def test_bool_list_copy(self):
        await self.set_up_contract('ListCopyBool.py')

        result, _ = await self.call('copy_bool_list', [[True, False], True], return_type=list)
        self.assertEqual([[True, False], [True, False, True]], result)

    async def test_list_copy_builtin_call(self):
        await self.set_up_contract('CopyListBuiltinCall.py')

        result, _ = await self.call('copy_list', [[1, 2, 3, 4], 5], return_type=list)
        self.assertEqual([[1, 2, 3, 4], [1, 2, 3, 4, 5]], result)

        result, _ = await self.call('copy_list', [['list', 'unit', 'test'], 'copy'], return_type=list)
        self.assertEqual([['list', 'unit', 'test'], ['list', 'unit', 'test', 'copy']], result)

        result, _ = await self.call('copy_list', [[True, False], True], return_type=list)
        self.assertEqual([[True, False], [True, False, True]], result)

    # endregion

    # region TestIndex

    async def test_list_index(self):
        await self.set_up_contract('IndexList.py')

        list_ = [1, 2, 3, 4]
        value = 3
        start = 0
        end = 4
        result, _ = await self.call('main', [list_, value, start, end], return_type=int)
        self.assertEqual(list_.index(value, start, end), result)

        list_ = [1, 2, 3, 4]
        value = 3
        start = 2
        end = 4
        result, _ = await self.call('main', [list_, value, start, end], return_type=int)
        self.assertEqual(list_.index(value, start, end), result)

        list_ = [1, 2, 3, 4]
        value = 3
        start = 0
        end = -1
        result, _ = await self.call('main', [list_, value, start, end], return_type=int)
        self.assertEqual(list_.index(value, start, end), result)

        list_ = [1, 2, 3, 4]
        value = 2
        start = 0
        end = 99
        result, _ = await self.call('main', [list_, value, start, end], return_type=int)
        self.assertEqual(list_.index(value, start, end), result)

        from boa3.internal.model.builtin.builtin import Builtin
        with self.assertRaises(FaultException) as context:
            await self.call('main', [[1, 2, 3, 4], 3, 3, 4], return_type=int)

        self.assertRegex(str(context.exception), f'{Builtin.SequenceIndex.exception_message}')

        with self.assertRaises(FaultException) as context:
            await self.call('main', [[1, 2, 3, 4], 3, 4, -1], return_type=int)

        self.assertRegex(str(context.exception), f'{Builtin.SequenceIndex.exception_message}')

        with self.assertRaises(FaultException) as context:
            await self.call('main', [[1, 2, 3, 4], 3, 0, -99], return_type=int)

        self.assertRegex(str(context.exception), f'{Builtin.SequenceIndex.exception_message}')

    async def test_list_index_end_default(self):
        await self.set_up_contract('IndexListEndDefault.py')

        list_ = [1, 2, 3, 4]
        value = 3
        start = 0
        result, _ = await self.call('main', [list_, value, start], return_type=int)
        self.assertEqual(list_.index(value, start), result)

        list_ = [1, 2, 3, 4]
        value = 2
        start = -10
        result, _ = await self.call('main', [list_, value, start], return_type=int)
        self.assertEqual(list_.index(value, start), result)

        from boa3.internal.model.builtin.builtin import Builtin
        with self.assertRaises(FaultException) as context:
            await self.call('main', [[1, 2, 3, 4], 2, 99], return_type=int)

        self.assertRegex(str(context.exception), f'{Builtin.SequenceIndex.exception_message}')

        with self.assertRaises(FaultException) as context:
            await self.call('main', [[1, 2, 3, 4], 4, -1], return_type=int)

        self.assertRegex(str(context.exception), f'{Builtin.SequenceIndex.exception_message}')

    async def test_list_index_defaults(self):
        await self.set_up_contract('IndexListDefaults.py')

        list_ = [1, 2, 3, 4]
        value = 3
        result, _ = await self.call('main', [list_, value], return_type=int)
        self.assertEqual(list_.index(value), result)

        list_ = [1, 2, 3, 4]
        value = 1
        result, _ = await self.call('main', [list_, value], return_type=int)
        self.assertEqual(list_.index(value), result)

    async def test_list_index_int(self):
        await self.set_up_contract('IndexListInt.py')

        list_ = [1, 2, 3, 4]
        value = 3
        result, _ = await self.call('main', [list_, value], return_type=int)
        self.assertEqual(list_.index(value), result)

    async def test_list_index_str(self):
        await self.set_up_contract('IndexListStr.py')

        list_ = ['unit', 'test', 'neo3-boa']
        value = 'test'
        result, _ = await self.call('main', [list_, value], return_type=int)
        self.assertEqual(list_.index(value), result)

    async def test_list_index_bool(self):
        await self.set_up_contract('IndexListBool.py')

        list_ = [True, True, False]
        value = False
        result, _ = await self.call('main', [list_, value], return_type=int)
        self.assertEqual(list_.index(value), result)

    # endregion

    # region TestSort

    async def test_list_sort(self):
        await self.set_up_contract('SortList.py')

        sorted_list = [5, 4, 3, 2, 6, 1]
        sorted_list.sort()
        result, _ = await self.call('sort_test', [], return_type=list)
        self.assertEqual(sorted_list, result)

    def test_list_sort_with_args(self):
        # list.sort arguments must be used as kwargs
        path = self.get_contract_path('SortArgsList.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_list_sort_reverse_true(self):
        await self.set_up_contract('SortReverseTrueList.py')

        sorted_list = [5, 4, 3, 2, 6, 1]
        sorted_list.sort(reverse=True)
        result, _ = await self.call('sort_test', [], return_type=list)
        self.assertEqual(sorted_list, result)

    async def test_list_sort_reverse_false(self):
        await self.set_up_contract('SortReverseFalseList.py')

        sorted_list = [5, 4, 3, 2, 6, 1]
        sorted_list.sort(reverse=False)
        result, _ = await self.call('sort_test', [], return_type=list)
        self.assertEqual(sorted_list, result)

    def test_list_sort_key(self):
        path = self.get_contract_path('SortKeyList.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_list_any_sort(self):
        path = self.get_contract_path('SortListAny.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_list_of_list_sort(self):
        path = self.get_contract_path('SortListOfList.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    # endregion

    # region TestComprehension

    def test_list_comprehension_str(self):
        path = self.get_contract_path('ListComprehensionStr.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    # endregion

    # region TestDel

    def test_del_list_item(self):
        path = self.get_contract_path('ListDelItem.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    # endregion
