import json

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.type.StackItem import StackItemType, serialize
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestStdlibClass(BoaTest):
    default_folder: str = 'test_sc/native_test/stdlib'

    def test_get_hash(self):
        path, _ = self.get_deploy_file_paths('GetHash.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(constants.STD_LIB_SCRIPT)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_base64_encode(self):
        import base64
        path, _ = self.get_deploy_file_paths('Base64Encode.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = base64.b64encode(b'unit test')
        invokes.append(runner.call_contract(path, 'Main', b'unit test',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        expected_result = base64.b64encode(b'')
        invokes.append(runner.call_contract(path, 'Main', b'',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        long_byte_string = (b'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                            b'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                            b'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                            b'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                            b'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                            b'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                            b'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                            b'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = base64.b64encode(long_byte_string)
        invokes.append(runner.call_contract(path, 'Main', long_byte_string,
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_base64_encode_mismatched_type(self):
        path = self.get_contract_path('Base64EncodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base64_decode(self):
        import base64
        path, _ = self.get_deploy_file_paths('Base64Decode.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        arg = String.from_bytes(base64.b64encode(b'unit test'))
        invokes.append(runner.call_contract(path, 'Main', arg,
                                            expected_result_type=bytes))
        expected_results.append(b'unit test')

        arg = String.from_bytes(base64.b64encode(b''))
        invokes.append(runner.call_contract(path, 'Main', arg,
                                            expected_result_type=bytes))
        expected_results.append(b'')

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = String.from_bytes(base64.b64encode(String(long_string).to_bytes()))
        invokes.append(runner.call_contract(path, 'Main', arg,
                                            expected_result_type=bytes))
        expected_results.append(String(long_string).to_bytes())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_base64_decode_mismatched_type(self):
        path = self.get_contract_path('Base64DecodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base58_encode(self):
        import base58
        path, _ = self.get_deploy_file_paths('Base58Encode.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = base58.b58encode('unit test')
        invokes.append(runner.call_contract(path, 'Main', 'unit test',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        expected_result = base58.b58encode('')
        invokes.append(runner.call_contract(path, 'Main', '',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = base58.b58encode(long_string)
        invokes.append(runner.call_contract(path, 'Main', long_string,
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_base58_encode_mismatched_type(self):
        path = self.get_contract_path('Base58EncodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base58_decode(self):
        import base58
        path, _ = self.get_deploy_file_paths('Base58Decode.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        arg = base58.b58encode('unit test')
        invokes.append(runner.call_contract(path, 'Main', arg))
        expected_results.append('unit test')

        arg = base58.b58encode('')
        invokes.append(runner.call_contract(path, 'Main', arg))
        expected_results.append('')

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = base58.b58encode(long_string)
        invokes.append(runner.call_contract(path, 'Main', arg))
        expected_results.append(long_string)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_base58_decode_mismatched_type(self):
        path = self.get_contract_path('Base58DecodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base58_check_decode(self):
        import base58
        path, _ = self.get_deploy_file_paths('Base58CheckDecode.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        arg = base58.b58encode_check('unit test'.encode('utf-8'))
        invokes.append(runner.call_contract(path, 'main', arg))
        expected_results.append('unit test')

        arg = base58.b58encode_check(''.encode('utf-8'))
        invokes.append(runner.call_contract(path, 'main', arg))
        expected_results.append('')

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = base58.b58encode_check(long_string.encode('utf-8'))
        invokes.append(runner.call_contract(path, 'main', arg))
        expected_results.append(long_string)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_base58_check_decode_mismatched_type(self):
        path = self.get_contract_path('Base58CheckDecodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_base58_check_encode(self):
        import base58
        path, _ = self.get_deploy_file_paths('Base58CheckEncode.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = base58.b58encode_check('unit test'.encode('utf-8'))
        invokes.append(runner.call_contract(path, 'main', 'unit test',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        expected_result = base58.b58encode_check(''.encode('utf-8'))
        invokes.append(runner.call_contract(path, 'main', '',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = base58.b58encode_check(long_string.encode('utf-8'))
        invokes.append(runner.call_contract(path, 'main', long_string,
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_base58_check_encode_mismatched_type(self):
        path = self.get_contract_path('Base58CheckEncodeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_serialize_int(self):
        path, _ = self.get_deploy_file_paths('SerializeInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'serialize_int',
                                            expected_result_type=bytes))
        expected_result = serialize(42)
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_serialize_bool(self):
        path, _ = self.get_deploy_file_paths('SerializeBool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'serialize_bool',
                                            expected_result_type=bytes))
        expected_result = serialize(True)
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_serialize_str(self):
        path, _ = self.get_deploy_file_paths('SerializeStr.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'serialize_str',
                                            expected_result_type=bytes))
        expected_result = serialize('42')
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_serialize_sequence(self):
        path, _ = self.get_deploy_file_paths('SerializeSequence.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'serialize_sequence',
                                            expected_result_type=bytes))
        expected_result = serialize([2, 3, 5, 7])
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_serialize_dict(self):
        path, _ = self.get_deploy_file_paths('SerializeDict.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'serialize_dict',
                                            expected_result_type=bytes))
        expected_result = serialize({1: 1, 2: 1, 3: 2})
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_deserialize(self):
        path, _ = self.get_deploy_file_paths('Deserialize.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = 42
        value = serialize(expected_result)
        invokes.append(runner.call_contract(path, 'deserialize_arg', value,
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        expected_result = True
        value = serialize(expected_result)
        invokes.append(runner.call_contract(path, 'deserialize_arg', value))
        expected_results.append(expected_result)

        value = StackItemType.Boolean + value[1:]
        invokes.append(runner.call_contract(path, 'deserialize_arg', value))
        expected_results.append(expected_result)

        expected_result = '42'
        value = serialize(expected_result)
        invokes.append(runner.call_contract(path, 'deserialize_arg', value))
        expected_results.append(expected_result)

        expected_result = b'42'
        value = serialize(expected_result)
        invokes.append(runner.call_contract(path, 'deserialize_arg', value,
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        expected_result = [1, '2', b'3']
        value = serialize(expected_result)
        invokes.append(runner.call_contract(path, 'deserialize_arg', value))
        expected_result[2] = String.from_bytes(expected_result[2])
        expected_results.append(expected_result)

        expected_result = {'int': 1, 'str': '2', 'bytes': b'3'}
        value = serialize(expected_result)
        invokes.append(runner.call_contract(path, 'deserialize_arg', value))
        expected_result['bytes'] = String.from_bytes(expected_result['bytes'])
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_deserialize_mismatched_type(self):
        path = self.get_contract_path('DeserializeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_json_serialize(self):
        path, _ = self.get_deploy_file_paths('JsonSerialize.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_input = {"one": 1, "two": 2, "three": 3}
        expected_result = json.dumps(test_input, separators=(',', ':'))
        invokes.append(runner.call_contract(path, 'main', test_input))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_serialize_int(self):
        path, _ = self.get_deploy_file_paths('JsonSerializeInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = json.dumps(10)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_serialize_bool(self):
        path, _ = self.get_deploy_file_paths('JsonSerializeBool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = json.dumps(True)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_serialize_str(self):
        path, _ = self.get_deploy_file_paths('JsonSerializeStr.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = json.dumps('unit test')
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_serialize_bytes(self):
        path, _ = self.get_deploy_file_paths('JsonSerializeBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        # Python does not accept bytes as parameter for json.dumps() method, since string and bytes ends up being the
        # same on Neo, it's being converted to string, before using dumps
        expected_result = json.dumps(String().from_bytes(b'unit test'))
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_deserialize(self):
        path, _ = self.get_deploy_file_paths('JsonDeserialize.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_input = json.dumps(12345)
        expected_result = json.loads(test_input)
        invokes.append(runner.call_contract(path, 'main', test_input))
        expected_results.append(expected_result)

        test_input = json.dumps('unit test')
        expected_result = json.loads(test_input)
        invokes.append(runner.call_contract(path, 'main', test_input))
        expected_results.append(expected_result)

        test_input = json.dumps(True)
        expected_result = json.loads(test_input)
        invokes.append(runner.call_contract(path, 'main', test_input))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_serialization_test1(self):
        path, _ = self.get_deploy_file_paths('SerializationBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, expected_result_type=bytes))
        expected_result = serialize(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'])
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_serialization_test2(self):
        path, _ = self.get_deploy_file_paths('SerializationBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 2, expected_result_type=bytes))
        expected_result = serialize(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'])
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_serialization_test3(self):
        path, _ = self.get_deploy_file_paths('SerializationBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 3))
        expected_results.append(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_serialization_test4(self):
        path, _ = self.get_deploy_file_paths('SerializationBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 4))
        expected_results.append(['j', 3, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_atoi(self):
        path, _ = self.get_deploy_file_paths('Atoi.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', '10', 10))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'main', '10', 16))
        expected_results.append(16)

        invokes.append(runner.call_contract(path, 'main', '123', 10))
        expected_results.append(123)

        invokes.append(runner.call_contract(path, 'main', '123', 16))
        expected_results.append(291)

        invokes.append(runner.call_contract(path, 'main', '1f', 16))
        expected_results.append(31)

        invokes.append(runner.call_contract(path, 'main', 'ff', 16))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', 'string', 10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.CANT_PARSE_VALUE_MSG)

        runner.call_contract(path, 'main', 'string', 16)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.CANT_PARSE_VALUE_MSG)

        runner.call_contract(path, 'main', 'abc', 10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.CANT_PARSE_VALUE_MSG)

        runner.call_contract(path, 'main', '10', 2)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.ARGUMENT_OUT_OF_RANGE_MSG_PREFIX}')

    def test_atoi_default(self):
        path, _ = self.get_deploy_file_paths('AtoiDefault.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', '10'))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'main', '123'))
        expected_results.append(123)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', 'string')
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.CANT_PARSE_VALUE_MSG)

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
        path, _ = self.get_deploy_file_paths('Itoa')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 10, 10))
        expected_results.append('10')
        invokes.append(runner.call_contract(path, 'main', 16, 16))
        expected_results.append('10')
        invokes.append(runner.call_contract(path, 'main', -1, 10))
        expected_results.append('-1')
        invokes.append(runner.call_contract(path, 'main', -1, 16))
        expected_results.append('f')
        invokes.append(runner.call_contract(path, 'main', 15, 16))
        expected_results.append('0f')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', 10, 2)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.ARGUMENT_OUT_OF_RANGE_MSG_PREFIX}')

    def test_itoa_default(self):
        path, _ = self.get_deploy_file_paths('ItoaDefault')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 10))
        expected_results.append('10')
        invokes.append(runner.call_contract(path, 'main', -1))
        expected_results.append('-1')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        path, _ = self.get_deploy_file_paths('MemorySearch')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'abcde', 'a', 0, False))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'a', 0, False))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'b', 0, False))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'c', 0, False))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'd', 0, False))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'e', 0, False))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'a', 1, False))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'cd', 0, False))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'abe', 0, False))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'main', b'aaaaa', b'a', 0, False))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', b'abcde', b'a', 20, False)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.ARGUMENT_OUT_OF_RANGE_MSG_PREFIX}')

    def test_memory_search_backward(self):
        path, _ = self.get_deploy_file_paths('MemorySearch')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'abcde', 'a', 5, True))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'a', 5, True))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'b', 5, True))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'c', 5, True))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'd', 5, True))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'e', 5, True))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'a', 0, True))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'cd', 5, True))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'abe', 5, True))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'main', b'aaaaa', b'a', 5, True))
        expected_results.append(4)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', b'abcde', b'a', 20, True)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.ARGUMENT_OUT_OF_RANGE_MSG_PREFIX}')

    def test_memory_search_start(self):
        path, _ = self.get_deploy_file_paths('MemorySearchStart')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'abcde', 'a', 0))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'a', 0))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'e', 0))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'a', 1))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'cd', 0))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'abe', 0))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'main', b'aaaaa', b'a', 0))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', b'abcde', b'a', 20)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.ARGUMENT_OUT_OF_RANGE_MSG_PREFIX}')

    def test_memory_search_default_values(self):
        path, _ = self.get_deploy_file_paths('MemorySearchDefault')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'abcde', 'a'))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'a'))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'b'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'c'))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'd'))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'e'))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'cd'))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', b'abcde', b'aa'))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        path, _ = self.get_deploy_file_paths('MemoryCompare')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'abc', 'abc'))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', 'abc', 'ABC'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', 'ABC', 'abc'))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'main', b'abc', b'abc'))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', b'abc', b'ABC'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', b'ABC', b'abc'))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_memory_compare_too_few_parameters(self):
        path = self.get_contract_path('MemoryCompareTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_memory_compare_too_many_parameters(self):
        path = self.get_contract_path('MemoryCompareTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_memory_compare_mismatched_type(self):
        path = self.get_contract_path('MemoryCompareMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
