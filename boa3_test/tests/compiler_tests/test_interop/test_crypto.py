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


class TestCryptoInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/crypto'
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

    def test_hash160_str(self):
        path = self.get_contract_path('Hash160Str.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        self.assertEqual(expected_result, result)

    def test_hash160_int(self):
        path = self.get_contract_path('Hash160Int.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(Integer(10).to_byte_array()).digest())).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_hash160_bool(self):
        path = self.get_contract_path('Hash160Bool.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(Integer(1).to_byte_array()).digest())).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_hash160_bytes(self):
        path = self.get_contract_path('Hash160Bytes.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

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

    def test_hash256_str(self):
        path = self.get_contract_path('Hash256Str.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(hashlib.sha256(b'unit test').digest()).digest()
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        self.assertEqual(expected_result, result)

    def test_hash256_int(self):
        path = self.get_contract_path('Hash256Int.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(hashlib.sha256(Integer(10).to_byte_array()).digest()).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_hash256_bool(self):
        path = self.get_contract_path('Hash256Bool.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(hashlib.sha256(Integer(1).to_byte_array()).digest()).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_hash256_bytes(self):
        path = self.get_contract_path('Hash256Bytes.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(hashlib.sha256(b'unit test').digest()).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_check_sig(self):
        byte_input0 = b'\x03\x5a\x92\x8f\x20\x16\x39\x20\x4e\x06\xb4\x36\x8b\x1a\x93\x36\x54\x62\xa8\xeb\xbf\xf0\xb8\x81\x81\x51\xb7\x4f\xaa\xb3\xa2\xb6\x1a'
        byte_input1 = b'wrongsignature'

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
            + self.ecpoint_init
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.STLOC1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.LDLOC0
            + Opcode.SYSCALL
            + Interop.CheckSig.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('CheckSig.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(False, result)

    def test_check_multisig(self):
        byte_input0 = b'\x03\xcd\xb0g\xd90\xfdZ\xda\xa6\xc6\x85E\x01`D\xaa\xdd\xecd\xba9\xe5H%\x0e\xae\xa5Q\x17.S\\'
        byte_input1 = b'\x03l\x841\xccx\xb31w\xa6\x0bK\xcc\x02\xba\xf6\r\x05\xfe\xe5\x03\x8es9\xd3\xa6\x88\xe3\x94\xc2\xcb\xd8C'
        byte_input2 = b'wrongsignature1'
        byte_input3 = b'wrongsignature2'

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + self.ecpoint_init
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
            + self.ecpoint_init
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(byte_input3)).to_byte_array(min_length=1)
            + byte_input3
            + Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.LDLOC0
            + Opcode.SYSCALL
            + Interop.CheckMultisig.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisig.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(False, result)

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

    def test_import_crypto(self):
        path = self.get_contract_path('ImportCrypto.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result = self.run_smart_contract(engine, path, 'main', 'unit test')
        self.assertEqual(expected_result, result)

    def test_import_interop_crypto(self):
        path = self.get_contract_path('ImportInteropCrypto.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result = self.run_smart_contract(engine, path, 'main', 'unit test')
        self.assertEqual(expected_result, result)
