from boa3.exception import CompilerError, CompilerWarning
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNeoTypes(BoaTest):
    default_folder: str = 'test_sc/neo_type_test'

    # region UInt160

    def test_uint160_call_bytes(self):
        path = self.get_contract_path('uint160', 'UInt160CallBytes.py')

        engine = TestEngine()
        value = bytes(20)
        result = self.run_smart_contract(engine, path, 'uint160', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(20))
        result = self.run_smart_contract(engine, path, 'uint160', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(10),
                                    expected_result_type=bytes)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(30),
                                    expected_result_type=bytes)

    def test_uint160_call_int(self):
        path = self.get_contract_path('uint160', 'UInt160CallInt.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'uint160', 0,
                                         expected_result_type=bytes)
        self.assertEqual(bytes(20), result)

        value = Integer(1_000_000_000).to_byte_array(min_length=20)
        result = self.run_smart_contract(engine, path, 'uint160', 1_000_000_000,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', -50,
                                    expected_result_type=bytes)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(30),
                                    expected_result_type=bytes)

    def test_uint160_call_without_args(self):
        path = self.get_contract_path('uint160', 'UInt160CallWithoutArgs.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'uint160',
                                         expected_result_type=bytes)
        self.assertEqual(bytes(20), result)

    def test_uint160_return_bytes(self):
        path = self.get_contract_path('uint160', 'UInt160ReturnBytes.py')

        engine = TestEngine()
        value = bytes(20)
        result = self.run_smart_contract(engine, path, 'uint160', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(20))
        result = self.run_smart_contract(engine, path, 'uint160', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(10),
                                    expected_result_type=bytes)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(30),
                                    expected_result_type=bytes)

    def test_uint160_concat_with_bytes(self):
        path = self.get_contract_path('uint160', 'UInt160ConcatWithBytes.py')
        engine = TestEngine()
        value = bytes(20)
        result = self.run_smart_contract(engine, path, 'uint160_method', value,
                                         expected_result_type=bytes)
        self.assertEqual(value + b'123', result)

        value = bytes(range(20))
        result = self.run_smart_contract(engine, path, 'uint160_method', value,
                                         expected_result_type=bytes)
        self.assertEqual(value + b'123', result)

    def test_uint160_mismatched_type(self):
        path = self.get_contract_path('uint160', 'UInt160CallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region UInt256

    def test_uint256_call_bytes(self):
        path = self.get_contract_path('uint256', 'UInt256CallBytes.py')

        engine = TestEngine()
        value = bytes(32)
        result = self.run_smart_contract(engine, path, 'uint256', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(32))
        result = self.run_smart_contract(engine, path, 'uint256', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(20),
                                    expected_result_type=bytes)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(30),
                                    expected_result_type=bytes)

    def test_uint256_call_int(self):
        path = self.get_contract_path('uint256', 'UInt256CallInt.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'uint256', 0,
                                         expected_result_type=bytes)
        self.assertEqual(bytes(32), result)

        value = Integer(1_000_000_000).to_byte_array(min_length=32)
        result = self.run_smart_contract(engine, path, 'uint256', 1_000_000_000,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', -50,
                                    expected_result_type=bytes)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(30),
                                    expected_result_type=bytes)

    def test_uint256_call_without_args(self):
        path = self.get_contract_path('uint256', 'UInt256CallWithoutArgs.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'uint256',
                                         expected_result_type=bytes)
        self.assertEqual(bytes(32), result)

    def test_uint256_return_bytes(self):
        path = self.get_contract_path('uint256', 'UInt256ReturnBytes.py')

        engine = TestEngine()
        value = bytes(32)
        result = self.run_smart_contract(engine, path, 'uint256', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(32))
        result = self.run_smart_contract(engine, path, 'uint256', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(10),
                                    expected_result_type=bytes)

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(30),
                                    expected_result_type=bytes)

    def test_uint256_concat_with_bytes(self):
        path = self.get_contract_path('uint256', 'UInt256ConcatWithBytes.py')
        engine = TestEngine()
        value = bytes(32)
        result = self.run_smart_contract(engine, path, 'uint256_method', value,
                                         expected_result_type=bytes)
        self.assertEqual(value + b'123', result)

        value = bytes(range(32))
        result = self.run_smart_contract(engine, path, 'uint256_method', value,
                                         expected_result_type=bytes)
        self.assertEqual(value + b'123', result)

    def test_uint256_mismatched_type(self):
        path = self.get_contract_path('uint256', 'UInt256CallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region ECPoint

    def test_ecpoint_call_bytes(self):
        path = self.get_contract_path('ecpoint', 'ECPointCallBytes.py')
        engine = TestEngine()

        value = bytes(33)
        result = self.run_smart_contract(engine, path, 'ecpoint', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(33))
        result = self.run_smart_contract(engine, path, 'ecpoint', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaisesRegex(TestExecutionException, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}'):
            self.run_smart_contract(engine, path, 'ecpoint', bytes(20),
                                    expected_result_type=bytes)

        with self.assertRaisesRegex(TestExecutionException, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}'):
            self.run_smart_contract(engine, path, 'ecpoint', bytes(30),
                                    expected_result_type=bytes)

    def test_ecpoint_call_without_args(self):
        path = self.get_contract_path('ecpoint', 'ECPointCallWithoutArgs.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_ecpoint_return_bytes(self):
        path = self.get_contract_path('ecpoint', 'ECPointReturnBytes.py')
        engine = TestEngine()

        value = bytes(33)
        result = self.run_smart_contract(engine, path, 'ecpoint', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(33))
        result = self.run_smart_contract(engine, path, 'ecpoint', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaisesRegex(TestExecutionException, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}'):
            self.run_smart_contract(engine, path, 'ecpoint', bytes(10),
                                    expected_result_type=bytes)

        with self.assertRaisesRegex(TestExecutionException, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}'):
            self.run_smart_contract(engine, path, 'ecpoint', bytes(30),
                                    expected_result_type=bytes)

    def test_ecpoint_concat_with_bytes(self):
        path = self.get_contract_path('ecpoint', 'ECPointConcatWithBytes.py')
        engine = TestEngine()

        value = bytes(33)
        result = self.run_smart_contract(engine, path, 'ecpoint_method', value,
                                         expected_result_type=bytes)
        self.assertEqual(value + b'123', result)

        value = bytes(range(33))
        result = self.run_smart_contract(engine, path, 'ecpoint_method', value,
                                         expected_result_type=bytes)
        self.assertEqual(value + b'123', result)

    def test_ecpoint_mismatched_type(self):
        path = self.get_contract_path('ecpoint', 'ECPointCallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_ecpoint_script_hash(self):
        path = self.get_contract_path('ecpoint', 'ECPointScriptHash.py')
        engine = TestEngine()

        from boa3.neo import public_key_to_script_hash
        value = bytes(range(33))
        script_hash = public_key_to_script_hash(value)

        result = self.run_smart_contract(engine, path, 'Main', value)
        self.assertEqual(script_hash, result)

    def test_ecpoint_script_hash_from_builtin(self):
        path = self.get_contract_path('ecpoint', 'ECPointScriptHashBuiltinCall.py')
        engine = TestEngine()

        from boa3.neo import public_key_to_script_hash
        value = bytes(range(33))
        script_hash = public_key_to_script_hash(value)

        result = self.run_smart_contract(engine, path, 'Main', value)
        self.assertEqual(script_hash, result)

    # endregion

    # region ByteString

    def test_byte_string_manifest_generation(self):
        path = self.get_contract_path('bytestring', 'ByteStringToBool.py')
        expected_manifest_output = path.replace('.py', '.manifest.json')
        output, manifest = self.get_output(path)

        import os
        from boa3.neo.vm.type.AbiType import AbiType

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

    def test_byte_string_to_bool(self):
        path = self.get_contract_path('bytestring', 'ByteStringToBool.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'to_bool', b'\x00')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'to_bool', '\x00')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'to_bool', b'\x01')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'to_bool', '\x01')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'to_bool', b'\x02')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'to_bool', '\x02')
        self.assertEqual(True, result)

    def test_byte_string_to_bool_with_builtin(self):
        path = self.get_contract_path('bytestring', 'ByteStringToBoolWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'to_bool', b'\x00')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'to_bool', '\x00')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'to_bool', b'\x01')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'to_bool', '\x01')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'to_bool', b'\x02')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'to_bool', '\x02')
        self.assertEqual(True, result)

    def test_byte_string_to_int(self):
        path = self.get_contract_path('bytestring', 'ByteStringToInt.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'to_int', b'\x01\x02')
        self.assertEqual(513, result)
        result = self.run_smart_contract(engine, path, 'to_int', '\x01\x02')
        self.assertEqual(513, result)

    def test_byte_string_to_int_with_builtin(self):
        path = self.get_contract_path('bytestring', 'ByteStringToIntWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'to_int', b'\x01\x02')
        self.assertEqual(513, result)
        result = self.run_smart_contract(engine, path, 'to_int', '\x01\x02')
        self.assertEqual(513, result)

    def test_byte_string_to_str(self):
        path = self.get_contract_path('bytestring', 'ByteStringToStr.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'to_str', b'abc')
        self.assertEqual('abc', result)

        result = self.run_smart_contract(engine, path, 'to_str', b'123')
        self.assertEqual('123', result)

    def test_byte_string_to_str_with_builtin(self):
        path = self.get_contract_path('bytestring', 'ByteStringToStrWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'to_str', b'abc')
        self.assertEqual('abc', result)

        result = self.run_smart_contract(engine, path, 'to_str', b'123')
        self.assertEqual('123', result)

    def test_byte_string_to_bytes(self):
        path = self.get_contract_path('bytestring', 'ByteStringToBytes.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'to_bytes', 'abc',
                                         expected_result_type=bytes)
        self.assertEqual(b'abc', result)

        result = self.run_smart_contract(engine, path, 'to_bytes', '123',
                                         expected_result_type=bytes)
        self.assertEqual(b'123', result)

    def test_byte_string_to_bytes_with_builtin(self):
        path = self.get_contract_path('bytestring', 'ByteStringToBytesWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'to_bytes', 'abc',
                                         expected_result_type=bytes)
        self.assertEqual(b'abc', result)

        result = self.run_smart_contract(engine, path, 'to_bytes', '123',
                                         expected_result_type=bytes)
        self.assertEqual(b'123', result)

    def test_concat_with_bytes(self):
        path = self.get_contract_path('bytestring', 'ConcatWithBytes.py')
        engine = TestEngine()

        prefix = b'12345'
        arg = b'a'
        result = self.run_smart_contract(engine, path, 'concat', arg,
                                         expected_result_type=bytes)
        self.assertEqual(prefix + arg, result)

        arg = '6789'
        result = self.run_smart_contract(engine, path, 'concat', arg,
                                         expected_result_type=bytes)
        self.assertEqual(prefix + String(arg).to_bytes(), result)

    def test_concat_with_str(self):
        path = self.get_contract_path('bytestring', 'ConcatWithStr.py')
        engine = TestEngine()

        prefix = '12345'
        arg = 'a'
        result = self.run_smart_contract(engine, path, 'concat', arg)
        self.assertEqual(prefix + arg, result)

        arg = b'6789'
        result = self.run_smart_contract(engine, path, 'concat', arg)
        self.assertEqual(prefix + String.from_bytes(arg), result)

    def test_concat_with_bytestring(self):
        path = self.get_contract_path('bytestring', 'ConcatWithByteString.py')
        engine = TestEngine()

        prefix = '12345'
        arg = 'a'
        result = self.run_smart_contract(engine, path, 'concat', prefix, arg)
        self.assertEqual(prefix + arg, result)

        arg = b'a'
        result = self.run_smart_contract(engine, path, 'concat', prefix, arg)
        self.assertEqual(prefix + String.from_bytes(arg), result)

        prefix = b'12345'
        arg = b'6789'
        result = self.run_smart_contract(engine, path, 'concat', prefix, arg,
                                         expected_result_type=bytes)
        self.assertEqual(prefix + arg, result)

        arg = '6789'
        result = self.run_smart_contract(engine, path, 'concat', prefix, arg,
                                         expected_result_type=bytes)
        self.assertEqual(prefix + String(arg).to_bytes(), result)

    def test_bytestring_multiplication(self):
        path = self.get_contract_path('bytestring', 'ByteStringMultiplication.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'bytestring_mult', b'a', 4,
                                         expected_result_type=bytes)
        self.assertEqual(b'aaaa', result)
        result = self.run_smart_contract(engine, path, 'bytestring_mult', 'unit', 50)
        self.assertEqual('unit' * 50, result)

    # endregion

    # region Opcode

    def test_opcode_manifest_generation(self):
        path = self.get_contract_path('opcode', 'ConcatWithBytes.py')
        expected_manifest_output = path.replace('.py', '.manifest.json')
        output, manifest = self.get_output(path)

        import os
        from boa3.neo.vm.type.AbiType import AbiType

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
        from boa3.neo.vm.opcode.Opcode import Opcode
        path = self.get_contract_path('opcode', 'ConcatWithOpcode.py')

        engine = TestEngine()
        expected_result = Opcode.LDARG0 + Opcode.LDARG1 + Opcode.ADD
        result = self.run_smart_contract(engine, path, 'concat')
        self.assertEqual(expected_result, result)

    def test_opcode_concat_with_bytes(self):
        from boa3.neo.vm.opcode.Opcode import Opcode
        path = self.get_contract_path('opcode', 'ConcatWithBytes.py')

        engine = TestEngine()
        concat_bytes = b'12345'
        arg = Opcode.LDARG0
        result = self.run_smart_contract(engine, path, 'concat', arg,
                                         expected_result_type=bytes)
        self.assertEqual(concat_bytes + arg, result)

        arg = Opcode.LDLOC1
        result = self.run_smart_contract(engine, path, 'concat', arg,
                                         expected_result_type=bytes)
        self.assertEqual(concat_bytes + arg, result)

        arg = Opcode.NOP
        result = self.run_smart_contract(engine, path, 'concat', arg,
                                         expected_result_type=bytes)
        self.assertEqual(concat_bytes + arg, result)

    def test_opcode_concat_mismatched_type(self):
        path = self.get_contract_path('opcode', 'ConcatMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_opcode_multiplication(self):
        from boa3.neo.vm.opcode.Opcode import Opcode
        path = self.get_contract_path('opcode', 'OpcodeMultiplication.py')

        engine = TestEngine()

        multiplier = 4
        result = self.run_smart_contract(engine, path, 'opcode_mult', multiplier,
                                         expected_result_type=bytes)
        self.assertEqual(Opcode.NOP * multiplier, result)

        multiplier = 50
        result = self.run_smart_contract(engine, path, 'opcode_mult', multiplier,
                                         expected_result_type=bytes)
        self.assertEqual(Opcode.NOP * multiplier, result)

    # endregion

    # region IsInstance Neo Types

    def test_isinstance_contract(self):
        path = self.get_contract_path('IsInstanceContract.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_contract', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_contract', [1, 2, 3])
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_contract', "test_with_string")
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_contract', 42)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'is_get_contract_a_contract')
        self.assertEqual(True, result)

    def test_isinstance_block(self):
        path = self.get_contract_path('IsInstanceBlock.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_block', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_block', [1, 2, 3])
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_block', "test_with_string")
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_block', 42)
        self.assertEqual(False, result)

        engine.increase_block(10)
        result = self.run_smart_contract(engine, path, 'get_block_is_block', 5)
        self.assertEqual(True, result)

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
        path = self.get_contract_path('IsInstanceTransaction.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_tx', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_tx', [1, 2, 3])
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_tx', "test_with_string")
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_tx', 42)
        self.assertEqual(False, result)

        txs = engine.current_block.get_transactions()
        self.assertGreater(len(txs), 0)
        tx_hash = txs[-1].hash

        result = self.run_smart_contract(engine, path, 'get_transaction_is_tx', tx_hash)
        self.assertEqual(True, result)

    def test_isinstance_notification(self):
        path = self.get_contract_path('IsInstanceNotification.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_notification', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_notification', [1, 2, 3])
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_notification', "test_with_string")
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_notification', 42)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'get_notifications_is_notification')
        self.assertEqual(True, result)

    def test_isinstance_storage_context(self):
        path = self.get_contract_path('IsInstanceStorageContext.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_context', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_context', [1, 2, 3])
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_context', "test_with_string")
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_context', 42)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'get_context_is_context')
        self.assertEqual(True, result)

    def test_isinstance_storage_map(self):
        path = self.get_contract_path('IsInstanceStorageMap.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_storage_map', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_storage_map', [1, 2, 3])
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_storage_map', "test_with_string")
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_storage_map', 42)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'create_map_is_storage_map')
        self.assertEqual(True, result)

    def test_isinstance_iterator(self):
        path = self.get_contract_path('IsInstanceIterator.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_iterator', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_iterator', [1, 2, 3])
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_iterator', "test_with_string")
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_iterator', 42)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'storage_find_is_context')
        self.assertEqual(True, result)

    def test_isinstance_ecpoint(self):
        path = self.get_contract_path('IsInstanceECPoint.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'is_ecpoint', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_ecpoint', bytes(33))
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'is_ecpoint', bytes(30))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_ecpoint', 42)
        self.assertEqual(False, result)

    # endregion
