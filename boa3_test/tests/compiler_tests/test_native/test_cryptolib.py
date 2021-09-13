import hashlib

from boa3 import constants
from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.model.builtin.interop.interop import Interop
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3.neo3.contracts.contracttypes import CallFlags
from boa3.neo3.contracts.namedcurve import NamedCurve
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestCryptoLibClass(BoaTest):

    default_folder: str = 'test_sc/native_test/cryptolib'
    ecpoint_init = (
        Opcode.CONVERT + Type.bytes.stack_item
        + Opcode.DUP
        + Opcode.ISNULL
        + Opcode.JMPIF + Integer(8).to_byte_array()
        + Opcode.DUP
        + Opcode.SIZE
        + Opcode.PUSHINT8 + Integer(33).to_byte_array(signed=True)
        + Opcode.JMPEQ + Integer(3).to_byte_array()
        + Opcode.THROW
    )

    def test_ripemd160_str(self):
        path = self.get_contract_path('Ripemd160Str.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', b'unit test')
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        self.assertEqual(expected_result.digest(), result)

        expected_result = hashlib.new('ripemd160', b'')
        result = self.run_smart_contract(engine, path, 'Main', '')
        self.assertEqual(expected_result.digest(), result)

    def test_ripemd160_int(self):
        path = self.get_contract_path('Ripemd160Int.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', Integer(10).to_byte_array())
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_ripemd160_bool(self):
        path = self.get_contract_path('Ripemd160Bool.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', Integer(1).to_byte_array())
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_ripemd160_bytes(self):
        path = self.get_contract_path('Ripemd160Bytes.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', b'unit test')
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_ripemd160_too_many_parameters(self):
        path = self.get_contract_path('Ripemd160TooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_ripemd160_too_few_parameters(self):
        path = self.get_contract_path('Ripemd160TooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_sha256_str(self):
        path = self.get_contract_path('Sha256Str.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(b'unit test')
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        self.assertEqual(expected_result.digest(), result)

        expected_result = hashlib.sha256(b'')
        result = self.run_smart_contract(engine, path, 'Main', '')
        self.assertEqual(expected_result.digest(), result)

    def test_sha256_int(self):
        path = self.get_contract_path('Sha256Int.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(Integer(10).to_byte_array())
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_sha256_bool(self):
        path = self.get_contract_path('Sha256Bool.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(Integer(1).to_byte_array())
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_sha256_bytes(self):
        path = self.get_contract_path('Sha256Bytes.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(b'unit test')
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_sha256_too_many_parameters(self):
        path = self.get_contract_path('Sha256TooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_sha256_too_few_parameters(self):
        path = self.get_contract_path('Sha256TooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_verify_with_ecdsa(self):
        path = self.get_contract_path('VerifyWithECDsa.py')
        Boa3.compile(path)

    def test_verify_with_ecdsa_secp256r1_str(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurve.SECP256R1).to_byte_array(signed=True, min_length=1)
        function_id = String(Interop.VerifyWithECDsa._sys_call).to_bytes()
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(named_curve)).to_byte_array(min_length=1)
            + named_curve
            + Opcode.CONVERT + Type.int.stack_item
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
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.PUSHDATA1
            + Integer(len(function_id)).to_byte_array() + function_id
            + Opcode.PUSHDATA1
            + Integer(len(constants.CRYPTO_SCRIPT)).to_byte_array() + constants.CRYPTO_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Str.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_bool(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        named_curve = Integer(NamedCurve.SECP256R1).to_byte_array(signed=True, min_length=1)
        function_id = String(Interop.VerifyWithECDsa._sys_call).to_bytes()
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(named_curve)).to_byte_array(min_length=1)
            + named_curve
            + Opcode.CONVERT + Type.int.stack_item
            + Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + self.ecpoint_init
            + Opcode.PUSH0
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.PUSHDATA1
            + Integer(len(function_id)).to_byte_array() + function_id
            + Opcode.PUSHDATA1
            + Integer(len(constants.CRYPTO_SCRIPT)).to_byte_array() + constants.CRYPTO_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Bool.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_int(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        named_curve = Integer(NamedCurve.SECP256R1).to_byte_array(signed=True, min_length=1)
        function_id = String(Interop.VerifyWithECDsa._sys_call).to_bytes()
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(named_curve)).to_byte_array(min_length=1)
            + named_curve
            + Opcode.CONVERT + Type.int.stack_item
            + Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + self.ecpoint_init
            + Opcode.PUSH10
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.PUSHDATA1
            + Integer(len(function_id)).to_byte_array() + function_id
            + Opcode.PUSHDATA1
            + Integer(len(constants.CRYPTO_SCRIPT)).to_byte_array() + constants.CRYPTO_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Int.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_bytes(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurve.SECP256R1).to_byte_array(signed=True, min_length=1)
        function_id = String(Interop.VerifyWithECDsa._sys_call).to_bytes()
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(named_curve)).to_byte_array(min_length=1)
            + named_curve
            + Opcode.CONVERT + Type.int.stack_item
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
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array(min_length=1)
            + call_flag
            + Opcode.PUSHDATA1
            + Integer(len(function_id)).to_byte_array() + function_id
            + Opcode.PUSHDATA1
            + Integer(len(constants.CRYPTO_SCRIPT)).to_byte_array() + constants.CRYPTO_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Bytes.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_mismatched_type(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256r1MismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256k1_str(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurve.SECP256K1).to_byte_array(signed=True, min_length=1)
        function_id = String(Interop.VerifyWithECDsa._sys_call).to_bytes()
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(named_curve)).to_byte_array(min_length=1)
            + named_curve
            + Opcode.CONVERT + Type.int.stack_item
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
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array() + call_flag
            + Opcode.PUSHDATA1
            + Integer(len(function_id)).to_byte_array() + function_id
            + Opcode.PUSHDATA1
            + Integer(len(constants.CRYPTO_SCRIPT)).to_byte_array() + constants.CRYPTO_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Str.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_bool(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        named_curve = Integer(NamedCurve.SECP256K1).to_byte_array(signed=True, min_length=1)
        function_id = String(Interop.VerifyWithECDsa._sys_call).to_bytes()
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(named_curve)).to_byte_array(min_length=1)
            + named_curve
            + Opcode.CONVERT + Type.int.stack_item
            + Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + self.ecpoint_init
            + Opcode.PUSH0
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array() + call_flag
            + Opcode.PUSHDATA1
            + Integer(len(function_id)).to_byte_array() + function_id
            + Opcode.PUSHDATA1
            + Integer(len(constants.CRYPTO_SCRIPT)).to_byte_array() + constants.CRYPTO_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Bool.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_int(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        named_curve = Integer(NamedCurve.SECP256K1).to_byte_array(signed=True, min_length=1)
        function_id = String(Interop.VerifyWithECDsa._sys_call).to_bytes()
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(named_curve)).to_byte_array(min_length=1)
            + named_curve
            + Opcode.CONVERT + Type.int.stack_item
            + Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + self.ecpoint_init
            + Opcode.PUSH10
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array() + call_flag
            + Opcode.PUSHDATA1
            + Integer(len(function_id)).to_byte_array() + function_id
            + Opcode.PUSHDATA1
            + Integer(len(constants.CRYPTO_SCRIPT)).to_byte_array() + constants.CRYPTO_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Int.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_bytes(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurve.SECP256K1).to_byte_array(signed=True, min_length=1)
        function_id = String(Interop.VerifyWithECDsa._sys_call).to_bytes()
        call_flag = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(named_curve)).to_byte_array(min_length=1)
            + named_curve
            + Opcode.CONVERT + Type.int.stack_item
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
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(call_flag)).to_byte_array() + call_flag
            + Opcode.PUSHDATA1
            + Integer(len(function_id)).to_byte_array() + function_id
            + Opcode.PUSHDATA1
            + Integer(len(constants.CRYPTO_SCRIPT)).to_byte_array() + constants.CRYPTO_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Bytes.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_mismatched_type(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256k1MismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
