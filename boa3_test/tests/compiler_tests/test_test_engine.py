from boa3.neo.utils import contract_parameter_to_json, stack_item_from_json
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItem import StackItemType
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTestEngine(BoaTest):

    def test_parameter_to_json_int(self):
        expected_result = {
            'type': AbiType.Integer.value,
            'value': 5
        }
        result = contract_parameter_to_json(5)
        self.assertEqual(expected_result, result)

        expected_result = {
            'type': AbiType.Integer.value,
            'value': 5000000
        }
        result = contract_parameter_to_json(5000000)
        self.assertEqual(expected_result, result)

    def test_parameter_to_json_bool(self):
        expected_result = {
            'type': AbiType.Boolean.value,
            'value': True
        }
        result = contract_parameter_to_json(True)
        self.assertEqual(expected_result, result)

        expected_result = {
            'type': AbiType.Boolean.value,
            'value': False
        }
        result = contract_parameter_to_json(False)
        self.assertEqual(expected_result, result)

    def test_parameter_to_json_str(self):
        expected_result = {
            'type': AbiType.String.value,
            'value': 'unittest'
        }
        result = contract_parameter_to_json('unittest')
        self.assertEqual(expected_result, result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = {
            'type': AbiType.String.value,
            'value': long_string
        }
        result = contract_parameter_to_json(long_string)
        self.assertEqual(expected_result, result)

    def test_parameter_to_json_none(self):
        expected_result = {
            'type': AbiType.Any.value,
        }
        result = contract_parameter_to_json(None)
        self.assertEqual(expected_result, result)

    def test_parameter_to_json_bytes(self):
        expected_result = {
            'type': AbiType.ByteArray.value,
            'value': 'AQIDBAU='
        }
        result = contract_parameter_to_json(b'\x01\x02\x03\x04\x05')
        self.assertEqual(expected_result, result)

        long_bytes = (String('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                             'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut '
                             'interdum et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, '
                             'rhoncus justo. Mauris sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue '
                             'tellus, vel pellentesque libero leo id dui. Morbi vel risus vehicula, consectetur '
                             'mauris eget, gravida ligula. Maecenas aliquam velit sit amet nisi ultricies, '
                             'ac sollicitudin nisi mollis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                             'Ut tincidunt, nisi in ullamcorper ornare, est enim dictum massa, id aliquet justo magna '
                             'in purus.')
                      .to_bytes())
        long_encoded = ('TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdC4gTnVsbGFtIGFjY3V' +
                        'tc2FuIG1hZ25hIGV1IG1hc3NhIHZ1bHB1dGF0ZSBiaWJlbmR1bS4gQWxpcXVhbSBjb21tb2RvIGV1aXNtb2QgdHJpc3' +
                        'RpcXVlLiBTZWQgcHVydXMgZXJhdCwgcHJldGl1bSB1dCBpbnRlcmR1bSBldCwgYWxpcXVldCBzZWQgbWF1cmlzLiBDd' +
                        'XJhYml0dXIgdml0YWUgdHVycGlzIGV1aXNtb2QsIGhlbmRyZXJpdCBtaSBhLCByaG9uY3VzIGp1c3RvLiBNYXVyaXMg' +
                        'c29sbGljaXR1ZGluLCBuaXNsIHNpdCBhbWV0IGZldWdpYXQgcGhhcmV0cmEsIG9kaW8gbGlndWxhIGNvbmd1ZSB0ZWx' +
                        'sdXMsIHZlbCBwZWxsZW50ZXNxdWUgbGliZXJvIGxlbyBpZCBkdWkuIE1vcmJpIHZlbCByaXN1cyB2ZWhpY3VsYSwgY2' +
                        '9uc2VjdGV0dXIgbWF1cmlzIGVnZXQsIGdyYXZpZGEgbGlndWxhLiBNYWVjZW5hcyBhbGlxdWFtIHZlbGl0IHNpdCBhb' +
                        'WV0IG5pc2kgdWx0cmljaWVzLCBhYyBzb2xsaWNpdHVkaW4gbmlzaSBtb2xsaXMuIExvcmVtIGlwc3VtIGRvbG9yIHNp' +
                        'dCBhbWV0LCBjb25zZWN0ZXR1ciBhZGlwaXNjaW5nIGVsaXQuIFV0IHRpbmNpZHVudCwgbmlzaSBpbiB1bGxhbWNvcnB' +
                        'lciBvcm5hcmUsIGVzdCBlbmltIGRpY3R1bSBtYXNzYSwgaWQgYWxpcXVldCBqdXN0byBtYWduYSBpbiBwdXJ1cy4=')
        expected_result = {
            'type': AbiType.ByteArray.value,
            'value': long_encoded
        }
        result = contract_parameter_to_json(long_bytes)
        self.assertEqual(expected_result, result)

    def test_parameter_to_json_list(self):
        expected_result = {
            'type': AbiType.Array.value,
            'value': [
                {
                    'type': AbiType.Integer.value,
                    'value': 1
                },
                {
                    'type': AbiType.Integer.value,
                    'value': 2
                },
                {
                    'type': AbiType.Integer.value,
                    'value': 3
                }
            ]
        }
        result = contract_parameter_to_json([1, 2, 3])
        self.assertEqual(expected_result, result)

        expected_result = {
            'type': AbiType.Array.value,
            'value': [
                {
                    'type': AbiType.Boolean.value,
                    'value': True
                },
                {
                    'type': AbiType.Integer.value,
                    'value': 2
                },
                {
                    'type': AbiType.String.value,
                    'value': '3'
                }
            ]
        }
        result = contract_parameter_to_json([True, 2, '3'])
        self.assertEqual(expected_result, result)

    def test_parameter_to_json_tuple(self):
        expected_result = {
            'type': AbiType.Array.value,
            'value': [
                {
                    'type': AbiType.ByteArray.value,
                    'value': 'AQ=='
                },
                {
                    'type': AbiType.ByteArray.value,
                    'value': 'Ag=='
                },
                {
                    'type': AbiType.ByteArray.value,
                    'value': 'Aw=='
                }
            ]
        }
        result = contract_parameter_to_json((b'\x01', b'\x02', b'\x03'))
        self.assertEqual(expected_result, result)

        expected_result = {
            'type': AbiType.Array.value,
            'value': [
                {
                    'type': AbiType.Boolean.value,
                    'value': True
                },
                {
                    'type': AbiType.Integer.value,
                    'value': 2
                },
                {
                    'type': AbiType.String.value,
                    'value': '3'
                }
            ]
        }
        result = contract_parameter_to_json((True, 2, '3'))
        self.assertEqual(expected_result, result)

    def test_parameter_to_json_dict(self):
        expected_result = {
            'type': AbiType.Map.value,
            'value': [
                {
                    'key': {
                        'type': AbiType.String.value,
                        'value': 'a'
                    },
                    'value': {
                        'type': AbiType.Integer.value,
                        'value': 1
                    }
                },
                {
                    'key': {
                        'type': AbiType.String.value,
                        'value': 'b'
                    },
                    'value': {
                        'type': AbiType.Boolean.value,
                        'value': False
                    }
                }
            ]
        }
        result = contract_parameter_to_json({
            'a': 1,
            'b': False
        })
        self.assertEqual(expected_result, result)

    def test_any_stack_item_from_json(self):
        stack_item = {
            'type': StackItemType.Any.name
        }
        result = stack_item_from_json(stack_item)
        self.assertIsNone(result)

    def test_integer_stack_item_from_json(self):
        stack_item = {
            'type': StackItemType.Integer.name,
            'value': 5
        }
        expected_result = 5
        result = stack_item_from_json(stack_item)
        self.assertEqual(expected_result, result)

        stack_item = {
            'type': StackItemType.Integer.name,
            'value': '5'
        }
        result = stack_item_from_json(stack_item)
        self.assertEqual(expected_result, result)

        stack_item = {
            'type': StackItemType.Integer.name,
            'value': 'xyz'
        }
        with self.assertRaises(ValueError):
            stack_item_from_json(stack_item)

    def test_boolean_stack_item_from_json(self):
        stack_item = {
            'type': StackItemType.Boolean.name,
            'value': False
        }
        expected_result = False
        result = stack_item_from_json(stack_item)
        self.assertEqual(expected_result, result)

        stack_item = {
            'type': StackItemType.Boolean.name,
            'value': 'False'
        }
        result = stack_item_from_json(stack_item)
        self.assertEqual(expected_result, result)

        stack_item = {
            'type': StackItemType.Boolean.name,
            'value': 1
        }
        with self.assertRaises(ValueError):
            stack_item_from_json(stack_item)

    def test_byte_string_stack_item_from_json(self):
        stack_item = {
            'type': StackItemType.ByteString.name,
            'value': 'dW5pdHRlc3Q='
        }
        expected_result = 'unittest'
        result = stack_item_from_json(stack_item)
        self.assertEqual(expected_result, result)

        stack_item = {
            'type': StackItemType.ByteString.name,
            'value': b'unittest'
        }
        with self.assertRaises(ValueError):
            stack_item_from_json(stack_item)

    def test_buffer_stack_item_from_json(self):
        stack_item = {
            'type': StackItemType.Buffer.name,
            'value': 'dW5pdHRlc3Q='
        }
        expected_result = 'unittest'
        result = stack_item_from_json(stack_item)
        self.assertEqual(expected_result, result)

        stack_item = {
            'type': StackItemType.Buffer.name,
            'value': b'unittest'
        }
        with self.assertRaises(ValueError):
            stack_item_from_json(stack_item)

    def test_map_stack_item_from_json(self):
        stack_item = {
            'type': 'Map',
            'value': [
                {
                    'key': {
                        'type': StackItemType.Integer.name,
                        'value': 1
                    },
                    'value': {
                        'type': StackItemType.Boolean.name,
                        'value': True
                    }
                },
                {
                    'key': {
                        'type': StackItemType.Integer.name,
                        'value': 2
                    },
                    'value': {
                        'type': StackItemType.Integer.name,
                        'value': 4
                    }
                },
                {
                    'key': {
                        'type': StackItemType.Integer.name,
                        'value': 3
                    },
                    'value': {
                        'type': StackItemType.ByteString.name,
                        'value': 'bmluZQ=='
                    }
                }
            ]
        }
        expected_result = {
            1: True,
            2: 4,
            3: 'nine'
        }
        result = stack_item_from_json(stack_item)
        self.assertEqual(expected_result, result)

    def test_run(self):
        path = self.get_contract_path('test_sc/generation_test', 'GenerationWithDecorator.py')
        self.compile_and_save(path)
        path = path.replace('.py', '.nef')

        engine = TestEngine()
        result = engine.run(path, 'Sub', 50, 20)
        self.assertEqual(30, result)

    def test_test_engine_not_found_error(self):
        # if the TestEngine is correctly installed a error should not occur
        from boa3 import env
        engine_path = env.TEST_ENGINE_DIRECTORY
        engine = TestEngine(engine_path)

        # however, if the TestEngine is not in the directory it will raise an Exception
        with self.assertRaises(FileNotFoundError):
            engine = TestEngine('{0}/boa3_test'.format(engine_path))
