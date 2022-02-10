import unittest

from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from test_runner import utils
from test_runner.neo_test_runner import NeoTestRunner


class TestTestRunner(BoaTest):

    @unittest.skip("don't run while circleci config is not updated with test runner")
    def test_run(self):
        path = self.get_contract_path('test_sc/generation_test', 'GenerationWithDecorator.py')
        self.compile_and_save(path)
        path = path.replace('.py', '.nef')

        runner = NeoTestRunner()
        result = runner.run(path, 'Sub', 50, 20)
        self.assertEqual(30, result)

    def test_int_value_to_invoke_parameter(self):
        expected_result = 5
        result = utils.value_to_parameter(5)
        self.assertEqual(expected_result, result)

        expected_result = 5000000
        result = utils.value_to_parameter(5000000)
        self.assertEqual(expected_result, result)

    def test_bool_value_to_invoke_parameter(self):
        expected_result = True
        result = utils.value_to_parameter(True)
        self.assertEqual(expected_result, result)

        expected_result = False
        result = utils.value_to_parameter(False)
        self.assertEqual(expected_result, result)

    def test_str_value_to_invoke_parameter(self):
        expected_result = 'unittest'
        result = utils.value_to_parameter('unittest')
        self.assertEqual(expected_result, result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = long_string
        result = utils.value_to_parameter(long_string)
        self.assertEqual(expected_result, result)

    def test_none_value_to_invoke_parameter(self):
        expected_result = None
        result = utils.value_to_parameter(None)
        self.assertEqual(expected_result, result)

    def test_bytes_value_to_invoke_parameter(self):
        expected_result = '0x0102030405'
        result = utils.value_to_parameter(b'\x01\x02\x03\x04\x05')
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

        expected_result = utils.bytes_to_hex(long_bytes)
        result = utils.value_to_parameter(long_bytes)
        self.assertEqual(expected_result, result)

    def test_list_value_to_invoke_parameter(self):
        expected_result = [1, 2, 3]
        result = utils.value_to_parameter([1, 2, 3])
        self.assertEqual(expected_result, result)

        expected_result = [True, 2, '3']
        result = utils.value_to_parameter([True, 2, '3'])
        self.assertEqual(expected_result, result)

    def test_tuple_value_to_invoke_parameter(self):
        expected_result = ['0x0102', '0x0304', '0x0506']
        result = utils.value_to_parameter((b'\x01\x02', b'\x03\x04', b'\x05\x06'))
        self.assertEqual(expected_result, result)

        expected_result = [True, 2, '3']
        result = utils.value_to_parameter((True, 2, '3'))
        self.assertEqual(expected_result, result)

    def test_dict_value_to_invoke_parameter(self):
        expected_result = {
            'type': AbiType.Map.value,
            'value': [
                {'key': '0x61', 'value': 1},
                {'key': '0x62', 'value': False}
            ]
        }
        result = utils.value_to_parameter({
            b'a': 1,
            b'b': False
        })
        self.assertEqual(expected_result, result)
