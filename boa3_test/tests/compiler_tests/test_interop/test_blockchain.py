from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.cryptography import hash160
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBlockchainInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/blockchain'

    def test_get_current_height(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.CurrentHeight.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('CurrentHeight.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_current_height_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('CurrentHeightCantAssign.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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

    def test_get_block_by_index(self):
        path = self.get_contract_path('GetBlockByIndex.py')

        engine = TestEngine()
        index = 0
        result = self.run_smart_contract(engine, path, 'Main', index)
        self.assertIsInstance(result, list)
        self.assertEqual(9, len(result))
        self.assertEqual(index, result[5])

        index = 10
        result = self.run_smart_contract(engine, path, 'Main', index)
        self.assertIsNone(result)

        engine.increase_block(10)
        result = self.run_smart_contract(engine, path, 'Main', index)
        self.assertIsInstance(result, list)
        self.assertEqual(9, len(result))
        self.assertEqual(index, result[5])

    def test_get_block_by_hash(self):
        path = self.get_contract_path('GetBlockByHash.py')

        engine = TestEngine()
        engine.increase_block(1)
        block_hash = bytes(32)
        result = self.run_smart_contract(engine, path, 'Main', block_hash)
        self.assertIsNone(result)

        from boa3.neo import from_hex_str
        # TODO: using genesis block hash for testing, change when TestEngine returns blocks hashes
        block_hash = from_hex_str('0xc3db4ba50ede4f9e749bd97e1499953ae17e65a415c6bf9e38c01cf92b03d156')

        result = self.run_smart_contract(engine, path, 'Main', block_hash)
        self.assertIsInstance(result, list)
        self.assertEqual(9, len(result))
        self.assertEqual(block_hash, result[0])
        self.assertEqual(0, result[5])  # genesis block's index is zero

    def test_get_block_mismatched_types(self):
        path = self.get_contract_path('GetBlockMismatchedTypes.py')
        self.assertCompilerLogs(MismatchedTypes, path)
