from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNeoTypes(BoaTest):

    default_folder: str = 'test_sc/neo_type_test'

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
        self.compile_and_save(path)

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
        self.compile_and_save(path)

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
        self.assertCompilerLogs(MismatchedTypes, path)

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
        self.compile_and_save(path)

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
        self.compile_and_save(path)

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
        self.assertCompilerLogs(MismatchedTypes, path)
