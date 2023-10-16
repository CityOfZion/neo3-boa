from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestOptional(BoaTest):
    default_folder: str = 'test_sc/optional_test'

    def test_optional_return(self):
        path, _ = self.get_deploy_file_paths('OptionalReturn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append('str')
        invokes.append(runner.call_contract(path, 'main', 2))
        expected_results.append(123)
        invokes.append(runner.call_contract(path, 'main', 3))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'union_test', 1))
        expected_results.append('str')
        invokes.append(runner.call_contract(path, 'union_test', 2))
        expected_results.append(123)
        invokes.append(runner.call_contract(path, 'union_test', 3))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_optional_variable_reassign(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH2  # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH2  # b = a
            + Opcode.STLOC1
            + Opcode.PUSHNULL  # c = None
            + Opcode.STLOC2
            + Opcode.LDLOC2  # b = c
            + Opcode.STLOC1
            + Opcode.RET  # return
        )

        path = self.get_contract_path('OptionalVariableReassign.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_optional_variable_argument(self):
        path, _ = self.get_deploy_file_paths('OptionalVariableArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'unittest'))
        expected_results.append('string')
        invokes.append(runner.call_contract(path, 'main', 123))
        expected_results.append('int')
        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append('None')

        invokes.append(runner.call_contract(path, 'union_test', 'unittest'))
        expected_results.append('string')
        invokes.append(runner.call_contract(path, 'union_test', 123))
        expected_results.append('int')
        invokes.append(runner.call_contract(path, 'union_test', None))
        expected_results.append('None')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_optional_isinstance_validation(self):
        path, _ = self.get_deploy_file_paths('OptionalIsInstanceValidation.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'unittest'))
        expected_results.append('unittest')
        invokes.append(runner.call_contract(path, 'main', 123))
        expected_results.append('int')
        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append('None')

        invokes.append(runner.call_contract(path, 'union_test', 'unittest'))
        expected_results.append('unittest')
        invokes.append(runner.call_contract(path, 'union_test', 123))
        expected_results.append('int')
        invokes.append(runner.call_contract(path, 'union_test', None))
        expected_results.append('None')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_optional_inside_dict(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0  # return a
            + Opcode.RET
        )

        path = self.get_contract_path('OptionalArgumentInsideDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', {}))
        expected_results.append({})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
