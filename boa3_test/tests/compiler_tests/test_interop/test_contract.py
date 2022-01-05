import json

from boa3 import constants
from boa3.boa3 import Boa3
from boa3.exception import CompilerError, CompilerWarning
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.cryptography import hash160
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct
from boa3_test.tests.test_classes.testengine import TestEngine


class TestContractInterop(BoaTest):
    default_folder: str = 'test_sc/interop_test/contract'

    def test_call_contract(self):
        path = self.get_contract_path('CallScriptHash.py')
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

    def test_call_contract_with_cast(self):
        path = self.get_contract_path('CallScriptHashWithCast.py')
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
        self.assertEqual(True, result)

    def test_call_contract_without_args(self):
        path = self.get_contract_path('CallScriptHashWithoutArgs.py')
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

    def test_call_contract_with_flags(self):
        path = self.get_contract_path('CallScriptHashWithFlags.py')
        call_contract_path = self.get_contract_path('CallFlagsUsage.py')

        contract, manifest = self.compile_and_save(call_contract_path)
        call_hash = hash160(contract)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine()
        with self.assertRaises(TestExecutionException, msg=self.CALLED_CONTRACT_DOES_NOT_EXIST_MSG):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'Main')
        engine.add_contract(call_contract_path)

        from boa3.neo3.contracts import CallFlags

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'get_value', ['num'], CallFlags.NONE)

        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'get_value', ['num'], CallFlags.READ_ONLY)
        self.assertEqual(0, result)

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'put_value', ['num', 10], CallFlags.READ_ONLY)
            self.run_smart_contract(engine, path, 'Main', call_hash, 'put_value', ['num', 10], CallFlags.NONE)

        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'put_value', ['num', 10], CallFlags.STATES)
        self.assertEqual(None, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'get_value', ['num'], CallFlags.READ_ONLY)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'put_value', ['num', 99], CallFlags.ALL)
        self.assertEqual(None, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'get_value', ['num'], CallFlags.READ_ONLY)
        self.assertEqual(99, result)

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'notify_user', [], CallFlags.READ_ONLY)
            self.run_smart_contract(engine, path, 'Main', call_hash, 'notify_user', [], CallFlags.STATES)
            self.run_smart_contract(engine, path, 'Main', call_hash, 'notify_user', [], CallFlags.NONE)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'notify_user', [], CallFlags.ALL)
        self.assertEqual(None, result)
        notify = engine.get_events(origin=call_hash)
        self.assertEqual(1, len(notify))
        self.assertEqual('Notify was called', notify[0].arguments[0])

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'call_another_contract', [], CallFlags.STATES)
            self.run_smart_contract(engine, path, 'Main', call_hash, 'call_another_contract', [], CallFlags.NONE)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'call_another_contract', [], CallFlags.ALL)
        self.assertEqual(0, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'call_another_contract',
                                         [], CallFlags.READ_ONLY)
        self.assertEqual(0, result)

    def test_call_contract_too_many_parameters(self):
        path = self.get_contract_path('CallScriptHashTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_call_contract_too_few_parameters(self):
        path = self.get_contract_path('CallScriptHashTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_create_contract(self):
        path = self.get_contract_path('CreateContract.py')
        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        Boa3.compile_and_save(call_contract_path)

        nef_file, manifest = self.get_bytes_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', nef_file, arg_manifest, None)

        self.assertEqual(5, len(result))
        self.assertEqual(nef_file, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    def test_create_contract_data_deploy(self):
        path = self.get_contract_path('CreateContract.py')
        call_contract_path = self.get_contract_path('NewContract.py')
        Boa3.compile_and_save(call_contract_path)

        nef_file, manifest = self.get_bytes_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        engine = TestEngine()
        data = 'some sort of data'
        result = self.run_smart_contract(engine, path, 'Main', nef_file, arg_manifest, data)

        self.assertEqual(5, len(result))
        self.assertEqual(nef_file, result[3])
        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

        notifies = engine.get_events('notify')
        self.assertEqual(2, len(notifies))
        self.assertEqual(False, notifies[0].arguments[0])  # not updated
        self.assertEqual(data, notifies[1].arguments[0])  # data
        result = self.run_smart_contract(engine, call_contract_path, 'main')
        self.assertEqual(data, result)

    def test_create_contract_too_many_parameters(self):
        path = self.get_contract_path('CreateContractTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_create_contract_too_few_parameters(self):
        path = self.get_contract_path('CreateContractTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_update_contract(self):
        path = self.get_contract_path('UpdateContract.py')
        engine = TestEngine()
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'new_method')

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_bytes_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        result = self.run_smart_contract(engine, path, 'update', new_nef, arg_manifest, None)
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'new_method')
        self.assertEqual(42, result)

    def test_update_contract_data_deploy(self):
        path = self.get_contract_path('UpdateContract.py')
        engine = TestEngine()
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'new_method')

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_bytes_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        data = 'this function was deployed'
        result = self.run_smart_contract(engine, path, 'update', new_nef, arg_manifest, data)
        self.assertIsVoid(result)
        notifies = engine.get_events('notify')
        self.assertEqual(2, len(notifies))
        self.assertEqual(True, notifies[0].arguments[0])
        self.assertEqual(data, notifies[1].arguments[0])

    def test_update_contract_too_many_parameters(self):
        path = self.get_contract_path('UpdateContractTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_update_contract_too_few_parameters(self):
        path = self.get_contract_path('UpdateContractTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_destroy_contract(self):
        path = self.get_contract_path('DestroyContract.py')
        output = Boa3.compile(path)
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
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_neo_native_script_hash(self):
        value = constants.NEO_SCRIPT
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
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_gas_native_script_hash(self):
        value = constants.GAS_SCRIPT
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
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_call_flags_type(self):
        path = self.get_contract_path('CallFlagsType.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'ALL')
        self.assertEqual(0b00001111, result)
        result = self.run_smart_contract(engine, path, 'main', 'READ_ONLY')
        self.assertEqual(0b00000101, result)
        result = self.run_smart_contract(engine, path, 'main', 'STATES')
        self.assertEqual(0b00000011, result)
        result = self.run_smart_contract(engine, path, 'main', 'ALLOW_NOTIFY')
        self.assertEqual(0b00001000, result)
        result = self.run_smart_contract(engine, path, 'main', 'ALLOW_CALL')
        self.assertEqual(0b00000100, result)
        result = self.run_smart_contract(engine, path, 'main', 'WRITE_STATES')
        self.assertEqual(0b00000010, result)
        result = self.run_smart_contract(engine, path, 'main', 'READ_STATES')
        self.assertEqual(0b00000001, result)
        result = self.run_smart_contract(engine, path, 'main', 'NONE')
        self.assertEqual(0, result)

    def test_get_call_flags(self):
        path = self.get_contract_path('CallScriptHashWithFlags.py')
        call_contract_path = self.get_contract_path('GetCallFlags.py')
        Boa3.compile_and_save(call_contract_path)

        contract, manifest = self.get_output(call_contract_path)
        call_hash = hash160(contract)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine()
        with self.assertRaises(TestExecutionException, msg=self.CALLED_CONTRACT_DOES_NOT_EXIST_MSG):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'main')
        engine.add_contract(call_contract_path)

        from boa3.neo3.contracts import CallFlags

        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'main', [], CallFlags.ALL)
        self.assertEqual(CallFlags.ALL, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'main', [], CallFlags.READ_ONLY)
        self.assertEqual(CallFlags.READ_ONLY, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'main', [], CallFlags.STATES)
        self.assertEqual(CallFlags.STATES, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'main', [], CallFlags.NONE)
        self.assertEqual(CallFlags.NONE, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'main', [], CallFlags.READ_STATES)
        self.assertEqual(CallFlags.READ_STATES, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'main', [], CallFlags.WRITE_STATES)
        self.assertEqual(CallFlags.WRITE_STATES, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'main', [], CallFlags.ALLOW_CALL)
        self.assertEqual(CallFlags.ALLOW_CALL, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'main', [], CallFlags.ALLOW_NOTIFY)
        self.assertEqual(CallFlags.ALLOW_NOTIFY, result)

    def test_import_contract(self):
        path = self.get_contract_path('ImportContract.py')
        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')
        Boa3.compile_and_save(path)
        Boa3.compile_and_save(call_contract_path)

        contract, manifest = self.get_output(call_contract_path)
        call_hash = hash160(contract)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine()
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'main', call_hash, 'add', [1, 2])
        self.assertEqual(3, result)

        result = self.run_smart_contract(engine, path, 'call_flags_all')
        from boa3.neo3.contracts import CallFlags
        self.assertEqual(CallFlags.ALL, result)

    def test_import_interop_contract(self):
        path = self.get_contract_path('ImportInteropContract.py')
        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')

        self.compile_and_save(path)
        self.compile_and_save(call_contract_path)

        contract, manifest = self.get_output(call_contract_path)
        call_hash = hash160(contract)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine()
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'main', call_hash, 'add', [1, 2])
        self.assertEqual(3, result)

        result = self.run_smart_contract(engine, path, 'call_flags_all')
        from boa3.neo3.contracts import CallFlags
        self.assertEqual(CallFlags.ALL, result)

    def test_create_standard_account(self):
        from boa3.neo.vm.type.StackItem import StackItemType
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.CONVERT
            + StackItemType.ByteString
            + Opcode.DUP
            + Opcode.ISNULL
            + Opcode.JMPIF
            + Integer(8).to_byte_array(min_length=1)
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.PUSHINT8
            + Integer(33).to_byte_array(min_length=1)
            + Opcode.JMPEQ
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.THROW
            + Opcode.SYSCALL
            + Interop.CreateStandardAccount.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('CreateStandardAccount.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_create_standard_account_too_few_parameters(self):
        path = self.get_contract_path('CreateStandardAccountTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_create_standard_account_too_many_parameters(self):
        path = self.get_contract_path('CreateStandardAccountTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_minimum_deployment_fee(self):
        path = self.get_contract_path('GetMinimumDeploymentFee.py')
        engine = TestEngine()

        minimum_cost = 10 * 10 ** 8  # minimum deployment cost is 10 GAS right now
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(minimum_cost, result)

    def test_get_minimum_deployment_fee_too_many_parameters(self):
        path = self.get_contract_path('GetMinimumDeploymentFeeTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_create_multisig_account(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CreateMultisigAccount.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('CreateMultisigAccount.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_create_multisig_account_too_few_parameters(self):
        path = self.get_contract_path('CreateMultisigAccountTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_create_multisig_account_too_many_parameters(self):
        path = self.get_contract_path('CreateMultisigAccountTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)
