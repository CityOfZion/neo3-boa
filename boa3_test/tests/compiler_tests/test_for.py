from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestFor(BoaTest):
    default_folder: str = 'test_sc/for_test'

    def test_for_tuple_condition(self):
        jmpif_address = Integer(19).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-22).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH15     # for_sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.PUSH0      # for_index = 0
            + Opcode.JMP        # begin for
            + jmpif_address
            + Opcode.OVER           # x = for_sequence[for_index]
            + Opcode.OVER
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.STLOC1
            + Opcode.LDLOC0         # a = a + x
            + Opcode.LDLOC1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.INC            # for_index = for_index + 1
            + Opcode.DUP        # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('TupleCondition.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(23)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_string_condition(self):
        path, _ = self.get_deploy_file_paths('StringCondition.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append('5')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_iterator_condition(self):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        call_method_address = Integer(39).to_byte_array(min_length=1, signed=True)
        jmpif_address = Integer(20).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-24).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x03'
            + b'\x00'
            + Opcode.CALL       # value = get_iterator()
            + call_method_address
            + Opcode.STLOC0
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC1
            + Opcode.LDLOC0
            + Opcode.DUP        # don't iterate with indexes when using iterator
            + Opcode.JMP        # begin for
            + jmpif_address
            + Opcode.DUP           # x = iterator.value
            + Opcode.SYSCALL
            + Interop.IteratorValue.interop_method_hash
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Struct
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.CONVERT + StackItemType.Array
            + Opcode.STLOC2
            + Opcode.LDLOC1         # a = a + x
            + Opcode.LDLOC2
            + Opcode.ADD
            + Opcode.STLOC1
            + Opcode.DUP        # iterator.next
            + Opcode.SYSCALL
            + Interop.IteratorNext.interop_method_hash
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC1     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('IteratorCondition.py')
        output = self.compile(path)
        self.assertStartsWith(output, expected_output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(6)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_mismatched_type_condition(self):
        path = self.get_contract_path('MismatchedTypeCondition.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_for_no_condition(self):
        path = self.get_contract_path('NoCondition.py')
        with self.assertRaises(SyntaxError):
            output = self.compile(path)

    def test_nested_for(self):
        outer_jmpif_address = Integer(47).to_byte_array(min_length=1, signed=True)
        outer_jmp_address = Integer(-50).to_byte_array(min_length=1, signed=True)

        inner_jmpif_address = Integer(21).to_byte_array(min_length=1, signed=True)
        inner_jmp_address = Integer(-24).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH15     # sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.LDLOC1     # outer_for_sequence = sequence
            + Opcode.PUSH0      # outer_for_index = 0
            + Opcode.JMP
            + outer_jmpif_address
            + Opcode.OVER           # x = outer_for_sequence[outer_for_index]
            + Opcode.OVER
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.STLOC2
            + Opcode.LDLOC1     # inner_for_sequence = sequence
            + Opcode.PUSH0      # inner_for_index = 0
            + Opcode.JMP
            + inner_jmpif_address
            + Opcode.OVER         # y = inner_for_sequence[inner_for_index]
            + Opcode.OVER
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.STLOC3
            + Opcode.LDLOC0         # a = a + x * y
            + Opcode.LDLOC2
            + Opcode.LDLOC3
            + Opcode.MUL
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.INC            # inner_for_index = inner_for_index + 1
            + Opcode.DUP        # if inner_for_index < len(inner_for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end inner_for
            + inner_jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.INC     # outer_for_index = outer_for_index + 1
            + Opcode.DUP        # if outer_for_index < len(outer_for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end outer_for
            + outer_jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('NestedFor.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(529)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_else(self):
        jmpif_address = Integer(19).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-22).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH15     # sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.LDLOC1     # for_sequence = sequence
            + Opcode.PUSH0      # for_index = 0
            + Opcode.JMP
            + jmpif_address
            + Opcode.OVER           # x = for_sequence[for_index]
            + Opcode.OVER
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.STLOC2
            + Opcode.LDLOC0         # a = a + x
            + Opcode.LDLOC2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.INC            # for_index = for_index + 1
            + Opcode.DUP        # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0     # a = a + 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('ForElse.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(24)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_continue(self):
        path, _ = self.get_deploy_file_paths('ForContinue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(20)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_break(self):
        path, _ = self.get_deploy_file_paths('ForBreak.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(6)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_break_else(self):
        path, _ = self.get_deploy_file_paths('ForBreakElse.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(6)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_iterate_dict(self):
        path = self.get_contract_path('ForIterateDict.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_boa2_iteration_test(self):
        path, _ = self.get_deploy_file_paths('IterBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(18)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_iteration_test2(self):
        path, _ = self.get_deploy_file_paths('IterBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(8)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_iteration_test3(self):
        path, _ = self.get_deploy_file_paths('IterBoa2Test3.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(7)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_iteration_test4(self):
        path = self.get_contract_path('IterBoa2Test4.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_boa2_iteration_test5(self):
        path, _ = self.get_deploy_file_paths('IterBoa2Test5.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(51)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_iteration_test6(self):
        path, _ = self.get_deploy_file_paths('IterBoa2Test6.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_iteration_test7(self):
        path, _ = self.get_deploy_file_paths('IterBoa2Test7.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(12)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_iteration_test8(self):
        path, _ = self.get_deploy_file_paths('IterBoa2Test8.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(6)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_pass(self):
        path = self.get_contract_path('ForPass.py')
        output = self.compile(path)
        self.assertIn(Opcode.NOP, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_for_range(self):
        path, _ = self.get_deploy_file_paths('ForWithContractInterface.py')
        path_contract_called, _ = self.get_deploy_file_paths('ForWithContractInterfaceCalled.py')

        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.deploy_contract(path_contract_called)

        invokes.append(runner.call_contract(path, 'main', 3))
        expected_results.append([0, 0, 0])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
