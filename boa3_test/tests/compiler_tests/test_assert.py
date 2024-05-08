from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestAssert(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/assert_test'

    def test_assert_unary_boolean_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0     # assert not a
            + Opcode.NOT
            + Opcode.ASSERT
            + Opcode.LDARG1     # return b
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertUnaryOperation.py')
        self.assertEqual(expected_output, output)

    async def test_assert_unary_boolean_operation_run(self):
        await self.set_up_contract('AssertUnaryOperation.py')

        result, _ = await self.call('Main', [False, 10], return_type=int)
        self.assertEqual(10, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('Main', [True, 20], return_type=int)

    def test_assert_binary_boolean_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0     # assert a != b
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertBinaryOperation.py')
        self.assertEqual(expected_output, output)

    async def test_assert_binary_boolean_operation_run(self):
        await self.set_up_contract('AssertBinaryOperation.py')

        result, _ = await self.call('Main', [10, 20], return_type=int)
        self.assertEqual(10, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('Main', [20, 20], return_type=int)

    def test_assert_with_message_compile(self):
        assert_msg = String('a must be greater than zero').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.GT
            + Opcode.PUSHDATA1  # assert a > 0, 'a must be greater than zero'
            + Integer(len(assert_msg)).to_byte_array() + assert_msg
            + Opcode.ASSERTMSG
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertWithMessage.py')
        self.assertEqual(expected_output, output)

    async def test_assert_with_message_run(self):
        await self.set_up_contract('AssertWithMessage.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)

        assert_msg = 'a must be greater than zero'
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('Main', [0], return_type=int)

        self.assertRegex(str(context.exception),  assert_msg)

    def test_assert_with_bytes_message_compile(self):
        assert_msg = String('a must be greater than zero').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.GT
            + Opcode.PUSHDATA1  # assert a > 0, b'a must be greater than zero'
            + Integer(len(assert_msg)).to_byte_array() + assert_msg
            + Opcode.ASSERTMSG
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertWithBytesMessage.py')
        self.assertEqual(expected_output, output)

    async def test_assert_with_bytes_message_run(self):
        await self.set_up_contract('AssertWithBytesMessage.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)

        assert_msg = b'a must be greater than zero'
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('Main', [0], return_type=int)

        self.assertRegex(String(str(context.exception)).to_bytes(), assert_msg)

    def test_assert_with_int_message(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'AssertWithIntMessage.py')

    def test_assert_with_bool_message(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'AssertWithBoolMessage.py')

    def test_assert_with_list_message(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'AssertWithListMessage.py')

    def test_assert_with_str_var_message_compile(self):
        assert_msg = String('a must be greater than zero').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1
            + Integer(len(assert_msg)).to_byte_array() + assert_msg
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.GT
            + Opcode.PUSHDATA1
            + Integer(len(assert_msg)).to_byte_array() + assert_msg  # assert a > 0, 'a must be greater than zero'
            + Opcode.ASSERTMSG
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertWithStrVarMessage.py')
        self.assertEqual(expected_output, output)

    async def test_assert_with_str_var_message_run(self):
        await self.set_up_contract('AssertWithStrVarMessage.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)

        assert_msg = 'a must be greater than zero'
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('Main', [0], return_type=int)

        self.assertRegex(str(context.exception), assert_msg)

    def test_assert_with_str_function_message_compile(self):
        assert_msg = String('a must be greater than zero').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.GT
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.ASSERTMSG
            + Opcode.LDARG0     # return a
            + Opcode.RET
            + Opcode.PUSHDATA1
            + Integer(len(assert_msg)).to_byte_array() + assert_msg  # assert a > 0, 'a must be greater than zero'
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertWithStrFunctionMessage.py')
        self.assertEqual(expected_output, output)

    async def test_assert_with_str_function_message_run(self):
        await self.set_up_contract('AssertWithStrFunctionMessage.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)

        assert_msg = 'a must be greater than zero'
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('Main', [0], return_type=int)

        self.assertRegex(str(context.exception), assert_msg)

    def test_assert_int_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertInt.py')
        self.assertEqual(expected_output, output)

    async def test_assert_int_run(self):
        await self.set_up_contract('AssertInt.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)
        result, _ = await self.call('Main', [-10], return_type=int)
        self.assertEqual(-10, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('Main', [0], return_type=int)

    def test_assert_str_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertStr.py')
        self.assertEqual(expected_output, output)

    async def test_assert_str_run(self):
        await self.set_up_contract('AssertStr.py')

        result, _ = await self.call('Main', ['unittest'], return_type=str)
        self.assertEqual('unittest', result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('Main', [''], return_type=str)

    def test_assert_bytes_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertBytes.py')
        self.assertEqual(expected_output, output)

    async def test_assert_bytes_run(self):
        await self.set_up_contract('AssertBytes.py')

        result, _ = await self.call('Main', [b'unittest'], return_type=bytes)
        self.assertEqual(b'unittest', result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('Main', [b''], return_type=bytes)

    def test_assert_list_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.LDARG0     # return len(a)
            + Opcode.SIZE
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertList.py')
        self.assertEqual(expected_output, output)

    async def test_assert_list_run(self):
        await self.set_up_contract('AssertList.py')

        result, _ = await self.call('Main', [[1,2,3]], return_type=int)
        self.assertEqual(3, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('Main', [[]], return_type=int)

    def test_assert_dict_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.LDARG0     # return len(a)
            + Opcode.SIZE
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertDict.py')
        self.assertEqual(expected_output, output)

    async def test_assert_dict_run(self):
        await self.set_up_contract('AssertDict.py')

        result, _ = await self.call('Main', [{1: 2, 2: 5}], return_type=int)
        self.assertEqual(2, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('Main', [{}], return_type=int)

    def test_assert_any_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Array
            + Opcode.JMPIF + Integer(12).to_byte_array(signed=True, min_length=1)
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Map
            + Opcode.JMPIF + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Struct
            + Opcode.JMPIFNOT + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssertAny.py')
        self.assertEqual(expected_output, output)

    async def test_assert_any_run(self):
        await self.set_up_contract('AssertAny.py')

        result, _ = await self.call('Main', [True], return_type=None)
        self.assertIsNone(result)

    async def test_boa2_throw_test(self):
        await self.set_up_contract('ThrowBoa2Test.py')

        result, _ = await self.call('main', [1], return_type=bool)
        self.assertEqual(True, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('main', [4], return_type=bool)
