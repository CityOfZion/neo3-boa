from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


class TestPolicyContract(BoaTest):
    default_folder: str = 'test_sc/native_test/policy'

    def test_get_hash(self):
        path, _ = self.get_deploy_file_paths('GetHash.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(constants.POLICY_SCRIPT)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_exec_fee_factor(self):
        path, _ = self.get_deploy_file_paths('GetExecFeeFactor.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(invoke.result, int)

    def test_get_exec_fee_too_many_parameters(self):
        path = self.get_contract_path('GetExecFeeFactorTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_fee_per_byte(self):
        path, _ = self.get_deploy_file_paths('GetFeePerByte.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(invoke.result, int)

    def test_get_fee_per_byte_too_many_parameters(self):
        path = self.get_contract_path('GetFeePerByteTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_storage_price(self):
        path, _ = self.get_deploy_file_paths('GetStoragePrice.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(invoke.result, int)

    def test_get_storage_price_too_many_parameters(self):
        path = self.get_contract_path('GetStoragePriceTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_is_blocked(self):
        path, _ = self.get_deploy_file_paths('IsBlocked.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', bytes(20)))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_is_blocked_mismatched_type(self):
        path = self.get_contract_path('IsBlockedMismatchedTypeInt.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

        path = self.get_contract_path('IsBlockedMismatchedTypeStr.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

        path = self.get_contract_path('IsBlockedMismatchedTypeBool.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_is_blocked_too_many_parameters(self):
        path = self.get_contract_path('IsBlockedTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_is_blocked_too_few_parameters(self):
        path = self.get_contract_path('IsBlockedTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)
