from dataclasses import dataclass
from typing import Self

from neo3.api import noderpc
from neo3.api.helpers.signing import sign_with_account, sign_with_multisig_account
from neo3.api.noderpc import Receipt
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.network.payloads import verification
from neo3.network.payloads.transaction import OracleResponse
from neo3.vm import ScriptBuilder
from neo3.wallet import account

from boa3.internal import constants
from boa3.internal.constants import ORACLE_SCRIPT
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo3.contracts.native import Role
from boa3.internal.neo3.network.payloads import OracleResponseCode
from boa3_test.tests import boatestcase


@dataclass
class OracleRequestEvent(boatestcase.BoaTestEvent):
    id: int
    request_contract: types.UInt160
    url: str
    filter: str

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


@dataclass
class OracleResponseEvent(boatestcase.BoaTestEvent):
    id: int
    original_tx: types.UInt256

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


class TestOracleContract(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/oracle'
    ORACLE_CONTRACT_NAME = 'OracleContract'
    ORACLE_SCRIPT_HASH = types.UInt160(constants.ORACLE_SCRIPT)

    owner: account.Account
    oracle_node: account.Account

    @classmethod
    def setupTestCase(cls):
        cls.owner = cls.node.wallet.account_new(label='owner')

        cls.oracle_node = cls.node.account_committee
        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 1000, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.oracle_node.script_hash, 1000, 8)

    async def send_response(self, request_id: int, data: bytes) -> Receipt:
        call_contract = await self.compile_and_deploy('test_sc/native_test/rolemanagement', 'DesignateAsRole.py')

        signer = verification.Signer(
            self.genesis.script_hash,
            verification.WitnessScope.GLOBAL
        )

        result, _ = await self.call('main',
                                    [Role.ORACLE, [self.oracle_node.public_key]],
                                    target_contract=call_contract, signers=[signer],
                                    signing_accounts=[self.genesis],
                                    return_type=None
                                    )
        self.assertIsNone(result)

        oracle_response = OracleResponse(request_id, OracleResponseCode.SUCCESS, data)

        script = ScriptBuilder().emit_contract_call(ORACLE_SCRIPT, "finish").to_array()

        from neo3.api.helpers.txbuilder import TxBuilder
        async with noderpc.NeoRpcClient(
                self.node.facade.rpc_host
        ) as client:
            builder = TxBuilder(client, script)
            await builder.init()

            from neo3.network.payloads.verification import Signer
            builder.add_signer(sign_with_multisig_account(self.oracle_node),
                               Signer(self.oracle_node.script_hash, verification.WitnessScope.NONE))
            builder.add_signer(sign_with_account(self.owner),
                               Signer(self.owner.script_hash, verification.WitnessScope.NONE))
            await builder.set_valid_until_block()
            builder.tx.attributes.append(oracle_response)
            builder.tx.system_fee = 10 ** 8
            builder.tx.network_fee = 10 ** 8 + 1234

            builder.tx.witnesses = []

            tx = await builder.build_and_sign()
            tx_id = await client.send_transaction(tx)

            return await client.wait_for_transaction_receipt(tx_id, retry_delay=1)

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
        self.assertIsInstance(oracle_requests[0].id, int)
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

    async def test_oracle_response(self):
        await self.set_up_contract('OracleRequestCall.py')

        test_url = 'https://unittest.fake.url/api/0/'
        callback = 'callback_method'
        user_data = b'Any Data Here'
        gas_for_response = 1 * 10 ** 8

        result, notifications = await self.call('oracle_call',
                                                [test_url, None, callback, user_data, gas_for_response],
                                                return_type=bool, signing_accounts=[self.owner]
                                                )
        oracle_request_tx = await self.get_last_tx()
        self.assertEqual(True, result)

        oracle_requests = self.filter_events(notifications,
                                             event_name='OracleRequest',
                                             origin=self.ORACLE_SCRIPT_HASH,
                                             notification_type=OracleRequestEvent
                                             )
        self.assertEqual(1, len(oracle_requests))
        oracle_request_id = oracle_requests[0].id

        result, _ = await self.call('get_storage',
                                    [],
                                    return_type=list
                                    )
        self.assertEqual(['', '', 0, ''], result)

        from boa3.internal import constants
        path_json = constants.PATH_SEPARATOR.join([self.dirname, self.default_test_folder, "OracleResponse.json"])
        with open(path_json) as f:
            response_data = f.read().encode('utf-8')

        tx_result = await self.send_response(oracle_request_id, response_data)

        result, notifications = await self.call('get_storage',
                                                [],
                                                return_type=list)
        from boa3.internal.neo.vm.type.StackItem import StackItemType
        self.assertEqual(4, len(result))
        self.assertEqual(test_url, result[0])
        self.assertEqual((StackItemType.ByteString + len(user_data).to_bytes(1, 'little') + user_data).decode('utf-8'),
                         result[1])
        self.assertEqual(OracleResponseCode.SUCCESS, result[2])
        self.assertEqual(response_data.decode('utf-8'), result[3])

        oracle_response = self.filter_events(tx_result.execution.notifications,
                                             event_name='OracleResponse',
                                             origin=self.ORACLE_SCRIPT_HASH,
                                             notification_type=OracleResponseEvent
                                             )

        self.assertEqual(1, len(oracle_response))
        self.assertEqual(oracle_request_id, oracle_response[0].id)
        self.assertEqual(oracle_request_tx.hash(), oracle_response[0].original_tx)

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'OracleRequestUrlMismatchedType.py')

    def test_oracle_request_filter_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'OracleRequestFilterMismatchedType.py')

    def test_oracle_request_callback_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'OracleRequestCallCallbackMismatchedType.py')

    def test_oracle_request_gas_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'OracleRequestGasMismatchedType.py')

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

    async def test_oracle_response_code_instantiate(self):
        await self.set_up_contract('OracleResponseCodeInstantiate.py')

        for oracle_response_code in OracleResponseCode:
            result, _ = await self.call('main', [oracle_response_code], return_type=int)
            self.assertEqual(oracle_response_code, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [0xcc], return_type=int)

        self.assertRegex(str(context.exception), "Invalid OracleResponseCode parameter value")

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [0x01], return_type=int)

        self.assertRegex(str(context.exception), "Invalid OracleResponseCode parameter value")

    async def test_oracle_response_code_not(self):
        await self.set_up_contract('OracleResponseCodeNot.py')

        for oracle_response_code in OracleResponseCode:
            result, _ = await self.call('main', [oracle_response_code], return_type=int)
            self.assertEqual(~oracle_response_code, result)
