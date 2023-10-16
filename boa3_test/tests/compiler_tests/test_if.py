from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestIf(BoaTest):
    default_folder: str = 'test_sc/if_test'

    def test_if_constant_condition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSHT
            + Opcode.JMPIFNOT   # if True
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2     # a = a + 2
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('ConstantCondition.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_variable_condition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # a = a + 2
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('VariableCondition.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_no_condition(self):
        path = self.get_contract_path('IfWithoutCondition.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    def test_if_no_body(self):
        path = self.get_contract_path('IfWithoutBody.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    def test_nested_if(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH0      # c = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # d = c
            + Opcode.STLOC1
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(13).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # c = c + 2
            + Opcode.STLOC0
            + Opcode.LDARG1
            + Opcode.JMPIFNOT   # if arg1
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH3      # d = d + 3
            + Opcode.STLOC1
            + Opcode.PUSH2      # c = c + d
            + Opcode.LDLOC1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return c
            + Opcode.RET
        )

        path = self.get_contract_path('NestedIf.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, True))
        expected_results.append(5)
        invokes.append(runner.call_contract(path, 'Main', True, False))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'Main', False, True))
        expected_results.append(0)
        invokes.append(runner.call_contract(path, 'Main', False, False))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_else(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # a = a + 2
            + Opcode.STLOC0
            + Opcode.JMP        # else
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH10     # a = 10
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('IfElse.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_else_no_body(self):
        path = self.get_contract_path('ElseWithoutBody.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    def test_if_elif(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH2      # a = a + 2
            + Opcode.STLOC0
            + Opcode.JMP
            + Integer(7).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # elif arg0
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.PUSH10     # a = 10
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('IfElif.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_elif_no_condition(self):
        path = self.get_contract_path('ElifWithoutCondition.py')
        with self.assertRaises(SyntaxError):
            output = self.compile(path)

    def test_elif_no_body(self):
        path = self.get_contract_path('ElifWithoutBody.py')
        with self.assertRaises(SyntaxError):
            output = self.compile(path)

    def test_if_relational_condition(self):
        jmp_address = Integer(4).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIFNOT   # if c < 10
            + jmp_address
            + Opcode.PUSH2      # a = a + 2
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('RelationalCondition.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_multiple_branches(self):
        twenty = Integer(20).to_byte_array()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT       # if arg0 < 0
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH0              # a = 0
            + Opcode.STLOC0
            + Opcode.JMP
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.PUSH5
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 5
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH5              # a = 5
            + Opcode.STLOC0
            + Opcode.JMP
            + Integer(23).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 10
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH10             # a = 10
            + Opcode.STLOC0
            + Opcode.JMP
            + Integer(14).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.PUSH15
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 15
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH15             # a = 15
            + Opcode.STLOC0
            + Opcode.JMP            # else
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.PUSHINT8 + twenty  # a = 20
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('MultipleBranches.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', -10))
        expected_results.append(0)
        invokes.append(runner.call_contract(path, 'Main', 2))
        expected_results.append(5)
        invokes.append(runner.call_contract(path, 'Main', 7))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'Main', 13))
        expected_results.append(15)
        invokes.append(runner.call_contract(path, 'Main', 17))
        expected_results.append(20)
        invokes.append(runner.call_contract(path, 'Main', 23))
        expected_results.append(20)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_expression_variable_condition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # a = 2 if arg0 else 3
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # 2
            + Opcode.JMP        # else
            + Integer(3).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH3      # 3
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('IfExpVariableCondition.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_expression_without_else_branch(self):
        path = self.get_contract_path('IfExpWithoutElse.py')
        with self.assertRaises(SyntaxError):
            output = self.compile(path)

    def test_if_expression_mismatched_types(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # a = 2 if condition else None
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # 2
            + Opcode.JMP        # else
            + Integer(3).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHNULL   # None
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedIfExp.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_inner_if_else(self):
        path, _ = self.get_deploy_file_paths('InnerIfElse.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 4, 3, 2, 1))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', 4, 3, 1, 2))
        expected_results.append(8)

        invokes.append(runner.call_contract(path, 'main', 4, 1, 2, 3))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'main', 1, 2, 4, 3))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', 1, 2, 3, 4))
        expected_results.append(11)

        invokes.append(runner.call_contract(path, 'main', 1, 3, 2, 4))
        expected_results.append(22)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_is_instance_condition(self):
        path, _ = self.get_deploy_file_paths('IfIsInstanceCondition.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'example', 4))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'example', '123'))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'example', -70))
        expected_results.append(-70)

        invokes.append(runner.call_contract(path, 'example', True))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_else_is_instance_condition(self):
        path, _ = self.get_deploy_file_paths('IfElseIsInstanceCondition.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'example', 4))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'example', '123'))
        expected_results.append(-1)

        invokes.append(runner.call_contract(path, 'example', -70))
        expected_results.append(-70)

        invokes.append(runner.call_contract(path, 'example', True))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_else_is_instance_condition_with_union_variable(self):
        path, _ = self.get_deploy_file_paths('IfElseIsInstanceConditionWithUnionVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'example', 4,
                                            expected_result_type=bytes))
        expected_results.append(b'\x04')

        invokes.append(runner.call_contract(path, 'example', '123',
                                            expected_result_type=bytes))
        expected_results.append(b'123')

        invokes.append(runner.call_contract(path, 'example', -70,
                                            expected_result_type=bytes))
        expected_results.append(Integer(-70).to_byte_array())

        invokes.append(runner.call_contract(path, 'example', True,
                                            expected_result_type=bytes))
        expected_results.append(b'\x01')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_else_multiple_is_instance_condition_with_union_variable(self):
        path, _ = self.get_deploy_file_paths('IfElseMultipleIsInstanceConditionWithUnionVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'example', 4))
        expected_results.append(16)

        invokes.append(runner.call_contract(path, 'example', [b'123456', b'789']))
        expected_results.append(6)

        invokes.append(runner.call_contract(path, 'example', -70))
        expected_results.append(4900)

        invokes.append(runner.call_contract(path, 'example', []))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'example', b'True'))
        expected_results.append(4)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_variable_in_if_scopes(self):
        path, _ = self.get_deploy_file_paths('VariablesInIfScopes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 2))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 3))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 4))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 5))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 6))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 7))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 8))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_compare_test0int(self):
        path, _ = self.get_deploy_file_paths('CompareBoa2Test0int.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 2, 4))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', 4, 2))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', 2, 2))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_compare_test0str(self):
        path, _ = self.get_deploy_file_paths('CompareBoa2Test0str.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'b', 'a'))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', 'a', 'b'))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_compare_test1(self):
        path, _ = self.get_deploy_file_paths('CompareBoa2Test1.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, 2, 3, 4))
        expected_results.append(11)

        invokes.append(runner.call_contract(path, 'main', 1, 2, 4, 3))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', 1, 4, 3, 5))
        expected_results.append(22)

        invokes.append(runner.call_contract(path, 'main', 4, 1, 5, 3))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', 9, 1, 3, 5))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'main', 9, 5, 3, 5))
        expected_results.append(8)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_compare_test2(self):
        path, _ = self.get_deploy_file_paths('CompareBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 2, 2))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 2, 3))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_op_call_test(self):
        path, _ = self.get_deploy_file_paths('OpCallBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'omin', 4, 4))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', 'omin', -4, 4))
        expected_results.append(-4)

        invokes.append(runner.call_contract(path, 'main', 'omin', 16, 0))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', 'omax', 4, 4))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', 'omax', -4, 4))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', 'omax', 16, 0))
        expected_results.append(16)

        from boa3.internal.neo.cryptography import sha256, hash160
        from boa3.internal.neo.vm.type.String import String
        invokes.append(runner.call_contract(path, 'main', 'sha256', 'abc', 4))
        expected_results.append(sha256(String('abc').to_bytes()))

        invokes.append(runner.call_contract(path, 'main', 'hash160', 'abc', 4))
        expected_results.append(hash160(String('abc').to_bytes()))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_test_many_elif(self):
        path, _ = self.get_deploy_file_paths('TestManyElifBoa2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', 3))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', 16))
        expected_results.append(17)

        invokes.append(runner.call_contract(path, 'main', 22))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_with_inner_while(self):
        path, _ = self.get_deploy_file_paths('IfWithInnerWhile.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append('{[]}')

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append('{[value1,value2,value3]}')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_with_inner_for(self):
        path, _ = self.get_deploy_file_paths('IfWithInnerFor.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append('{[]}')

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append('{[value1,value2,value3]}')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_implicit_boolean(self):
        path, _ = self.get_deploy_file_paths('IfImplicitBoolean.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 'unit_test'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', ''))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', b'unit test'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', b''))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', [1, 2, 3, 4]))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', []))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', {'a': 1, 'b': 2}))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', {}))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_implicit_boolean_literal(self):
        path, _ = self.get_deploy_file_paths('IfImplicitBooleanLiteral.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(4)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_pass(self):
        path = self.get_contract_path('IfPass.py')
        output = self.compile(path)
        self.assertIn(Opcode.NOP, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_else_pass(self):
        path = self.get_contract_path('ElsePass.py')
        output = self.compile(path)
        self.assertIn(Opcode.NOP, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append(5)
        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_else_pass(self):
        path = self.get_contract_path('IfElsePass.py')
        output = self.compile(path)
        n_nop = 0
        for byte_value in output:
            if byte_value == int.from_bytes(Opcode.NOP.value, 'little'):
                n_nop += 1
        self.assertEqual(n_nop, 2)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_is_none(self):
        path, _ = self.get_deploy_file_paths('IfIsNone.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 123))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_is_not_none(self):
        path, _ = self.get_deploy_file_paths('IfIsNotNone.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 123))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_if_is_none_type_check(self):
        path, _ = self.get_deploy_file_paths('IfIsNoneTypeCheck.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_input = bytes(20)
        invokes.append(runner.call_contract(path, 'main', test_input,
                                            expected_result_type=bytes))
        expected_results.append(test_input)

        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
