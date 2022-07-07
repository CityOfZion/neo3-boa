from boa3.exception import CompilerError
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBuiltinMethod(BoaTest):
    default_folder: str = 'test_sc/boa_built_in_methods_test'

    def test_abort(self):
        path = self.get_contract_path('Abort.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', False)
        self.assertEqual(123, result)

        with self.assertRaisesRegex(TestExecutionException, self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'main', True)

    def test_deploy_def(self):
        path = self.get_contract_path('DeployDef.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'get_var')
        self.assertEqual(10, result)

    def test_deploy_def_incorrect_signature(self):
        path = self.get_contract_path('DeployDefWrongSignature.py')
        self.assertCompilerLogs(CompilerError.InternalIncorrectSignature, path)

    def test_will_not_compile(self):
        path = self.get_contract_path('WillNotCompile.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    # region math builtins

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

    def test_decimal_floor_method(self):
        path = self.get_contract_path('DecimalFloor.py')
        engine = TestEngine()

        from math import floor

        value = 4.2
        decimals = 8

        multiplier = 10 ** decimals
        value_floor = int(floor(value)) * multiplier
        integer_value = int(value * multiplier)
        result = self.run_smart_contract(engine, path, 'main', integer_value, decimals)
        self.assertEqual(value_floor, result)

        decimals = 12

        multiplier = 10 ** decimals
        value_floor = int(floor(value)) * multiplier
        integer_value = int(value * multiplier)
        result = self.run_smart_contract(engine, path, 'main', integer_value, decimals)
        self.assertEqual(value_floor, result)

        value = -3.983541

        multiplier = 10 ** decimals
        value_floor = int(floor(value) * multiplier)
        integer_value = int(value * multiplier)
        result = self.run_smart_contract(engine, path, 'main', integer_value, decimals)
        self.assertEqual(value_floor, result)

        # negative decimals will raise an exception
        from boa3.model.builtin.builtin import Builtin
        with self.assertRaisesRegex(TestExecutionException, f'{Builtin.BuiltinMathFloor.exception_message}$'):
            self.run_smart_contract(engine, path, 'main', integer_value, -1)

    def test_decimal_ceil_method(self):
        path = self.get_contract_path('DecimalCeiling.py')
        engine = TestEngine()

        from math import ceil

        value = 4.2
        decimals = 8

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value)) * multiplier
        integer_value = int(value * multiplier)
        result = self.run_smart_contract(engine, path, 'main', integer_value, decimals)
        self.assertEqual(value_ceiling, result)

        decimals = 12

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value)) * multiplier
        integer_value = int(value * multiplier)
        result = self.run_smart_contract(engine, path, 'main', integer_value, decimals)
        self.assertEqual(value_ceiling, result)

        value = -3.983541

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value) * multiplier)
        integer_value = int(value * multiplier)
        result = self.run_smart_contract(engine, path, 'main', integer_value, decimals)
        self.assertEqual(value_ceiling, result)

        # negative decimals will raise an exception
        from boa3.model.builtin.builtin import Builtin
        with self.assertRaisesRegex(TestExecutionException, f'{Builtin.BuiltinMathCeil.exception_message}$'):
            self.run_smart_contract(engine, path, 'main', integer_value, -1)

    # endregion
