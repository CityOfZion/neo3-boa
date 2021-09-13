import json

from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.neo.cryptography import hash160
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct
from boa3_test.tests.test_classes.testengine import TestEngine


class TestContractManagementContract(BoaTest):

    default_folder: str = 'test_sc/native_test/contractmanagement'

    def test_get_minimum_deployment_fee(self):
        path = self.get_contract_path('GetMinimumDeploymentFee.py')
        engine = TestEngine()

        minimum_cost = 10 * 10**8   # minimum deployment cost is 10 GAS right now
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(minimum_cost, result)

    def test_get_minimum_deployment_fee_too_many_parameters(self):
        path = self.get_contract_path('GetMinimumDeploymentFeeTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_contract(self):
        path = self.get_contract_path('GetContract.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', bytes(20))
        self.assertIsNone(result)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        Boa3.compile_and_save(call_contract_path)

        script, manifest = self.get_output(call_contract_path)
        nef, manifest = self.get_bytes_output(call_contract_path)
        call_hash = hash160(script)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'main', call_hash)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_deploy_contract(self):
        path = self.get_contract_path('DeployContract.py')
        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        Boa3.compile_and_save(call_contract_path)

        nef_file, manifest = self.get_bytes_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', nef_file, arg_manifest, None)

        self.assertEqual(5, len(result))
        self.assertEqual(nef_file, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_deploy_contract_data_deploy(self):
        path = self.get_contract_path('DeployContract.py')
        call_contract_path = self.get_contract_path('boa3_test/test_sc/interop_test/contract', 'NewContract.py')
        self.compile_and_save(call_contract_path)

        nef_file, manifest = self.get_bytes_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        engine = TestEngine()
        data = 'some sort of data'
        result = self.run_smart_contract(engine, path, 'Main', nef_file, arg_manifest, data)

        self.assertEqual(5, len(result))
        self.assertEqual(nef_file, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

        notifies = engine.get_events('notify')
        self.assertEqual(2, len(notifies))
        self.assertEqual(False, notifies[0].arguments[0])   # not updated
        self.assertEqual(data, notifies[1].arguments[0])    # data
        result = self.run_smart_contract(engine, call_contract_path, 'main')
        self.assertEqual(data, result)

    def test_deploy_contract_too_many_parameters(self):
        path = self.get_contract_path('DeployContractTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_deploy_contract_too_few_parameters(self):
        path = self.get_contract_path('DeployContractTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_update_contract(self):
        path = self.get_contract_path('UpdateContract.py')
        engine = TestEngine()
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'new_method')

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_bytes_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        result = self.run_smart_contract(engine, path, 'update', new_nef, arg_manifest, None)
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'new_method')
        self.assertEqual(42, result)

    def test_update_contract_data_deploy(self):
        path = self.get_contract_path('UpdateContract.py')
        engine = TestEngine()
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'new_method')

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_bytes_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        data = 'this function was deployed'
        result = self.run_smart_contract(engine, path, 'update', new_nef, arg_manifest, data)
        self.assertIsVoid(result)
        notifies = engine.get_events('notify')
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
        path = self.get_contract_path('DestroyContract.py')
        output = Boa3.compile(path)
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

        script_hash = hash160(output)
        call_contract_path = self.get_contract_path('boa3_test/test_sc/interop_test/contract', 'CallScriptHash.py')
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, call_contract_path, 'Main',
                                    script_hash, 'Main', [])

    def test_destroy_contract_too_many_parameters(self):
        path = self.get_contract_path('DestroyContractTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)
