from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3.neo3.contracts import CallFlags
from boa3.neo3.core.types import UInt160, UInt256
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBlockchainInterop(BoaTest):
    default_folder: str = 'test_sc/interop_test/blockchain'

    def test_block_constructor(self):
        path = self.get_contract_path('Block.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, list)
        self.assertEqual(10, len(result))
        for k in range(len(result)):
            if isinstance(result[k], str):
                result[k] = String(result[k]).to_bytes()
        self.assertEqual(UInt256(), UInt256(result[0]))  # hash
        self.assertEqual(0, result[1])  # version
        self.assertEqual(UInt256(), UInt256(result[2]))  # previous_hash
        self.assertEqual(UInt256(), UInt256(result[3]))  # merkle_root
        self.assertEqual(0, result[4])  # timestamp
        self.assertEqual(0, result[5])  # nonce
        self.assertEqual(0, result[6])  # index
        self.assertEqual(0, result[7])  # primary_index
        self.assertEqual(UInt160(), UInt160(result[8]))  # next_consensus
        self.assertEqual(0, result[9])  # transaction_count

    def test_get_contract(self):
        path = self.get_contract_path('GetContract.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', bytes(20))
        self.assertIsNone(result)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        self.run_smart_contract(engine, call_contract_path, 'add', 1, 2)
        call_hash = engine.executed_script_hash.to_array()

        nef, manifest = self.get_bytes_output(call_contract_path)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine.reset_engine()
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'main', call_hash)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_get_block_by_index(self):
        path = self.get_contract_path('GetBlockByIndex.py')

        engine = TestEngine()
        index = 0
        result = self.run_smart_contract(engine, path, 'Main', index)
        self.assertIsInstance(result, list)
        self.assertEqual(10, len(result))
        self.assertEqual(index, result[6])

        index = 10
        result = self.run_smart_contract(engine, path, 'Main', index)
        self.assertIsNone(result)

        engine.increase_block(10)
        result = self.run_smart_contract(engine, path, 'Main', index)
        self.assertIsInstance(result, list)
        self.assertEqual(10, len(result))
        self.assertEqual(index, result[6])

    def test_get_block_by_hash(self):
        path = self.get_contract_path('GetBlockByHash.py')

        engine = TestEngine()
        engine.increase_block(1)
        block_hash = bytes(32)
        result = self.run_smart_contract(engine, path, 'Main', block_hash)
        self.assertIsNone(result)

        current_block = engine.current_block
        self.assertIsNotNone(current_block.hash)

        result = self.run_smart_contract(engine, path, 'Main', current_block.hash)
        self.assertIsInstance(result, list)
        self.assertEqual(10, len(result))
        self.assertEqual(current_block.hash, result[0])
        self.assertEqual(current_block.timestamp, result[4])
        self.assertEqual(current_block.index, result[6])

    def test_get_block_mismatched_types(self):
        path = self.get_contract_path('GetBlockMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_transaction_init(self):
        path = self.get_contract_path('Transaction.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(8, len(result))
        if isinstance(result[0], str):
            result[0] = String(result[0]).to_bytes()
        self.assertEqual(UInt256(), UInt256(result[0]))  # hash
        self.assertEqual(0, result[1])  # version
        self.assertEqual(0, result[2])  # nonce
        if isinstance(result[3], str):
            result[3] = String(result[3]).to_bytes()
        self.assertEqual(UInt160(), UInt160(result[3]))  # sender
        self.assertEqual(0, result[4])  # system_fee
        self.assertEqual(0, result[5])  # network_fee
        self.assertEqual(0, result[6])  # valid_until_block
        if isinstance(result[7], str):
            result[7] = String(result[7]).to_bytes()
        self.assertEqual(b'', result[7])  # script

    def test_get_transaction(self):
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String('getTransaction').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransaction.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../runtime', 'BurnGas.py')
        engine = TestEngine()

        engine.increase_block()
        sender = bytes(range(20))
        self.run_smart_contract(engine, path_burn_gas, 'main', 1000, signer_accounts=[sender])

        txs = engine.get_transactions()
        self.assertGreater(len(txs), 0)
        hash_ = txs[0].hash
        script = txs[0]._script

        result = self.run_smart_contract(engine, path, 'main', hash_)
        self.assertEqual(8, len(result))
        if isinstance(result[0], str):
            result[0] = String(result[0]).to_bytes()
        self.assertEqual(UInt256(hash_), UInt256(result[0]))  # hash
        self.assertIsInstance(result[1], int)  # version
        self.assertIsInstance(result[2], int)  # nonce
        if isinstance(result[3], str):
            result[3] = String(result[3]).to_bytes()
        self.assertEqual(UInt160(sender), UInt160(result[3]))  # sender
        self.assertIsInstance(result[4], int)  # system_fee
        self.assertIsInstance(result[5], int)  # network_fee
        self.assertIsInstance(result[6], int)  # valid_until_block
        if isinstance(result[7], str):
            result[7] = String(result[7]).to_bytes()
        self.assertEqual(script, result[7])  # script

    def test_get_transaction_mismatched_type(self):
        path = self.get_contract_path('GetTransactionMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_get_transaction_from_block_int(self):
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String('getTransactionFromBlock').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransactionFromBlockInt.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../runtime', 'BurnGas.py')
        engine = TestEngine()

        engine.increase_block(10)
        sender = bytes(range(20))
        self.run_smart_contract(engine, path_burn_gas, 'main', 100, signer_accounts=[sender])

        block_10 = engine.current_block
        txs = block_10.get_transactions()
        hash_ = txs[0].hash
        script = txs[0]._script

        engine.increase_block()

        result = self.run_smart_contract(engine, path, 'main', 10, 0)
        self.assertEqual(8, len(result))
        if isinstance(result[0], str):
            result[0] = String(result[0]).to_bytes()
        self.assertEqual(UInt256(hash_), UInt256(result[0]))  # hash
        self.assertIsInstance(result[1], int)  # version
        self.assertIsInstance(result[2], int)  # nonce
        if isinstance(result[3], str):
            result[3] = String(result[3]).to_bytes()
        self.assertEqual(UInt160(sender), UInt160(result[3]))  # sender
        self.assertIsInstance(result[4], int)  # system_fee
        self.assertIsInstance(result[5], int)  # network_fee
        self.assertIsInstance(result[6], int)  # valid_until_block
        if isinstance(result[7], str):
            result[7] = String(result[7]).to_bytes()
        self.assertEqual(script, result[7])  # script

    def test_get_transaction_from_block_uint256(self):
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String('getTransactionFromBlock').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransactionFromBlockUInt256.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../runtime', 'BurnGas.py')
        engine = TestEngine()

        engine.increase_block(10)
        sender = bytes(range(20))
        self.run_smart_contract(engine, path_burn_gas, 'main', 100, signer_accounts=[sender])

        block_10 = engine.current_block
        block_hash = block_10.hash
        self.assertIsNotNone(block_hash)
        txs = block_10.get_transactions()
        tx_hash = txs[0].hash
        tx_script = txs[0]._script

        engine.increase_block()

        result = self.run_smart_contract(engine, path, 'main', block_hash, 0)
        self.assertEqual(8, len(result))
        if isinstance(result[0], str):
            result[0] = String(result[0]).to_bytes()
        self.assertEqual(UInt256(tx_hash), UInt256(result[0]))  # hash
        self.assertIsInstance(result[1], int)  # version
        self.assertIsInstance(result[2], int)  # nonce
        if isinstance(result[3], str):
            result[3] = String(result[3]).to_bytes()
        self.assertEqual(UInt160(sender), UInt160(result[3]))  # sender
        self.assertIsInstance(result[4], int)  # system_fee
        self.assertIsInstance(result[5], int)  # network_fee
        self.assertIsInstance(result[6], int)  # valid_until_block
        if isinstance(result[7], str):
            result[7] = String(result[7]).to_bytes()
        self.assertEqual(tx_script, result[7])  # script

    def test_get_transaction_from_block_mismatched_type(self):
        path = self.get_contract_path('GetTransactionFromBlockMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_get_transaction_height(self):
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String('getTransactionHeight').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransactionHeight.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../runtime', 'BurnGas.py')
        engine = TestEngine()

        expected_block_index = 10
        engine.increase_block(expected_block_index)
        self.run_smart_contract(engine, path_burn_gas, 'main', 1000)

        txs = engine.get_transactions()
        self.assertGreater(len(txs), 0)
        hash_ = txs[0].hash

        result = self.run_smart_contract(engine, path, 'main', hash_)
        self.assertEqual(expected_block_index, result)

    def test_get_transaction_height_mismatched_type(self):
        path = self.get_contract_path('GetTransactionHeightMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_get_transaction_signers(self):
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String('getTransactionSigners').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransactionSigners.py')
        output, manifest = self.get_output(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../runtime', 'BurnGas.py')
        engine = TestEngine()

        example_account_1 = bytes(range(20))
        example_account_2 = bytes(20)
        self.run_smart_contract(engine, path_burn_gas, 'main', 1000,
                                signer_accounts=[example_account_1, example_account_2])

        txs = engine.get_transactions()
        self.assertGreater(len(txs), 0)
        hash_ = txs[0].hash

        result = self.run_smart_contract(engine, path, 'main', hash_)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], list)
        self.assertEqual(len(result[0]), len(Interop.SignerType.variables))
        self.assertEqual(result[0][0], String.from_bytes(example_account_1))

    def test_get_transaction_signers_mismatched_type(self):
        path = self.get_contract_path('GetTransactionSignersMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_get_transaction_vm_state(self):
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String('getTransactionVMState').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransactionVMState.py')
        output, manifest = self.get_output(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../runtime', 'BurnGas.py')
        engine = TestEngine()

        self.run_smart_contract(engine, path_burn_gas, 'main', 1000)
        expected_vm_state = engine.vm_state.value

        txs = engine.get_transactions()
        self.assertGreater(len(txs), 0)
        hash_ = txs[0].hash

        result = self.run_smart_contract(engine, path, 'main', hash_)
        self.assertEqual(expected_vm_state, result)

    def test_get_transaction_vm_state_mismatched_type(self):
        path = self.get_contract_path('GetTransactionVMStateMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_import_blockchain(self):
        path = self.get_contract_path('ImportBlockchain.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', bytes(20))
        self.assertIsNone(result)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        self.run_smart_contract(engine, call_contract_path, 'add', 1, 2)
        call_hash = engine.executed_script_hash.to_array()

        nef, manifest = self.get_bytes_output(call_contract_path)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine()
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'main', call_hash)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_import_interop_blockchain(self):
        path = self.get_contract_path('ImportInteropBlockchain.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', bytes(20))
        self.assertIsNone(result)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        self.run_smart_contract(engine, call_contract_path, 'add', 1, 2)
        call_hash = engine.executed_script_hash.to_array()

        nef, manifest = self.get_bytes_output(call_contract_path)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine()
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'main', call_hash)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_current_hash(self):
        path = self.get_contract_path('CurrentHash.py')
        engine = TestEngine()

        engine.increase_block()

        result = self.run_smart_contract(engine, path, 'main', expected_result_type=bytes)

        block = engine.current_block
        self.assertEqual(block.hash, result)

    def test_current_index(self):
        path = self.get_contract_path('CurrentIndex.py')
        engine = TestEngine()

        engine.increase_block()
        result = self.run_smart_contract(engine, path, 'main')
        if isinstance(result, str):
            result = String(result).to_bytes()
        block = engine.current_block
        self.assertEqual(block.index, result)
