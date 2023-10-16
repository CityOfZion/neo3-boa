from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestNeoTypes(BoaTest):
    default_folder: str = 'test_sc/neo_type_test'

    # region UInt160

    def test_uint160_call_bytes(self):
        path, _ = self.get_deploy_file_paths('uint160', 'UInt160CallBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(20)
        invokes.append(runner.call_contract(path, 'uint160', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        value = bytes(range(20))
        invokes.append(runner.call_contract(path, 'uint160', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'uint160', bytes(10),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'uint160', bytes(30),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_uint160_call_int(self):
        path, _ = self.get_deploy_file_paths('uint160', 'UInt160CallInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'uint160', 0,
                                            expected_result_type=bytes))
        expected_results.append(bytes(20))

        value = Integer(1_000_000_000).to_byte_array(min_length=20)
        invokes.append(runner.call_contract(path, 'uint160', 1_000_000_000,
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'uint160', -50,
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'uint160', bytes(30),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_uint160_call_without_args(self):
        path, _ = self.get_deploy_file_paths('uint160', 'UInt160CallWithoutArgs.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'uint160',
                                            expected_result_type=bytes))
        expected_results.append(bytes(20))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_uint160_return_bytes(self):
        path, _ = self.get_deploy_file_paths('uint160', 'UInt160ReturnBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(20)
        invokes.append(runner.call_contract(path, 'uint160', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        value = bytes(range(20))
        invokes.append(runner.call_contract(path, 'uint160', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'uint160', bytes(10),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'uint160', bytes(30),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_uint160_concat_with_bytes(self):
        path, _ = self.get_deploy_file_paths('uint160', 'UInt160ConcatWithBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(20)
        invokes.append(runner.call_contract(path, 'uint160_method', value,
                                            expected_result_type=bytes))
        expected_results.append(value + b'123')

        value = bytes(range(20))
        invokes.append(runner.call_contract(path, 'uint160_method', value,
                                            expected_result_type=bytes))
        expected_results.append(value + b'123')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_uint160_mismatched_type(self):
        path = self.get_contract_path('uint160', 'UInt160CallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region UInt256

    def test_uint256_call_bytes(self):
        path, _ = self.get_deploy_file_paths('uint256', 'UInt256CallBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(32)
        invokes.append(runner.call_contract(path, 'uint256', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        value = bytes(range(32))
        invokes.append(runner.call_contract(path, 'uint256', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'uint256', bytes(20),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'uint256', bytes(30),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_uint256_call_int(self):
        path, _ = self.get_deploy_file_paths('uint256', 'UInt256CallInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'uint256', 0,
                                            expected_result_type=bytes))
        expected_results.append(bytes(32))

        value = Integer(1_000_000_000).to_byte_array(min_length=32)
        invokes.append(runner.call_contract(path, 'uint256', 1_000_000_000,
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'uint256', -50,
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'uint256', bytes(30),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_uint256_call_without_args(self):
        path, _ = self.get_deploy_file_paths('uint256', 'UInt256CallWithoutArgs.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'uint256',
                                            expected_result_type=bytes))
        expected_results.append(bytes(32))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_uint256_return_bytes(self):
        path, _ = self.get_deploy_file_paths('uint256', 'UInt256ReturnBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(32)
        invokes.append(runner.call_contract(path, 'uint256', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        value = bytes(range(32))
        invokes.append(runner.call_contract(path, 'uint256', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'uint256', bytes(10),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'uint256', bytes(30),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_uint256_concat_with_bytes(self):
        path, _ = self.get_deploy_file_paths('uint256', 'UInt256ConcatWithBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(32)
        invokes.append(runner.call_contract(path, 'uint256_method', value,
                                            expected_result_type=bytes))
        expected_results.append(value + b'123')

        value = bytes(range(32))
        invokes.append(runner.call_contract(path, 'uint256_method', value,
                                            expected_result_type=bytes))
        expected_results.append(value + b'123')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_uint256_mismatched_type(self):
        path = self.get_contract_path('uint256', 'UInt256CallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region ECPoint

    def test_ecpoint_call_bytes(self):
        path, _ = self.get_deploy_file_paths('ecpoint', 'ECPointCallBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(33)
        invokes.append(runner.call_contract(path, 'ecpoint', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        value = bytes(range(33))
        invokes.append(runner.call_contract(path, 'ecpoint', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'ecpoint', bytes(20),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

        runner.call_contract(path, 'ecpoint', bytes(30),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

    def test_ecpoint_call_without_args(self):
        path = self.get_contract_path('ecpoint', 'ECPointCallWithoutArgs.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_ecpoint_return_bytes(self):
        path, _ = self.get_deploy_file_paths('ecpoint', 'ECPointReturnBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(33)
        invokes.append(runner.call_contract(path, 'ecpoint', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        value = bytes(range(33))
        invokes.append(runner.call_contract(path, 'ecpoint', value,
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'ecpoint', bytes(10),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

        runner.call_contract(path, 'ecpoint', bytes(30),
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

    def test_ecpoint_concat_with_bytes(self):
        path, _ = self.get_deploy_file_paths('ecpoint', 'ECPointConcatWithBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = bytes(33)
        invokes.append(runner.call_contract(path, 'ecpoint_method', value,
                                            expected_result_type=bytes))
        expected_results.append(value + b'123')

        value = bytes(range(33))
        invokes.append(runner.call_contract(path, 'ecpoint_method', value,
                                            expected_result_type=bytes))
        expected_results.append(value + b'123')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ecpoint_mismatched_type(self):
        path = self.get_contract_path('ecpoint', 'ECPointCallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_ecpoint_script_hash(self):
        path, _ = self.get_deploy_file_paths('ecpoint', 'ECPointScriptHash.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from boa3.internal.neo import public_key_to_script_hash
        value = bytes(range(33))
        script_hash = public_key_to_script_hash(value)

        invokes.append(runner.call_contract(path, 'Main', value))
        expected_results.append(script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ecpoint_script_hash_from_builtin(self):
        path, _ = self.get_deploy_file_paths('ecpoint', 'ECPointScriptHashBuiltinCall.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from boa3.internal.neo import public_key_to_script_hash
        value = bytes(range(33))
        script_hash = public_key_to_script_hash(value)

        invokes.append(runner.call_contract(path, 'Main', value))
        expected_results.append(script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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

    def test_opcode_concat(self):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        path, _ = self.get_deploy_file_paths('opcode', 'ConcatWithOpcode.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = Opcode.LDARG0 + Opcode.LDARG1 + Opcode.ADD
        invokes.append(runner.call_contract(path, 'concat'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_opcode_concat_with_bytes(self):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        path, _ = self.get_deploy_file_paths('opcode', 'ConcatWithBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        concat_bytes = b'12345'
        arg = Opcode.LDARG0
        invokes.append(runner.call_contract(path, 'concat', arg,
                                            expected_result_type=bytes))
        expected_results.append(concat_bytes + arg)

        arg = Opcode.LDLOC1
        invokes.append(runner.call_contract(path, 'concat', arg,
                                            expected_result_type=bytes))
        expected_results.append(concat_bytes + arg)

        arg = Opcode.NOP
        invokes.append(runner.call_contract(path, 'concat', arg,
                                            expected_result_type=bytes))
        expected_results.append(concat_bytes + arg)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_opcode_concat_mismatched_type(self):
        path = self.get_contract_path('opcode', 'ConcatMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_opcode_multiplication(self):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        path, _ = self.get_deploy_file_paths('opcode', 'OpcodeMultiplication.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        multiplier = 4
        invokes.append(runner.call_contract(path, 'opcode_mult', multiplier,
                                            expected_result_type=bytes))
        expected_results.append(Opcode.NOP * multiplier)

        multiplier = 50
        invokes.append(runner.call_contract(path, 'opcode_mult', multiplier,
                                            expected_result_type=bytes))
        expected_results.append(Opcode.NOP * multiplier)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region IsInstance Neo Types

    def test_isinstance_contract(self):
        path, _ = self.get_deploy_file_paths('IsInstanceContract.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'is_contract', bytes(10)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_contract', [1, 2, 3]))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_contract', "test_with_string"))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_contract', 42))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invokes.append(runner.call_contract(path, 'is_get_contract_a_contract'))
        expected_results.append(True)

    def test_isinstance_block(self):
        path, _ = self.get_deploy_file_paths('IsInstanceBlock.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'is_block', bytes(10)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_block', [1, 2, 3]))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_block', "test_with_string"))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_block', 42))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'get_block_is_block', 0))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_transaction_cast_and_get_hash(self):
        path = self.get_contract_path('CastTransactionGetHash.py')
        self.assertCompilerLogs(CompilerWarning.TypeCasting, path)

    def test_transaction_implicit_cast_and_get_hash(self):
        path = self.get_contract_path('ImplicitCastTransactionGetHash.py')
        self.assertCompilerLogs(CompilerWarning.TypeCasting, path)

    def test_transaction_cast_and_assign_hash_to_variable(self):
        path = self.get_contract_path('CastTransactionGetHashToVariable.py')
        self.assertCompilerLogs(CompilerWarning.TypeCasting, path)

    def test_isinstance_transaction(self):
        path, _ = self.get_deploy_file_paths('IsInstanceTransaction.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        contract_deploy = runner.deploy_contract(path)
        runner.update_contracts(export_checkpoint=True)
        tx_hash = contract_deploy.tx_id.to_array()

        invokes.append(runner.call_contract(path, 'is_tx', bytes(10)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_tx', [1, 2, 3]))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_tx', "test_with_string"))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_tx', 42))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'get_transaction_is_tx', tx_hash))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_notification(self):
        path, _ = self.get_deploy_file_paths('IsInstanceNotification.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'is_notification', bytes(10)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_notification', [1, 2, 3]))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_notification', "test_with_string"))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_notification', 42))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'get_notifications_is_notification'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_storage_context(self):
        path, _ = self.get_deploy_file_paths('IsInstanceStorageContext.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'is_context', bytes(10)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_context', [1, 2, 3]))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_context', "test_with_string"))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_context', 42))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'get_context_is_context'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_storage_map(self):
        path, _ = self.get_deploy_file_paths('IsInstanceStorageMap.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'is_storage_map', bytes(10)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_storage_map', [1, 2, 3]))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_storage_map', "test_with_string"))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_storage_map', 42))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'create_map_is_storage_map'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_iterator(self):
        path, _ = self.get_deploy_file_paths('IsInstanceIterator.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'is_iterator', bytes(10)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_iterator', [1, 2, 3]))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_iterator', "test_with_string"))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_iterator', 42))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'storage_find_is_context'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_ecpoint(self):
        path, _ = self.get_deploy_file_paths('IsInstanceECPoint.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'is_ecpoint', bytes(10)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_ecpoint', bytes(33)))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'is_ecpoint', bytes(30)))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'is_ecpoint', 42))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion
