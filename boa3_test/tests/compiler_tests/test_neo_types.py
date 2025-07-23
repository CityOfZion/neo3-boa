from neo3.core import cryptography, types

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.contracts import CallFlags
from boa3.internal.neo3.network.payloads.verification import WitnessScope, WitnessRuleAction, WitnessConditionType
from boa3.internal.neo3.vm import VMState
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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'uint160', 'UInt160CallMismatchedType.py')

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'uint256', 'UInt256CallMismatchedType.py')

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
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ecpoint', 'ECPointCallWithoutArgs.py')

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ecpoint', 'ECPointCallMismatchedType.py')

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'opcode', 'ConcatMismatchedType.py')

    async def test_opcode_multiplication(self):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        await self.set_up_contract('opcode', 'OpcodeMultiplication.py')

        multiplier = 4
        result, _ = await self.call('opcode_mult', [multiplier], return_type=bytes)
        self.assertEqual(Opcode.NOP * multiplier, result)

        multiplier = 50
        result, _ = await self.call('opcode_mult', [multiplier], return_type=bytes)
        self.assertEqual(Opcode.NOP * multiplier, result)

    async def test_opcode_instantiate(self):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        await self.set_up_contract('opcode', 'OpcodeInstantiate.py')

        for opcode in Opcode:
            result, _ = await self.call('main', [opcode], return_type=bytes)
            self.assertEqual(opcode, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [b'\xff'], return_type=bytes)

        self.assertRegex(str(context.exception), "Invalid Opcode parameter value")

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
        self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastTransactionGetHash.py')

    def test_transaction_implicit_cast_and_get_hash(self):
        self.assertCompilerLogs(CompilerWarning.TypeCasting, 'ImplicitCastTransactionGetHash.py')

    def test_transaction_cast_and_assign_hash_to_variable(self):
        self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastTransactionGetHashToVariable.py')

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

    # region Witness

    async def test_witness_scope_instantiate(self):
        await self.set_up_contract('witness', 'WitnessScopeInstantiate.py')

        result, _ = await self.call('main', [WitnessScope.NONE], return_type=int)
        self.assertEqual(WitnessScope.NONE, result)

        result, _ = await self.call('main', [WitnessScope.CALLED_BY_ENTRY], return_type=int)
        self.assertEqual(WitnessScope.CALLED_BY_ENTRY, result)

        result, _ = await self.call('main', [WitnessScope.CUSTOM_CONTRACTS], return_type=int)
        self.assertEqual(WitnessScope.CUSTOM_CONTRACTS, result)

        result, _ = await self.call('main', [WitnessScope.CUSTOM_GROUPS], return_type=int)
        self.assertEqual(WitnessScope.CUSTOM_GROUPS, result)

        result, _ = await self.call('main', [WitnessScope.WITNESS_RULES], return_type=int)
        self.assertEqual(WitnessScope.WITNESS_RULES, result)

        result, _ = await self.call('main', [WitnessScope.GLOBAL], return_type=int)
        self.assertEqual(WitnessScope.GLOBAL, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [0xFF], return_type=int)

        self.assertRegex(str(context.exception), "Invalid WitnessScope parameter value")

    async def test_witness_scope_not(self):
        await self.set_up_contract('witness', 'WitnessScopeNot.py')

        for witness_scope in WitnessScope:
            result, _ = await self.call('main', [witness_scope], return_type=int)
            self.assertEqual(~witness_scope, result)

    async def test_witness_rule_action_instantiate(self):
        await self.set_up_contract('witness', 'WitnessRuleActionInstantiate.py')

        result, _ = await self.call('main', [WitnessRuleAction.DENY], return_type=int)
        self.assertEqual(WitnessRuleAction.DENY, result)

        result, _ = await self.call('main', [WitnessRuleAction.ALLOW], return_type=int)
        self.assertEqual(WitnessRuleAction.ALLOW, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [2], return_type=int)

        self.assertRegex(str(context.exception), "Invalid WitnessRuleAction parameter value")

    async def test_witness_rule_action_not(self):
        await self.set_up_contract('witness', 'WitnessRuleActionNot.py')

        for witness_rule_action in WitnessRuleAction:
            result, _ = await self.call('main', [witness_rule_action], return_type=int)
            self.assertEqual(~witness_rule_action, result)

    async def test_witness_condition_type_action_instantiate(self):
        await self.set_up_contract('witness', 'WitnessConditionTypeInstantiate.py')

        for witness_condition_type in WitnessConditionType:
            result, _ = await self.call('main', [witness_condition_type], return_type=int)
            self.assertEqual(witness_condition_type, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [0xFF], return_type=int)

        self.assertRegex(str(context.exception), "Invalid WitnessConditionType parameter value")

    async def test_witness_condition_type_action_not(self):
        await self.set_up_contract('witness', 'WitnessConditionTypeNot.py')

        for witness_condition_type in WitnessConditionType:
            result, _ = await self.call('main', [witness_condition_type], return_type=int)
            self.assertEqual(~witness_condition_type, result)

    # endregion

    # region VMState

    async def test_vm_state_instantiate(self):
        await self.set_up_contract('VMStateInstantiate.py')

        result, _ = await self.call('main', [VMState.NONE], return_type=int)
        self.assertEqual(VMState.NONE, result)

        result, _ = await self.call('main', [VMState.HALT], return_type=int)
        self.assertEqual(VMState.HALT, result)

        result, _ = await self.call('main', [VMState.FAULT], return_type=int)
        self.assertEqual(VMState.FAULT, result)

        result, _ = await self.call('main', [VMState.BREAK], return_type=int)
        self.assertEqual(VMState.BREAK, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [0xFF], return_type=int)

        self.assertRegex(str(context.exception), "Invalid VMState parameter value")

    async def test_vm_state_not(self):
        await self.set_up_contract('VMStateNot.py')

        for vm_state in VMState:
            result, _ = await self.call('main', [vm_state], return_type=int)
            self.assertEqual(~vm_state, result)

    # endregion

    # region ContractParameterType

    async def test_contract_parameter_type_instantiate(self):
        await self.set_up_contract('ContractParameterTypeInstantiate.py')

        for param_type in ContractParameterType:
            result, _ = await self.call('main', [param_type], return_type=int)
            self.assertEqual(param_type, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [1], return_type=int)

        self.assertRegex(str(context.exception), "Invalid ContractParameterType parameter value")

    async def test_contract_parameter_type_not(self):
        await self.set_up_contract('ContractParameterTypeNot.py')

        for param_type in ContractParameterType:
            result, _ = await self.call('main', [param_type], return_type=int)
            self.assertEqual(~param_type, result)

    # endregion

    # region CallFlags

    async def test_call_flags_instantiate(self):
        await self.set_up_contract('CallFlagsInstantiate.py')

        for call_flags in CallFlags:
            result, _ = await self.call('main', [call_flags], return_type=int)
            self.assertEqual(call_flags, result)

        result, _ = await self.call('main', [CallFlags.STATES | CallFlags.ALLOW_CALL], return_type=int)
        self.assertEqual(CallFlags.STATES | CallFlags.ALLOW_CALL, result)

        result, _ = await self.call('main', [CallFlags.STATES | CallFlags.ALLOW_NOTIFY], return_type=int)
        self.assertEqual(CallFlags.STATES | CallFlags.ALLOW_NOTIFY, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [128], return_type=int)

        self.assertRegex(str(context.exception), "Invalid CallFlags parameter value")

    async def test_call_flags_not(self):
        await self.set_up_contract('CallFlagsNot.py')

        for call_flags in CallFlags:
            result, _ = await self.call('main', [call_flags], return_type=int)
            self.assertEqual(~call_flags, result)

    # endregion
