from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestMatchCase(BoaTest):
    default_folder: str = 'test_sc/match_case_test'

    def test_any_type_match_case(self):
        path, _ = self.get_deploy_file_paths('AnyTypeMatchCase.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append("True")

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append("one")

        invokes.append(runner.call_contract(path, 'main', "2"))
        expected_results.append("2 string")

        invokes.append(runner.call_contract(path, 'main', 'other value'))
        expected_results.append("other")

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_type_match_case(self):
        path, _ = self.get_deploy_file_paths('BoolTypeMatchCase.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append("True")

        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append("False")

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_int_type_match_case(self):
        path, _ = self.get_deploy_file_paths('IntTypeMatchCase.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 10))
        expected_results.append("ten")

        invokes.append(runner.call_contract(path, 'main', -10))
        expected_results.append("minus ten")

        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append("zero")

        invokes.append(runner.call_contract(path, 'main', 123))
        expected_results.append("other")
        invokes.append(runner.call_contract(path, 'main', -999))
        expected_results.append("other")

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_type_match_case(self):
        path, _ = self.get_deploy_file_paths('StrTypeMatchCase.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'first'))
        expected_results.append("1")

        invokes.append(runner.call_contract(path, 'main', 'second'))
        expected_results.append("2")

        invokes.append(runner.call_contract(path, 'main', 'third'))
        expected_results.append("3")

        invokes.append(runner.call_contract(path, 'main', 'another value'))
        expected_results.append("other")
        invokes.append(runner.call_contract(path, 'main', 'unit test'))
        expected_results.append("other")

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_outer_var_inside_match(self):
        path, _ = self.get_deploy_file_paths('OuterVariableInsideMatch.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append("String is: True")

        invokes.append(runner.call_contract(path, 'main', 10))
        expected_results.append("String is: 10")

        invokes.append(runner.call_contract(path, 'main', "2"))
        expected_results.append("String is: 2 string")

        invokes.append(runner.call_contract(path, 'main', 'another value'))
        expected_results.append("String is: other")
        invokes.append(runner.call_contract(path, 'main', 'unit test'))
        expected_results.append("String is: other")

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_var_existing_in_all_cases(self):
        path, _ = self.get_deploy_file_paths('VarExistingInAllCases.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append("True")

        invokes.append(runner.call_contract(path, 'main', 10))
        expected_results.append("10")

        invokes.append(runner.call_contract(path, 'main', "2"))
        expected_results.append("2 string")

        invokes.append(runner.call_contract(path, 'main', 'another value'))
        expected_results.append("other")
        invokes.append(runner.call_contract(path, 'main', 'unit test'))
        expected_results.append("other")

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_unsupported_case(self):
        path = self.get_contract_path('UnsupportedCase.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)
