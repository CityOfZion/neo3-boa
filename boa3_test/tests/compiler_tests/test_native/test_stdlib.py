import json
import unittest

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.StackItem import StackItemType, serialize
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestStdlibClass(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/stdlib'
    INVALID_FORMAT_MSG = 'invalid format'
    INVALID_BASE_MSG = 'invalid base'

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        result, _ = await self.call('main', [], return_type=bytes)
        self.assertEqual(constants.STD_LIB_SCRIPT, result)

    async def test_base64_encode(self):
        import base64
        await self.set_up_contract('Base64Encode.py')

        expected_result = base64.b64encode(b'unit test')
        result, _ = await self.call('Main', [b'unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = base64.b64encode(b'')
        result, _ = await self.call('Main', [b''], return_type=bytes)
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
        result, _ = await self.call('Main', [long_byte_string], return_type=bytes)
        self.assertEqual(expected_result, result)

    def test_base64_encode_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Base64EncodeMismatchedType.py')

    async def test_base64_decode(self):
        import base64
        await self.set_up_contract('Base64Decode.py')

        arg = String.from_bytes(base64.b64encode(b'unit test'))
        result, _ = await self.call('Main', [arg], return_type=bytes)
        self.assertEqual(b'unit test', result)

        arg = String.from_bytes(base64.b64encode(b''))
        result, _ = await self.call('Main', [arg], return_type=bytes)
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
        result, _ = await self.call('Main', [arg], return_type=bytes)
        self.assertEqual(String(long_string).to_bytes(), result)

    def test_base64_decode_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Base64DecodeMismatchedType.py')

    async def test_base58_encode(self):
        import base58
        await self.set_up_contract('Base58Encode.py')

        expected_result = base58.b58encode('unit test')
        result, _ = await self.call('Main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = base58.b58encode('')
        result, _ = await self.call('Main', [''], return_type=bytes)
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
        result, _ = await self.call('Main', [long_string], return_type=bytes)
        self.assertEqual(expected_result, result)

    def test_base58_encode_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Base58EncodeMismatchedType.py')

    async def test_base58_decode(self):
        import base58
        await self.set_up_contract('Base58Decode.py')

        arg = base58.b58encode('unit test')
        result, _ = await self.call('Main', [arg], return_type=str)
        self.assertEqual('unit test', result)

        arg = base58.b58encode('')
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [arg], return_type=str)

        self.assertRegex(str(context.exception), 'zero length string')

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = base58.b58encode(long_string)
        result, _ = await self.call('Main', [arg], return_type=str)
        self.assertEqual(long_string, result)

    def test_base58_decode_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Base58DecodeMismatchedType.py')

    async def test_base58_check_decode(self):
        import base58
        await self.set_up_contract('Base58CheckDecode.py')

        arg = base58.b58encode_check('unit test'.encode('utf-8'))
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual('unit test', result)

        arg = base58.b58encode_check(''.encode('utf-8'))
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [arg], return_type=str)

        self.assertRegex(str(context.exception), 'missing checksum')

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = base58.b58encode_check(long_string.encode('utf-8'))
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(long_string, result)

    def test_base58_check_decode_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Base58CheckDecodeMismatchedType.py')

    async def test_base58_check_encode(self):
        import base58
        await self.set_up_contract('Base58CheckEncode.py')

        expected_result = base58.b58encode_check('unit test'.encode('utf-8'))
        result, _ = await self.call('main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = base58.b58encode_check(''.encode('utf-8'))
        result, _ = await self.call('main', [''], return_type=bytes)
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
        result, _ = await self.call('main', [long_string], return_type=bytes)
        self.assertEqual(expected_result, result)

    def test_base58_check_encode_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'Base58CheckEncodeMismatchedType.py')

    async def test_serialize_int(self):
        await self.set_up_contract('SerializeInt.py')

        expected_result = serialize(42)
        result, _ = await self.call('serialize_int', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_serialize_bool(self):
        await self.set_up_contract('SerializeBool.py')

        expected_result = serialize(True)
        result, _ = await self.call('serialize_bool', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_serialize_str(self):
        await self.set_up_contract('SerializeStr.py')

        expected_result = serialize('42')
        result, _ = await self.call('serialize_str', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_serialize_sequence(self):
        await self.set_up_contract('SerializeSequence.py')

        expected_result = serialize([2, 3, 5, 7])
        result, _ = await self.call('serialize_sequence', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_serialize_dict(self):
        await self.set_up_contract('SerializeDict.py')

        expected_result = serialize({1: 1, 2: 1, 3: 2})
        result, _ = await self.call('serialize_dict', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_deserialize(self):
        await self.set_up_contract('Deserialize.py')

        expected_result = 42
        value = serialize(expected_result)
        result, _ = await self.call('deserialize_arg', [value], return_type=int)
        self.assertEqual(expected_result, result)

        expected_result = True
        value = serialize(expected_result)
        result, _ = await self.call('deserialize_arg', [value], return_type=bool)
        self.assertEqual(expected_result, result)

        value = StackItemType.Boolean + value[1:]
        result, _ = await self.call('deserialize_arg', [value], return_type=bool)
        self.assertEqual(expected_result, result)

        expected_result = '42'
        value = serialize(expected_result)
        result, _ = await self.call('deserialize_arg', [value], return_type=str)
        self.assertEqual(expected_result, result)

        expected_result = b'42'
        value = serialize(expected_result)
        result, _ = await self.call('deserialize_arg', [value], return_type=bytes)
        self.assertEqual(expected_result, result)

        expected_result = [1, '2', b'3']
        value = serialize(expected_result)
        expected_result[2] = String.from_bytes(expected_result[2])
        result, _ = await self.call('deserialize_arg', [value], return_type=list)
        self.assertEqual(expected_result, result)

        expected_result = {'int': 1, 'str': '2', 'bytes': b'3'}
        value = serialize(expected_result)
        expected_result['bytes'] = String.from_bytes(expected_result['bytes'])
        result, _ = await self.call('deserialize_arg', [value], return_type=dict[str, str])
        self.assertEqual(expected_result, result)

    def test_deserialize_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'DeserializeMismatchedType.py')

    async def test_json_serialize(self):
        await self.set_up_contract('JsonSerialize.py')

        test_input = {"one": 1, "two": 2, "three": 3}
        expected_result = json.dumps(test_input, separators=(',', ':'))
        result, _ = await self.call('main', [test_input], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_serialize_int(self):
        await self.set_up_contract('JsonSerializeInt.py')

        expected_result = json.dumps(10)
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_serialize_bool(self):
        await self.set_up_contract('JsonSerializeBool.py')

        expected_result = json.dumps(True)
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_serialize_str(self):
        await self.set_up_contract('JsonSerializeStr.py')

        expected_result = json.dumps('unit test')
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_serialize_bytes(self):
        await self.set_up_contract('JsonSerializeBytes.py')

        # Python does not accept bytes as parameter for json.dumps() method, since string and bytes ends up being the
        # same on Neo, it's being converted to string, before using dumps
        expected_result = json.dumps(String().from_bytes(b'unit test'))
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_deserialize(self):
        await self.set_up_contract('JsonDeserialize.py')

        test_input = json.dumps(12345)
        expected_result = json.loads(test_input)
        result, _ = await self.call('main', [test_input], return_type=int)
        self.assertEqual(expected_result, result)

        test_input = json.dumps('unit test')
        expected_result = json.loads(test_input)
        result, _ = await self.call('main', [test_input], return_type=str)
        self.assertEqual(expected_result, result)

        test_input = json.dumps(True)
        expected_result = json.loads(test_input)
        result, _ = await self.call('main', [test_input], return_type=bool)
        self.assertEqual(expected_result, result)

    async def test_boa2_serialization_test1(self):
        await self.set_up_contract('SerializationBoa2Test.py')

        expected_result = serialize(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'])
        result, _ = await self.call('main', [1], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_boa2_serialization_test2(self):
        await self.set_up_contract('SerializationBoa2Test.py')

        expected_result = serialize(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'])
        result, _ = await self.call('main', [2], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_boa2_serialization_test3(self):
        await self.set_up_contract('SerializationBoa2Test.py')

        result, _ = await self.call('main', [3], return_type=list)
        self.assertEqual(['a', 3, ['j', 3, 5], 'jk', 'lmnopqr'], result)

    async def test_boa2_serialization_test4(self):
        await self.set_up_contract('SerializationBoa2Test.py')

        result, _ = await self.call('main', [4], return_type=list)
        self.assertEqual(['j', 3, 5], result)

    async def test_user_class_serialization(self):
        await self.set_up_contract('SerializationUserClass.py')

        expected_class = [2, 4]
        expected_result = serialize(expected_class)
        result, _ = await self.call('serialize_user_class', [], return_type=bytes)
        self.assertEqual(expected_result, result)

        serialized = result

        result, _ = await self.call('deserialize_user_class', [serialized], return_type=list)
        self.assertEqual(expected_class, result)

        result, _ = await self.call('get_variable_from_deserialized', [serialized], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('call_method_from_deserialized', [serialized], return_type=int)
        self.assertEqual(42, result)

    async def test_atoi(self):
        await self.set_up_contract('Atoi.py')

        result, _ = await self.call('main', ['10', 10], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('main', ['10', 16], return_type=int)
        self.assertEqual(16, result)

        result, _ = await self.call('main', ['123', 10], return_type=int)
        self.assertEqual(123, result)

        result, _ = await self.call('main', ['123', 16], return_type=int)
        self.assertEqual(291, result)

        result, _ = await self.call('main', ['1f', 16], return_type=int)
        self.assertEqual(31, result)

        result, _ = await self.call('main', ['ff', 16], return_type=int)
        self.assertEqual(-1, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['string', 10], return_type=int)

        self.assertRegex(str(context.exception), self.INVALID_FORMAT_MSG)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['string', 16], return_type=int)

        self.assertRegex(str(context.exception), self.INVALID_FORMAT_MSG)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['abc', 10], return_type=int)

        self.assertRegex(str(context.exception), self.INVALID_FORMAT_MSG)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['10', 2], return_type=int)

        self.assertRegex(str(context.exception), self.INVALID_BASE_MSG)

    async def test_atoi_default(self):
        await self.set_up_contract('AtoiDefault.py')

        result, _ = await self.call('main', ['10'], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('main', ['123'], return_type=int)
        self.assertEqual(123, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', ['string'], return_type=int)

        self.assertRegex(str(context.exception), self.INVALID_FORMAT_MSG)

    def test_atoi_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'AtoiTooFewArguments.py')

    def test_atoi_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'AtoiTooManyArguments.py')

    def test_atoi_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'AtoiMismatchedType.py')

    async def test_itoa(self):
        await self.set_up_contract('Itoa')

        result, _ = await self.call('main', [10, 10], return_type=str)
        self.assertEqual('10', result)

        result, _ = await self.call('main', [16, 16], return_type=str)
        self.assertEqual('10', result)

        result, _ = await self.call('main', [-1, 10], return_type=str)
        self.assertEqual('-1', result)

        result, _ = await self.call('main', [-1, 16], return_type=str)
        self.assertEqual('f', result)

        result, _ = await self.call('main', [15, 16], return_type=str)
        self.assertEqual('0f', result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [10, 2], return_type=int)

        self.assertRegex(str(context.exception), self.INVALID_BASE_MSG)

    async def test_itoa_default(self):
        await self.set_up_contract('ItoaDefault')

        result, _ = await self.call('main', [10], return_type=str)
        self.assertEqual('10', result)

        result, _ = await self.call('main', [-1], return_type=str)
        self.assertEqual('-1', result)

    def test_itoa_too_few_arguments(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ItoaTooFewArguments')

    def test_itoa_too_many_arguments(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ItoaTooManyArguments')

    def test_itoa_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ItoaMismatchedType')

    async def test_memory_search(self):
        await self.set_up_contract('MemorySearch')

        result, _ = await self.call('main', ['abcde', 'a', 0, False], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abcde', b'a', 0, False], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abcde', b'b', 0, False], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', [b'abcde', b'c', 0, False], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [b'abcde', b'd', 0, False], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [b'abcde', b'e', 0, False], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', [b'abcde', b'a', 1, False], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('main', [b'abcde', b'cd', 0, False], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [b'abcde', b'abe', 0, False], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('main', [b'aaaaa', b'a', 0, False], return_type=int)
        self.assertEqual(0, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [b'abcde', b'a', 20, False], return_type=int)

        self.assertRegex(str(context.exception), 'slice bounds out of range')

    async def test_memory_search_backward(self):
        await self.set_up_contract('MemorySearch')

        result, _ = await self.call('main', ['abcde', 'a', 5, True], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abcde', b'a', 5, True], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abcde', b'b', 5, True], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', [b'abcde', b'c', 5, True], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [b'abcde', b'd', 5, True], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [b'abcde', b'e', 5, True], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', [b'abcde', b'a', 0, True], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('main', [b'abcde', b'cd', 5, True], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [b'abcde', b'abe', 5, True], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('main', [b'aaaaa', b'a', 5, True], return_type=int)
        self.assertEqual(4, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [b'abcde', b'a', 20, True], return_type=int)

        self.assertRegex(str(context.exception), 'invalid start index')

    async def test_memory_search_start(self):
        await self.set_up_contract('MemorySearchStart')

        result, _ = await self.call('main', ['abcde', 'a', 0], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abcde', b'a', 0], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abcde', b'e', 0], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', [b'abcde', b'a', 1], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('main', [b'abcde', b'cd', 0], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [b'abcde', b'abe', 0], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('main', [b'aaaaa', b'a', 0], return_type=int)
        self.assertEqual(0, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [b'abcde', b'a', 20], return_type=int)

        self.assertRegex(str(context.exception), 'slice bounds out of range')

    async def test_memory_search_default_values(self):
        await self.set_up_contract('MemorySearchDefault')

        result, _ = await self.call('main', ['abcde', 'a'], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abcde', b'a'], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abcde', b'b'], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', [b'abcde', b'c'], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [b'abcde', b'd'], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [b'abcde', b'e'], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', [b'abcde', b'cd'], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [b'abcde', b'aa'], return_type=int)
        self.assertEqual(-1, result)

    def test_memory_search_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MemorySearchMismatchedType.py')

    def test_memory_search_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'MemorySearchTooFewArguments.py')

    def test_memory_search_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'MemorySearchTooManyArguments.py')

    async def test_memory_compare(self):
        await self.set_up_contract('MemoryCompare')

        result, _ = await self.call('main', ['abc', 'abc'], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', ['abc', 'ABC'], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', ['ABC', 'abc'], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('main', [b'abc', b'abc'], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [b'abc', b'ABC'], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', [b'ABC', b'abc'], return_type=int)
        self.assertEqual(-1, result)

    def test_memory_compare_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'MemoryCompareTooFewArguments.py')

    def test_memory_compare_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'MemoryCompareTooManyArguments.py')

    def test_memory_compare_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MemoryCompareMismatchedType.py')

    async def test_import_contracts_stdlib(self):
        await self.set_up_contract('ImportContractsStdlib.py')

        value = 123
        result, _ = await self.call('main', [value], return_type=int)
        self.assertEqual(value, result)

        value = 'string'
        result, _ = await self.call('main', [value], return_type=str)

    async def test_import_sc_interop_json(self):
        await self.set_up_contract('ImportScContractsStdlib.py')

        value = 123
        result, _ = await self.call('main', [value], return_type=int)
        self.assertEqual(value, result)

        value = 'string'
        result, _ = await self.call('main', [value], return_type=str)
        self.assertEqual(value, result)

    async def test_string_split(self):
        await self.set_up_contract('StringSplit.py')

        string = 'abc,def,ghi'
        separator = ','
        result, _ = await self.call('main', [string, separator], return_type=list[str])
        self.assertEqual(string.split(separator), result)

        string = 'abc,def,ghi,,'
        separator = ','
        result, _ = await self.call('main', [string, separator], return_type=list[str])
        self.assertEqual(string.split(separator), result)

    async def test_str_len(self):
        await self.set_up_contract('StrLen.py')

        string = 'abcdefghijklmnopqrstuvwxyz'
        result, _ = await self.call('main', [string], return_type=int)
        self.assertEqual(len(string), result)

        string = '😀'
        result, _ = await self.call('main', [string], return_type=int)
        self.assertEqual(len(string), result)

    def test_overwrite_hash(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'CompilerErrorOverwriteHash.py')

    def test_hex_decode_compile(self):
        expected_output = (
                Opcode.INITSLOT
                + b'\x00\x01'
                + Opcode.LDARG0
                + Opcode.CALLT + b'\x00\x00'
                + Opcode.RET
        )

        output, _ = self.assertCompile('HexDecode.py')
        self.assertEqual(expected_output, output)

    @unittest.skip("Can not test without a Neo 3.9 node")
    async def test_hex_decode(self):
        await self.set_up_contract('HexDecode.py')

        value = '00010203'
        result, _ = await self.call('main', [value], return_type=bytes)
        self.assertEqual(bytes.fromhex(value), result)

    def test_hex_encode_compile(self):
        expected_output = (
                Opcode.INITSLOT
                + b'\x00\x01'
                + Opcode.LDARG0
                + Opcode.CALLT + b'\x00\x00'
                + Opcode.RET
        )

        output, _ = self.assertCompile('HexEncode.py')
        self.assertEqual(expected_output, output)

    @unittest.skip("Can not test without a Neo 3.9 node")
    async def test_hex_encode(self):
        await self.set_up_contract('HexEncode.py')

        value = b'\x00\x01\x02\x03'
        result, _ = await self.call('main', [value], return_type=str)
        self.assertEqual(value.hex(), result)
