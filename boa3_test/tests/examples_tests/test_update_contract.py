import json

from boa3.boa3 import Boa3
from boa3.neo import to_script_hash
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestUpdateContractTemplate(BoaTest):

    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')

    def test_update_contract_compile(self):
        path = self.get_contract_path('update_contract.py')
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        Boa3.compile(path)
        Boa3.compile(path_new)

    def test_update_contract(self):
        path = self.get_contract_path('update_contract.py')
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        self.compile_and_save(path_new)
        self.compile_and_save(path)

        new_nef, new_manifest = self.get_bytes_output(path_new)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()
        engine = TestEngine()

        # Saving user's balance before calling method to compare it later
        tokens_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)

        event_transfer = engine.get_events('Transfer')
        # Transfer emitted when deploying the smart contract
        self.assertEqual(1, len(event_transfer))

        # The bugged method is being called and the user is able to receive tokens for free
        result = self.run_smart_contract(engine, path, 'method', self.OTHER_ACCOUNT_1)
        self.assertIsVoid(result)

        event_transfer = engine.get_events('Transfer')
        self.assertEqual(2, len(event_transfer))
        # The amount of tokens will be higher after calling the method
        tokens_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertGreater(tokens_after, tokens_before)

        # The smart contract will be updated to fix the bug in the method
        result = self.run_smart_contract(engine, path, 'update_sc', new_nef, arg_manifest, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertIsVoid(result)

        # An `Update` event will be emitted
        event_update = engine.get_events('Update')
        self.assertEqual(1, len(event_update))

        # Saving user's balance before calling method to compare it later
        tokens_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)

        # Now, when method is called, it won't mint new tokens to any user that called it
        result = self.run_smart_contract(engine, path, 'method', self.OTHER_ACCOUNT_1)
        self.assertIsVoid(result)

        # The amount of tokens now is the same before and after calling the method
        tokens_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(tokens_after, tokens_before)
