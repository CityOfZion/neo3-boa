from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNeoTypes(BoaTest):

    def test_uint160_call_bytes(self):
        path = '%s/boa3_test/test_sc/neo_type_test/UInt160CallBytes.py' % self.dirname

        engine = TestEngine(self.dirname)
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
        path = '%s/boa3_test/test_sc/neo_type_test/UInt160CallInt.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
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
        path = '%s/boa3_test/test_sc/neo_type_test/UInt160CallWithoutArgs.py' % self.dirname

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'uint160',
                                         expected_result_type=bytes)
        self.assertEqual(bytes(20), result)

    def test_uint160_return_bytes(self):
        path = '%s/boa3_test/test_sc/neo_type_test/UInt160ReturnBytes.py' % self.dirname

        engine = TestEngine(self.dirname)
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
        path = '%s/boa3_test/test_sc/neo_type_test/UInt160ConcatWithBytes.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        value = bytes(20)
        result = self.run_smart_contract(engine, path, 'uint160_method', value,
                                         expected_result_type=bytes)
        self.assertEqual(value + b'123', result)

        value = bytes(range(20))
        result = self.run_smart_contract(engine, path, 'uint160_method', value,
                                         expected_result_type=bytes)
        self.assertEqual(value + b'123', result)
