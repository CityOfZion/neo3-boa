from typing import cast

from boaconstructor import storage
from neo3.core import cryptography, types

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.contracts import CallFlags
from boa3.internal.neo3.contracts import TriggerType
from boa3.internal.neo3.network.payloads.verification import WitnessScope, WitnessRuleAction, WitnessConditionType
from boa3.internal.neo3.vm import VMState
from boa3_test.tests import boatestcase, annotation


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
        await self.set_up_contract('callflags', 'CallFlagsInstantiate.py')

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
        await self.set_up_contract('callflags', 'CallFlagsNot.py')

        for call_flags in CallFlags:
            result, _ = await self.call('main', [call_flags], return_type=int)
            self.assertEqual(~call_flags, result)

    async def test_call_flags_type(self):
        await self.set_up_contract('callflags', 'CallFlagsType.py')

        from neo3.contracts.callflags import CallFlags

        result, _ = await self.call('main', ['ALL'], return_type=int)
        self.assertEqual(CallFlags.ALL, result)

        result, _ = await self.call('main', ['READ_ONLY'], return_type=int)
        self.assertEqual(CallFlags.READ_ONLY, result)

        result, _ = await self.call('main', ['STATES'], return_type=int)
        self.assertEqual(CallFlags.STATES, result)

        result, _ = await self.call('main', ['ALLOW_NOTIFY'], return_type=int)
        self.assertEqual(CallFlags.ALLOW_NOTIFY, result)

        result, _ = await self.call('main', ['ALLOW_CALL'], return_type=int)
        self.assertEqual(CallFlags.ALLOW_CALL, result)

        result, _ = await self.call('main', ['WRITE_STATES'], return_type=int)
        self.assertEqual(CallFlags.WRITE_STATES, result)

        result, _ = await self.call('main', ['READ_STATES'], return_type=int)
        self.assertEqual(CallFlags.READ_STATES, result)

        result, _ = await self.call('main', ['NONE'], return_type=int)
        self.assertEqual(CallFlags.NONE, result)

    async def test_get_call_flags(self):
        await self.set_up_contract('callflags', 'CallScriptHashWithFlags.py')
        call_hash = await self.compile_and_deploy('callflags', 'GetCallFlags.py')

        from neo3.contracts.callflags import CallFlags

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.ALL], return_type=int)
        self.assertEqual(CallFlags.ALL, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.READ_ONLY], return_type=int)
        self.assertEqual(CallFlags.READ_ONLY, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.STATES], return_type=int)
        self.assertEqual(CallFlags.STATES, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.NONE], return_type=int)
        self.assertEqual(CallFlags.NONE, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.READ_STATES], return_type=int)
        self.assertEqual(CallFlags.READ_STATES, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.WRITE_STATES], return_type=int)
        self.assertEqual(CallFlags.WRITE_STATES, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.ALLOW_CALL], return_type=int)
        self.assertEqual(CallFlags.ALLOW_CALL, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.ALLOW_NOTIFY], return_type=int)
        self.assertEqual(CallFlags.ALLOW_NOTIFY, result)

    # endregion

    # region Block

    async def test_block_constructor(self):
        await self.set_up_contract('Block.py')

        zero_uint256 = types.UInt256.zero()
        expected: annotation.Block = (
            zero_uint256,  # hash
            0,  # version
            zero_uint256,  # previous hash
            zero_uint256,  # merkle root
            0,  # timestamp
            0,  # nonce
            0,  # index
            0,  # primary index
            types.UInt160.zero(),  # next consensus
            0  # tx count
        )
        result, _ = await self.call('main', [], return_type=annotation.Block)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    # endregion

    # region Transaction

    async def test_transaction_init(self):
        await self.set_up_contract('Transaction.py')

        expected: annotation.Transaction = (
            types.UInt256.zero(),  # hash
            0,  # version
            0,  # nonce
            types.UInt160.zero(),  # sender
            0,  # system fee
            0,  # network fee
            0,  # valid until block
            b''  # script
        )
        result, _ = await self.call('main', [], return_type=annotation.Transaction)
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    # endregion

    # region Iterator

    def test_iterator_create(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'iterator', 'IteratorCreate.py')

    async def test_iterator_next(self):
        await self.set_up_contract('iterator', 'IteratorNext.py')

        prefix = b'test_iterator_next'
        result, _ = await self.call('has_next', [prefix], return_type=bool)
        self.assertEqual(False, result)

        key = prefix + b'example1'
        value = 1
        await self.call('store_data', [key, value], return_type=None, signing_accounts=[self.genesis])

        contract_storage = cast(
            dict[bytes, int],
            await self.get_storage(
                prefix=prefix,
                values_post_processor=storage.as_int
            )
        )
        self.assertIn(key, contract_storage)
        self.assertEqual(value, contract_storage[key])

        result, _ = await self.call('has_next', [prefix], return_type=bool)
        self.assertEqual(True, result)

    async def test_iterator_value(self):
        await self.set_up_contract('iterator', 'IteratorValue.py')

        prefix = b'test_iterator_value'
        result, _ = await self.call('test_iterator', [prefix], return_type=None)
        self.assertIsNone(result)

        key = prefix + b'example1'
        await self.call('store_data', [key, 1], return_type=None, signing_accounts=[self.genesis])

        contract_storage = cast(
            dict[bytes, int],
            await self.get_storage(
                prefix=prefix
            )
        )
        self.assertIn(key, contract_storage)

        result, _ = await self.call('test_iterator', [prefix], return_type=tuple[bytes, bytes])
        self.assertEqual((key, contract_storage[key]), result)

    def test_iterator_value_dict_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'iterator', 'IteratorValueMismatchedType.py')

    async def test_import_iterator(self):
        await self.set_up_contract('iterator', 'ImportIterator.py')

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('return_iterator', [], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

    async def test_iterator_implicit_typing(self):
        await self.set_up_contract('iterator', 'IteratorImplicitTyping.py')

        prefix = b'test_iterator_'
        prefix_str = String.from_bytes(prefix)
        result, _ = await self.call('search_storage', [prefix], return_type=dict[str, int])
        self.assertEqual({}, result)

        result, _ = await self.call('store', [prefix + b'1', 1], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        result, _ = await self.call('store', [prefix + b'2', 2], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        result, _ = await self.call('search_storage', [prefix], return_type=dict[str, int])
        self.assertEqual({f'{prefix_str}1': 1, f'{prefix_str}2': 2}, result)

    async def test_iterator_value_access(self):
        await self.set_up_contract('iterator', 'IteratorValueAccess.py')

        prefix = b'test_iterator_'
        prefix_str = String.from_bytes(prefix)
        result, _ = await self.call('search_storage', [prefix], return_type=dict[str, int])
        self.assertEqual({}, result)

        result, _ = await self.call('store', [prefix + b'1', 1], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        result, _ = await self.call('store', [prefix + b'2', 2], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        result, _ = await self.call('search_storage', [prefix], return_type=dict[str, int])
        self.assertEqual({f'{prefix_str}1': 1, f'{prefix_str}2': 2}, result)

    # endregion

    # region TriggerType

    async def test_trigger_type_instantiate(self):
        await self.set_up_contract('triggertype', 'TriggerTypeInstantiate.py')

        for trigger_type in TriggerType:
            result, _ = await self.call('main', [trigger_type], return_type=int)
            self.assertEqual(trigger_type, result)

        result, _ = await self.call('main', [TriggerType.ON_PERSIST | TriggerType.VERIFICATION], return_type=int)
        self.assertEqual(TriggerType.ON_PERSIST | TriggerType.VERIFICATION, result)

        result, _ = await self.call('main', [TriggerType.POST_PERSIST | TriggerType.APPLICATION], return_type=int)
        self.assertEqual(TriggerType.POST_PERSIST | TriggerType.APPLICATION, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [128], return_type=int)

        self.assertRegex(str(context.exception), "Invalid TriggerType parameter value")

    async def test_boa2_trigger_type_test(self):
        await self.set_up_contract('triggertype', 'TriggerTypeBoa2Test.py')

        result, _ = await self.call('main', [1], return_type=int)
        self.assertEqual(0x40, result)

        result, _ = await self.call('main', [2], return_type=int)
        self.assertEqual(0x20, result)

        result, _ = await self.call('main', [3], return_type=bytes)
        self.assertEqual(b'\x20', result)

        result, _ = await self.call('main', [0], return_type=int)
        self.assertEqual(-1, result)

    def test_is_application_trigger_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        application = Integer(TriggerType.APPLICATION).to_byte_array()
        expected_output = (
                Opcode.SYSCALL
                + Interop.GetTrigger.interop_method_hash
                + Opcode.PUSHINT8 + application
                + Opcode.NUMEQUAL
                + Opcode.RET
        )

        output, _ = self.assertCompile('triggertype/TriggerApplication.py')
        self.assertEqual(expected_output, output)

    def test_is_verification_trigger_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        verification = Integer(TriggerType.VERIFICATION).to_byte_array()
        expected_output = (
                Opcode.SYSCALL
                + Interop.GetTrigger.interop_method_hash
                + Opcode.PUSHINT8 + verification
                + Opcode.NUMEQUAL
                + Opcode.RET
        )

        output, _ = self.assertCompile('triggertype/TriggerVerification.py')
        self.assertEqual(expected_output, output)

    async def test_trigger_type_not(self):
        await self.set_up_contract('triggertype', 'TriggerTypeNot.py')

        for trigger_type in TriggerType:
            result, _ = await self.call('main', [trigger_type], return_type=int)
            self.assertEqual(~trigger_type, result)

    async def test_trigger_not_system(self):
        await self.set_up_contract('triggertype', 'TriggerNotSystem.py')

        result, _ = await self.call('main', return_type=bool)
        self.assertEqual(True, result)

    async def test_is_application_trigger_run(self):
        await self.set_up_contract('triggertype', 'TriggerApplication.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_is_verification_trigger_run(self):
        await self.set_up_contract('triggertype', 'TriggerVerification.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(False, result)

    # endregion
