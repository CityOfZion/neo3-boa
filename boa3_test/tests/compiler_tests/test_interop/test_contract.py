import json

from boa3 import constants
from boa3.boa3 import Boa3
from boa3.constants import GAS_SCRIPT, NEO_SCRIPT
from boa3.exception.CompilerError import UnexpectedArgument, UnfilledArgument
from boa3.exception.CompilerWarning import NameShadowing
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.cryptography import hash160
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3.neo3.contracts import CallFlags
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct
from boa3_test.tests.test_classes.testengine import TestEngine


class TestContractInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/contract'

    def test_call_contract(self):
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG2
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.ROT
            + Opcode.ROT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('CallScriptHash.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        Boa3.compile_and_save(call_contract_path)

        contract, manifest = self.get_output(call_contract_path)
        call_hash = hash160(contract)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine()
        with self.assertRaises(TestExecutionException, msg=self.CALLED_CONTRACT_DOES_NOT_EXIST_MSG):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'add', [1, 2])
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'add', [1, 2])
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'add', [-42, -24])
        self.assertEqual(-66, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'add', [-42, 24])
        self.assertEqual(-18, result)

    def test_call_contract_without_args(self):
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.NEWARRAY0
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.ROT
            + Opcode.ROT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('CallScriptHashWithoutArgs.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        call_contract_path = self.get_contract_path('test_sc/list_test', 'IntList.py')
        Boa3.compile_and_save(call_contract_path)

        contract, manifest = self.get_output(call_contract_path)
        call_hash = hash160(contract)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine()
        with self.assertRaises(TestExecutionException, msg=self.CALLED_CONTRACT_DOES_NOT_EXIST_MSG):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'Main')
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'Main')
        self.assertEqual([1, 2, 3], result)

    def test_call_contract_too_many_parameters(self):
        path = self.get_contract_path('CallScriptHashTooManyArguments.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_call_contract_too_few_parameters(self):
        path = self.get_contract_path('CallScriptHashTooFewArguments.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_create_contract(self):
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.DUP
            + Opcode.PUSHNULL
            + Opcode.APPEND
            + Opcode.PUSHDATA1
            + Integer(len(Interop.CreateContract.method_name)).to_byte_array(min_length=1)
            + String(Interop.CreateContract.method_name).to_bytes()
            + Opcode.PUSHDATA1
            + Integer(len(constants.MANAGEMENT_SCRIPT)).to_byte_array(min_length=1)
            + constants.MANAGEMENT_SCRIPT
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.ROT
            + Opcode.ROT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('CreateContract.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        Boa3.compile_and_save(call_contract_path)

        nef_file, manifest = self.get_bytes_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', nef_file, arg_manifest)

        self.assertEqual(5, len(result))
        self.assertEqual(nef_file, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_create_contract_too_many_parameters(self):
        path = self.get_contract_path('CreateContractTooManyArguments.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_create_contract_too_few_parameters(self):
        path = self.get_contract_path('CreateContractTooFewArguments.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_update_contract(self):
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        expected_output = (
            Opcode.INITSLOT
            + b'\00'
            + b'\02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(Interop.UpdateContract.method_name)).to_byte_array(min_length=1)
            + String(Interop.UpdateContract.method_name).to_bytes()
            + Opcode.PUSHDATA1
            + Integer(len(constants.MANAGEMENT_SCRIPT)).to_byte_array(min_length=1)
            + constants.MANAGEMENT_SCRIPT
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.ROT
            + Opcode.ROT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('UpdateContract.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'new_method')

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_bytes_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        result = self.run_smart_contract(engine, path, 'update', new_nef, arg_manifest)
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'new_method')
        self.assertEqual(42, result)

    def test_update_contract_too_many_parameters(self):
        path = self.get_contract_path('UpdateContractTooManyArguments.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_update_contract_too_few_parameters(self):
        path = self.get_contract_path('UpdateContractTooFewArguments.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_destroy_contract(self):
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.PUSHDATA1
            + Integer(len(Interop.DestroyContract.method_name)).to_byte_array(min_length=1)
            + String(Interop.DestroyContract.method_name).to_bytes()
            + Opcode.PUSHDATA1
            + Integer(len(constants.MANAGEMENT_SCRIPT)).to_byte_array(min_length=1)
            + constants.MANAGEMENT_SCRIPT
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.ROT
            + Opcode.ROT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('DestroyContract.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

        script_hash = hash160(output)
        call_contract_path = self.get_contract_path('CallScriptHash.py')
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, call_contract_path, 'Main',
                                    script_hash, 'Main', [])

    def test_destroy_contract_too_many_parameters(self):
        path = self.get_contract_path('DestroyContractTooManyArguments.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_get_neo_native_script_hash(self):
        value = NEO_SCRIPT
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array()
            + value
            + Opcode.RET
        )

        path = self.get_contract_path('NeoScriptHash.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(value, result)

    def test_neo_native_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('NeoScriptHashCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_gas_native_script_hash(self):
        value = GAS_SCRIPT
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array()
            + value
            + Opcode.RET
        )

        path = self.get_contract_path('GasScriptHash.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(value, result)

    def test_gas_native_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('GasScriptHashCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)
