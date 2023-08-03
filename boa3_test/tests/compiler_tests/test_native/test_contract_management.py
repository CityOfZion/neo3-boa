import json

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestContractManagementContract(BoaTest):
    default_folder: str = 'test_sc/native_test/contractmanagement'

    def test_get_hash(self):
        path, _ = self.get_deploy_file_paths('GetHash.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(constants.MANAGEMENT_SCRIPT)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_minimum_deployment_fee(self):
        path, _ = self.get_deploy_file_paths('GetMinimumDeploymentFee.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        minimum_cost = 10 * 10 ** 8  # minimum deployment cost is 10 GAS right now
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(minimum_cost)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_minimum_deployment_fee_too_many_parameters(self):
        path = self.get_contract_path('GetMinimumDeploymentFeeTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_contract(self):
        path, _ = self.get_deploy_file_paths('GetContract.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', bytes(20)))
        expected_results.append(None)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        nef, manifest = self.get_bytes_output(call_contract_path)

        call_contract_path, _ = self.get_deploy_file_paths(call_contract_path)
        contract = runner.deploy_contract(call_contract_path)
        runner.update_contracts(export_checkpoint=True)
        call_hash = contract.script_hash

        invoke = runner.call_contract(path, 'main', call_hash)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        result = invoke.result
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_has_method(self):
        path, _ = self.get_deploy_file_paths('HasMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        call_contract_path, _ = self.get_deploy_file_paths('test_sc/arithmetic_test', 'Addition.py')
        contract = runner.deploy_contract(call_contract_path)
        runner.update_contracts(export_checkpoint=True)
        call_hash = contract.script_hash

        test_method = 'add'
        test_parameter_count = 2
        invokes.append(runner.call_contract(path, 'main', bytes(20), test_method, test_parameter_count))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', call_hash, test_method, test_parameter_count))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_deploy_contract(self):
        path, _ = self.get_deploy_file_paths('DeployContract.py')
        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')

        self.compile_and_save(call_contract_path)
        nef_file, manifest = self.get_bytes_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'Main', nef_file, arg_manifest, None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        result = invoke.result
        self.assertEqual(5, len(result))
        self.assertEqual(nef_file, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_deploy_contract_data_deploy(self):
        path, _ = self.get_deploy_file_paths('DeployContract.py')
        call_contract_path = self.get_contract_path('boa3_test/test_sc/interop_test/contract', 'NewContract.py')

        self.compile_and_save(call_contract_path)
        nef_file, manifest = self.get_bytes_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        runner = BoaTestRunner(runner_id=self.method_name())
        runner.file_name = 'test_create_contract'

        data = 'some sort of data'
        invoke = runner.call_contract(path, 'Main', nef_file, arg_manifest, data)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        result = invoke.result
        self.assertEqual(5, len(result))
        self.assertEqual(nef_file, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

        notifies = runner.get_events('notify')
        self.assertEqual(2, len(notifies))
        self.assertEqual(False, notifies[0].arguments[0])  # not updated
        self.assertEqual(data, notifies[1].arguments[0])  # data

    def test_deploy_contract_too_many_parameters(self):
        path = self.get_contract_path('DeployContractTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_deploy_contract_too_few_parameters(self):
        path = self.get_contract_path('DeployContractTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_update_contract(self):
        path, _ = self.get_deploy_file_paths('UpdateContract.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.call_contract(path, 'new_method')
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.FORMAT_METHOD_DOESNT_EXIST_IN_CONTRACT_MSG_REGEX_PREFIX.format('new_method'))

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_bytes_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        invokes.append(runner.call_contract(path, 'update', new_nef, arg_manifest, None))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'new_method'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_update_contract_data_deploy(self):
        path, _ = self.get_deploy_file_paths('UpdateContract.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.call_contract(path, 'new_method')
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.FORMAT_METHOD_DOESNT_EXIST_IN_CONTRACT_MSG_REGEX_PREFIX.format('new_method'))

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        new_nef, new_manifest = self.get_bytes_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        data = 'this function was deployed'
        invokes.append(runner.call_contract(path, 'update', new_nef, arg_manifest, data))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        notifies = runner.get_events('notify')
        self.assertEqual(2, len(notifies))
        self.assertEqual(True, notifies[0].arguments[0])
        self.assertEqual(data, notifies[1].arguments[0])

    def test_update_contract_too_many_parameters(self):
        path = self.get_contract_path('UpdateContractTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_update_contract_too_few_parameters(self):
        path = self.get_contract_path('UpdateContractTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_destroy_contract(self):
        path, _ = self.get_deploy_file_paths('DestroyContract.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        call = runner.call_contract(path, 'Main')
        invokes.append(call)
        expected_results.append(None)

        runner.execute(clear_invokes=False)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        script_hash = call.invoke.contract.script_hash

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        call_contract_path, _ = self.get_deploy_file_paths('boa3_test/test_sc/interop_test/contract', 'CallScriptHash.py')
        runner.call_contract(call_contract_path, 'Main',
                             script_hash, 'Main', [])
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.CALLED_CONTRACT_DOES_NOT_EXIST_MSG}')

    def test_destroy_contract_too_many_parameters(self):
        path = self.get_contract_path('DestroyContractTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)
