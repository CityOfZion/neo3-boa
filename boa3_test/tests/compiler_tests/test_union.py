from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestUnion(BoaTest):
    default_folder: str = 'test_sc/union_test'

    def test_union_return(self):
        integer = Integer(42).to_byte_array()
        string = String('42').to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHINT8 + integer  # return 42
            + Opcode.RET
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.RET        # return
        )

        path = self.get_contract_path('UnionReturn.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append(42)

        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append('42')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_union_variable_reassign(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH2      # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH2      # b = a
            + Opcode.STLOC1
            + Opcode.PUSH2      # c = [a, b]
            + Opcode.PUSH2
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.LDLOC2     # b = c
            + Opcode.STLOC1
            + Opcode.RET        # return
        )

        path = self.get_contract_path('UnionVariableReassign.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_union_variable_argument(self):
        path, _ = self.get_deploy_file_paths('UnionVariableArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'unittest'))
        expected_results.append('string')

        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append('boolean')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_union_isinstance_validation(self):
        path, _ = self.get_deploy_file_paths('UnionIsInstanceValidation.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'unittest'))
        expected_results.append('unittest')

        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append('boolean')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_union_int_none(self):
        path, _ = self.get_deploy_file_paths('UnionIntNone.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
