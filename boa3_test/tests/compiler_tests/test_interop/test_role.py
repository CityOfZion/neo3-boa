from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests import boatestcase


class TestRoleInterop(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/interop_test/role'

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

    def test_import_role(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        output, _ = self.assertCompile('ImportRole.py')
        self.assertEqual(expected_output, output)

        output, _ = self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'ImportRole.py')
        self.assertEqual(expected_output, output)

    def test_import_interop_role(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        output, _ = self.assertCompile('ImportInteropRole.py')
        self.assertEqual(expected_output, output)
        
        output, _ = self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'ImportInteropRole.py')
        self.assertEqual(expected_output, output)
