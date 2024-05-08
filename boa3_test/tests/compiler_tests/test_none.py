from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests import boatestcase


class TestNone(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/none_test'

    def test_variable_none(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHNULL
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('VariableNone.py')
        self.assertEqual(expected_output, output)

    def test_none_tuple(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHNULL   # a = (None, None, None)
            + Opcode.PUSHNULL
            + Opcode.PUSHNULL
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('NoneTuple.py')
        self.assertEqual(expected_output, output)

    def test_none_identity_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.ISNULL
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('NoneTestNoneIdentity.py')
        self.assertEqual(expected_output, output)

    async def test_none_identity_run(self):
        await self.set_up_contract('NoneTestNoneIdentity.py')

        result, _ = await self.call('Main', [None], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [5], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', ['5'], return_type=bool)
        self.assertEqual(False, result)

    def test_none_not_identity_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.ISNULL
            + Opcode.NOT
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('NoneTestNoneNotIdentity.py')
        self.assertEqual(expected_output, output)

    async def test_none_not_identity_run(self):
        await self.set_up_contract('NoneTestNoneNotIdentity.py')

        result, _ = await self.call('Main', [None], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [5], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', ['5'], return_type=bool)
        self.assertEqual(True, result)

    def test_none_equality(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'NoneEquality.py')

    def test_mismatched_type_int_operation(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MismatchedTypesInOperation.py')

    def test_reassign_variable_with_none_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH2          # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH4          # b = a * 2
            + Opcode.STLOC1
            + Opcode.PUSHNULL       # a = None
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('ReassignVariableWithNone.py')
        self.assertEqual(expected_output, output)

    async def test_reassign_variable_with_none_run(self):
        await self.set_up_contract('ReassignVariableWithNone.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertEqual(None, result)

    def test_reassign_variable_after_none_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHNULL       # a = None
            + Opcode.STLOC0
            + Opcode.PUSH2          # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH4          # b = a * 2
            + Opcode.STLOC1
            + Opcode.RET        # return
        )
        output, _ = self.assertCompile('ReassignVariableAfterNone.py')
        self.assertEqual(expected_output, output)

    async def test_reassign_variable_after_none_run(self):
        await self.set_up_contract('ReassignVariableAfterNone.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertEqual(None, result)

    def test_boa2_none_test(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'NoneBoa2Test.py')
