from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


class TestNativeContracts(BoaTest):
    default_folder: str = 'test_sc/native_test/oracle'
    ORACLE_CONTRACT_NAME = 'OracleContract'

    def test_get_hash(self):
        path, _ = self.get_deploy_file_paths('GetHash.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(constants.ORACLE_SCRIPT)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_oracle_request(self):
        path, _ = self.get_deploy_file_paths('OracleRequestCall.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000

        oracle_invoke = runner.call_contract(path, 'oracle_call',
                                             test_url, request_filter, callback, None, gas_for_response)
        invokes.append(oracle_invoke)
        expected_results.append(None)

        runner.execute(clear_invokes=False)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        contract_script = oracle_invoke.invoke.contract.script_hash

        oracle_requests = runner.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[0].arguments))
        self.assertEqual(contract_script, oracle_requests[0].arguments[1])
        self.assertEqual(test_url, oracle_requests[0].arguments[2])
        self.assertEqual(request_filter, oracle_requests[0].arguments[3])

        test_url = 'abc'
        request_filter = 'ABC'
        callback = 'test_callback'
        gas_for_response = 1_0000000

        invokes.append(runner.call_contract(path, 'oracle_call',
                                            test_url, request_filter, callback, None, gas_for_response))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        oracle_requests = runner.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(2, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[1].arguments))

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_oracle_request_url_mismatched_type(self):
        path = self.get_contract_path('OracleRequestUrlMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_oracle_request_filter_mismatched_type(self):
        path = self.get_contract_path('OracleRequestFilterMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_oracle_request_callback_mismatched_type(self):
        path = self.get_contract_path('OracleRequestCallCallbackMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_oracle_request_gas_mismatched_type(self):
        path = self.get_contract_path('OracleRequestGasMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_import_interop_oracle(self):
        path, _ = self.get_deploy_file_paths('ImportOracle.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000

        oracle_invoke = runner.call_contract(path, 'oracle_call',
                                             test_url, request_filter, callback, None, gas_for_response)
        invokes.append(oracle_invoke)
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        contract_script = oracle_invoke.invoke.contract.script_hash

        oracle_requests = runner.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[0].arguments))
        self.assertEqual(contract_script, oracle_requests[0].arguments[1])
        self.assertEqual(test_url, oracle_requests[0].arguments[2])
        self.assertEqual(request_filter, oracle_requests[0].arguments[3])

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_interop_oracle_package(self):
        path, _ = self.get_deploy_file_paths('ImportInteropOracle.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000

        oracle_invoke = runner.call_contract(path, 'oracle_call',
                                             test_url, request_filter, callback, None, gas_for_response)
        invokes.append(oracle_invoke)
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        contract_script = oracle_invoke.invoke.contract.script_hash

        oracle_requests = runner.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[0].arguments))
        self.assertEqual(contract_script, oracle_requests[0].arguments[1])
        self.assertEqual(test_url, oracle_requests[0].arguments[2])
        self.assertEqual(request_filter, oracle_requests[0].arguments[3])

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_oracle_get_price(self):
        from boa3.internal.neo3.contracts import CallFlags
        from boa3.internal.model.builtin.interop.oracle.oraclegetpricemethod import OracleGetPriceMethod

        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String(OracleGetPriceMethod().method_name).to_bytes()

        expected_output = (
            Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('OracleGetPrice.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(invoke.result, int)
