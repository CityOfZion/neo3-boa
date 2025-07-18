import hashlib

from boa3.internal import constants
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.contracts.namedcurvehash import NamedCurveHash
from boa3_test.tests import boatestcase


class TestCryptoLibClass(boatestcase.BoaTestCase):
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

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        result, _ = await self.call('main', [], return_type=bytes)
        self.assertEqual(constants.CRYPTO_SCRIPT, result)

    async def test_get_hash_deprecated(self):
        await self.set_up_contract('GetHashDeprecated.py')
        self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'GetHashDeprecated.py')

        result, _ = await self.call('main', [], return_type=bytes)
        self.assertEqual(constants.CRYPTO_SCRIPT, result)

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

    def test_verify_with_ecdsa(self):
        path = self.get_contract_path('VerifyWithECDsa.py')
        self.compile(path)

    def test_verify_with_ecdsa_secp256r1_str(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256r1Sha256Str.py')

    def test_verify_with_ecdsa_secp256r1_bool(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256r1Sha256Bool.py')

    def test_verify_with_ecdsa_secp256r1_int(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256r1Sha256Int.py')

    def test_verify_with_ecdsa_secp256r1sha256_bytes(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurveHash.SECP256R1SHA256).to_byte_array(signed=True, min_length=1)

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

        output, _ = self.assertCompile('VerifyWithECDsaSecp256r1Sha256Bytes.py')
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1keccak256(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurveHash.SECP256R1KECCAK256).to_byte_array(signed=True, min_length=1)

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

        output, _ = self.assertCompile('VerifyWithECDsaSecp256r1Keccak256.py')
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256r1_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256r1Sha256MismatchedType.py')

    def test_verify_with_ecdsa_secp256k1_str(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1Sha256Str.py')

    def test_verify_with_ecdsa_secp256k1_bool(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1Sha256Bool.py')

    def test_verify_with_ecdsa_secp256k1_int(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1Sha256Int.py')

    def test_verify_with_ecdsa_secp256k1sha256_bytes(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurveHash.SECP256K1SHA256).to_byte_array(signed=True, min_length=1)

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

        output, _ = self.assertCompile('VerifyWithECDsaSecp256k1Sha256Bytes.py')
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1keccak256(self):
        byte_input1 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'
        byte_input2 = b'signature'
        string = b'unit test'
        named_curve = Integer(NamedCurveHash.SECP256K1KECCAK256).to_byte_array(signed=True, min_length=1)

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

        output, _ = self.assertCompile('VerifyWithECDsaSecp256k1Keccak256.py')
        self.assertEqual(expected_output, output)

    def test_verify_with_ecdsa_secp256k1_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'VerifyWithECDsaSecp256k1Sha256MismatchedType.py')

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

    async def test_keccak256(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        output, _ = self.assertCompile('Keccak256.py')
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

    def test_bls12_381_add_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Bls12381AddMismatchedType.py')

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

    def test_bls12_381_equal_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Bls12381EqualMismatchedType.py')

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

    def test_bls12_381_mul_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Bls12381MulMismatchedType.py')

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

    def test_bls12_381_pairing_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Bls12381PairingMismatchedType.py')

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

    def test_bls12_381_serialize_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Bls12381SerializeMismatchedType.py')

    async def test_named_curve_hash_instantiate(self):
        await self.set_up_contract('NamedCurveHashInstantiate.py')

        result, _ = await self.call('main', [NamedCurveHash.SECP256K1SHA256], return_type=int)
        self.assertEqual(NamedCurveHash.SECP256K1SHA256, result)

        result, _ = await self.call('main', [NamedCurveHash.SECP256R1SHA256], return_type=int)
        self.assertEqual(NamedCurveHash.SECP256R1SHA256, result)

        result, _ = await self.call('main', [NamedCurveHash.SECP256K1KECCAK256], return_type=int)
        self.assertEqual(NamedCurveHash.SECP256K1KECCAK256, result)

        result, _ = await self.call('main', [NamedCurveHash.SECP256R1KECCAK256], return_type=int)
        self.assertEqual(NamedCurveHash.SECP256R1KECCAK256, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [1], return_type=int)

        self.assertRegex(str(context.exception), "Invalid NamedCurveHash parameter value")

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [-1], return_type=int)

        self.assertRegex(str(context.exception), "Invalid NamedCurveHash parameter value")

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [999], return_type=int)

        self.assertRegex(str(context.exception), "Invalid NamedCurveHash parameter value")

    async def test_named_curve_hash_not(self):
        await self.set_up_contract('NamedCurveHashNot.py')

        for named_curve_hash in NamedCurveHash:
            result, _ = await self.call('main', [named_curve_hash], return_type=int)
            self.assertEqual(~named_curve_hash, result)
