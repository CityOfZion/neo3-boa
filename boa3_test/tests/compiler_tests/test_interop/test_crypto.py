import hashlib

from boa3.internal.exception import CompilerError
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.contracts.namedcurve import NamedCurve
from boa3_test.tests import boatestcase


class TestCryptoInterop(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/interop_test/crypto'
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

    async def test_ripemd160_str(self):
        await self.set_up_contract('Ripemd160Str.py')

        expected_result = hashlib.new('ripemd160', b'unit test')
        result, _ = await self.call('Main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

        expected_result = hashlib.new('ripemd160', b'')
        result, _ = await self.call('Main', [''], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

    async def test_ripemd160_int(self):
        await self.set_up_contract('Ripemd160Int.py')

        expected_result = hashlib.new('ripemd160', Integer(10).to_byte_array())
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

    async def test_ripemd160_bool(self):
        await self.set_up_contract('Ripemd160Bool.py')

        expected_result = hashlib.new('ripemd160', Integer(1).to_byte_array())
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

    async def test_ripemd160_bytes(self):
        await self.set_up_contract('Ripemd160Bytes.py')

        expected_result = hashlib.new('ripemd160', b'unit test')
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

    def test_ripemd160_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'Ripemd160TooManyArguments.py')

    def test_ripemd160_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'Ripemd160TooFewArguments.py')

    async def test_hash160_str(self):
        await self.set_up_contract('Hash160Str.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result, _ = await self.call('Main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash160_int(self):
        await self.set_up_contract('Hash160Int.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(Integer(10).to_byte_array()).digest())).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash160_bool(self):
        await self.set_up_contract('Hash160Bool.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(Integer(1).to_byte_array()).digest())).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash160_bytes(self):
        await self.set_up_contract('Hash160Bytes.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_sha256_str(self):
        await self.set_up_contract('Sha256Str.py')

        expected_result = hashlib.sha256(b'unit test')
        result, _ = await self.call('Main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

        expected_result = hashlib.sha256(b'')
        result, _ = await self.call('Main', [''], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

    async def test_sha256_int(self):
        await self.set_up_contract('Sha256Int.py')

        expected_result = hashlib.sha256(Integer(10).to_byte_array())
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

    async def test_sha256_bool(self):
        await self.set_up_contract('Sha256Bool.py')

        expected_result = hashlib.sha256(Integer(1).to_byte_array())
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

    async def test_sha256_bytes(self):
        await self.set_up_contract('Sha256Bytes.py')

        expected_result = hashlib.sha256(b'unit test')
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result.digest(), result)

    def test_sha256_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'Sha256TooManyArguments.py')

    def test_sha256_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'Sha256TooFewArguments.py')

    async def test_hash256_str(self):
        await self.set_up_contract('Hash256Str.py')

        expected_result = hashlib.sha256(hashlib.sha256(b'unit test').digest()).digest()
        result, _ = await self.call('Main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash256_int(self):
        await self.set_up_contract('Hash256Int.py')

        expected_result = hashlib.sha256(hashlib.sha256(Integer(10).to_byte_array()).digest()).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash256_bool(self):
        await self.set_up_contract('Hash256Bool.py')

        expected_result = hashlib.sha256(hashlib.sha256(Integer(1).to_byte_array()).digest()).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash256_bytes(self):
        await self.set_up_contract('Hash256Bytes.py')

        expected_result = hashlib.sha256(hashlib.sha256(b'unit test').digest()).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    def test_check_sig_compile(self):
        byte_input0 = b'\x03\x5a\x92\x8f\x20\x16\x39\x20\x4e\x06\xb4\x36\x8b\x1a\x93\x36\x54\x62\xa8\xeb\xbf\xf0\xb8\x81\x81\x51\xb7\x4f\xaa\xb3\xa2\xb6\x1a'
        byte_input1 = b'wrongsignature'

        from boa3.internal.model.builtin.interop.interop import Interop

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

        output, _ = self.assertCompile('CheckSig.py')
        self.assertEqual(expected_output, output)

    async def test_check_sig_run(self):
        await self.set_up_contract('CheckSig.py')

        result, _ = await self.call('main', [], return_type=bool)
        self.assertEqual(False, result)

    def test_check_multisig_compile(self):
        byte_input0 = b'\x03\xcd\xb0g\xd90\xfdZ\xda\xa6\xc6\x85E\x01`D\xaa\xdd\xecd\xba9\xe5H%\x0e\xae\xa5Q\x17.S\\'
        byte_input1 = b'\x03l\x841\xccx\xb31w\xa6\x0bK\xcc\x02\xba\xf6\r\x05\xfe\xe5\x03\x8es9\xd3\xa6\x88\xe3\x94\xc2\xcb\xd8C'
        byte_input2 = b'wrongsignature1'
        byte_input3 = b'wrongsignature2'

        from boa3.internal.model.builtin.interop.interop import Interop

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

        output, _ = self.assertCompile('CheckMultisig.py')
        self.assertEqual(expected_output, output)

    async def test_check_multisig_run(self):
        await self.set_up_contract('CheckMultisig.py')

        result, _ = await self.call('main', [], return_type=bool)
        self.assertEqual(False, result)

    def test_verify_with_ecdsa(self):
        path = self.get_contract_path('VerifyWithECDsa.py')
        self.compile(path)

    def test_verify_with_ecdsa_secp256r1_str(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256r1Str.py')

    def test_verify_with_ecdsa_secp256r1_bool(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256r1Bool.py')

    def test_verify_with_ecdsa_secp256r1_int(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256r1Int.py')

    def test_verify_with_ecdsa_secp256r1_bytes(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1Bool.py')

    def test_verify_with_ecdsa_secp256r1_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256r1MismatchedType.py')

    def test_verify_with_ecdsa_secp256k1_str(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1Str.py')

    def test_verify_with_ecdsa_secp256k1_bool(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1Bool.py')

    def test_verify_with_ecdsa_secp256k1_int(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1Int.py')

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

        output, _ = self.assertCompile('VerifyWithECDsaSecp256k1Bytes.py')
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1MismatchedType.py')

    async def test_import_crypto(self):
        await self.set_up_contract('ImportCrypto.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result, _ = await self.call('main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_import_interop_crypto(self):
        await self.set_up_contract('ImportInteropCrypto.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result, _ = await self.call('main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

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

        output, _ = self.assertCompile('Murmur32.py')
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

        output, _ = self.assertCompile('Bls12381Add.py')
        self.assertEqual(expected_output, output)

    def test_bls12_381_deserialize(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        output, _ = self.assertCompile('Bls12381Deserialize.py')
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

        output, _ = self.assertCompile('Bls12381Equal.py')
        self.assertEqual(expected_output, output)

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

        output, _ = self.assertCompile('Bls12381Mul.py')
        self.assertEqual(expected_output, output)

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

        output, _ = self.assertCompile('Bls12381Pairing.py')
        self.assertEqual(expected_output, output)

    def test_bls12_381_serialize(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        output, _ = self.assertCompile('Bls12381Serialize.py')
        self.assertEqual(expected_output, output)
