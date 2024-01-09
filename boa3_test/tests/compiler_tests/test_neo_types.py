from neo3.core import cryptography, types

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.type.Integer import Integer
from boa3_test.tests import boatestcase


class TestNeoTypes(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/neo_type_test'

    # region UInt160

    async def test_uint160_call_bytes(self):
        await self.set_up_contract('uint160', 'UInt160CallBytes.py')

        value = types.UInt160.zero()
        result, _ = await self.call('uint160', [value.to_array()], return_type=types.UInt160)
        self.assertEqual(value, result)

        value = types.UInt160(bytes(range(types.UInt160._BYTE_LEN)))
        result, _ = await self.call('uint160', [value.to_array()], return_type=types.UInt160)
        self.assertEqual(value, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint160', [bytes(10)], return_type=types.UInt160)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint160', [bytes(30)], return_type=types.UInt160)

    async def test_uint160_call_int(self):
        await self.set_up_contract('uint160', 'UInt160CallInt.py')

        result, _ = await self.call('uint160', [0], return_type=types.UInt160)
        self.assertEqual(types.UInt160.zero(), result)

        integer = 1_000_000_000
        value = types.UInt160(Integer(integer).to_byte_array(min_length=types.UInt160._BYTE_LEN))
        result, _ = await self.call('uint160', [integer], return_type=types.UInt160)
        self.assertEqual(value, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint160', [-50], return_type=types.UInt160)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint160', [bytes(30)], return_type=types.UInt160)

    async def test_uint160_call_without_args(self):
        await self.set_up_contract('uint160', 'UInt160CallWithoutArgs.py')

        result, _ = await self.call('uint160', [], return_type=types.UInt160)
        self.assertEqual(types.UInt160.zero(), result)

    async def test_uint160_return_bytes(self):
        await self.set_up_contract('uint160', 'UInt160ReturnBytes.py')

        value = types.UInt160.zero().to_array()
        result, _ = await self.call('uint160', [value], return_type=bytes)
        self.assertEqual(value, result)

        value = types.UInt160(bytes(range(types.UInt160._BYTE_LEN))).to_array()
        result, _ = await self.call('uint160', [value], return_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint160', [bytes(10)], return_type=bytes)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint160', [bytes(30)], return_type=bytes)

    async def test_uint160_concat_with_bytes(self):
        await self.set_up_contract('uint160', 'UInt160ConcatWithBytes.py')

        value = types.UInt160.zero()
        result, _ = await self.call('uint160_method', [value], return_type=bytes)
        self.assertEqual(value.to_array() + b'123', result)

        value = types.UInt160(bytes(range(20)))
        result, _ = await self.call('uint160_method', [value], return_type=bytes)
        self.assertEqual(value.to_array() + b'123', result)

    def test_uint160_mismatched_type(self):
        path = self.get_contract_path('uint160', 'UInt160CallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region UInt256

    async def test_uint256_call_bytes(self):
        await self.set_up_contract('uint256', 'UInt256CallBytes.py')

        value = types.UInt256.zero()
        result, _ = await self.call('uint256', [value.to_array()], return_type=types.UInt256)
        self.assertEqual(value, result)

        value = types.UInt256(bytes(range(types.UInt256._BYTE_LEN)))
        result, _ = await self.call('uint256', [value.to_array()], return_type=types.UInt256)
        self.assertEqual(value, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint256', [bytes(20)], return_type=types.UInt256)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint256', [bytes(30)], return_type=types.UInt256)

    async def test_uint256_call_int(self):
        await self.set_up_contract('uint256', 'UInt256CallInt.py')

        result, _ = await self.call('uint256', [0], return_type=types.UInt256)
        self.assertEqual(types.UInt256.zero(), result)

        integer = 1_000_000_000
        value = types.UInt256(Integer(integer).to_byte_array(min_length=types.UInt256._BYTE_LEN))
        result, _ = await self.call('uint256', [integer], return_type=types.UInt256)
        self.assertEqual(value, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint256', [-50], return_type=types.UInt256)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint256', [bytes(30)], return_type=types.UInt256)

    async def test_uint256_call_without_args(self):
        await self.set_up_contract('uint256', 'UInt256CallWithoutArgs.py')

        result, _ = await self.call('uint256', [], return_type=types.UInt256)
        self.assertEqual(types.UInt256.zero(), result)

    async def test_uint256_return_bytes(self):
        await self.set_up_contract('uint256', 'UInt256ReturnBytes.py')

        value = types.UInt256.zero().to_array()
        result, _ = await self.call('uint256', [value], return_type=bytes)
        self.assertEqual(value, result)

        value = types.UInt256(bytes(range(types.UInt256._BYTE_LEN))).to_array()
        result, _ = await self.call('uint256', [value], return_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint256', [bytes(10)], return_type=bytes)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('uint256', [bytes(30)], return_type=bytes)

    async def test_uint256_concat_with_bytes(self):
        await self.set_up_contract('uint256', 'UInt256ConcatWithBytes.py')

        value = types.UInt256.zero()
        result, _ = await self.call('uint256_method', [value], return_type=bytes)
        self.assertEqual(value.to_array() + b'123', result)

        value = types.UInt256(bytes(range(32)))
        result, _ = await self.call('uint256_method', [value], return_type=bytes)
        self.assertEqual(value.to_array() + b'123', result)

    def test_uint256_mismatched_type(self):
        path = self.get_contract_path('uint256', 'UInt256CallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region ECPoint

    def create_ecpoint(self, publickey: bytes) -> cryptography.ECPoint:
        return cryptography.ECPoint(publickey, cryptography.ECCCurve.SECP256R1)

    def ecpoint_to_array(self, ecpoint: cryptography.ECPoint) -> bytes:
        return ecpoint.to_array().zfill(33).zfill(33).replace(b'0', b'\x00')

    async def test_ecpoint_call_bytes(self):
        await self.set_up_contract('ecpoint', 'ECPointCallBytes.py')

        value = self.create_ecpoint(bytes(range(2)) * 16)
        result, _ = await self.call('ecpoint', [self.ecpoint_to_array(value)], return_type=cryptography.ECPoint)
        self.assertEqual(value, result)

        value = self.create_ecpoint(bytes(range(32)))
        result, _ = await self.call('ecpoint', [self.ecpoint_to_array(value)], return_type=cryptography.ECPoint)
        self.assertEqual(value, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('ecpoint', [bytes(20)], return_type=cryptography.ECPoint)
        self.assertRegex(str(context.exception), 'unhandled exception')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('ecpoint', [bytes(30)], return_type=cryptography.ECPoint)
        self.assertRegex(str(context.exception), 'unhandled exception')

    def test_ecpoint_call_without_args(self):
        path = self.get_contract_path('ecpoint', 'ECPointCallWithoutArgs.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    async def test_ecpoint_return_bytes(self):
        await self.set_up_contract('ecpoint', 'ECPointReturnBytes.py')

        value = self.ecpoint_to_array(
            self.create_ecpoint(bytes(range(2)) * 16)
        )
        result, _ = await self.call('ecpoint', [value], return_type=bytes)
        self.assertEqual(value, result)

        value = self.ecpoint_to_array(
            self.create_ecpoint(bytes(range(32)))
        )
        result, _ = await self.call('ecpoint', [value], return_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('ecpoint', [bytes(10)], return_type=bytes)
        self.assertRegex(str(context.exception), 'unhandled exception')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('ecpoint', [bytes(30)], return_type=bytes)
        self.assertRegex(str(context.exception), 'unhandled exception')

    async def test_ecpoint_concat_with_bytes(self):
        await self.set_up_contract('ecpoint', 'ECPointConcatWithBytes.py')

        value = self.create_ecpoint(bytes(range(2)) * 16)
        result, _ = await self.call('ecpoint_method', [value], return_type=bytes)
        self.assertEqual(self.ecpoint_to_array(value) + b'123', result)

        value = self.create_ecpoint(bytes(range(32)))
        result, _ = await self.call('ecpoint_method', [value], return_type=bytes)
        self.assertEqual(self.ecpoint_to_array(value) + b'123', result)

    def test_ecpoint_mismatched_type(self):
        path = self.get_contract_path('ecpoint', 'ECPointCallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_ecpoint_script_hash(self):
        await self.set_up_contract('ecpoint', 'ECPointScriptHash.py')

        from boa3.internal.neo import public_key_to_script_hash
        value = self.ecpoint_to_array(
            self.create_ecpoint(bytes(range(2)) * 16)
        )
        script_hash = public_key_to_script_hash(value)

        result, _ = await self.call('Main', [value], return_type=bytes)
        self.assertEqual(script_hash, result)

    async def test_ecpoint_script_hash_from_builtin(self):
        await self.set_up_contract('ecpoint', 'ECPointScriptHashBuiltinCall.py')

        from boa3.internal.neo import public_key_to_script_hash
        value = self.ecpoint_to_array(self.create_ecpoint(bytes(range(2)) * 16))
        script_hash = public_key_to_script_hash(value)

        result, _ = await self.call('Main', [value], return_type=bytes)
        self.assertEqual(script_hash, result)

    # endregion

    # region Opcode

    def test_opcode_manifest_generation(self):
        path = self.get_contract_path('opcode', 'ConcatWithBytes.py')
        _, expected_manifest_output = self.get_deploy_file_paths(path)
        output, manifest = self.get_output(path)

        import os
        from boa3.internal.neo.vm.type.AbiType import AbiType

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(1, len(abi['methods']))

        method = abi['methods'][0]

        self.assertIn('parameters', method)
        self.assertEqual(1, len(method['parameters']))
        self.assertIn('type', method['parameters'][0])
        self.assertEqual(AbiType.ByteArray, method['parameters'][0]['type'])

    async def test_opcode_concat(self):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        await self.set_up_contract('opcode', 'ConcatWithOpcode.py')

        expected_result = Opcode.LDARG0 + Opcode.LDARG1 + Opcode.ADD
        result, _ = await self.call('concat', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_opcode_concat_with_bytes(self):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        await self.set_up_contract('opcode', 'ConcatWithBytes.py')

        concat_bytes = b'12345'
        arg = Opcode.LDARG0
        result, _ = await self.call('concat', [arg], return_type=bytes)
        self.assertEqual(concat_bytes + arg, result)

        arg = Opcode.LDLOC1
        result, _ = await self.call('concat', [arg], return_type=bytes)
        self.assertEqual(concat_bytes + arg, result)

        arg = Opcode.NOP
        result, _ = await self.call('concat', [arg], return_type=bytes)
        self.assertEqual(concat_bytes + arg, result)

    def test_opcode_concat_mismatched_type(self):
        path = self.get_contract_path('opcode', 'ConcatMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_opcode_multiplication(self):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        await self.set_up_contract('opcode', 'OpcodeMultiplication.py')

        multiplier = 4
        result, _ = await self.call('opcode_mult', [multiplier], return_type=bytes)
        self.assertEqual(Opcode.NOP * multiplier, result)

        multiplier = 50
        result, _ = await self.call('opcode_mult', [multiplier], return_type=bytes)
        self.assertEqual(Opcode.NOP * multiplier, result)

    # endregion

    # region IsInstance Neo Types

    async def test_isinstance_contract(self):
        await self.set_up_contract('IsInstanceContract.py')

        result, _ = await self.call('is_contract', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_contract', [[1, 2, 3]], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_contract', ["test_with_string"], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_contract', [42], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_get_contract_a_contract', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_block(self):
        await self.set_up_contract('IsInstanceBlock.py', compile_if_found=True)

        result, _ = await self.call('is_block', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_block', [[1, 2, 3]], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_block', ["test_with_string"], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_block', [42], return_type=bool)
        self.assertEqual(False, result)

        # this one is failing because the get_block return is different (has 9 variables instead of 10)
        # uncomment this when th refactoring of #86a1wvt6u is done
        # result, _ = await self.call('get_block_is_block', [0], return_type=list)
        # self.assertEqual(True, result)

    def test_transaction_cast_and_get_hash(self):
        path = self.get_contract_path('CastTransactionGetHash.py')
        self.assertCompilerLogs(CompilerWarning.TypeCasting, path)

    def test_transaction_implicit_cast_and_get_hash(self):
        path = self.get_contract_path('ImplicitCastTransactionGetHash.py')
        self.assertCompilerLogs(CompilerWarning.TypeCasting, path)

    def test_transaction_cast_and_assign_hash_to_variable(self):
        path = self.get_contract_path('CastTransactionGetHashToVariable.py')
        self.assertCompilerLogs(CompilerWarning.TypeCasting, path)

    async def test_isinstance_transaction(self):
        await self.set_up_contract('IsInstanceTransaction.py')

        tx_hash = await self.get_valid_tx()

        result, _ = await self.call('is_tx', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_tx', [[1, 2, 3]], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_tx', ["test_with_string"], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_tx', [42], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('get_transaction_is_tx', [tx_hash], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_notification(self):
        await self.set_up_contract('IsInstanceNotification.py')

        result, _ = await self.call('is_notification', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_notification', [[1, 2, 3]], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_notification', ["test_with_string"], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_notification', [42], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('get_notifications_is_notification', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_storage_context(self):
        await self.set_up_contract('IsInstanceStorageContext.py')

        result, _ = await self.call('is_context', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_context', [[1, 2, 3]], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_context', ["test_with_string"], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_context', [42], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('get_context_is_context', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_storage_map(self):
        await self.set_up_contract('IsInstanceStorageMap.py')

        result, _ = await self.call('is_storage_map', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_storage_map', [[1, 2, 3]], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_storage_map', ["test_with_string"], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_storage_map', [42], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('create_map_is_storage_map', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_iterator(self):
        await self.set_up_contract('IsInstanceIterator.py')

        result, _ = await self.call('is_iterator', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_iterator', [[1, 2, 3]], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_iterator', ["test_with_string"], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_iterator', [42], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('storage_find_is_context', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_isinstance_ecpoint(self):
        await self.set_up_contract('IsInstanceECPoint.py')

        result, _ = await self.call('is_ecpoint', [bytes(10)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_ecpoint', [self.create_ecpoint(bytes(range(32)))], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('is_ecpoint', [bytes(30)], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('is_ecpoint', [42], return_type=bool)
        self.assertEqual(False, result)

    # endregion
