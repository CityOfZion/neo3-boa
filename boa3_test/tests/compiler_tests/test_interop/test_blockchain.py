from neo3.core import types
from neo3.network.payloads import block

from boa3.internal import constants
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests import annotation, boatestcase, stackitem


class TestBlockchainInterop(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/interop_test/blockchain'

    genesis_block: block.Block

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        cls.genesis_block = await cls.get_genesis_block()

    async def test_block_constructor(self):
        await self.set_up_contract('Block.py')

        zero_uint256 = types.UInt256.zero()
        expected: annotation.Block = (
            zero_uint256,  # hash
            0,  # version
            zero_uint256,  # previous hash
            zero_uint256,  # merkle root
            0,  # timestamp
            0,  # nonce
            0,  # index
            types.UInt160.zero(),  # next consensus
            0  # tx count
        )
        result, _ = await self.call('main', [], return_type=annotation.Block)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    async def test_get_contract(self):
        await self.set_up_contract('GetContract.py')

        invalid_contract = types.UInt160.zero()
        result, _ = await self.call('main', [invalid_contract], return_type=None)
        self.assertIsNone(result)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        nef, manifest = self.get_serialized_output(call_contract_path)
        manifest = stackitem.from_manifest(manifest)

        call_hash = await self.compile_and_deploy(call_contract_path)
        result, _ = await self.call('main', [call_hash], return_type=annotation.Contract)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        self.assertEqual(manifest, result[4])

    async def test_get_block_by_index(self):
        await self.set_up_contract('GetBlockByIndex.py')

        invalid_block_index = 10 ** 5
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [invalid_block_index], return_type=annotation.Block)

        self.assertRegex(str(context.exception), f'no block with index {invalid_block_index}')

        valid_block = self.genesis_block
        block_index = valid_block.index
        expected = stackitem.from_block(valid_block)
        result, _ = await self.call('Main', [block_index], return_type=annotation.Block)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

        valid_block = await self.get_latest_block()
        block_index = valid_block.index
        expected = stackitem.from_block(valid_block)
        result, _ = await self.call('Main', [block_index], return_type=annotation.Block)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    async def test_get_block_by_hash(self):
        await self.set_up_contract('GetBlockByHash.py')

        invalid_block_hash = types.UInt256(bytes(range(32)))
        result, _ = await self.call('Main', [invalid_block_hash], return_type=None)
        self.assertIsNone(result)

        valid_block = self.genesis_block
        valid_block_hash = valid_block.hash()
        expected = stackitem.from_block(valid_block)
        result, _ = await self.call('Main', [valid_block_hash], return_type=annotation.Block)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    def test_get_block_mismatched_types(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'GetBlockMismatchedTypes.py')

    async def test_transaction_init(self):
        await self.set_up_contract('Transaction.py')

        expected: annotation.Transaction = (
            types.UInt256.zero(),  # hash
            0,  # version
            0,  # nonce
            types.UInt160.zero(),  # sender
            0,  # system fee
            0,  # network fee
            0,  # valid until block
            b''  # script
        )
        result, _ = await self.call('main', [], return_type=annotation.Transaction)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    def test_get_transaction_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        output, _ = self.assertCompile('GetTransaction.py')
        self.assertEqual(expected_output, output)

    async def test_get_transaction_run(self):
        await self.set_up_contract('GetTransaction.py')

        invalid_tx = types.UInt256.zero()
        result, _ = await self.call('main', [invalid_tx], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        tx = await self.get_last_tx()
        self.assertIsNotNone(tx)
        hash_ = tx.hash()

        expected = stackitem.from_transaction(tx)
        result, _ = await self.call('main', [hash_], return_type=annotation.Transaction)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    def test_get_transaction_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'GetTransactionMismatchedType.py')

    def test_get_transaction_from_block_int_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        output, _ = self.assertCompile('GetTransactionFromBlockInt.py')
        self.assertEqual(expected_output, output)

    async def test_get_transaction_from_block_int_run(self):
        await self.set_up_contract('GetTransactionFromBlockInt.py')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main',
                            [0, 0],
                            return_type=annotation.Transaction
                            )

        self.assertRegex(str(context.exception), 'wrong transaction index')

        block_ = await self.get_latest_block()
        self.assertGreater(len(block_.transactions), 0)

        expected_block_index = block_.index
        tx = block_.transactions[0]
        self.assertIsNotNone(tx)

        expected = stackitem.from_transaction(tx)
        result, _ = await self.call('main', [expected_block_index, 0], return_type=annotation.Transaction)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    def test_get_transaction_from_block_uint256_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        output, _ = self.assertCompile('GetTransactionFromBlockUInt256.py')
        self.assertEqual(expected_output, output)

    async def test_get_transaction_from_block_uint256_run(self):
        await self.set_up_contract('GetTransactionFromBlockUInt256.py')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main',
                            [types.UInt256.zero(), 0],
                            return_type=annotation.Transaction
                            )

        self.assertRegex(str(context.exception), 'wrong transaction index')

        block_ = await self.get_latest_block()
        self.assertGreater(len(block_.transactions), 0)

        expected_block_hash = block_.hash()
        tx = block_.transactions[0]
        self.assertIsNotNone(tx)

        expected = stackitem.from_transaction(tx)
        result, _ = await self.call('main', [expected_block_hash, 0], return_type=annotation.Transaction)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    def test_get_transaction_from_block_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'GetTransactionFromBlockMismatchedType.py')

    def test_get_transaction_height_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        output, _ = self.assertCompile('GetTransactionHeight.py')
        self.assertEqual(expected_output, output)

    async def test_get_transaction_height_run(self):
        await self.set_up_contract('GetTransactionHeight.py')

        block_ = await self.get_latest_block()
        self.assertGreater(len(block_.transactions), 0)
        tx = block_.transactions[0]

        expected = block_.index
        result, _ = await self.call('main', [tx.hash()], return_type=int)
        self.assertEqual(expected, result)

    def test_get_transaction_height_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'GetTransactionHeightMismatchedType.py')

    def test_get_transaction_signers_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        output, _ = self.assertCompile('GetTransactionSigners.py')
        self.assertEqual(expected_output, output)

    async def test_get_transaction_signers_run(self):
        await self.set_up_contract('GetTransactionSigners.py')

        invalid_tx = types.UInt256.zero()
        result, _ = await self.call('main',
                                    [invalid_tx],
                                    return_type=None,
                                    signing_accounts=[self.genesis]  # persist to emit a new block
                                    )
        self.assertIsNone(result)

        tx = await self.get_last_tx()
        self.assertIsNotNone(tx)
        self.assertGreater(len(tx.signers), 0)
        hash_ = tx.hash()

        expected: list[annotation.Signer] = [
            stackitem.from_signer(signer) for signer in tx.signers
        ]
        result, _ = await self.call('main', [hash_], return_type=list[annotation.Signer])
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    def test_get_transaction_signers_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'GetTransactionSignersMismatchedType.py')

    def test_get_transaction_vm_state_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )
        output, _ = self.assertCompile('GetTransactionVMState.py')
        self.assertEqual(expected_output, output)

    async def test_get_transaction_vm_state_run(self):
        await self.set_up_contract('GetTransactionVMState.py')

        hash_ = self.called_tx
        self.assertIsNotNone(hash_)

        native_result, _ = await self.call('getTransactionVMState',
                                           [hash_],
                                           return_type=int,
                                           target_contract=types.UInt160(constants.LEDGER_SCRIPT)
                                           )

        contract_invoke, _ = await self.call('main',
                                             [hash_],
                                             return_type=int
                                             )
        self.assertEqual(native_result, contract_invoke)

    def test_get_transaction_vm_state_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'GetTransactionVMStateMismatchedType.py')

    async def test_import_blockchain(self):
        self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'ImportBlockchain.py')
        await self.set_up_contract('ImportBlockchain.py')

        invalid_contract = types.UInt160.zero()
        result, _ = await self.call('main', [invalid_contract], return_type=None)
        self.assertIsNone(result)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Subtraction.py')
        nef, manifest = self.get_serialized_output(call_contract_path)
        manifest = stackitem.from_manifest(manifest)

        call_hash = await self.compile_and_deploy(call_contract_path)
        result, _ = await self.call('main', [call_hash], return_type=annotation.Contract)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        self.assertEqual(manifest, result[4])

    async def test_import_interop_blockchain(self):
        self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'ImportInteropBlockchain.py')
        await self.set_up_contract('ImportInteropBlockchain.py')

        invalid_contract = types.UInt160.zero()
        result, _ = await self.call('main', [invalid_contract], return_type=None)
        self.assertIsNone(result)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Concatenation.py')
        nef, manifest = self.get_serialized_output(call_contract_path)
        manifest = stackitem.from_manifest(manifest)

        call_hash = await self.compile_and_deploy(call_contract_path)
        result, _ = await self.call('main', [call_hash], return_type=annotation.Contract)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(nef, result[3])
        self.assertEqual(manifest, result[4])

    async def test_current_hash(self):
        await self.set_up_contract('CurrentHash.py')

        result, _ = await self.call('main', [], return_type=types.UInt256, signing_accounts=[self.genesis])
        block_ = await self.get_last_block(self.called_tx)
        expected = block_.hash()
        self.assertEqual(expected, result)

    async def test_current_index(self):
        await self.set_up_contract('CurrentIndex.py')

        result, _ = await self.call('main', [], return_type=int, signing_accounts=[self.genesis])
        block_ = await self.get_last_block(self.called_tx)
        expected = block_.index
        self.assertEqual(expected, result)
