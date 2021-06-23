from boa3.exception import CompilerError
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestReversed(BoaTest):

    default_folder: str = 'test_sc/reversed_test'

    def test_reversed_list_bool(self):
        path = self.get_contract_path('ReversedListBool.py')
        engine = TestEngine()

        list_bool = [True, True, False]
        result = self.run_smart_contract(engine, path, 'main')
        reversed_list = [element for element in reversed(list_bool)]
        self.assertEqual(reversed_list, result)

    def test_reversed_list_bytes(self):
        path = self.get_contract_path('ReversedListBytes.py')
        engine = TestEngine()

        list_bytes = [b'1', b'2', b'3']
        reversed_list = [element for element in reversed(list_bytes)]
        result = self.run_smart_contract(engine, path, 'main')
        if isinstance(result, list):
            for k in range(len(result)):
                if isinstance(result[k], str):
                    result[k] = String(result[k]).to_bytes()
        self.assertEqual(reversed_list, result)

    def test_reversed_list_int(self):
        path = self.get_contract_path('ReversedListInt.py')
        engine = TestEngine()

        list_int = [1, 2, 3]
        result = self.run_smart_contract(engine, path, 'main')
        reversed_list = [element for element in reversed(list_int)]
        self.assertEqual(reversed_list, result)

    def test_reversed_list_str(self):
        path = self.get_contract_path('ReversedListStr.py')
        engine = TestEngine()

        list_str = ['neo3-boa', 'unit', 'test']
        result = self.run_smart_contract(engine, path, 'main')
        reversed_list = [element for element in reversed(list_str)]
        self.assertEqual(reversed_list, result)

    def test_reversed_list(self):
        path = self.get_contract_path('ReversedList.py')
        engine = TestEngine()

        list_any = [1, 'string', False]
        result = self.run_smart_contract(engine, path, 'main', list_any)
        reversed_list = [element for element in reversed(list_any)]
        self.assertEqual(reversed_list, result)

    def test_reversed_string(self):
        path = self.get_contract_path('ReversedString.py')
        engine = TestEngine()

        string = 'unit_test'
        result = self.run_smart_contract(engine, path, 'main', string)
        reversed_list = [element for element in reversed(string)]
        self.assertEqual(reversed_list, result)

    def test_reversed_bytes(self):
        path = self.get_contract_path('ReversedBytes.py')
        engine = TestEngine()

        bytes_value = b'unit_test'
        reversed_list = [element for element in reversed(bytes_value)]
        result = self.run_smart_contract(engine, path, 'main', bytes_value)
        self.assertEqual(reversed_list, result)

    def test_reversed_range(self):
        path = self.get_contract_path('ReversedRange.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        reversed_list = [element for element in reversed(range(3))]
        self.assertEqual(reversed_list, result)

    def test_reversed_tuple(self):
        path = self.get_contract_path('ReversedTuple.py')
        engine = TestEngine()

        tuple_value = (1, 2, 3)
        result = self.run_smart_contract(engine, path, 'main', tuple_value)
        reversed_list = [element for element in reversed(tuple_value)]
        self.assertEqual(reversed_list, result)

    def test_mismatched_type(self):
        path = self.get_contract_path('ReversedParameterMismatchedType')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
