from boa3.exception import CompilerError
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestMath(BoaTest):

    default_folder: str = 'test_sc/math_test'

    def test_no_import(self):
        path = self.get_contract_path('NoImport.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    # region pow test

    def test_pow_method(self):
        path = self.get_contract_path('Pow.py')
        engine = TestEngine()

        import math

        base = 1
        exponent = 4
        result = self.run_smart_contract(engine, path, 'main', base, exponent)
        self.assertEqual(math.pow(base, exponent), result)

        base = 5
        exponent = 2
        result = self.run_smart_contract(engine, path, 'main', base, exponent)
        self.assertEqual(math.pow(base, exponent), result)

        base = -2
        exponent = 2
        result = self.run_smart_contract(engine, path, 'main', base, exponent)
        self.assertEqual(math.pow(base, exponent), result)

        base = -2
        exponent = 3
        result = self.run_smart_contract(engine, path, 'main', base, exponent)
        self.assertEqual(math.pow(base, exponent), result)

        base = 2
        exponent = 0
        result = self.run_smart_contract(engine, path, 'main', base, exponent)
        self.assertEqual(math.pow(base, exponent), result)

    def test_pow_method_from_math(self):
        path = self.get_contract_path('PowFromMath.py')
        engine = TestEngine()

        from math import pow

        base = 2
        exponent = 3
        result = self.run_smart_contract(engine, path, 'main', base, exponent)
        self.assertEqual(pow(base, exponent), result)

    # endregion

    # region sqrt test

    def test_sqrt_method(self):
        path = self.get_contract_path('Sqrt.py')
        engine = TestEngine()

        from math import sqrt

        expected_result = int(sqrt(0))
        result = self.run_smart_contract(engine, path, 'main', 0)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(1))
        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(3))
        result = self.run_smart_contract(engine, path, 'main', 3)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(4))
        result = self.run_smart_contract(engine, path, 'main', 4)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(8))
        result = self.run_smart_contract(engine, path, 'main', 8)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(10))
        result = self.run_smart_contract(engine, path, 'main', 10)
        self.assertEqual(expected_result, result)

        with self.assertRaisesRegex(TestExecutionException, self.VALUE_CANNOT_BE_NEGATIVE_MSG):
            self.run_smart_contract(engine, path, 'main', -1)

        val = 25
        expected_result = int(sqrt(val))
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(expected_result, result)

    def test_sqrt_method_from_math(self):
        path = self.get_contract_path('SqrtFromMath.py')
        engine = TestEngine()

        from math import sqrt

        val = 25
        expected_result = int(sqrt(val))
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(expected_result, result)

    # endregion
