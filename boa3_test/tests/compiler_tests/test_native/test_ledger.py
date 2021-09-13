from boa3 import constants
from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3.neo3.contracts import CallFlags
from boa3.neo3.core.types import UInt160, UInt256
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestLedgerContract(BoaTest):

    default_folder: str = 'test_sc/native_test/ledger'

    def test_get_block_by_hash(self):
        path = self.get_contract_path('GetBlockByHash.py')
        engine = TestEngine()
        engine.increase_block(1)
        block_hash = bytes(32)
        result = self.run_smart_contract(engine, path, 'Main', block_hash)
        self.assertIsNone(result)

        from boa3.neo import from_hex_str
        # TODO: using genesis block hash for testing, change when TestEngine returns blocks hashes
        block_hash = from_hex_str('0x1f4d1defa46faa5e7b9b8d3f79a06bec777d7c26c4aa5f6f5899a291daa87c15')

        result = self.run_smart_contract(engine, path, 'Main', block_hash)
        self.assertIsInstance(result, list)
        self.assertEqual(10, len(result))
        self.assertEqual(block_hash, result[0])
        self.assertEqual(0, result[6])  # genesis block's index is zero

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

    def test_get_block_mismatched_types(self):
        path = self.get_contract_path('GetBlockMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_get_transaction(self):
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String('getTransaction').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flags)).to_byte_array()
            + call_flags
            + Opcode.PUSHDATA1
            + Integer(len(method)).to_byte_array()
            + method
            + Opcode.PUSHDATA1
            + Integer(len(constants.LEDGER_SCRIPT)).to_byte_array()
            + constants.LEDGER_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransaction.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../../interop_test/runtime', 'BurnGas.py')
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
        self.assertEqual(UInt256(hash_), UInt256(result[0]))   # hash
        self.assertIsInstance(result[1], int)   # version
        self.assertIsInstance(result[2], int)   # nonce
        if isinstance(result[3], str):
            result[3] = String(result[3]).to_bytes()
        self.assertEqual(UInt160(sender), UInt160(result[3]))   # sender
        self.assertIsInstance(result[4], int)   # system_fee
        self.assertIsInstance(result[5], int)   # network_fee
        self.assertIsInstance(result[6], int)   # valid_until_block
        if isinstance(result[7], str):
            result[7] = String(result[7]).to_bytes()
        self.assertEqual(script, result[7])   # script

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
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flags)).to_byte_array()
            + call_flags
            + Opcode.PUSHDATA1
            + Integer(len(method)).to_byte_array()
            + method
            + Opcode.PUSHDATA1
            + Integer(len(constants.LEDGER_SCRIPT)).to_byte_array()
            + constants.LEDGER_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransactionFromBlockInt.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../../interop_test/runtime', 'BurnGas.py')
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
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flags)).to_byte_array()
            + call_flags
            + Opcode.PUSHDATA1
            + Integer(len(method)).to_byte_array()
            + method
            + Opcode.PUSHDATA1
            + Integer(len(constants.LEDGER_SCRIPT)).to_byte_array()
            + constants.LEDGER_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransactionFromBlockUInt256.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../../interop_test/runtime', 'BurnGas.py')
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
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flags)).to_byte_array()
            + call_flags
            + Opcode.PUSHDATA1
            + Integer(len(method)).to_byte_array()
            + method
            + Opcode.PUSHDATA1
            + Integer(len(constants.LEDGER_SCRIPT)).to_byte_array()
            + constants.LEDGER_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('GetTransactionHeight.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        path_burn_gas = self.get_contract_path('../../interop_test/runtime', 'BurnGas.py')
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
