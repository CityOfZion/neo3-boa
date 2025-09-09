from neo3.core import types

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo3.contracts.native import Role
from boa3_test.tests import boatestcase


class TestRoleManagementClass(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/rolemanagement'

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        expected = types.UInt160(constants.ROLE_MANAGEMENT)
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    def test_get_designated_by_role(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        output, _ = self.assertCompile('GetDesignatedByRole.py')
        self.assertEqual(expected_output, output)

    def test_get_designated_by_role_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'GetDesignatedByRoleTooManyArguments.py')

    def test_get_designated_by_role_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'GetDesignatedByRoleTooFewArguments.py')

    async def test_role_instantiate(self):
        await self.set_up_contract('RoleInstantiate.py')

        result, _ = await self.call('main', [Role.STATE_VALIDATOR], return_type=int)
        self.assertEqual(Role.STATE_VALIDATOR, result)

        result, _ = await self.call('main', [Role.ORACLE], return_type=int)
        self.assertEqual(Role.ORACLE, result)

        result, _ = await self.call('main', [Role.NEO_FS_ALPHABET_NODE], return_type=int)
        self.assertEqual(Role.NEO_FS_ALPHABET_NODE, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [1], return_type=int)

        self.assertRegex(str(context.exception), "Invalid Role parameter value")

    async def test_role_not(self):
        await self.set_up_contract('RoleNot.py')

        for role in Role:
            result, _ = await self.call('main', [role], return_type=int)
            self.assertEqual(~role, result)

    def test_import_contracts_role_management(self):
        expected_output = (
                Opcode.INITSLOT
                + b'\x00\x02'
                + Opcode.LDARG1
                + Opcode.LDARG0
                + Opcode.CALLT + b'\x00\x00'
                + Opcode.RET
        )

        output, _ = self.assertCompile('ImportContractsRoleManagement.py')
        self.assertEqual(expected_output, output)

    def test_import_sc_contracts_role_management(self):
        expected_output = (
                Opcode.INITSLOT
                + b'\x00\x02'
                + Opcode.LDARG1
                + Opcode.LDARG0
                + Opcode.CALLT + b'\x00\x00'
                + Opcode.RET
        )

        output, _ = self.assertCompile('ImportScContractsRoleManagement.py')
        self.assertEqual(expected_output, output)
