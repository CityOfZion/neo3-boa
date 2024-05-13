import json

from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.wallet import account

from boa3.internal import constants
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import annotation, boatestcase, event, stackitem


class TestContractManagementContract(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/contractmanagement'
    account: account.Account

    @classmethod
    def setupTestCase(cls):
        cls.account = cls.node.wallet.account_new(label='test', password='123')
        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account.script_hash, 100)

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        expected = types.UInt160(constants.MANAGEMENT_SCRIPT)
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_get_hash_deprecated(self):
        await self.set_up_contract('GetHashDeprecated.py')
        self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'GetHashDeprecated.py')

        expected = types.UInt160(constants.MANAGEMENT_SCRIPT)
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_get_minimum_deployment_fee(self):
        await self.set_up_contract('GetMinimumDeploymentFee.py')

        minimum_cost = 10 * 10 ** 8  # minimum deployment cost is 10 GAS right now
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(minimum_cost, result)

    def test_get_minimum_deployment_fee_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'GetMinimumDeploymentFeeTooManyArguments.py')

    async def test_get_contract(self):
        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')

        await self.set_up_contract('GetContract.py')
        call_hash = await self.compile_and_deploy(call_contract_path)

        nef, manifest = self.get_serialized_output(call_contract_path)
        manifest = stackitem.from_manifest(manifest)
        result, _ = await self.call('main', [bytes(20)], return_type=None)
        self.assertIsNone(result)

        result, _ = await self.call('main', [call_hash], return_type=annotation.Contract)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        self.assertEqual(manifest, result[4])

    async def test_has_method(self):
        await self.set_up_contract('HasMethod.py')
        call_hash = await self.compile_and_deploy('test_sc/arithmetic_test', 'Addition.py')

        test_method = 'add'
        test_parameter_count = 2
        result, _ = await self.call('main', [bytes(20), test_method, test_parameter_count], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [call_hash, test_method, test_parameter_count], return_type=bool)
        self.assertEqual(True, result)

    async def test_deploy_contract(self):
        await self.set_up_contract('DeployContract.py')
        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Subtraction.py')

        self.compile_and_save(call_contract_path)
        nef_file, manifest = self.get_serialized_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        manifest = stackitem.from_manifest(manifest)
        result, notifications = await self.call('Main',
                                                [nef_file, arg_manifest, None],
                                                return_type=annotation.Contract
                                                )

        deploy_events = self.filter_events(notifications,
                                           event_name='Deploy',
                                           notification_type=event.DeployEvent
                                           )
        self.assertEqual(1, len(deploy_events))

        self.assertEqual(5, len(result))
        self.assertEqual(0, result[1])  # contract update counter must be zero on deploy
        self.assertEqual(nef_file, result[3])
        self.assertEqual(manifest, result[4])

    async def test_deploy_contract_data_deploy(self):
        await self.set_up_contract('DeployContract.py')
        call_contract_path = self.get_contract_path('boa3_test/test_sc/interop_test/contract', 'NewContract.py')

        self.compile_and_save(call_contract_path)
        nef_file, manifest = self.get_serialized_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()
        manifest = stackitem.from_manifest(manifest)

        data = 'some sort of data'
        result, notifications = await self.call('Main',
                                                [nef_file, arg_manifest, data],
                                                return_type=annotation.Contract
                                                )
        self.assertEqual(5, len(result))
        self.assertEqual(0, result[1])  # contract update counter must be zero on deploy
        self.assertEqual(nef_file, result[3])
        self.assertEqual(manifest, result[4])

        deploy_events = self.filter_events(notifications,
                                           event_name='Deploy',
                                           notification_type=event.DeployEvent
                                           )
        self.assertEqual(1, len(deploy_events))

        notifies = self.filter_events(notifications,
                                      event_name='notify',
                                      notification_type=boatestcase.BoaTestEvent
                                      )
        self.assertEqual(2, len(notifies))
        self.assertEqual(False, notifies[0].state[0])  # not updated
        self.assertEqual(data, notifies[1].state[0])  # data

    def test_deploy_contract_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'DeployContractTooManyArguments.py')

    def test_deploy_contract_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'DeployContractTooFewArguments.py')

    async def test_update_contract(self):
        await self.set_up_contract('UpdateContract.py')

        updated_method = 'new_method'
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call(updated_method, [], return_type=None)

        self.assertRegex(str(context.exception), fr"method not found: {updated_method}/\d+")

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_serialized_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        result, notifications = await self.call('update',
                                                [new_nef, arg_manifest, None],
                                                return_type=None,
                                                signing_accounts=[self.genesis]
                                                )
        self.assertIsNone(result)
        update_events = self.filter_events(notifications,
                                           event_name='Update',
                                           notification_type=event.UpdateEvent
                                           )
        self.assertEqual(1, len(update_events))
        self.assertEqual(self.contract_hash, update_events[0].updated_contract)

        result, _ = await self.call(updated_method, [], return_type=int)
        self.assertEqual(42, result)

    async def test_update_contract_data_deploy(self):
        await self.set_up_contract('UpdateContract.py', signing_account=self.account)

        updated_method = 'new_method'
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call(updated_method, [], return_type=int)

        self.assertRegex(str(context.exception), fr"method not found: {updated_method}/\d+")

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_serialized_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        data = 'this function was deployed'
        result, notifications = await self.call('update', [new_nef, arg_manifest, data], return_type=None)
        self.assertIsNone(result)
        update_events = self.filter_events(notifications,
                                           event_name='Update',
                                           notification_type=event.UpdateEvent
                                           )
        self.assertEqual(1, len(update_events))
        self.assertEqual(self.contract_hash, update_events[0].updated_contract)

        notifies = self.filter_events(notifications,
                                      event_name='notify',
                                      notification_type=boatestcase.BoaTestEvent
                                      )
        self.assertEqual(2, len(notifies))
        self.assertEqual(True, notifies[0].state[0])
        self.assertEqual(data, notifies[1].state[0])

    def test_update_contract_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'UpdateContractTooManyArguments.py')

    def test_update_contract_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'UpdateContractTooFewArguments.py')

    async def test_destroy_contract(self):
        await self.set_up_contract('DestroyContract.py')

        contract_hash = self.contract_hash
        result, notifications = await self.call('Main', [], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)
        destroy_events = self.filter_events(notifications,
                                            event_name='Destroy',
                                            notification_type=event.DestroyEvent
                                            )
        self.assertEqual(1, len(destroy_events))
        self.assertEqual(contract_hash, destroy_events[0].destroyed_contract)

        call_contract = await self.compile_and_deploy('boa3_test/test_sc/interop_test/contract', 'CallScriptHash.py')
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main',
                            [contract_hash, 'Main', []],
                            return_type=None,
                            target_contract=call_contract
                            )

        self.assertRegex(str(context.exception), f'called contract {contract_hash} not found')

    def test_destroy_contract_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'DestroyContractTooManyArguments.py')
