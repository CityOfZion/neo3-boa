from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestMultipleExpressions(BoaTest):
    default_folder: str = 'test_sc'

    def test_multiple_arithmetic_expressions(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x02'
            + Opcode.PUSH1      # d = 1
            + Opcode.STLOC0
            + Opcode.PUSH2      # e = 2
            + Opcode.STLOC1
            + Opcode.LDARG0     # c = a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return c
            + Opcode.RET
        )

        path = self.get_contract_path('arithmetic_test', 'MultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2))
        expected_results.append(3)
        invokes.append(runner.call_contract(path, 'Main', 5, -7))
        expected_results.append(-2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_multiple_relational_expressions(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x02'
            + Opcode.LDARG0     # is_equal = a == b
            + Opcode.LDARG1
            + Opcode.NUMEQUAL
            + Opcode.STLOC0
            + Opcode.LDARG0     # is_greater = a > b
            + Opcode.LDARG1
            + Opcode.GT
            + Opcode.STLOC1
            + Opcode.LDARG0     # is_less = a < b
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.STLOC2
            + Opcode.LDLOC0     # return not is_equal
            + Opcode.NOT
            + Opcode.RET
        )

        path = self.get_contract_path('relational_test', 'MultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1, 2))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', 5, -7))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', -4, -4))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_multiple_logic_expressions(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x03'
            + Opcode.LDARG0     # a1 = a and b
            + Opcode.LDARG1
            + Opcode.BOOLAND
            + Opcode.STLOC0
            + Opcode.LDARG1     # b1 = b and c
            + Opcode.LDARG2
            + Opcode.BOOLAND
            + Opcode.STLOC1
            + Opcode.LDARG0     # c1 = a or c
            + Opcode.LDARG2
            + Opcode.BOOLOR
            + Opcode.STLOC2
            + Opcode.LDLOC0     # return a1 and not b1 and c1
            + Opcode.LDLOC1
            + Opcode.NOT
            + Opcode.BOOLAND
            + Opcode.LDLOC2
            + Opcode.BOOLAND
            + Opcode.RET
        )

        path = self.get_contract_path('logical_test', 'MultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, False, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', False, True, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', False, False, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', True, True, False))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_multiple_tuple_expressions(self):
        a = String('a').to_bytes()
        b = String('b').to_bytes()
        c = String('c').to_bytes()
        d = String('d').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x01'
            + Opcode.PUSHDATA1  # items2 = ('a', 'b', 'c', 'd')
            + Integer(len(d)).to_byte_array() + d
            + Opcode.PUSHDATA1
            + Integer(len(c)).to_byte_array() + c
            + Opcode.PUSHDATA1
            + Integer(len(b)).to_byte_array() + b
            + Opcode.PUSHDATA1
            + Integer(len(a)).to_byte_array() + a
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.STLOC0     # items2 = array
            + Opcode.LDARG0     # value = items1[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.STLOC1
            + Opcode.LDLOC1     # count = value + len(items2)
            + Opcode.LDLOC0
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return count
            + Opcode.RET
        )

        path = self.get_contract_path('tuple_test', 'MultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2]))
        expected_results.append(5)
        invokes.append(runner.call_contract(path, 'Main', [-5, -7]))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_multiple_list_expressions(self):
        one = String('1').to_bytes()
        four = String('4').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x01'
            + Opcode.PUSHDATA1  # items2 = [False, '1', 2, 3, '4']
            + Integer(len(four)).to_byte_array() + four
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSHDATA1
            + Integer(len(one)).to_byte_array() + one
            + Opcode.PUSHF
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0     # items2 = array
            + Opcode.LDARG0     # value = items1[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.STLOC1
            + Opcode.LDLOC1     # count = value + len(items2)
            + Opcode.LDLOC0
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return count
            + Opcode.RET
        )

        path = self.get_contract_path('list_test', 'MultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [2, 1]))
        expected_results.append(7)
        invokes.append(runner.call_contract(path, 'Main', [-7, 5]))
        expected_results.append(-2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
