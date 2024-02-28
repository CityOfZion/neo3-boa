from dataclasses import dataclass

from neo3.api import noderpc
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.wallet import account

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests import boatestcase


def _deep_scan(iterable: [dict, list], key: str, list_of_values: list):
    """
    Used to get a similar result to the oracle filter JsonPath deep scan
    """
    if isinstance(iterable, dict):
        for key_inside in iterable:
            value = iterable[key_inside]

            if key_inside == key:
                list_of_values.append(value)
            elif isinstance(value, dict):
                _deep_scan(value, key, list_of_values)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        _deep_scan(item, key, list_of_values)
    elif isinstance(iterable, list):
        for item in iterable:
            if isinstance(item, dict):
                _deep_scan(item, key, list_of_values)


@dataclass
class OracleRequestEvent(boatestcase.BoaTestEvent):
    id: int
    request_contract: types.UInt160
    url: str
    filter: str

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification):
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


@dataclass
class OracleResponseEvent(boatestcase.BoaTestEvent):
    id: int
    original_tx: types.UInt256

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification):
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


class TestNativeContracts(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/oracle'
    ORACLE_CONTRACT_NAME = 'OracleContract'
    ORACLE_SCRIPT_HASH = types.UInt160(constants.ORACLE_SCRIPT)

    owner: account.Account

    @classmethod
    def setupTestCase(cls):
        cls.owner = cls.node.wallet.account_new(label='owner', password='123')

        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 100)

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        expected = self.ORACLE_SCRIPT_HASH
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_oracle_request(self):
        await self.set_up_contract('OracleRequestCall.py')

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000

        result, notifications = await self.call('oracle_call',
                                                [test_url, request_filter, callback, None, gas_for_response],
                                                return_type=bool
                                                )
        self.assertEqual(True, result)
        contract_script = self.contract_hash

        oracle_requests = self.filter_events(notifications,
                                             event_name='OracleRequest',
                                             origin=self.ORACLE_SCRIPT_HASH,
                                             notification_type=OracleRequestEvent
                                             )

        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(contract_script, oracle_requests[0].request_contract)
        self.assertEqual(test_url, oracle_requests[0].url)
        self.assertEqual(request_filter, oracle_requests[0].filter)

        test_url = 'abc'
        request_filter = 'ABC'
        callback = 'test_callback'
        gas_for_response = 1_0000000

        result, notifications = await self.call('oracle_call',
                                                [test_url, request_filter, callback, None, gas_for_response],
                                                return_type=bool
                                                )
        self.assertEqual(True, result)

        oracle_requests = self.filter_events(notifications,
                                             event_name='OracleRequest',
                                             origin=self.ORACLE_SCRIPT_HASH,
                                             notification_type=OracleRequestEvent
                                             )

        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(contract_script, oracle_requests[0].request_contract)
        self.assertEqual(test_url, oracle_requests[0].url)
        self.assertEqual(request_filter, oracle_requests[0].filter)

    def test_oracle_response(self):
        from boa3.internal.neo3.vm import VMState
        from boa3_test.tests.test_drive import neoxp
        from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner

        path, _ = self.get_deploy_file_paths('OracleRequestCall.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_url = 'https://unittest.fake.url/api/0/'
        callback = 'callback_method'
        user_data = 'Any Data Here'
        gas_for_response = 1 * 10 ** 8

        OWNER = neoxp.utils.get_account_by_name('owner')
        genesis = neoxp.utils.get_account_by_name('genesis')
        runner.oracle_enable(genesis)

        runner.add_gas(OWNER.address, 1000 * 10 ** 8)

        invokes.append(runner.call_contract(path, 'oracle_call', test_url, None, callback, user_data, gas_for_response))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'get_storage'))
        expected_results.append(['', '', 0, ''])

        runner.execute(account=OWNER, add_invokes_to_batch=True)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        runner.update_contracts(export_checkpoint=True)

        path_json = path.replace(path.split(constants.PATH_SEPARATOR).pop(), 'OracleResponse.json')
        response_tx_ids = runner.oracle_response(test_url, path_json)

        with open(path_json) as f:
            import json
            json_data = json.loads(f.read())

        storage = runner.call_contract(path, 'get_storage')
        from boa3_test.tests.test_classes.transactionattribute.oracleresponse import OracleResponseCode

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        from boa3.internal.neo.vm.type.StackItem import StackItemType
        self.assertEqual(test_url, storage.result[0])
        self.assertEqual(f"{(StackItemType.ByteString + len(user_data).to_bytes(1,'little')).decode()}{user_data}",
                         storage.result[1])
        self.assertEqual(OracleResponseCode.Success, storage.result[2])
        self.assertEqual(json_data, json.loads(storage.result[3]))

        self.assertEqual(1, len(response_tx_ids))
        response_tx = runner.get_transaction(response_tx_ids[0])
        self.assertIsNotNone(response_tx)
        self.assertTrue(hasattr(response_tx, 'attributes'))

        response_tx_attr = response_tx.attributes[0].to_json()
        self.assertEqual('OracleResponse', response_tx_attr['type'])
        self.assertEqual(0, response_tx_attr['id'])
        self.assertEqual('Success', response_tx_attr['code'])
        self.assertEqual(json_data, response_tx_attr['result'])

    def test_oracle_response_filter(self):
        from boa3.internal.neo3.vm import VMState
        from boa3_test.tests.test_drive import neoxp
        from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner

        path, _ = self.get_deploy_file_paths('OracleRequestCall.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_url = 'https://unittest.fake.url/api/0/'
        callback = 'callback_method'
        user_data = 'Any Data Here'
        gas_for_response = 1 * 10 ** 8

        OWNER = neoxp.utils.get_account_by_name('owner')
        runner.add_gas(OWNER.address, 1000 * 10 ** 8)
        genesis = neoxp.utils.get_account_by_name('genesis')
        runner.oracle_enable(genesis)

        invokes.append(runner.call_contract(path, 'oracle_call', test_url, "$..book[-2:]", callback, user_data, gas_for_response))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'oracle_call', test_url, "$.store.book[*].author", callback, user_data, gas_for_response))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'oracle_call', test_url, "$.store.*", callback, user_data, gas_for_response))
        expected_results.append(True)

        runner.execute(account=OWNER, add_invokes_to_batch=True)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        runner.update_contracts(export_checkpoint=True)

        path_json = path.replace(path.split(constants.PATH_SEPARATOR).pop(), 'OracleResponse.json')
        response_tx_ids = runner.oracle_response(test_url, path_json)

        with open(path_json) as f:
            import json
            json_data = json.loads(f.read())

        storage = runner.call_contract(path, 'get_storage')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertNotEqual(['', '', '', ''], storage)
        self.assertEqual(3, len(response_tx_ids))

        # Oracle can filter Json with JsonPath,
        # Pythons json module doesn't use JsonPath, so it needs to be done manually
        response_tx_attributes = [runner.get_transaction(tx_id).attributes[0].to_json() for tx_id in response_tx_ids]

        books_inside_json = []
        _deep_scan(json_data, 'book', books_inside_json)

        # filter used was "$..book[-2:]"
        last_2_books_inside_book = [book
                                    for book_list in books_inside_json
                                    for index, book in enumerate(book_list)
                                    if index >= len(book_list) - 2]
        self.assertEqual(last_2_books_inside_book, response_tx_attributes[0]['result'])

        # filter used was "$.store.book[*].author"
        authors_of_books_in_store = [book['author'] for book in json_data['store']['book']]
        self.assertEqual(authors_of_books_in_store, response_tx_attributes[1]['result'])

        # filter used was "$.store.*"
        everything_inside_store = [json_data['store'][key] for key in json_data['store']]
        self.assertEqual(everything_inside_store, response_tx_attributes[2]['result'])

    async def test_oracle_request_invalid_gas(self):
        await self.set_up_contract('OracleRequestCall.py')

        test_url = 'https://unittest.fake.url/api/0/'
        callback = 'callback_method'
        user_data = 'Any Data Here'
        filter = "$.store.*"
        gas_for_response = 9999999  # GAS can not be lower than 0.1 GAS

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('oracle_call',
                            [test_url, filter, callback, user_data, gas_for_response],
                            return_type=bool
                            )

        self.assertRegex(str(context.exception), 'not enough gas for response')

    async def test_oracle_request_invalid_callback(self):
        await self.set_up_contract('OracleRequestCall.py')

        test_url = 'https://unittest.fake.url/api/0/'
        user_data = 'Any Data Here'
        filter = "$.store.*"
        gas_for_response = 1 * 10 ** 8

        callback = '_private_method'  # method can not start with '_' (underscore)
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('oracle_call',
                            [test_url, filter, callback, user_data, gas_for_response],
                            return_type=bool
                            )

        self.assertRegex(str(context.exception), r"disallowed callback method \(starts with '_'\)")

        callback = 'a' * 33  # callback length can not be greater than 32
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('oracle_call',
                            [test_url, filter, callback, user_data, gas_for_response],
                            return_type=bool
                            )

        self.assertRegex(str(context.exception), 'some of the arguments are invalid')

    async def test_oracle_request_invalid_filter(self):
        await self.set_up_contract('OracleRequestCall.py')

        test_url = 'https://unittest.fake.url/api/0/'
        callback = 'callback_method'
        user_data = 'Any Data Here'
        gas_for_response = 1 * 10 ** 8

        filter = "a" * 129  # filter length can not be greater than 128
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('oracle_call',
                            [test_url, filter, callback, user_data, gas_for_response],
                            return_type=bool
                            )

        self.assertRegex(str(context.exception), 'some of the arguments are invalid')

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

    async def test_import_interop_oracle(self):
        await self.set_up_contract('ImportOracle.py')

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000

        result, notifications = await self.call('oracle_call',
                                                [test_url, request_filter, callback, None, gas_for_response],
                                                return_type=None
                                                )
        self.assertIsNone(result)
        contract_script = self.contract_hash

        oracle_requests = self.filter_events(notifications,
                                             origin=self.ORACLE_SCRIPT_HASH,
                                             event_name='OracleRequest',
                                             notification_type=OracleRequestEvent
                                             )
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(contract_script, oracle_requests[0].request_contract)
        self.assertEqual(test_url, oracle_requests[0].url)
        self.assertEqual(request_filter, oracle_requests[0].filter)

    async def test_import_interop_oracle_package(self):
        await self.set_up_contract('ImportInteropOracle.py')

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000

        result, notifications = await self.call('oracle_call',
                                                [test_url, request_filter, callback, None, gas_for_response],
                                                return_type=None
                                                )
        self.assertIsNone(result)
        contract_script = self.contract_hash

        oracle_requests = self.filter_events(notifications,
                                             origin=self.ORACLE_SCRIPT_HASH,
                                             event_name='OracleRequest',
                                             notification_type=OracleRequestEvent
                                             )
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(contract_script, oracle_requests[0].request_contract)
        self.assertEqual(test_url, oracle_requests[0].url)
        self.assertEqual(request_filter, oracle_requests[0].filter)

    def test_oracle_get_price_compile(self):
        expected_output = (
            Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        output, _ = self.assertCompile('OracleGetPrice.py')
        self.assertEqual(expected_output, output)

    async def test_oracle_get_price_run(self):
        await self.set_up_contract('OracleGetPrice.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertGreater(result, 0)
