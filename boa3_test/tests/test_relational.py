from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestRelational(BoaTest):

    default_folder: str = 'test_sc/relational_test'

    def test_number_equality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('NumEquality.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(True, result)

    def test_number_inequality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('NumInequality.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(False, result)

    def test_number_inequality_operation_2(self):
        path = self.get_contract_path('NumInequalityPython2.py')

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_number_less_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.RET
        )

        path = self.get_contract_path('NumLessThan.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1)
        self.assertEqual(False, result)

    def test_number_less_or_equal_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LE
            + Opcode.RET
        )

        path = self.get_contract_path('NumLessOrEqual.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1)
        self.assertEqual(False, result)

    def test_number_greater_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GT
            + Opcode.RET
        )

        path = self.get_contract_path('NumGreaterThan.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1)
        self.assertEqual(True, result)

    def test_number_greater_or_equal_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GE
            + Opcode.RET
        )

        path = self.get_contract_path('NumGreaterOrEqual.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1)
        self.assertEqual(True, result)

    def test_identity_operation(self):
        path = self.get_contract_path('NumIdentity.py')
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_boolean_equality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('BoolEquality.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(True, result)

    def test_boolean_inequality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('BoolInequality.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(False, result)

    def test_multiple_comparisons(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.LE
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LE
            + Opcode.BOOLAND
            + Opcode.RET
        )

        path = self.get_contract_path('NumRange.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 2, 5)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1, 5)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 5, 1, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 5, 1)
        self.assertEqual(False, result)

    def test_string_equality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.EQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('StrEquality.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(True, result)

    def test_string_inequality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NOTEQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('StrInequality.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(False, result)

    def test_string_less_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.RET
        )

        path = self.get_contract_path('StrLessThan.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'test', 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(True, result)

    def test_string_less_or_equal_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LE
            + Opcode.RET
        )

        path = self.get_contract_path('StrLessOrEqual.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'test', 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(True, result)

    def test_string_greater_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GT
            + Opcode.RET
        )

        path = self.get_contract_path('StrGreaterThan.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'test', 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(False, result)

    def test_string_greater_or_equal_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GE
            + Opcode.RET
        )

        path = self.get_contract_path('StrGreaterOrEqual.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'test', 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(False, result)

    def test_mixed_equality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.EQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('MixedEquality.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 123, '123')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', Integer.from_bytes(b'123'), '123')
        self.assertEqual(False, result)

    def test_mixed_inequality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NOTEQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('MixedInequality.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 1, 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 123, '123')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', Integer.from_bytes(b'123'), '123')
        self.assertEqual(True, result)

    def test_mixed_less_than_operation(self):
        path = self.get_contract_path('MixedLessThan.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mixed_less_or_equal_than_operation(self):
        path = self.get_contract_path('MixedLessOrEqual.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mixed_greater_than_operation(self):
        path = self.get_contract_path('MixedGreaterThan.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mixed_greater_or_equal_than_operation(self):
        path = self.get_contract_path('MixedGreaterOrEqual.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_list_equality_with_slice(self):
        path = self.get_contract_path('ListEqualityWithSlice.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', ['unittest', '123'], 'unittest',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', ['unittest', '123'], '123',
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'main', [], '')

    def test_compare_same_value_hard_coded(self):
        path = self.get_contract_path('CompareSameValueHardCoded.py')
        Boa3.compile_and_save(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'testing_something',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_compare_same_value_argument(self):
        path = self.get_contract_path('CompareSameValueArgument.py')
        Boa3.compile_and_save(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'testing_something', bytes(20),
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_boa2_equality_test2(self):
        path = self.get_contract_path('Equality2Boa2Test.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 2)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 3)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 4)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 5)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 6)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 7)
        self.assertEqual(False, result)
