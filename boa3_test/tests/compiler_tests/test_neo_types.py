from boa3.exception import CompilerError, CompilerWarning
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNeoTypes(BoaTest):

    default_folder: str = 'test_sc/neo_type_test'

    # region UInt160

    def test_uint160_call_bytes(self):
        path = self.get_contract_path('UInt160CallBytes.py')

        engine = TestEngine()
        value = bytes(20)
        result = self.run_smart_contract(engine, path, 'uint160', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(20))
        result = self.run_smart_contract(engine, path, 'uint160', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(10),
                                    expected_result_type=bytes)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(30),
                                    expected_result_type=bytes)

    def test_uint160_call_int(self):
        path = self.get_contract_path('UInt160CallInt.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'uint160', 0,
                                         expected_result_type=bytes)
        self.assertEqual(bytes(20), result)

        value = Integer(1_000_000_000).to_byte_array(min_length=20)
        result = self.run_smart_contract(engine, path, 'uint160', 1_000_000_000,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', -50,
                                    expected_result_type=bytes)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(30),
                                    expected_result_type=bytes)

    def test_uint160_call_without_args(self):
        path = self.get_contract_path('UInt160CallWithoutArgs.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'uint160',
                                         expected_result_type=bytes)
        self.assertEqual(bytes(20), result)

    def test_uint160_return_bytes(self):
        path = self.get_contract_path('UInt160ReturnBytes.py')

        engine = TestEngine()
        value = bytes(20)
        result = self.run_smart_contract(engine, path, 'uint160', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(20))
        result = self.run_smart_contract(engine, path, 'uint160', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(10),
                                    expected_result_type=bytes)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(30),
                                    expected_result_type=bytes)

    def test_uint160_concat_with_bytes(self):
        path = self.get_contract_path('UInt160ConcatWithBytes.py')
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
        path = self.get_contract_path('UInt160CallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region UInt256

    def test_uint256_call_bytes(self):
        path = self.get_contract_path('UInt256CallBytes.py')

        engine = TestEngine()
        value = bytes(32)
        result = self.run_smart_contract(engine, path, 'uint256', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(32))
        result = self.run_smart_contract(engine, path, 'uint256', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(20),
                                    expected_result_type=bytes)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(30),
                                    expected_result_type=bytes)

    def test_uint256_call_int(self):
        path = self.get_contract_path('UInt256CallInt.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'uint256', 0,
                                         expected_result_type=bytes)
        self.assertEqual(bytes(32), result)

        value = Integer(1_000_000_000).to_byte_array(min_length=32)
        result = self.run_smart_contract(engine, path, 'uint256', 1_000_000_000,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', -50,
                                    expected_result_type=bytes)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(30),
                                    expected_result_type=bytes)

    def test_uint256_call_without_args(self):
        path = self.get_contract_path('UInt256CallWithoutArgs.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'uint256',
                                         expected_result_type=bytes)
        self.assertEqual(bytes(32), result)

    def test_uint256_return_bytes(self):
        path = self.get_contract_path('UInt256ReturnBytes.py')

        engine = TestEngine()
        value = bytes(32)
        result = self.run_smart_contract(engine, path, 'uint256', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(32))
        result = self.run_smart_contract(engine, path, 'uint256', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(10),
                                    expected_result_type=bytes)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint256', bytes(30),
                                    expected_result_type=bytes)

    def test_uint256_concat_with_bytes(self):
        path = self.get_contract_path('UInt256ConcatWithBytes.py')
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
        path = self.get_contract_path('UInt256CallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region ECPoint

    def test_ecpoint_call_bytes(self):
        path = self.get_contract_path('ECPointCallBytes.py')
        engine = TestEngine()

        value = bytes(33)
        result = self.run_smart_contract(engine, path, 'ecpoint', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(33))
        result = self.run_smart_contract(engine, path, 'ecpoint', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'ecpoint', bytes(20),
                                    expected_result_type=bytes)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'uint160', bytes(30),
                                    expected_result_type=bytes)

    def test_ecpoint_call_without_args(self):
        path = self.get_contract_path('ECPointCallWithoutArgs.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_ecpoint_return_bytes(self):
        path = self.get_contract_path('ECPointReturnBytes.py')
        engine = TestEngine()

        value = bytes(33)
        result = self.run_smart_contract(engine, path, 'ecpoint', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        value = bytes(range(33))
        result = self.run_smart_contract(engine, path, 'ecpoint', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'ecpoint', bytes(10),
                                    expected_result_type=bytes)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'ecpoint', bytes(30),
                                    expected_result_type=bytes)

    def test_ecpoint_concat_with_bytes(self):
        path = self.get_contract_path('ECPointConcatWithBytes.py')
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
        path = self.get_contract_path('ECPointCallMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region IsInstance Neo Types

    def test_isinstance_contract(self):
        path = self.get_contract_path('IsInstanceContract.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_contract', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_contract', [1, 2, 3],
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_contract', "test_with_string",
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_contract', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'is_get_contract_a_contract',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_isinstance_block(self):
        path = self.get_contract_path('IsInstanceBlock.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_block', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_block', [1, 2, 3],
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_block', "test_with_string",
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_block', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        engine.increase_block(10)
        result = self.run_smart_contract(engine, path, 'get_block_is_block', 5,
                                         expected_result_type=bool)
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
        result = self.run_smart_contract(engine, path, 'is_tx', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_tx', [1, 2, 3],
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_tx', "test_with_string",
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_tx', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        txs = engine.current_block.get_transactions()
        self.assertGreater(len(txs), 0)
        tx_hash = txs[-1].hash

        result = self.run_smart_contract(engine, path, 'get_transaction_is_tx', tx_hash,
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_isinstance_notification(self):
        path = self.get_contract_path('IsInstanceNotification.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_notification', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_notification', [1, 2, 3],
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_notification', "test_with_string",
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_notification', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'get_notifications_is_notification',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_isinstance_storage_context(self):
        path = self.get_contract_path('IsInstanceStorageContext.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_context', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_context', [1, 2, 3],
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_context', "test_with_string",
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_context', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'get_context_is_context',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_isinstance_storage_map(self):
        path = self.get_contract_path('IsInstanceStorageMap.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_storage_map', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_storage_map', [1, 2, 3],
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_storage_map', "test_with_string",
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_storage_map', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'create_map_is_storage_map',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_isinstance_iterator(self):
        path = self.get_contract_path('IsInstanceIterator.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'is_iterator', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_iterator', [1, 2, 3],
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_iterator', "test_with_string",
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_iterator', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'storage_find_is_context',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_isinstance_ecpoint(self):
        path = self.get_contract_path('IsInstanceECPoint.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'is_ecpoint', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_ecpoint', bytes(33),
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'is_ecpoint', bytes(30),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'is_ecpoint', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

    # endregion
