from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestCryptoInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/crypto'

    def test_ripemd160_str(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.Ripemd160.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('Ripemd160Str.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        import hashlib
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', b'unit test')
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        self.assertEqual(expected_result.digest(), result)

        expected_result = hashlib.new('ripemd160', b'')
        result = self.run_smart_contract(engine, path, 'Main', '')
        self.assertEqual(expected_result.digest(), result)

    def test_ripemd160_int(self):
        import hashlib
        path = self.get_contract_path('Ripemd160Int.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', Integer(10).to_byte_array())
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_ripemd160_bool(self):
        import hashlib
        path = self.get_contract_path('Ripemd160Bool.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', Integer(1).to_byte_array())
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_ripemd160_bytes(self):
        import hashlib
        path = self.get_contract_path('Ripemd160Bytes.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', b'unit test')
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_hash160_str(self):
        import hashlib
        path = self.get_contract_path('Hash160Str.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        self.assertEqual(expected_result, result)

    def test_hash160_int(self):
        import hashlib
        path = self.get_contract_path('Hash160Int.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(Integer(10).to_byte_array()).digest())).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_hash160_bool(self):
        import hashlib
        path = self.get_contract_path('Hash160Bool.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(Integer(1).to_byte_array()).digest())).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_hash160_bytes(self):
        import hashlib
        path = self.get_contract_path('Hash160Bytes.py')
        engine = TestEngine()
        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_sha256_str(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.Sha256.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('Sha256Str.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        import hashlib
        engine = TestEngine()
        expected_result = hashlib.sha256(b'unit test')
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        self.assertEqual(expected_result.digest(), result)

        expected_result = hashlib.sha256(b'')
        result = self.run_smart_contract(engine, path, 'Main', '')
        self.assertEqual(expected_result.digest(), result)

    def test_sha256_int(self):
        import hashlib
        path = self.get_contract_path('Sha256Int.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(Integer(10).to_byte_array())
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_sha256_bool(self):
        import hashlib
        path = self.get_contract_path('Sha256Bool.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(Integer(1).to_byte_array())
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_sha256_bytes(self):
        import hashlib
        path = self.get_contract_path('Sha256Bytes.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(b'unit test')
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result.digest(), result)

    def test_hash256_str(self):
        import hashlib
        path = self.get_contract_path('Hash256Str.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(hashlib.sha256(b'unit test').digest()).digest()
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        self.assertEqual(expected_result, result)

    def test_hash256_int(self):
        import hashlib
        path = self.get_contract_path('Hash256Int.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(hashlib.sha256(Integer(10).to_byte_array()).digest()).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_hash256_bool(self):
        import hashlib
        path = self.get_contract_path('Hash256Bool.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(hashlib.sha256(Integer(1).to_byte_array()).digest()).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_hash256_bytes(self):
        import hashlib
        path = self.get_contract_path('Hash256Bytes.py')
        engine = TestEngine()
        expected_result = hashlib.sha256(hashlib.sha256(b'unit test').digest()).digest()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(expected_result, result)

    def test_check_multisig_with_ecdsa_secp256r1_str(self):
        string = String('test').to_bytes()
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
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
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.CheckMultisigWithECDsaSecp256r1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisigWithECDsaSecp256r1Str.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256r1_int(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
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
            + Opcode.PUSH10
            + Opcode.SYSCALL
            + Interop.CheckMultisigWithECDsaSecp256r1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisigWithECDsaSecp256r1Int.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256r1_bool(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
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
            + Opcode.PUSH0
            + Opcode.SYSCALL
            + Interop.CheckMultisigWithECDsaSecp256r1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisigWithECDsaSecp256r1Bool.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256r1_byte(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()
        byte_input4 = b'\x00\x01\x02'

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
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
            + Opcode.PUSHDATA1
            + Integer(len(byte_input4)).to_byte_array(min_length=1)
            + byte_input4
            + Opcode.SYSCALL
            + Interop.CheckMultisigWithECDsaSecp256r1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisigWithECDsaSecp256r1Byte.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256k1_str(self):
        string = String('test').to_bytes()
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
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
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.CheckMultisigWithECDsaSecp256k1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisigWithECDsaSecp256k1Str.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256k1_int(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
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
            + Opcode.PUSH10
            + Opcode.SYSCALL
            + Interop.CheckMultisigWithECDsaSecp256k1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisigWithECDsaSecp256k1Int.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256k1_bool(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
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
            + Opcode.PUSH0
            + Opcode.SYSCALL
            + Interop.CheckMultisigWithECDsaSecp256k1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisigWithECDsaSecp256k1Bool.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256k1_byte(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()
        byte_input4 = b'\x00\x01\x02'

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array(min_length=1)
            + byte_input0
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
            + Opcode.PUSHDATA1
            + Integer(len(byte_input4)).to_byte_array(min_length=1)
            + byte_input4
            + Opcode.SYSCALL
            + Interop.CheckMultisigWithECDsaSecp256k1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('CheckMultisigWithECDsaSecp256k1Byte.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_str(self):
        byte_input1 = b'publickey'
        byte_input2 = b'signature'
        string = b'unit test'
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.VerifyWithECDsaSecp256r1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Str.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_bool(self):
        byte_input1 = b'publickey'
        byte_input2 = b'signature'
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSH0
            + Opcode.SYSCALL
            + Interop.VerifyWithECDsaSecp256r1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Bool.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_int(self):
        byte_input1 = b'publickey'
        byte_input2 = b'signature'
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSH10
            + Opcode.SYSCALL
            + Interop.VerifyWithECDsaSecp256r1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Int.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_bytes(self):
        byte_input1 = b'publickey'
        byte_input2 = b'signature'
        string = b'unit test'
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.VerifyWithECDsaSecp256r1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256r1Bytes.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_mismatched_type(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256r1MismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_verify_with_ecdsa_secp256k1_str(self):
        byte_input1 = b'publickey'
        byte_input2 = b'signature'
        string = b'unit test'
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.VerifyWithECDsaSecp256k1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Str.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_bool(self):
        byte_input1 = b'publickey'
        byte_input2 = b'signature'
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSH0
            + Opcode.SYSCALL
            + Interop.VerifyWithECDsaSecp256k1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Bool.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_int(self):
        byte_input1 = b'publickey'
        byte_input2 = b'signature'
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSH10
            + Opcode.SYSCALL
            + Interop.VerifyWithECDsaSecp256k1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Int.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_bytes(self):
        byte_input1 = b'publickey'
        byte_input2 = b'signature'
        string = b'unit test'
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array(min_length=1)
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array(min_length=1)
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.VerifyWithECDsaSecp256k1.interop_method_hash
            + Opcode.DROP
            + Opcode.RET
        )

        path = self.get_contract_path('VerifyWithECDsaSecp256k1Bytes.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_mismatched_type(self):
        path = self.get_contract_path('VerifyWithECDsaSecp256k1MismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)
