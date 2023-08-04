from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestWhile(BoaTest):
    default_folder: str = 'test_sc/while_test'

    def test_while_constant_condition(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.JMP        # begin while
            + jmpif_address
            + Opcode.LDLOC0     # a = a + 2
            + Opcode.PUSH2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.PUSHF
            + Opcode.JMPIF      # end while False
            + jmp_address
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
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_while_variable_condition(self):
        jmpif_address = Integer(12).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-11).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # condition = a < value
            + Opcode.LDARG0
            + Opcode.LT
            + Opcode.STLOC1
            + Opcode.JMP        # begin while
            + jmpif_address
            + Opcode.LDLOC0     # a = a + 2
            + Opcode.PUSH2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # condition = a < value * 2
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.MUL
            + Opcode.LT
            + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.JMPIF      # end while arg0
            + jmp_address
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

        invokes.append(runner.call_contract(path, 'Main', -2))
        expected_results.append(0)
        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'Main', 8))
        expected_results.append(16)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_while_mismatched_type_condition(self):
        path = self.get_contract_path('MismatchedTypeCondition.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_while_no_condition(self):
        path = self.get_contract_path('NoCondition.py')
        with self.assertRaises(SyntaxError):
            output = self.compile(path)

    def test_nested_while(self):
        path, _ = self.get_deploy_file_paths('NestedWhile.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(8)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_while_else(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.JMP        # begin while
            + jmpif_address
            + Opcode.LDLOC0     # a = a + 2
            + Opcode.PUSH2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.PUSHF
            + Opcode.JMPIF      # end while False
            + jmp_address
            + Opcode.LDLOC0     # else
            + Opcode.PUSH1          # a = a + 1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('WhileElse.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_while_relational_condition(self):
        jmpif_address = Integer(10).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-11).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # b = 0
            + Opcode.STLOC1
            + Opcode.JMP        # begin while
            + jmpif_address
            + Opcode.LDLOC0     # a = a + 2
            + Opcode.PUSH2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC1     # b = b + 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIF      # end while b < 10
            + jmp_address
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

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(20)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_while_multiple_relational_condition(self):
        jmpif_address = Integer(10).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-15).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # b = 0
            + Opcode.STLOC1
            + Opcode.JMP        # begin while
            + jmpif_address
            + Opcode.LDLOC0     # a = a + 2
            + Opcode.PUSH2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC1     # b = b + 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.PUSH10
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.BOOLAND
            + Opcode.JMPIF      # end while b < 10 < arg1
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('MultipleRelationalCondition.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', '', 1))
        expected_results.append(0)
        invokes.append(runner.call_contract(path, 'Main', '', 10))
        expected_results.append(0)
        invokes.append(runner.call_contract(path, 'Main', '', 100))
        expected_results.append(20)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_while_continue(self):
        path, _ = self.get_deploy_file_paths('WhileContinue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(20)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_while_break(self):
        path, _ = self.get_deploy_file_paths('WhileBreak.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(6)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_while_test(self):
        path, _ = self.get_deploy_file_paths('WhileBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(24)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_while_test1(self):
        path, _ = self.get_deploy_file_paths('WhileBoa2Test1.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(6)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_while_test2(self):
        path, _ = self.get_deploy_file_paths('WhileBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(6)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_while_interop_condition(self):
        path, _ = self.get_deploy_file_paths('WhileWithInteropCondition.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'deploy'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'test_end_while_jump'))
        expected_results.append(True)

        contract = invokes[0].invoke.contract
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # test notifications inserted into the code for validating if the code flow is correct
        notifications = runner.get_events('notify', origin=contract)
        contract_hash = contract.script_hash
        self.assertEqual(2, len(notifications))

        self.assertEqual(1, len(notifications[0].arguments))
        self.assertIsInstance(notifications[0].arguments[0], list)
        self.assertEqual(4, len(notifications[0].arguments[0]))
        token, executing_script_hash, fee_receiver, fee_amount = notifications[0].arguments[0]
        if isinstance(fee_receiver, str):
            fee_receiver = String(fee_receiver).to_bytes()
        if isinstance(fee_amount, str):
            fee_amount = String(fee_amount).to_bytes()
        if isinstance(fee_amount, bytes):
            fee_amount = Integer.from_bytes(fee_amount)

        self.assertEqual(constants.GAS_SCRIPT, token)
        self.assertEqual(contract_hash, executing_script_hash)
        self.assertEqual(bytes(20), fee_receiver)
        self.assertEqual(10, fee_amount)

        self.assertEqual(1, len(notifications[1].arguments))
        self.assertIsInstance(notifications[1].arguments[0], list)
        self.assertEqual(4, len(notifications[1].arguments[0]))
        token, executing_script_hash, fee_receiver, fee_amount = notifications[1].arguments[0]
        if isinstance(fee_receiver, str):
            fee_receiver = String(fee_receiver).to_bytes()
        if isinstance(fee_amount, str):
            fee_amount = String(fee_amount).to_bytes()
        if isinstance(fee_amount, bytes):
            fee_amount = Integer.from_bytes(fee_amount)

        self.assertEqual(constants.NEO_SCRIPT, token)
        self.assertEqual(contract_hash, executing_script_hash)
        self.assertEqual(bytes(20), fee_receiver)
        self.assertEqual(20, fee_amount)
