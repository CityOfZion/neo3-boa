from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


class TestBuiltinMethod(BoaTest):
    default_folder: str = 'test_sc/boa_built_in_methods_test'

    def test_abort(self):
        path, _ = self.get_deploy_file_paths('Abort.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append(123)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', True)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)

    def test_deploy_def(self):
        path, _ = self.get_deploy_file_paths('DeployDef.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_var'))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_deploy_def_incorrect_signature(self):
        path = self.get_contract_path('DeployDefWrongSignature.py')
        self.assertCompilerLogs(CompilerError.InternalIncorrectSignature, path)

    def test_will_not_compile(self):
        path = self.get_contract_path('WillNotCompile.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    # region math builtins

    def test_sqrt_method(self):
        path, _ = self.get_deploy_file_paths('Sqrt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

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
        runner = NeoTestRunner(runner_id=self.method_name())

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

    def test_decimal_floor_method(self):
        path, _ = self.get_deploy_file_paths('DecimalFloor.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from math import floor

        value = 4.2
        decimals = 8

        multiplier = 10 ** decimals
        value_floor = int(floor(value)) * multiplier
        integer_value = int(value * multiplier)
        invokes.append(runner.call_contract(path, 'main', integer_value, decimals))
        expected_results.append(value_floor)

        decimals = 12

        multiplier = 10 ** decimals
        value_floor = int(floor(value)) * multiplier
        integer_value = int(value * multiplier)
        invokes.append(runner.call_contract(path, 'main', integer_value, decimals))
        expected_results.append(value_floor)

        value = -3.983541

        multiplier = 10 ** decimals
        value_floor = int(floor(value) * multiplier)
        integer_value = int(value * multiplier)
        invokes.append(runner.call_contract(path, 'main', integer_value, decimals))
        expected_results.append(value_floor)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # negative decimals will raise an exception
        runner.call_contract(path, 'main', integer_value, -1)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        from boa3.internal.model.builtin.builtin import Builtin
        self.assertRegex(runner.error, f'{Builtin.BuiltinMathFloor.exception_message}$')

    def test_decimal_ceil_method(self):
        path, _ = self.get_deploy_file_paths('DecimalCeiling.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from math import ceil

        value = 4.2
        decimals = 8

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value)) * multiplier
        integer_value = int(value * multiplier)
        invokes.append(runner.call_contract(path, 'main', integer_value, decimals))
        expected_results.append(value_ceiling)

        decimals = 12

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value)) * multiplier
        integer_value = int(value * multiplier)
        invokes.append(runner.call_contract(path, 'main', integer_value, decimals))
        expected_results.append(value_ceiling)

        value = -3.983541

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value) * multiplier)
        integer_value = int(value * multiplier)
        invokes.append(runner.call_contract(path, 'main', integer_value, decimals))
        expected_results.append(value_ceiling)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # negative decimals will raise an exception
        runner.call_contract(path, 'main', integer_value, -1)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        from boa3.internal.model.builtin.builtin import Builtin
        self.assertRegex(runner.error, f'{Builtin.BuiltinMathCeil.exception_message}$')

    # endregion
