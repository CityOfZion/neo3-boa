from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestMath(BoaTest):

    default_folder: str = 'test_sc/math_test'

    def test_no_import(self):
        path = self.get_contract_path('NoImport.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    # region pow test

    def test_pow_method(self):
        path, _ = self.get_deploy_file_paths('Pow.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        import math

        base = 1
        exponent = 4
        invokes.append(runner.call_contract(path, 'main', base, exponent))
        expected_results.append(math.pow(base, exponent))

        base = 5
        exponent = 2
        invokes.append(runner.call_contract(path, 'main', base, exponent))
        expected_results.append(math.pow(base, exponent))

        base = -2
        exponent = 2
        invokes.append(runner.call_contract(path, 'main', base, exponent))
        expected_results.append(math.pow(base, exponent))

        base = -2
        exponent = 3
        invokes.append(runner.call_contract(path, 'main', base, exponent))
        expected_results.append(math.pow(base, exponent))

        base = 2
        exponent = 0
        invokes.append(runner.call_contract(path, 'main', base, exponent))
        expected_results.append(math.pow(base, exponent))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_pow_method_from_math(self):
        path, _ = self.get_deploy_file_paths('PowFromMath.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from math import pow

        base = 2
        exponent = 3
        invokes.append(runner.call_contract(path, 'main', base, exponent))
        expected_results.append(pow(base, exponent))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region sqrt test

    def test_sqrt_method(self):
        path, _ = self.get_deploy_file_paths('Sqrt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from math import sqrt

        expected_result = int(sqrt(0))
        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append(expected_result)

        expected_result = int(sqrt(1))
        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(expected_result)

        expected_result = int(sqrt(3))
        invokes.append(runner.call_contract(path, 'main', 3))
        expected_results.append(expected_result)

        expected_result = int(sqrt(4))
        invokes.append(runner.call_contract(path, 'main', 4))
        expected_results.append(expected_result)

        expected_result = int(sqrt(8))
        invokes.append(runner.call_contract(path, 'main', 8))
        expected_results.append(expected_result)

        expected_result = int(sqrt(10))
        invokes.append(runner.call_contract(path, 'main', 10))
        expected_results.append(expected_result)

        val = 25
        expected_result = int(sqrt(val))
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', -1)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_CANNOT_BE_NEGATIVE_MSG)

    def test_sqrt_method_from_math(self):
        path, _ = self.get_deploy_file_paths('SqrtFromMath.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from math import sqrt

        val = 25
        expected_result = int(sqrt(val))
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion
