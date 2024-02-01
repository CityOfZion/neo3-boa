import hashlib

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.contracts.namedcurve import NamedCurve
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestCryptoLibClass(BoaTest):
    default_folder: str = 'test_sc/native_test/cryptolib'
    ecpoint_init = (
        Opcode.DUP
        + Opcode.ISNULL
        + Opcode.NOT
        + Opcode.JMPIFNOT
        + Integer(11).to_byte_array(min_length=1)
        + Opcode.CONVERT + Type.bytes.stack_item
        + Opcode.DUP
        + Opcode.SIZE
        + Opcode.PUSHINT8 + Integer(33).to_byte_array(signed=True)
        + Opcode.NUMEQUAL
        + Opcode.JMPIF + Integer(3).to_byte_array()
        + Opcode.THROW
    )

    def test_get_hash(self):
        path, _ = self.get_deploy_file_paths('GetHash.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(constants.CRYPTO_SCRIPT)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ripemd160_str(self):
        path, _ = self.get_deploy_file_paths('Ripemd160Str.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = hashlib.new('ripemd160', b'unit test')
        invokes.append(runner.call_contract(path, 'Main', 'unit test'))
        expected_results.append(expected_result.digest())

        expected_result = hashlib.new('ripemd160', b'')
        invokes.append(runner.call_contract(path, 'Main', ''))
        expected_results.append(expected_result.digest())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ripemd160_int(self):
        path, _ = self.get_deploy_file_paths('Ripemd160Int.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = hashlib.new('ripemd160', Integer(10).to_byte_array())
        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(expected_result.digest())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ripemd160_bool(self):
        path, _ = self.get_deploy_file_paths('Ripemd160Bool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = hashlib.new('ripemd160', Integer(1).to_byte_array())
        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(expected_result.digest())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ripemd160_bytes(self):
        path, _ = self.get_deploy_file_paths('Ripemd160Bytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = hashlib.new('ripemd160', b'unit test')
        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(expected_result.digest())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ripemd160_too_many_parameters(self):
        path = self.get_contract_path('Ripemd160TooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_ripemd160_too_few_parameters(self):
        path = self.get_contract_path('Ripemd160TooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_sha256_str(self):
        path, _ = self.get_deploy_file_paths('Sha256Str.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = hashlib.sha256(b'unit test')
        invokes.append(runner.call_contract(path, 'Main', 'unit test'))
        expected_results.append(expected_result.digest())

        expected_result = hashlib.sha256(b'')
        invokes.append(runner.call_contract(path, 'Main', ''))
        expected_results.append(expected_result.digest())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sha256_int(self):
        path, _ = self.get_deploy_file_paths('Sha256Int.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = hashlib.sha256(Integer(10).to_byte_array())
        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(expected_result.digest())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sha256_bool(self):
        path, _ = self.get_deploy_file_paths('Sha256Bool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = hashlib.sha256(Integer(1).to_byte_array())
        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(expected_result.digest())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sha256_bytes(self):
        path, _ = self.get_deploy_file_paths('Sha256Bytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = hashlib.sha256(b'unit test')
        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(expected_result.digest())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sha256_too_many_parameters(self):
        path = self.get_contract_path('Sha256TooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_sha256_too_few_parameters(self):
        path = self.get_contract_path('Sha256TooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_verify_with_ecdsa(self):
        path = self.get_contract_path('VerifyWithECDsa.py')
        self.compile(path)

    def test_verify_with_ecdsa_secp256r1_str(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256r1Str.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256r1_bool(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256r1Bool.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256r1_int(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256r1Int.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256r1_bytes(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurve.SECP256R1).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHINT8 + named_curve
            + Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + self.ecpoint_init
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Bytes.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_mismatched_type(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256r1MismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256k1_str(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256k1Str.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256k1_bool(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256k1Bool.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256k1_int(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256k1Int.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256k1_bytes(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurve.SECP256K1).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHINT8 + named_curve
            + Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + self.ecpoint_init
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Bytes.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_mismatched_type(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256k1MismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_murmur32(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('Murmur32.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_bls12_381_add(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('Bls12381Add.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_bls12_381_add_mismatched_type(self):
        path = self.get_contract_path('Bls12381AddMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bls12_381_deserialize(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('Bls12381Deserialize.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_bls12_381_equal(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('Bls12381Equal.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_bls12_381_equal_mismatched_type(self):
        path = self.get_contract_path('Bls12381EqualMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bls12_381_mul(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.PUSHT
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('Bls12381Mul.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_bls12_381_mul_mismatched_type(self):
        path = self.get_contract_path('Bls12381MulMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bls12_381_pairing(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('Bls12381Pairing.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_bls12_381_pairing_mismatched_type(self):
        path = self.get_contract_path('Bls12381PairingMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bls12_381_serialize(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('Bls12381Serialize.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_bls12_381_serialize_mismatched_type(self):
        path = self.get_contract_path('Bls12381SerializeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)