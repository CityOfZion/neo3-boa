from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.StackItem import StackItemType, serialize
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBinaryInterop(BoaTest):

    def test_base64_encode(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.Base64Encode.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/binary/Base64Encode.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        import base64
        engine = TestEngine(self.dirname)
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
        path = '%s/boa3_test/test_sc/interop_test/binary/Base64EncodeMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_base64_decode(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.Base64Decode.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/binary/Base64Decode.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        import base64
        engine = TestEngine(self.dirname)
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
        path = '%s/boa3_test/test_sc/interop_test/binary/Base64DecodeMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_base58_encode(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.Base58Encode.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/binary/Base58Encode.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        import base58
        engine = TestEngine(self.dirname)
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
        path = '%s/boa3_test/test_sc/interop_test/binary/Base58EncodeMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_base58_decode(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.Base58Decode.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/binary/Base58Decode.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        import base58
        engine = TestEngine(self.dirname)
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
        path = '%s/boa3_test/test_sc/interop_test/binary/Base58DecodeMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_serialize_int(self):
        path = '%s/boa3_test/test_sc/interop_test/binary/SerializeInt.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'serialize_int',
                                         expected_result_type=bytes)
        expected_result = serialize(42)
        self.assertEqual(expected_result, result)

    def test_serialize_bool(self):
        path = '%s/boa3_test/test_sc/interop_test/binary/SerializeBool.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'serialize_bool',
                                         expected_result_type=bytes)
        expected_result = serialize(True)
        self.assertEqual(expected_result, result)

    def test_serialize_str(self):
        path = '%s/boa3_test/test_sc/interop_test/binary/SerializeStr.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'serialize_str',
                                         expected_result_type=bytes)
        expected_result = serialize('42')
        self.assertEqual(expected_result, result)

    def test_serialize_sequence(self):
        path = '%s/boa3_test/test_sc/interop_test/binary/SerializeSequence.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'serialize_sequence',
                                         expected_result_type=bytes)
        expected_result = serialize([2, 3, 5, 7])
        self.assertEqual(expected_result, result)

    def test_serialize_dict(self):
        path = '%s/boa3_test/test_sc/interop_test/binary/SerializeDict.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'serialize_dict',
                                         expected_result_type=bytes)
        expected_result = serialize({1: 1, 2: 1, 3: 2})
        self.assertEqual(expected_result, result)

    def test_deserialize(self):
        path = '%s/boa3_test/test_sc/interop_test/binary/Deserialize.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)

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
        path = '%s/boa3_test/test_sc/interop_test/binary/DeserializeMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)