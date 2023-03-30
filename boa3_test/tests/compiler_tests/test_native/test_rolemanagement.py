from boa3.boa3 import Boa3
from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.contracts import CallFlags
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestRoleManagementClass(BoaTest):
    default_folder: str = 'test_sc/native_test/rolemanagement'

    def test_get_hash(self):
        path = self.get_contract_path('GetHash.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(constants.ROLE_MANAGEMENT, result)

    def test_get_designated_by_role(self):
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String(Interop.GetDesignatedByRole.method_name).to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('GetDesignatedByRole.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_get_designated_by_role_too_many_parameters(self):
        path = self.get_contract_path('GetDesignatedByRoleTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_designated_by_role_too_few_parameters(self):
        path = self.get_contract_path('GetDesignatedByRoleTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)
