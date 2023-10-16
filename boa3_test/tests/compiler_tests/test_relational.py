from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.contracts import FindOptions
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestRelational(BoaTest):
    default_folder: str = 'test_sc/relational_test'

    # region GreaterThan

    def test_builtin_type_greater_than_operation(self):
        path, _ = self.get_deploy_file_paths('BuiltinTypeGreaterThan.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES))
        expected_results.append(FindOptions.VALUES_ONLY > FindOptions.DESERIALIZE_VALUES)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 2, 2))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 2, 1))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'test', 'unit'))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'unit'))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'test'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region GreaterThanOrEqual

    def test_builtin_type_greater_than_or_equal_operation(self):
        path, _ = self.get_deploy_file_paths('BuiltinTypeGreaterThanOrEqual.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.VALUES_ONLY >= FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 2, 2))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 2, 1))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'test', 'unit'))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'unit'))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'test'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region Identity

    def test_boolean_identity_operation(self):
        path, _ = self.get_deploy_file_paths('BoolIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = True
        b = True
        invokes.append(runner.call_contract(path, 'without_attribution_true'))
        expected_results.append(a is b)

        a = True
        b = False
        invokes.append(runner.call_contract(path, 'without_attribution_false'))
        expected_results.append(a is b)

        c = True
        d = c
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(c is d)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_identity(self):
        path, _ = self.get_deploy_file_paths('ListIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = [1, 2, 3]
        b = a
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(a is b)

        a = [1, 2, 3]
        b = [1, 2, 3]
        invokes.append(runner.call_contract(path, 'without_attribution'))
        expected_results.append(a is b)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mixed_identity(self):
        path, _ = self.get_deploy_file_paths('MixedIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        # a mixed identity should always result in False, but will compile
        invokes.append(runner.call_contract(path, 'mixed'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_none_identity_operation(self):
        path, _ = self.get_deploy_file_paths('NoneIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 'string'))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', b'bytes'))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_number_identity_operation(self):
        path, _ = self.get_deploy_file_paths('NumIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = 1
        b = 1
        invokes.append(runner.call_contract(path, 'without_attribution_true'))
        expected_results.append(a is b)

        a = 1
        b = 2
        invokes.append(runner.call_contract(path, 'without_attribution_false'))
        expected_results.append(a is b)

        c = 1
        d = c
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(c is d)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_identity_operation(self):
        path, _ = self.get_deploy_file_paths('StrIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = 'unit'
        b = 'unit'
        invokes.append(runner.call_contract(path, 'without_attribution_true'))
        expected_results.append(a is b)

        a = 'unit'
        b = 'test'
        invokes.append(runner.call_contract(path, 'without_attribution_false'))
        expected_results.append(a is b)

        c = 'unit'
        d = c
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(c is d)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_identity(self):
        path, _ = self.get_deploy_file_paths('TupleIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = (1, 2, 3)
        b = a
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(a is b)

        # Python will try conserve memory and will make a and b reference the same position, since Tuples are immutable
        # this will deviate from Neo's expected behavior
        invokes.append(runner.call_contract(path, 'without_attribution'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region LessThan

    def test_builtin_type_less_than_operation(self):
        path, _ = self.get_deploy_file_paths('BuiltinTypeLessThan.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.VALUES_ONLY < FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 2, 2))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 2, 1))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'test', 'unit'))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'unit'))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'test'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region LessThanOrEqual

    def test_builtin_type_less_than_or_equal_operation(self):
        path, _ = self.get_deploy_file_paths('BuiltinTypeLessThanOrEqual.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.VALUES_ONLY <= FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 2, 2))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 2, 1))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'test', 'unit'))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'unit'))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'test'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 'unit'))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 123, '123'))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', Integer.from_bytes(b'123'), '123'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_equality_test2(self):
        path, _ = self.get_deploy_file_paths('Equality2Boa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 2))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 3))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 4))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 5))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 6))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 7))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 'unit'))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 123, '123'))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', Integer.from_bytes(b'123'), '123'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region NotIdentity

    def test_boolean_not_identity_operation(self):
        path, _ = self.get_deploy_file_paths('BoolNotIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = True
        b = False
        invokes.append(runner.call_contract(path, 'without_attribution_true'))
        expected_results.append(a is not b)

        a = True
        b = True
        invokes.append(runner.call_contract(path, 'without_attribution_false'))
        expected_results.append(a is not b)

        c = True
        d = c
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(c is not d)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_not_identity(self):
        path, _ = self.get_deploy_file_paths('ListNotIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = [1, 2, 3]
        b = a
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(a is not b)

        a = [1, 2, 3]
        b = [1, 2, 3]
        invokes.append(runner.call_contract(path, 'without_attribution'))
        expected_results.append(a is not b)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_none_not_identity_operation(self):
        path, _ = self.get_deploy_file_paths('NoneNotIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 'string'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', b'bytes'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_number_not_identity_operation(self):
        path, _ = self.get_deploy_file_paths('NumNotIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = 1
        b = 2
        invokes.append(runner.call_contract(path, 'without_attribution_true'))
        expected_results.append(a is not b)

        a = 1
        b = 1
        invokes.append(runner.call_contract(path, 'without_attribution_false'))
        expected_results.append(a is not b)

        c = 1
        d = c
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(c is not d)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_not_identity_operation(self):
        path, _ = self.get_deploy_file_paths('StrNotIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = 'unit'
        b = 'test'
        invokes.append(runner.call_contract(path, 'without_attribution_true'))
        expected_results.append(a is not b)

        a = 'unit'
        b = 'unit'
        invokes.append(runner.call_contract(path, 'without_attribution_false'))
        expected_results.append(a is not b)

        c = 'unit'
        d = c
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(c is not d)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_not_identity(self):
        path, _ = self.get_deploy_file_paths('TupleNotIdentity.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = (1, 2, 3)
        b = a
        invokes.append(runner.call_contract(path, 'with_attribution'))
        expected_results.append(a is not b)

        # Python will try conserve memory and will make a and b reference the same position, since Tuples are immutable
        # this will deviate from Neo's expected behavior
        invokes.append(runner.call_contract(path, 'without_attribution'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', True, True))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_builtin_equality_operation(self):
        path, _ = self.get_deploy_file_paths('BuiltinTypeEquality.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.VALUES_ONLY == FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2, 5))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 2, 1, 5))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 5, 1, 2))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 2, 5, 1))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 2, 2))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, False))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', True, True))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_builtin_inequality_operation(self):
        path, _ = self.get_deploy_file_paths('BuiltinTypeInequality.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.VALUES_ONLY != FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 2, 2))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_number_inequality_operation_2(self):
        path = self.get_contract_path('NumInequalityPython2.py')

        with self.assertRaises(SyntaxError):
            self.compile(path)

    # endregion

    # region ObjectEquality

    def test_compare_same_value_argument(self):
        path, _ = self.get_deploy_file_paths('CompareSameValueArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'testing_something', bytes(20)))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_compare_same_value_hard_coded(self):
        path, _ = self.get_deploy_file_paths('CompareSameValueHardCoded.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'testing_something'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_compare_string(self):
        path, _ = self.get_deploy_file_paths('CompareString.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test1', '|'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'test2', '|'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'test3', '|'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'test4', '|'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_equality_with_slice(self):
        path, _ = self.get_deploy_file_paths('ListEqualityWithSlice.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', ['unittest', '123'], 'unittest'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', ['unittest', '123'], '123'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', [], '')
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'unit', 'test'))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'unit'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'unit', 'test'))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 'unit', 'unit'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion
