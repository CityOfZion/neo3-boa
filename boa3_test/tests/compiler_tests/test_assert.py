from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


class TestAssert(BoaTest):
    default_folder: str = 'test_sc/assert_test'

    def test_assert_unary_boolean_operation(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0     # assert not a
            + Opcode.NOT
            + Opcode.ASSERT
            + Opcode.LDARG1     # return b
            + Opcode.RET
        )

        path = self.get_contract_path('AssertUnaryOperation.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', False, 10))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', True, 20)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_assert_binary_boolean_operation(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0     # assert a != b
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('AssertBinaryOperation.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10, 20))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', 20, 20)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_assert_with_message(self):
        path, _ = self.get_deploy_file_paths('AssertWithMessage.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        runner.deploy_contract(path)
        runner.update_contracts()
        self.assertEqual(VMState.NONE, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.cli_log, self.BAD_SCRIPT_EXCEPTION_MSG)

    def test_assert_with_bytes_message(self):
        path, _ = self.get_deploy_file_paths('AssertWithBytesMessage.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        runner.deploy_contract(path)
        runner.update_contracts()
        self.assertEqual(VMState.NONE, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.cli_log, self.BAD_SCRIPT_EXCEPTION_MSG)

    def test_assert_with_int_message(self):
        path = self.get_contract_path('AssertWithIntMessage.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_assert_with_bool_message(self):
        path = self.get_contract_path('AssertWithBoolMessage.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_assert_with_list_message(self):
        path = self.get_contract_path('AssertWithListMessage.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_assert_with_str_var_message(self):
        path, _ = self.get_deploy_file_paths('AssertWithStrVarMessage.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        runner.deploy_contract(path)
        runner.update_contracts()
        self.assertEqual(VMState.NONE, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.cli_log, self.BAD_SCRIPT_EXCEPTION_MSG)

    def test_assert_with_str_function_message(self):
        path, _ = self.get_deploy_file_paths('AssertWithStrFunctionMessage.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        runner.deploy_contract(path)
        runner.update_contracts()
        self.assertEqual(VMState.NONE, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.cli_log, self.BAD_SCRIPT_EXCEPTION_MSG)

    def test_assert_int(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('AssertInt.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'Main', -10))
        expected_results.append(-10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', 0)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_assert_str(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('AssertStr.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'unittest'))
        expected_results.append('unittest')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', '')
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_assert_bytes(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('AssertBytes.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', b'unittest',
                                            expected_result_type=bytes))
        expected_results.append(b'unittest')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', b'')
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_assert_list(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.LDARG0     # return len(a)
            + Opcode.SIZE
            + Opcode.RET
        )

        path = self.get_contract_path('AssertList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3]))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', [])
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_assert_dict(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.LDARG0     # return len(a)
            + Opcode.SIZE
            + Opcode.RET
        )

        path = self.get_contract_path('AssertDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', {1: 2, 2: 5}))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', {})
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_assert_any(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Array
            + Opcode.JMPIF + Integer(12).to_byte_array(signed=True, min_length=1)
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Map
            + Opcode.JMPIF + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Struct
            + Opcode.JMPIFNOT + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.RET
        )

        path = self.get_contract_path('AssertAny.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_throw_test(self):
        path, _ = self.get_deploy_file_paths('ThrowBoa2Test.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', 4)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)
