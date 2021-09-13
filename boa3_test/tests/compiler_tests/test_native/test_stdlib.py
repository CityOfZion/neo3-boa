import json

from boa3.exception import CompilerError
from boa3.neo.vm.type.StackItem import StackItemType, serialize
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestStdlibClass(BoaTest):

    default_folder: str = 'test_sc/native_test/stdlib'

    def test_base64_encode(self):
        import base64
        path = self.get_contract_path('Base64Encode.py')
        engine = TestEngine()
        expected_result = base64.b64encode(b'unit test')
        result = self.run_smart_contract(engine, path, 'Main', b'unit test',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = base64.b64encode(b'')
        result = self.run_smart_contract(engine, path, 'Main', b'',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        long_byte_string = (b'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                            b'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                            b'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                            b'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                            b'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                            b'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                            b'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                            b'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = base64.b64encode(long_byte_string)
        result = self.run_smart_contract(engine, path, 'Main', long_byte_string,
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_base64_encode_mismatched_type(self):
        path = self.get_contract_path('Base64EncodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base64_decode(self):
        import base64
        path = self.get_contract_path('Base64Decode.py')
        engine = TestEngine()
        arg = String.from_bytes(base64.b64encode(b'unit test'))
        result = self.run_smart_contract(engine, path, 'Main', arg,
                                         expected_result_type=bytes)
        self.assertEqual(b'unit test', result)

        arg = String.from_bytes(base64.b64encode(b''))
        result = self.run_smart_contract(engine, path, 'Main', arg,
                                         expected_result_type=bytes)
        self.assertEqual(b'', result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = String.from_bytes(base64.b64encode(String(long_string).to_bytes()))
        result = self.run_smart_contract(engine, path, 'Main', arg,
                                         expected_result_type=bytes)
        self.assertEqual(String(long_string).to_bytes(), result)

    def test_base64_decode_mismatched_type(self):
        path = self.get_contract_path('Base64DecodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base58_encode(self):
        import base58
        path = self.get_contract_path('Base58Encode.py')
        engine = TestEngine()
        expected_result = base58.b58encode('unit test')
        result = self.run_smart_contract(engine, path, 'Main', 'unit test',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = base58.b58encode('')
        result = self.run_smart_contract(engine, path, 'Main', '',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = base58.b58encode(long_string)
        result = self.run_smart_contract(engine, path, 'Main', long_string,
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_base58_encode_mismatched_type(self):
        path = self.get_contract_path('Base58EncodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base58_decode(self):
        import base58
        path = self.get_contract_path('Base58Decode.py')
        engine = TestEngine()
        arg = base58.b58encode('unit test')
        result = self.run_smart_contract(engine, path, 'Main', arg)
        self.assertEqual('unit test', result)

        arg = base58.b58encode('')
        result = self.run_smart_contract(engine, path, 'Main', arg)
        self.assertEqual('', result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = base58.b58encode(long_string)
        result = self.run_smart_contract(engine, path, 'Main', arg)
        self.assertEqual(long_string, result)

    def test_base58_decode_mismatched_type(self):
        path = self.get_contract_path('Base58DecodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base58_check_decode(self):
        import base58
        path = self.get_contract_path('Base58CheckDecode.py')
        engine = TestEngine()
        arg = base58.b58encode_check('unit test'.encode('utf-8'))
        result = self.run_smart_contract(engine, path, 'main', arg)
        self.assertEqual('unit test', result)

        arg = base58.b58encode_check(''.encode('utf-8'))
        result = self.run_smart_contract(engine, path, 'main', arg)
        self.assertEqual('', result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = base58.b58encode_check(long_string.encode('utf-8'))
        result = self.run_smart_contract(engine, path, 'main', arg)
        self.assertEqual(long_string, result)

    def test_base58_check_decode_mismatched_type(self):
        path = self.get_contract_path('Base58CheckDecodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base58_check_encode(self):
        import base58
        path = self.get_contract_path('Base58CheckEncode.py')
        engine = TestEngine()
        expected_result = base58.b58encode_check('unit test'.encode('utf-8'))
        result = self.run_smart_contract(engine, path, 'main', 'unit test',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = base58.b58encode_check(''.encode('utf-8'))
        result = self.run_smart_contract(engine, path, 'main', '',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = base58.b58encode_check(long_string.encode('utf-8'))
        result = self.run_smart_contract(engine, path, 'main', long_string,
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_base58_check_encode_mismatched_type(self):
        path = self.get_contract_path('Base58CheckEncodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_serialize_int(self):
        path = self.get_contract_path('SerializeInt.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'serialize_int',
                                         expected_result_type=bytes)
        expected_result = serialize(42)
        self.assertEqual(expected_result, result)

    def test_serialize_bool(self):
        path = self.get_contract_path('SerializeBool.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'serialize_bool',
                                         expected_result_type=bytes)
        expected_result = serialize(True)
        self.assertEqual(expected_result, result)

    def test_serialize_str(self):
        path = self.get_contract_path('SerializeStr.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'serialize_str',
                                         expected_result_type=bytes)
        expected_result = serialize('42')
        self.assertEqual(expected_result, result)

    def test_serialize_sequence(self):
        path = self.get_contract_path('SerializeSequence.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'serialize_sequence',
                                         expected_result_type=bytes)
        expected_result = serialize([2, 3, 5, 7])
        self.assertEqual(expected_result, result)

    def test_serialize_dict(self):
        path = self.get_contract_path('SerializeDict.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'serialize_dict',
                                         expected_result_type=bytes)
        expected_result = serialize({1: 1, 2: 1, 3: 2})
        self.assertEqual(expected_result, result)

    def test_deserialize(self):
        path = self.get_contract_path('Deserialize.py')
        engine = TestEngine()

        expected_result = 42
        value = serialize(expected_result)
        result = self.run_smart_contract(engine, path, 'deserialize_arg', value,
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = True
        value = serialize(expected_result)
        result = self.run_smart_contract(engine, path, 'deserialize_arg', value)

        # it shouldn't be equal to the convertion, because it converts as an int instead of a boolean
        self.assertEqual(expected_result, result)
        self.assertNotEqual(type(expected_result), type(result))

        value = StackItemType.Boolean + value[1:]
        result = self.run_smart_contract(engine, path, 'deserialize_arg', value,
                                         expected_result_type=bool)
        self.assertEqual(expected_result, result)
        self.assertEqual(type(expected_result), type(result))

        expected_result = '42'
        value = serialize(expected_result)
        result = self.run_smart_contract(engine, path, 'deserialize_arg', value)
        self.assertEqual(expected_result, result)

        expected_result = b'42'
        value = serialize(expected_result)
        result = self.run_smart_contract(engine, path, 'deserialize_arg', value,
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = [1, '2', b'3']
        value = serialize(expected_result)
        result = self.run_smart_contract(engine, path, 'deserialize_arg', value)
        expected_result[2] = String.from_bytes(expected_result[2])
        self.assertEqual(expected_result, result)

        expected_result = {'int': 1, 'str': '2', 'bytes': b'3'}
        value = serialize(expected_result)
        result = self.run_smart_contract(engine, path, 'deserialize_arg', value)
        expected_result['bytes'] = String.from_bytes(expected_result['bytes'])
        self.assertEqual(expected_result, result)

    def test_deserialize_mismatched_type(self):
        path = self.get_contract_path('DeserializeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_json_serialize(self):
        path = self.get_contract_path('JsonSerialize.py')

        engine = TestEngine()
        test_input = {"one": 1, "two": 2, "three": 3}
        expected_result = json.dumps(test_input, separators=(',', ':'))
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

    def test_json_serialize_int(self):
        path = self.get_contract_path('JsonSerializeInt.py')

        engine = TestEngine()
        expected_result = json.dumps(10)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_json_serialize_bool(self):
        path = self.get_contract_path('JsonSerializeBool.py')

        engine = TestEngine()
        expected_result = json.dumps(1)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_json_serialize_str(self):
        path = self.get_contract_path('JsonSerializeStr.py')

        engine = TestEngine()
        expected_result = json.dumps('unit test')
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_json_serialize_bytes(self):
        path = self.get_contract_path('JsonSerializeBytes.py')

        engine = TestEngine()
        # Python does not accept bytes as parameter for json.dumps() method, since string and bytes ends up being the
        # same on Neo, it's being converted to string, before using dumps
        expected_result = json.dumps(String().from_bytes(b'unit test'))
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_json_deserialize(self):
        path = self.get_contract_path('JsonDeserialize.py')
        engine = TestEngine()

        test_input = json.dumps(12345)
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

        test_input = json.dumps('unit test')
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

        test_input = json.dumps(True)
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

    def test_boa2_serialization_test1(self):
        path = self.get_contract_path('SerializationBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, expected_result_type=bytes)
        expected_result = serialize(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'])
        self.assertEqual(expected_result, result)

    def test_boa2_serialization_test2(self):
        path = self.get_contract_path('SerializationBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 2, expected_result_type=bytes)
        expected_result = serialize(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'])
        self.assertEqual(expected_result, result)

    def test_boa2_serialization_test3(self):
        path = self.get_contract_path('SerializationBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 3)
        self.assertEqual(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'], result)

    def test_boa2_serialization_test4(self):
        path = self.get_contract_path('SerializationBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 4)
        self.assertEqual(['j', 3, 5], result)

    def test_atoi(self):
        path = self.get_contract_path('Atoi.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', '10', 10)
        self.assertEqual(10, result)

        result = self.run_smart_contract(engine, path, 'main', '10', 16)
        self.assertEqual(16, result)

        result = self.run_smart_contract(engine, path, 'main', '123', 10)
        self.assertEqual(123, result)

        result = self.run_smart_contract(engine, path, 'main', '123', 16)
        self.assertEqual(291, result)

        result = self.run_smart_contract(engine, path, 'main', '1f', 16)
        self.assertEqual(31, result)

        result = self.run_smart_contract(engine, path, 'main', 'ff', 16)
        self.assertEqual(-1, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'main', 'string', 10)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'main', 'string', 16)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'main', 'abc', 10)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'main', '10', 2)

    def test_atoi_default(self):
        path = self.get_contract_path('AtoiDefault.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', '10')
        self.assertEqual(10, result)

        result = self.run_smart_contract(engine, path, 'main', '123')
        self.assertEqual(123, result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'main', 'string')

    def test_atoi_too_few_parameters(self):
        path = self.get_contract_path('AtoiTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_atoi_too_many_parameters(self):
        path = self.get_contract_path('AtoiTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_atoi_mismatched_type(self):
        path = self.get_contract_path('AtoiMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_itoa(self):
        path = self.get_contract_path('Itoa')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 10, 10)
        self.assertEqual('10', result)
        result = self.run_smart_contract(engine, path, 'main', 16, 16)
        self.assertEqual('10', result)
        result = self.run_smart_contract(engine, path, 'main', -1, 10)
        self.assertEqual('-1', result)
        result = self.run_smart_contract(engine, path, 'main', -1, 16)
        self.assertEqual('f', result)
        result = self.run_smart_contract(engine, path, 'main', 15, 16)
        self.assertEqual('0f', result)

        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'main', 10, 2)

    def test_itoa_default(self):
        path = self.get_contract_path('ItoaDefault')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 10)
        self.assertEqual('10', result)
        result = self.run_smart_contract(engine, path, 'main', -1)
        self.assertEqual('-1', result)

    def test_itoa_too_few_arguments(self):
        path = self.get_contract_path('ItoaTooFewArguments')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_itoa_too_many_arguments(self):
        path = self.get_contract_path('ItoaTooManyArguments')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_itoa_mismatched_type(self):
        path = self.get_contract_path('ItoaMismatchedType')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_memory_search(self):
        path = self.get_contract_path('MemorySearch')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'abcde', 'a', 0, False)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 0, False)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'b', 0, False)
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'c', 0, False)
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'd', 0, False)
        self.assertEqual(3, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'e', 0, False)
        self.assertEqual(4, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 1, False)
        self.assertEqual(-1, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'cd', 0, False)
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'abe', 0, False)
        self.assertEqual(-1, result)

        result = self.run_smart_contract(engine, path, 'main', b'aaaaa', b'a', 0, False)
        self.assertEqual(0, result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 20, False)

    def test_memory_search_backward(self):
        path = self.get_contract_path('MemorySearch')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'abcde', 'a', 5, True)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 5, True)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'b', 5, True)
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'c', 5, True)
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'd', 5, True)
        self.assertEqual(3, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'e', 5, True)
        self.assertEqual(4, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 0, True)
        self.assertEqual(-1, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'cd', 5, True)
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'abe', 5, True)
        self.assertEqual(-1, result)

        result = self.run_smart_contract(engine, path, 'main', b'aaaaa', b'a', 5, True)
        self.assertEqual(4, result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 20, True)

    def test_memory_search_start(self):
        path = self.get_contract_path('MemorySearchStart')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'abcde', 'a', 0)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 0)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'e', 0)
        self.assertEqual(4, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 1)
        self.assertEqual(-1, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'cd', 0)
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'abe', 0)
        self.assertEqual(-1, result)

        result = self.run_smart_contract(engine, path, 'main', b'aaaaa', b'a', 0)
        self.assertEqual(0, result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'main', b'abcde', b'a', 20)

    def test_memory_search_default_values(self):
        path = self.get_contract_path('MemorySearchDefault')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'abcde', 'a')
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'a')
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'b')
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'c')
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'd')
        self.assertEqual(3, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'e')
        self.assertEqual(4, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'cd')
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'main', b'abcde', b'aa')
        self.assertEqual(-1, result)

    def test_memory_search_mismatched_type(self):
        path = self.get_contract_path('MemorySearchMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_memory_search_too_few_parameters(self):
        path = self.get_contract_path('MemorySearchTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_memory_search_too_many_parameters(self):
        path = self.get_contract_path('MemorySearchTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_memory_compare(self):
        path = self.get_contract_path('MemoryCompare')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'abc', 'abc')
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', 'abc', 'ABC')
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'main', 'ABC', 'abc')
        self.assertEqual(-1, result)

        result = self.run_smart_contract(engine, path, 'main', b'abc', b'abc')
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', b'abc', b'ABC')
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'main', b'ABC', b'abc')
        self.assertEqual(-1, result)

    def test_memory_compare_too_few_parameters(self):
        path = self.get_contract_path('MemoryCompareTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_memory_compare_too_many_parameters(self):
        path = self.get_contract_path('MemoryCompareTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_memory_compare_mismatched_type(self):
        path = self.get_contract_path('MemoryCompareMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
