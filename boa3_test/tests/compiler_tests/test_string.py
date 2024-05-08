from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests import boatestcase
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestString(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/string_test'

    SUBSTRING_NOT_FOUND_MSG = 'substring not found'
    VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX = r'The value \d+ is out of range.'
    INVALID_OFFSET_MSG = 'invalid offset'
    NEGATIVE_INDEX_MSG = 'negative index'

    def test_string_get_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PUSH1
            + Opcode.SUBSTR
            + Opcode.CONVERT + StackItemType.ByteString
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('StringGetValue.py')
        self.assertEqual(expected_output, output)

    async def test_string_get_value(self):
        await self.set_up_contract('StringGetValue.py')

        result, _ = await self.call('Main', ['unit'], return_type=str)
        self.assertEqual('u', result)
        result, _ = await self.call('Main', ['123'], return_type=str)
        self.assertEqual('1', result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [''], return_type=str)

        self.assertRegex(str(context.exception), self.INVALID_OFFSET_MSG)

    def test_string_get_value_with_negative_index_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[-1]
            + Opcode.PUSHM1

            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.PUSH1
            + Opcode.SUBSTR
            + Opcode.CONVERT + StackItemType.ByteString
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('StringGetValueNegativeIndex.py')
        self.assertEqual(expected_output, output)

    async def test_string_get_value_with_negative_index(self):
        await self.set_up_contract('StringGetValueNegativeIndex.py')

        result, _ = await self.call('main', ['unit_test'], return_type=str)
        self.assertEqual('t', result)
        result, _ = await self.call('main', ['abc'], return_type=str)
        self.assertEqual('c', result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [[]], return_type=str)

        self.assertRegex(str(context.exception), self.NEGATIVE_INDEX_MSG)

    def test_string_get_value_with_variable_compile(self):
        test_string = String('test').to_bytes(min_length=1)

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.PUSHDATA1
            + Integer(len(test_string)).to_byte_array()
            + test_string
            + Opcode.LDARG0     # 'test'[arg]

            + Opcode.DUP        # will check if number is negative
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.PUSH1
            + Opcode.DUP
            + Opcode.PUSH0
            + Opcode.GE
            + Opcode.JMPIF
            + Integer(4).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.SUBSTR
            + Opcode.CONVERT + StackItemType.ByteString
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('StringGetValueWithVariable.py')
        self.assertEqual(expected_output, output)

    async def test_string_get_value_with_variable(self):
        await self.set_up_contract('StringGetValueWithVariable.py')

        result, _ = await self.call('main', [1], return_type=str)
        self.assertEqual('e', result)
        result, _ = await self.call('main', [2], return_type=str)
        self.assertEqual('s', result)

    async def test_string_get_value_to_variable(self):
        await self.set_up_contract('StringGetValueToVariable.py')

        result, _ = await self.call('Main', ['unit'], return_type=str)
        self.assertEqual('u', result)
        result, _ = await self.call('Main', ['123'], return_type=str)
        self.assertEqual('1', result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [''], return_type=str)

        self.assertRegex(str(context.exception), self.INVALID_OFFSET_MSG)

    def test_string_set_value(self):
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, 'StringSetValue.py')

    async def test_string_slicing(self):
        await self.set_up_contract('StringSlicingLiteralValues.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('i', result)

    async def test_string_slicing_start_larger_than_ending(self):
        await self.set_up_contract('StringSlicingStartLargerThanEnding.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('', result)

    async def test_string_slicing_with_variables(self):
        await self.set_up_contract('StringSlicingVariableValues.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('i', result)

    async def test_string_slicing_negative_start(self):
        await self.set_up_contract('StringSlicingNegativeStartOmitted.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('unit_', result)

    async def test_string_slicing_negative_end_omitted(self):
        await self.set_up_contract('StringSlicingNegativeEndOmitted.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('test', result)

    async def test_string_slicing_start_omitted(self):
        await self.set_up_contract('StringSlicingStartOmitted.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('uni', result)

    def test_string_slicing_omitted_compile(self):
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

        output, _ = self.assertCompile('StringSlicingOmitted.py')
        self.assertEqual(expected_output, output)

    async def test_string_slicing_omitted(self):
        await self.set_up_contract('StringSlicingOmitted.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('unit_test', result)

    async def test_string_slicing_end_omitted(self):
        await self.set_up_contract('StringSlicingEndOmitted.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('it_test', result)

    def test_string_slicing_positive_index_opcode(self):
        unit_test_string = String('unit_test').to_bytes(min_length=1)
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(unit_test_string)).to_byte_array()
            + unit_test_string
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(unit_test_string)).to_byte_array()
            + unit_test_string
            + Opcode.PUSH2

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

            + Opcode.PUSH3

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

            + Opcode.OVER  # starts getting the substring
        )

        path = self.get_contract_path('StringSlicingLiteralValues.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    def test_string_slicing_negative_lower_index_opcode(self):
        unit_test_string = String('unit_test').to_bytes(min_length=1)
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(unit_test_string)).to_byte_array()
            + unit_test_string
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(unit_test_string)).to_byte_array()
            + unit_test_string
            + Opcode.PUSH4      # lower index
            + Opcode.NEGATE

            + Opcode.OVER       # fix negative index
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

            + Opcode.OVER   # gets the upper index
            + Opcode.SIZE
            + Opcode.SWAP
            + Opcode.SUB

            + Opcode.RIGHT  # starts getting the substring
            + Opcode.CONVERT + StackItemType.ByteString
            + Opcode.RET
        )

        output, _ = self.assertCompile('StringSlicingNegativeEndOmitted.py')
        self.assertEqual(expected_output, output)

    def test_string_slicing_negative_upper_index_opcode(self):
        unit_test_string = String('unit_test').to_bytes(min_length=1)
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(unit_test_string)).to_byte_array()
            + unit_test_string
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(unit_test_string)).to_byte_array()
            + unit_test_string
            + Opcode.PUSH4      # upper index
            + Opcode.NEGATE

            + Opcode.OVER       # fix negative index
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.DUP        # checks if upper index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.LEFT  # starts getting the substring
            + Opcode.CONVERT + StackItemType.ByteString
            + Opcode.RET
        )

        output, _ = self.assertCompile('StringSlicingNegativeStartOmitted.py')
        self.assertEqual(expected_output, output)

    def test_string_slicing_variable_index_opcode(self):
        unit_test_string = String('unit_test').to_bytes(min_length=1)
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.PUSHDATA1
            + Integer(len(unit_test_string)).to_byte_array()
            + unit_test_string
            + Opcode.LDARG0     # lower index

            + Opcode.DUP        # check if lower index is negative
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)

            + Opcode.OVER       # fix negative index
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

            + Opcode.LDARG1     # upper index

            + Opcode.DUP        # check if upper index is negative
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(6).to_byte_array(min_length=1)

            + Opcode.PUSH2      # fix negative index
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

            + Opcode.OVER  # starts getting the substring
        )

        path = self.get_contract_path('StringSlicingWithVariables.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    async def test_string_slicing_with_stride(self):
        await self.set_up_contract('StringSlicingWithStride.py')

        a = 'unit_test'
        expected_result = a[2:5:2]
        result, _ = await self.call('literal_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6:5:2]
        result, _ = await self.call('negative_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:-1:2]
        result, _ = await self.call('negative_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6:-1:2]
        result, _ = await self.call('negative_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999:5:2]
        result, _ = await self.call('negative_really_low_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:-999:2]
        result, _ = await self.call('negative_really_low_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999:-999:2]
        result, _ = await self.call('negative_really_low_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999:5:2]
        result, _ = await self.call('really_high_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:999:2]
        result, _ = await self.call('really_high_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999:999:2]
        result, _ = await self.call('really_high_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        x = 0
        y = 5
        expected_result = a[x:y:2]
        result, _ = await self.call('with_variables', [x, y], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_string_slicing_with_negative_stride(self):
        await self.set_up_contract('StringSlicingWithNegativeStride.py')

        a = 'unit_test'
        expected_result = a[2:5:-1]
        result, _ = await self.call('literal_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6:5:-1]
        result, _ = await self.call('negative_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:-1:-1]
        result, _ = await self.call('negative_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6:-1:-1]
        result, _ = await self.call('negative_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999:5:-1]
        result, _ = await self.call('negative_really_low_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:-999:-1]
        result, _ = await self.call('negative_really_low_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999:-999:-1]
        result, _ = await self.call('negative_really_low_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999:5:-1]
        result, _ = await self.call('really_high_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:999:-1]
        result, _ = await self.call('really_high_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999:999:-1]
        result, _ = await self.call('really_high_values', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_string_slicing_omitted_with_stride(self):
        await self.set_up_contract('StringSlicingOmittedWithStride.py')

        a = 'unit_test'
        expected_result = a[::2]
        result, _ = await self.call('omitted_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:5:2]
        result, _ = await self.call('omitted_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[2::2]
        result, _ = await self.call('omitted_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6::2]
        result, _ = await self.call('negative_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:-1:2]
        result, _ = await self.call('negative_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999::2]
        result, _ = await self.call('negative_really_low_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:-999:2]
        result, _ = await self.call('negative_really_low_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999::2]
        result, _ = await self.call('really_high_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:999:2]
        result, _ = await self.call('really_high_end', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_string_slicing_omitted_with_negative_stride(self):
        await self.set_up_contract('StringSlicingOmittedWithNegativeStride.py')

        a = 'unit_test'
        expected_result = a[::-2]
        result, _ = await self.call('omitted_values', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:5:-2]
        result, _ = await self.call('omitted_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[2::-2]
        result, _ = await self.call('omitted_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6::-2]
        result, _ = await self.call('negative_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:-1:-2]
        result, _ = await self.call('negative_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999::-2]
        result, _ = await self.call('negative_really_low_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:-999:-2]
        result, _ = await self.call('negative_really_low_end', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999::-2]
        result, _ = await self.call('really_high_start', [], return_type=str)
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:999:-2]
        result, _ = await self.call('really_high_end', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_string_simple_concat(self):
        await self.set_up_contract('StringSimpleConcat.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('bye worldhi', result)

    async def test_boa2_string_concat_test(self):
        await self.set_up_contract('ConcatBoa2Test.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('helloworld', result)

    async def test_boa2_string_concat_test2(self):
        await self.set_up_contract('ConcatBoa2Test2.py')

        result, _ = await self.call('main', ['concat', ['hello', 'world']], return_type=str)
        self.assertEqual('helloworld', result)

        result, _ = await self.call('main', ['blah', ['hello', 'world']], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', ['concat', ['blah']], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', ['concat', ['hello', 'world', 'third']], return_type=str)
        self.assertEqual('helloworld', result)

        result, _ = await self.call('main', ['concat', ['1', 'neo']], return_type=str)
        self.assertEqual('1neo', result)

        result, _ = await self.call('main', ['concat', ['', 'neo']], return_type=str)
        self.assertEqual('neo', result)

    async def test_string_with_double_quotes(self):
        await self.set_up_contract('StringWithDoubleQuotes.py')

        result, _ = await self.call('string_test', ['hello', 'world'], return_type=str)
        self.assertEqual('"hell"test_symbol":world}"', result)

        result, _ = await self.call('string_test', ['1', 'neo'], return_type=str)
        self.assertEqual('""test_symbol":neo}"', result)

        result, _ = await self.call('string_test', ['neo', ''], return_type=str)
        self.assertEqual('"ne"test_symbol":}"', result)

    async def test_string_upper(self):
        await self.set_up_contract('UpperStringMethod.py')

        string = 'abcdefghijklmnopqrstuvwxyz'
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.upper(), result)

        string = 'a1b123y3z'
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.upper(), result)

        string = '!@#$%123*-/'
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.upper(), result)

        string = 'áõèñ'
        not_as_expected, _ = await self.call('main', [string], return_type=str)
        # upper was implemented for ASCII characters only
        self.assertNotEqual(string.upper(), not_as_expected)

    async def test_string_lower(self):
        await self.set_up_contract('LowerStringMethod.py')

        string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.lower(), result)

        string = 'A1B123Y3Z'
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.lower(), result)

        string = '!@#$%123*-/'
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.lower(), result)

        string = 'ÁÕÈÑ'
        not_as_expected, _ = await self.call('main', [string], return_type=str)
        # lower was implemented for ASCII characters only
        self.assertNotEqual(string.lower(), not_as_expected)

    async def test_string_startswith_method(self):
        await self.set_up_contract('StartswithStringMethod.py')

        string = 'unit_test'
        substring = 'unit'
        start = 0
        end = len(string)
        result, _ = await self.call('main', [string, substring, start, end], return_type=bool)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'unit'
        start = 2
        end = 6
        result, _ = await self.call('main', [string, substring, start, end], return_type=bool)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'it'
        start = 2
        end = 6
        result, _ = await self.call('main', [string, substring, start, end], return_type=bool)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'it'
        start = 2
        end = 3
        result, _ = await self.call('main', [string, substring, start, end], return_type=bool)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'unit_tes'
        start = -99
        end = -1
        result, _ = await self.call('main', [string, substring, start, end], return_type=bool)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = ''
        start = 0
        end = 0
        result, _ = await self.call('main', [string, substring, start, end], return_type=bool)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'unit_test'
        start = 0
        end = 99
        result, _ = await self.call('main', [string, substring, start, end], return_type=bool)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'unit_test'
        start = 100
        end = 99
        result, _ = await self.call('main', [string, substring, start, end], return_type=bool)
        self.assertEqual(string.startswith(substring, start, end), result)

    async def test_string_startswith_method_default_end(self):
        await self.set_up_contract('StartswithStringMethodDefaultEnd.py')

        string = 'unit_test'
        substring = 'unit'
        start = 0
        result, _ = await self.call('main', [string, substring, start], return_type=bool)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'unit'
        start = 2
        result, _ = await self.call('main', [string, substring, start], return_type=bool)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'it'
        start = 2
        result, _ = await self.call('main', [string, substring, start], return_type=bool)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'it'
        start = 3
        result, _ = await self.call('main', [string, substring, start], return_type=bool)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'unit_tes'
        start = -99
        result, _ = await self.call('main', [string, substring, start], return_type=bool)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = ''
        start = 0
        result, _ = await self.call('main', [string, substring, start], return_type=bool)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = ''
        start = 99
        result, _ = await self.call('main', [string, substring, start], return_type=bool)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'unit_test'
        start = 0
        result, _ = await self.call('main', [string, substring, start], return_type=bool)
        self.assertEqual(string.startswith(substring, start), result)

    async def test_string_startswith_method_defaults(self):
        await self.set_up_contract('StartswithStringMethodDefaults.py')

        string = 'unit_test'
        substring = 'unit'
        result, _ = await self.call('main', [string, substring], return_type=bool)
        self.assertEqual(string.startswith(substring), result)

        string = 'unit_test'
        substring = 'unit_test'
        result, _ = await self.call('main', [string, substring], return_type=bool)
        self.assertEqual(string.startswith(substring), result)

        string = 'unit_test'
        substring = ''
        result, _ = await self.call('main', [string, substring], return_type=bool)
        self.assertEqual(string.startswith(substring), result)

        string = 'unit_test'
        substring = '12345'
        result, _ = await self.call('main', [string, substring], return_type=bool)
        self.assertEqual(string.startswith(substring), result)

        string = 'unit_test'
        substring = 'bigger substring'
        result, _ = await self.call('main', [string, substring], return_type=bool)
        self.assertEqual(string.startswith(substring), result)

    async def test_string_strip(self):
        await self.set_up_contract('StripStringMethod.py')

        string = 'abcdefghijklmnopqrstuvwxyz'
        chars = 'abcxyz'
        result, _ = await self.call('main', [string, chars], return_type=str)
        self.assertEqual(string.strip(chars), result)

        string = 'abcdefghijklmnopqrsvwxyz unit test abcdefghijklmnopqrsvwxyz'
        chars = 'abcdefghijklmnopqrsvwxyz '
        result, _ = await self.call('main', [string, chars], return_type=str)
        self.assertEqual(string.strip(chars), result)

        string = '0123456789hello world987654310'
        chars = '0987654321'
        result, _ = await self.call('main', [string, chars], return_type=str)
        self.assertEqual(string.strip(chars), result)

    async def test_string_strip_default(self):
        await self.set_up_contract('StripStringMethodDefault.py')

        string = '     unit test    '
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.strip(), result)

        string = 'unit test    '
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.strip(), result)

        string = '    unit test'
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.strip(), result)

        string = ' \t\n\r\f\vunit test \t\n\r\f\v'
        result, _ = await self.call('main', [string], return_type=str)
        self.assertEqual(string.strip(), result)

    async def test_isdigit_method(self):
        await self.set_up_contract('StringIsdigitMethod.py')

        string = '0123456789'
        result, _ = await self.call('main', [string], return_type=bool)
        self.assertEqual(string.isdigit(), result)

        string = '23mixed01'
        result, _ = await self.call('main', [string], return_type=bool)
        self.assertEqual(string.isdigit(), result)

        string = 'no digits here'
        result, _ = await self.call('main', [string], return_type=bool)
        self.assertEqual(string.isdigit(), result)

        string = ''
        result, _ = await self.call('main', [string], return_type=bool)
        self.assertEqual(string.isdigit(), result)

        string = '¹²³'
        not_as_expected, _ = await self.call('main', [string], return_type=bool)
        # neo3-boas isdigit implementation does not verify values that are not from the ASCII
        self.assertNotEqual(string.isdigit(), not_as_expected)

    async def test_string_join_with_sequence(self):
        await self.set_up_contract('JoinStringMethodWithSequence.py')

        string = ' '
        sequence = ["Unit", "Test", "Neo3-boa"]
        result, _ = await self.call('main', [string, sequence], return_type=str)
        self.assertEqual(string.join(sequence), result)

        string = ' '
        sequence = []
        result, _ = await self.call('main', [string, sequence], return_type=str)
        self.assertEqual(string.join(sequence), result)

        string = ' '
        sequence = ["UnitTest"]
        result, _ = await self.call('main', [string, sequence], return_type=str)
        self.assertEqual(string.join(sequence), result)

    async def test_string_join_with_dictionary(self):
        await self.set_up_contract('JoinStringMethodWithDictionary.py')

        string = ' '
        dictionary = {"Unit": 1, "Test": 2, "Neo3-boa": 3}
        result, _ = await self.call('main', [string, dictionary], return_type=str)
        self.assertEqual(string.join(dictionary), result)

        string = ' '
        dictionary = {}
        result, _ = await self.call('main', [string, dictionary], return_type=str)
        self.assertEqual(string.join(dictionary), result)

        string = ' '
        dictionary = {"UnitTest": 1}
        result, _ = await self.call('main', [string, dictionary], return_type=str)
        self.assertEqual(string.join(dictionary), result)

    async def test_string_index(self):
        await self.set_up_contract('IndexString.py')

        string = 'unit test'
        substring = 'i'
        start = 0
        end = 4
        result, _ = await self.call('main', [string, substring, start, end], return_type=int)
        self.assertEqual(string.index(substring, start, end), result)

        string = 'unit test'
        substring = 'i'
        start = 2
        end = 4
        result, _ = await self.call('main', [string, substring, start, end], return_type=int)
        self.assertEqual(string.index(substring, start, end), result)

        string = 'unit test'
        substring = 'i'
        start = 0
        end = -1
        result, _ = await self.call('main', [string, substring, start, end], return_type=int)
        self.assertEqual(string.index(substring, start, end), result)

        string = 'unit test'
        substring = 'n'
        start = 0
        end = 99
        result, _ = await self.call('main', [string, substring, start, end], return_type=int)
        self.assertEqual(string.index(substring, start, end), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['unit test', 'i', 3, 4], return_type=int)

        self.assertRegex(str(context.exception), self.SUBSTRING_NOT_FOUND_MSG)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['unit test', 'i', 4, -1], return_type=int)

        self.assertRegex(str(context.exception), self.SUBSTRING_NOT_FOUND_MSG)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['unit test', 'i', 0, -99], return_type=int)

        self.assertRegex(str(context.exception), self.SUBSTRING_NOT_FOUND_MSG)

    async def test_string_index_end_default(self):
        await self.set_up_contract('IndexStringEndDefault.py')

        string = 'unit test'
        substring = 't'
        start = 0
        result, _ = await self.call('main', [string, substring, start], return_type=int)
        self.assertEqual(string.index(substring, start), result)

        string = 'unit test'
        substring = 't'
        start = 4
        result, _ = await self.call('main', [string, substring, start], return_type=int)
        self.assertEqual(string.index(substring, start), result)

        string = 'unit test'
        substring = 't'
        start = 6
        result, _ = await self.call('main', [string, substring, start], return_type=int)
        self.assertEqual(string.index(substring, start), result)

        string = 'unit test'
        substring = 'i'
        start = -10
        result, _ = await self.call('main', [string, substring, start], return_type=int)
        self.assertEqual(string.index(substring, start), result)

        string = 'unit test'
        substring = 'i'
        start = 99
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [string, substring, start], return_type=int)

        self.assertRegex(str(context.exception), self.SUBSTRING_NOT_FOUND_MSG)
        self.assertRaises(ValueError, string.index, substring, start)

        string = 'unit test'
        substring = 's'
        start = -1
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [string, substring, start], return_type=int)

        self.assertRegex(str(context.exception), self.SUBSTRING_NOT_FOUND_MSG)
        self.assertRaises(ValueError, string.index, substring, start)

    async def test_string_index_defaults(self):
        await self.set_up_contract('IndexStringDefaults.py')

        string = 'unit test'
        substring = 'u'
        result, _ = await self.call('main', [string, substring], return_type=int)
        self.assertEqual(string.index(substring), result)

        string = 'unit test'
        substring = 't'
        result, _ = await self.call('main', [string, substring], return_type=int)
        self.assertEqual(string.index(substring), result)

        string = 'unit test'
        substring = ' '
        result, _ = await self.call('main', [string, substring], return_type=int)
        self.assertEqual(string.index(substring), result)

    def test_string_index_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'IndexStringMismatchedType.py')

    async def test_string_property_slicing(self):
        await self.set_up_contract('StringPropertySlicing.py')

        string = 'unit test'
        start = 0
        end = len(string)
        result, _ = await self.call('main', [string, start, end], return_type=str)
        self.assertEqual(string[start:end], result)

        start = 2
        end = len(string) - 1
        result, _ = await self.call('main', [string, start, end], return_type=str)
        self.assertEqual(string[start:end], result)

        start = len(string)
        end = 0
        result, _ = await self.call('main', [string, start, end], return_type=str)
        self.assertEqual(string[start:end], result)

    async def test_string_instance_variable_slicing(self):
        await self.set_up_contract('StringInstanceVariableSlicing.py')

        string = 'unit test'
        start = 0
        end = len(string)
        result, _ = await self.call('main', [string, start, end], return_type=str)
        self.assertEqual(string[start:end], result)

        start = 2
        end = len(string) - 1
        result, _ = await self.call('main', [string, start, end], return_type=str)
        self.assertEqual(string[start:end], result)

        start = len(string)
        end = 0
        result, _ = await self.call('main', [string, start, end], return_type=str)
        self.assertEqual(string[start:end], result)

    async def test_string_class_variable_slicing(self):
        await self.set_up_contract('StringClassVariableSlicing.py')

        string = 'unit test'
        start = 0
        end = len(string)
        result, _ = await self.call('main', [start, end], return_type=str)
        self.assertEqual(string[start:end], result)

        start = 2
        end = len(string) - 1
        result, _ = await self.call('main', [start, end], return_type=str)
        self.assertEqual(string[start:end], result)

        start = len(string)
        end = 0
        result, _ = await self.call('main', [start, end], return_type=str)
        self.assertEqual(string[start:end], result)

    def test_f_string_literal(self):
        path, _ = self.get_deploy_file_paths('FStringLiteral.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        expected_result = "unit test"

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(expected_result, invoke.result)

    async def test_f_string_string_var(self):
        await self.set_up_contract('FStringStringVar.py')

        result, _ = await self.call('main', ["unit test"], return_type=str)
        self.assertEqual("F-string: unit test", result)

        result, _ = await self.call('main', [""], return_type=str)
        self.assertEqual("F-string: ", result)

    async def test_f_string_int_var(self):
        await self.set_up_contract('FStringIntVar.py')

        result, _ = await self.call('main', [123], return_type=str)
        self.assertEqual("F-string: 123", result)

        result, _ = await self.call('main', [-100], return_type=str)
        self.assertEqual("F-string: -100", result)

    async def test_f_string_bool_var(self):
        await self.set_up_contract('FStringBoolVar.py')

        result, _ = await self.call('main', [True], return_type=str)
        self.assertEqual("F-string: True", result)

        result, _ = await self.call('main', [False], return_type=str)
        self.assertEqual("F-string: False", result)

    async def test_f_string_bytes_var(self):
        await self.set_up_contract('FStringBytesVar.py')

        result, _ = await self.call('main', [b"unit test"], return_type=str)
        self.assertEqual("F-string: unit test", result)

        result, _ = await self.call('main', [""], return_type=str)
        self.assertEqual("F-string: ", result)

    async def test_f_string_sequence_var(self):
        await self.set_up_contract('FStringSequenceVar.py')

        result, _ = await self.call('main', [[1, 2, 3]], return_type=str)
        self.assertEqual("F-string: [1,2,3]", result)

        result, _ = await self.call('main', [[]], return_type=str)
        self.assertEqual("F-string: []", result)

    async def test_f_string_user_class_var(self):
        await self.set_up_contract('FStringUserClassVar.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('F-string: {"string":"unit test","number":123}', result)

    def test_f_string_any_var(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'FStringAnyVar.py')

    def test_f_string_union_var(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'FStringUnionVar.py')

    async def test_string_replace(self):
        await self.set_up_contract('ReplaceStringMethod.py')

        string = 'banana'
        old = 'an'
        new = 'o'
        count = -1
        result, _ = await self.call('main', [string, old, new, count], return_type=str)
        self.assertEqual(string.replace(old, new, count), result)

        old = 'a'
        new = 'o'
        count = -1
        result, _ = await self.call('main', [string, old, new, count], return_type=str)
        self.assertEqual(string.replace(old, new, count), result)

        old = 'a'
        new = 'oo'
        count = -1
        result, _ = await self.call('main', [string, old, new, count], return_type=str)
        self.assertEqual(string.replace(old, new, count), result)

        string = 'banana'
        old = 'an'
        new = 'o'
        count = 1
        result, _ = await self.call('main', [string, old, new, count], return_type=str)
        self.assertEqual(string.replace(old, new, count), result)

        string = 'banana'
        old = 'an'
        new = 'o'
        count = 2
        result, _ = await self.call('main', [string, old, new, count], return_type=str)
        self.assertEqual(string.replace(old, new, count), result)

        string = 'banana'
        old = 'an'
        new = 'o'
        count = 3
        result, _ = await self.call('main', [string, old, new, count], return_type=str)
        self.assertEqual(string.replace(old, new, count), result)

        string = 'banana'
        old = 'an'
        new = 'o'
        result, _ = await self.call('main_default_count', [string, old, new], return_type=str)
        self.assertEqual(string.replace(old, new), result)

    def test_string_replace_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ReplaceStringMethodMismatchedType.py')

    def test_string_replace_too_many_arguments(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ReplaceStringMethodTooManyArguments.py')

    def test_string_replace_too_few_arguments(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ReplaceStringMethodTooFewArguments.py')
