from boa3.boa3 import Boa3
from boa3.builtin.interop.contract import GAS, NEO
from boa3.neo import to_script_hash
from boa3.neo.cryptography import hash160
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestHTLCTemplate(BoaTest):

    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = bytes(range(20))

    def test_HTLC_compile(self):
        path = self.get_contract_path('HTLC.py')
        Boa3.compile(path)

    def test_HTLC_deploy(self):
        path = self.get_contract_path('HTLC.py')
        engine = TestEngine()

        # deploying the smart contract
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # deploy can not occur more than once
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

    def test_HTLC_atomic_swap(self):
        path = self.get_contract_path('HTLC.py')
        engine = TestEngine()

        # can not atomic_swap() without deploying first
        result = self.run_smart_contract(engine, path, 'atomic_swap', self.OWNER_SCRIPT_HASH, NEO, 10 * 10**8,
                                         self.OTHER_ACCOUNT_1, GAS, 10000 * 10**8, hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # deploying contract
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # starting atomic swap by using the atomic_swap method
        result = self.run_smart_contract(engine, path, 'atomic_swap', self.OWNER_SCRIPT_HASH, NEO, 10 * 10 ** 8,
                                         self.OTHER_ACCOUNT_1, GAS, 10000 * 10 ** 8, hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_HTLC_onPayment(self):
        path = self.get_contract_path('HTLC.py')
        engine = TestEngine()
        example_contract = self.get_contract_path('test_native/example_contract_for_htlc.py')
        transferred_amount_neo = 10 * 10**8
        transferred_amount_gas = 10000 * 10**8

        output, manifest = self.compile_and_save(example_contract)
        contract_address1 = bytes(range(20))
        contract_address2 = hash160(output)

        output, manifest = self.compile_and_save(path)
        htlc_address = hash160(output)

        engine.add_neo(contract_address1, transferred_amount_neo)
        engine.add_gas(contract_address2, transferred_amount_gas)

        # deploying contract
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # starting atomic swap
        result = self.run_smart_contract(engine, path, 'atomic_swap', contract_address1, NEO, transferred_amount_neo,
                                         contract_address2, GAS, transferred_amount_gas,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # TODO: Test if onPayment is successful when update the TestEngine to make Neo/Gas transfers

    def test_HTLC_withdraw(self):
        path = self.get_contract_path('HTLC.py')
        engine = TestEngine()
        example_contract = self.get_contract_path('test_native/example_contract_for_htlc.py')
        transferred_amount_neo = 10 * 10**8
        transferred_amount_gas = 10000 * 10**8

        output, manifest = self.compile_and_save(example_contract)
        contract_address1 = bytes(range(20))
        contract_address2 = hash160(output)

        output, manifest = self.compile_and_save(path)
        htlc_address = hash160(output)

        engine.add_neo(contract_address1, transferred_amount_neo)
        engine.add_gas(contract_address2, transferred_amount_gas)

        # deploying smart contract
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # starting atomic swap by using the atomic_swap method
        result = self.run_smart_contract(engine, path, 'atomic_swap', contract_address1, NEO, transferred_amount_neo,
                                         contract_address2, GAS, transferred_amount_gas,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # won't be able to withdraw, because no one transferred cryptocurrency to the smart contract
        result = self.run_smart_contract(engine, path, 'withdraw', 'unit test',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # TODO: Test if the withdraw is successful when update the TestEngine to make Neo/Gas transfers

    def test_HTLC_refund(self):
        path = self.get_contract_path('HTLC.py')
        engine = TestEngine()
        example_contract = self.get_contract_path('test_native/example_contract_for_htlc.py')
        transferred_amount_neo = 10 * 10**8
        transferred_amount_gas = 10000 * 10**8

        output, manifest = self.compile_and_save(example_contract)
        contract_address1 = bytes(range(20))
        contract_address2 = hash160(output)

        output, manifest = self.compile_and_save(path)
        htlc_address = hash160(output)

        engine.add_neo(contract_address1, transferred_amount_neo)
        engine.add_gas(contract_address2, transferred_amount_gas)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'atomic_swap', contract_address1, NEO, transferred_amount_neo,
                                         contract_address2, GAS, transferred_amount_gas,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # won't be able to refund, because not enough time has passed
        result = self.run_smart_contract(engine, path, 'refund',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # this simulates a new block in the blockchain
        # get_time only changes value when a new block enters the blockchain
        engine.increase_block()
        # will be able to refund, because enough time has passed
        result = self.run_smart_contract(engine, path, 'refund',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # no one transferred cryptocurrency to the contract, so no one was refunded and no Transfer occurred
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(0, len(transfer_events))

        # TODO: Test if the refund is successful when update the TestEngine to make Neo/Gas transfers
