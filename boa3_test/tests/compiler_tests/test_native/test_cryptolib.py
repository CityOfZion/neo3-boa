import hashlib

from boa3.internal import constants
from boa3.internal.exception import CompilerError
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

    async def test_ripemd160_str(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Ripemd160Str.py')

    async def test_ripemd160_int(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Ripemd160Int.py')

    async def test_ripemd160_bool(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Ripemd160Bool.py')

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Sha256Str.py')

    async def test_sha256_int(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Sha256Int.py')

    async def test_sha256_bool(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Sha256Bool.py')

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

    async def test_recover_secp256k1(self):
        await self.set_up_contract('RecoverSecp256K1.py')

        result, _ = await self.call('main', [b'unit test', b'wrong signature'], return_type=None)
        self.assertEqual(None, result)

        message_hash = bytes.fromhex('5ae8317d34d1e595e3fa7247db80c0af4320cce1116de187f8f7e2e099c0d8d0')
        signature = bytes.fromhex(
            "45c0b7f8c09a9e1f1cea0c25785594427b6bf8f9f878a8af0b1abbb48e16d0920d8becd0c220f67c51217eecfd7184ef0732481c843857e6bc7fc095c4f6b78801")
        public_key = bytes.fromhex('034a071e8a6e10aada2b8cf39fa3b5fb3400b04e99ea8ae64ceea1a977dbeaf5d5')
        result, _ = await self.call('main', [message_hash, signature], return_type=bytes)
        self.assertEqual(public_key, result)

        message_hash = bytes.fromhex('586052916fb6f746e1d417766cceffbe1baf95579bab67ad49addaaa6e798862')
        signature = bytes.fromhex(
            "4e0ea79d4a476276e4b067facdec7460d2c98c8a65326a6e5c998fd7c65061140e45aea5034af973410e65cf97651b3f2b976e3fc79c6a93065ed7cb69a2ab5a01")
        public_key = bytes.fromhex('02dbf1f4092deb3cfd4246b2011f7b24840bc5dbedae02f28471ce5b3bfbf06e71')
        result, _ = await self.call('main', [message_hash, signature], return_type=bytes)
        self.assertEqual(public_key, result)

        message_hash = bytes.fromhex('c36d0ecf4bfd178835c97aae7585f6a87de7dfa23cc927944f99a8d60feff68b')
        signature = bytes.fromhex(
            "f25b86e1d8a11d72475b3ed273b0781c7d7f6f9e1dae0dd5d3ee9b84f3fab89163d9c4e1391de077244583e9a6e3d8e8e1f236a3bf5963735353b93b1a3ba93500")
        public_key = bytes.fromhex('03414549fd05bfb7803ae507ff86b99becd36f8d66037a7f5ba612792841d42eb9')
        result, _ = await self.call('main', [message_hash, signature], return_type=bytes)
        self.assertEqual(public_key, result)
