from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo3.contracts import FindOptions
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestRelational(BoaTest):
    default_folder: str = 'test_sc/relational_test'

    # region GreaterThan

    def test_builtin_type_greater_than_operation(self):
        path = self.get_contract_path('BuiltinTypeGreaterThan.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES)
        self.assertEqual(FindOptions.VALUES_ONLY > FindOptions.DESERIALIZE_VALUES, result)

    def test_mixed_greater_than_operation(self):
        path = self.get_contract_path('MixedGreaterThan.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

    # endregion

    # region GreaterThanOrEqual

    def test_builtin_type_greater_than_or_equal_operation(self):
        path = self.get_contract_path('BuiltinTypeGreaterThanOrEqual.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY)
        self.assertEqual(FindOptions.VALUES_ONLY >= FindOptions.VALUES_ONLY, result)

    def test_mixed_greater_or_equal_than_operation(self):
        path = self.get_contract_path('MixedGreaterOrEqual.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

    # endregion

    # region Identity

    def test_boolean_identity_operation(self):
        path = self.get_contract_path('BoolIdentity.py')
        engine = TestEngine()

        a = True
        b = True
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'without_attribution_true')
        self.assertEqual(expected_result, result)

        a = True
        b = False
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'without_attribution_false')
        self.assertEqual(expected_result, result)

        c = True
        d = c
        expected_result = c is d
        result = self.run_smart_contract(engine, path, 'with_attribution')
        self.assertEqual(expected_result, result)

    def test_list_identity(self):
        path = self.get_contract_path('ListIdentity.py')
        engine = TestEngine()

        a = [1, 2, 3]
        b = a
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'with_attribution', expected_result_type=bool)
        self.assertEqual(expected_result, result)

        a = [1, 2, 3]
        b = [1, 2, 3]
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'without_attribution', expected_result_type=bool)
        self.assertEqual(expected_result, result)

    def test_mixed_identity(self):
        path = self.get_contract_path('MixedIdentity.py')
        engine = TestEngine()

        # a mixed identity should always result in False, but will compile
        result = self.run_smart_contract(engine, path, 'mixed', expected_result_type=bool)
        self.assertEqual(False, result)

    def test_none_identity_operation(self):
        path = self.get_contract_path('NoneIdentity.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', True)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 'string')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', b'bytes')
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', None)
        self.assertEqual(True, result)

    def test_number_identity_operation(self):
        path = self.get_contract_path('NumIdentity.py')
        engine = TestEngine()

        a = 1
        b = 1
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'without_attribution_true')
        self.assertEqual(expected_result, result)

        a = 1
        b = 2
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'without_attribution_false')
        self.assertEqual(expected_result, result)

        c = 1
        d = c
        expected_result = c is d
        result = self.run_smart_contract(engine, path, 'with_attribution')
        self.assertEqual(expected_result, result)

    def test_string_identity_operation(self):
        path = self.get_contract_path('StrIdentity.py')
        engine = TestEngine()

        a = 'unit'
        b = 'unit'
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'without_attribution_true')
        self.assertEqual(expected_result, result)

        a = 'unit'
        b = 'test'
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'without_attribution_false')
        self.assertEqual(expected_result, result)

        c = 'unit'
        d = c
        expected_result = c is d
        result = self.run_smart_contract(engine, path, 'with_attribution')
        self.assertEqual(expected_result, result)

    def test_tuple_identity(self):
        path = self.get_contract_path('TupleIdentity.py')
        engine = TestEngine()

        a = (1, 2, 3)
        b = a
        expected_result = a is b
        result = self.run_smart_contract(engine, path, 'with_attribution', expected_result_type=bool)
        self.assertEqual(expected_result, result)

        # Python will try conserve memory and will make a and b reference the same position, since Tuples are immutable
        # this will deviate from Neo's expected behavior
        result = self.run_smart_contract(engine, path, 'without_attribution', expected_result_type=bool)
        self.assertEqual(False, result)

    # endregion

    # region LessThan

    def test_builtin_type_less_than_operation(self):
        path = self.get_contract_path('BuiltinTypeLessThan.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY)
        self.assertEqual(FindOptions.VALUES_ONLY < FindOptions.VALUES_ONLY, result)

    def test_mixed_less_than_operation(self):
        path = self.get_contract_path('MixedLessThan.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

    # endregion

    # region LessThanOrEqual

    def test_builtin_type_less_than_or_equal_operation(self):
        path = self.get_contract_path('BuiltinTypeLessThanOrEqual.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY)
        self.assertEqual(FindOptions.VALUES_ONLY <= FindOptions.VALUES_ONLY, result)

    def test_mixed_less_or_equal_than_operation(self):
        path = self.get_contract_path('MixedLessOrEqual.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

    # endregion

    # region MixedEquality

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

    # endregion

    # region MixedInequality

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

    # endregion

    # region NotIdentity

    def test_boolean_not_identity_operation(self):
        path = self.get_contract_path('BoolNotIdentity.py')
        engine = TestEngine()

        a = True
        b = False
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'without_attribution_true')
        self.assertEqual(expected_result, result)

        a = True
        b = True
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'without_attribution_false')
        self.assertEqual(expected_result, result)

        c = True
        d = c
        expected_result = c is not d
        result = self.run_smart_contract(engine, path, 'with_attribution')
        self.assertEqual(expected_result, result)

    def test_list_not_identity(self):
        path = self.get_contract_path('ListNotIdentity.py')
        engine = TestEngine()

        a = [1, 2, 3]
        b = a
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'with_attribution', expected_result_type=bool)
        self.assertEqual(expected_result, result)

        a = [1, 2, 3]
        b = [1, 2, 3]
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'without_attribution', expected_result_type=bool)
        self.assertEqual(expected_result, result)

    def test_none_not_identity_operation(self):
        path = self.get_contract_path('NoneNotIdentity.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', True)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 'string')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', b'bytes')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', None)
        self.assertEqual(False, result)

    def test_number_not_identity_operation(self):
        path = self.get_contract_path('NumNotIdentity.py')
        engine = TestEngine()

        a = 1
        b = 2
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'without_attribution_true')
        self.assertEqual(expected_result, result)

        a = 1
        b = 1
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'without_attribution_false')
        self.assertEqual(expected_result, result)

        c = 1
        d = c
        expected_result = c is not d
        result = self.run_smart_contract(engine, path, 'with_attribution')
        self.assertEqual(expected_result, result)

    def test_string_not_identity_operation(self):
        path = self.get_contract_path('StrNotIdentity.py')
        engine = TestEngine()

        a = 'unit'
        b = 'test'
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'without_attribution_true')
        self.assertEqual(expected_result, result)

        a = 'unit'
        b = 'unit'
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'without_attribution_false')
        self.assertEqual(expected_result, result)

        c = 'unit'
        d = c
        expected_result = c is not d
        result = self.run_smart_contract(engine, path, 'with_attribution')
        self.assertEqual(expected_result, result)

    def test_tuple_not_identity(self):
        path = self.get_contract_path('TupleNotIdentity.py')
        engine = TestEngine()

        a = (1, 2, 3)
        b = a
        expected_result = a is not b
        result = self.run_smart_contract(engine, path, 'with_attribution', expected_result_type=bool)
        self.assertEqual(expected_result, result)

        # Python will try conserve memory and will make a and b reference the same position, since Tuples are immutable
        # this will deviate from Neo's expected behavior
        result = self.run_smart_contract(engine, path, 'without_attribution', expected_result_type=bool)
        self.assertEqual(True, result)

    # endregion

    # region NumericEquality

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

    def test_builtin_equality_operation(self):
        path = self.get_contract_path('BuiltinTypeEquality.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY)
        self.assertEqual(FindOptions.VALUES_ONLY == FindOptions.VALUES_ONLY, result)

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

    # endregion

    # region NumericInequality

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

    def test_builtin_inequality_operation(self):
        path = self.get_contract_path('BuiltinTypeInequality.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY)
        self.assertEqual(FindOptions.VALUES_ONLY != FindOptions.VALUES_ONLY, result)

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
            Boa3.compile(path)

    # endregion

    # region ObjectEquality

    def test_compare_same_value_argument(self):
        path = self.get_contract_path('CompareSameValueArgument.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'testing_something', bytes(20),
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_compare_same_value_hard_coded(self):
        path = self.get_contract_path('CompareSameValueHardCoded.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'testing_something',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_compare_string(self):
        path = self.get_contract_path('CompareString.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'test1', '|',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'test2', '|',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'test3', '|',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'test4', '|',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

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

    # endregion

    # region ObjectInequality

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

    # endregion
