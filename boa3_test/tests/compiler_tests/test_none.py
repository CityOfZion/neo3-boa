from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestNone(BoaTest):
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

        path = self.get_contract_path('VariableNone.py')
        output = self.compile(path)
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

        path = self.get_contract_path('NoneTuple.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_none_identity(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.ISNULL
            + Opcode.RET        # return
        )

        path = self.get_contract_path('NoneIdentity.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', None))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', '5'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_none_not_identity(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.ISNULL
            + Opcode.NOT
            + Opcode.RET        # return
        )

        path = self.get_contract_path('NoneNotIdentity.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', None))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', '5'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_none_equality(self):
        path = self.get_contract_path('NoneEquality.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_mismatched_type_int_operation(self):
        path = self.get_contract_path('MismatchedTypesInOperation.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_reassign_variable_with_none(self):
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

        path = self.get_contract_path('ReassignVariableWithNone.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reassign_variable_after_none(self):
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
        path = self.get_contract_path('ReassignVariableAfterNone.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_none_test(self):
        path = self.get_contract_path('NoneBoa2Test.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
