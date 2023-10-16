from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.builtin.builtin import Builtin
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestException(BoaTest):
    default_folder: str = 'test_sc/exception_test'

    EXCEPTION_EMPTY_MESSAGE = String(Builtin.Exception.default_message).to_bytes()

    def test_raise_exception_empty_message(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(14).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise Exception
            + Integer(len(self.EXCEPTION_EMPTY_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.EXCEPTION_EMPTY_MESSAGE
            + Opcode.THROW
            + Opcode.RET
        )

        path = self.get_contract_path('RaiseExceptionEmptyMessage.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.call_contract(path, 'test_raise', 10)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.call_contract(path, 'test_raise', -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

    def test_raise_exception_with_message(self):
        exception_message = String('raised an exception').to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(24).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise Exception('raised an exception')
            + Integer(len(exception_message)).to_byte_array(signed=True, min_length=1)
            + exception_message
            + Opcode.THROW
            + Opcode.RET
        )

        path = self.get_contract_path('RaiseExceptionWithMessage.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.call_contract(path, 'test_raise', 10)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.call_contract(path, 'test_raise', -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

    def test_raise_exception_without_call(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(14).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise Exception
            + Integer(len(self.EXCEPTION_EMPTY_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.EXCEPTION_EMPTY_MESSAGE
            + Opcode.THROW
            + Opcode.RET
        )

        path = self.get_contract_path('RaiseExceptionWithoutCall.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.call_contract(path, 'test_raise', 10)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.call_contract(path, 'test_raise', -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

    def test_raise_variable_exception(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1  # x = Exception
            + Integer(len(self.EXCEPTION_EMPTY_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.EXCEPTION_EMPTY_MESSAGE
            + Opcode.STLOC0
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0         # raise x
            + Opcode.THROW
            + Opcode.RET
        )

        path = self.get_contract_path('RaiseVariableException.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.call_contract(path, 'test_raise', 10)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.call_contract(path, 'test_raise', -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

    def test_raise_exception_variable_message(self):
        message = 'raised an exception'
        exception_message = String(message).to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1  # x = 'raised an exception'
            + Integer(len(exception_message)).to_byte_array(signed=True, min_length=1)
            + exception_message
            + Opcode.STLOC0
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(24).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise Exception(x)
            + Integer(len(exception_message)).to_byte_array(signed=True, min_length=1)
            + exception_message
            + Opcode.THROW
            + Opcode.RET
        )

        path = self.get_contract_path('RaiseExceptionVariableMessage.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.call_contract(path, 'test_raise', 10)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.call_contract(path, 'test_raise', -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, message)

    def test_raise_specific_exception(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(14).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise ValueError
            + Integer(len(self.EXCEPTION_EMPTY_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.EXCEPTION_EMPTY_MESSAGE
            + Opcode.THROW
            + Opcode.RET
        )

        path = self.get_contract_path('RaiseSpecificException.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.call_contract(path, 'test_raise', 10)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.call_contract(path, 'test_raise', -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.UNHANDLED_EXCEPTION_MSG_PREFIX}')

    def test_raise_mismatched_type(self):
        path = self.get_contract_path('RaiseMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_try_except_without_exception(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.TRY        # try:
            + Integer(7).to_byte_array(signed=True, min_length=1)  # jmp to exception
            + Integer(0).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDARG0         # x = arg
            + Opcode.STLOC0
            + Opcode.JMP        # except:
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0          # x = 0
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(2).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('TryExceptWithoutException.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test_try_except', 10))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'test_try_except', -110))
        expected_results.append(-110)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_try_except_base_exception(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.TRY        # try:
            + Integer(7).to_byte_array(signed=True, min_length=1)  # jmp to exception
            + Integer(0).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDARG0         # x = arg
            + Opcode.STLOC0
            + Opcode.JMP        # except BaseException:
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0          # x = 0
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(2).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('TryExceptBaseException.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test_try_except', 10))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'test_try_except', -110))
        expected_results.append(-110)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_try_except_specific_exception(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.TRY        # try:
            + Integer(7).to_byte_array(signed=True, min_length=1)  # jmp to exception
            + Integer(0).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDARG0         # x = arg
            + Opcode.STLOC0
            + Opcode.JMP        # except ValueError:
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0          # x = 0
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(2).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('TryExceptSpecificException.py')
        output = self.assertCompilerLogs(CompilerWarning.UsingSpecificException, path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test_try_except', 10))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'test_try_except', -110))
        expected_results.append(-110)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_try_except_with_name(self):
        path = self.get_contract_path('TryExceptWithName.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_try_except_finally(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH4
            + Opcode.DIV
            + Opcode.STLOC0
            + Opcode.TRY        # try:
            + Integer(9).to_byte_array(signed=True, min_length=1)   # jmp to exception
            + Integer(15).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDLOC0         # x += arg
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.JMP        # except ValueError:
            + Integer(6).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.LDLOC0         # x = -x
            + Opcode.NEGATE
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # finally
            + Opcode.PUSH2          # x *= 2
            + Opcode.MUL
            + Opcode.STLOC0
            + Opcode.ENDFINALLY
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('TryExceptFinally.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test_try_except', 10))
        expected_results.append(24)
        invokes.append(runner.call_contract(path, 'test_try_except', -110))
        expected_results.append(-274)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_try_except_else(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.TRY        # try:
            + Integer(7).to_byte_array(signed=True, min_length=1)  # jmp to exception
            + Integer(0).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDARG0         # x = arg
            + Opcode.STLOC0
            + Opcode.JMP        # except BaseException:
            + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0          # x = 0
            + Opcode.STLOC0
            + Opcode.JMP        # else:
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.LDARG0         # x = -arg
            + Opcode.NEGATE
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(2).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('TryExceptElse.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test_try_except', 10))
        expected_results.append(-10)
        invokes.append(runner.call_contract(path, 'test_try_except', -110))
        expected_results.append(110)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_try_except_else_finally(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH4
            + Opcode.DIV
            + Opcode.STLOC0
            + Opcode.TRY        # try:
            + Integer(9).to_byte_array(signed=True, min_length=1)   # jmp to exception
            + Integer(21).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDLOC0         # x += arg
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.JMP        # except ValueError:
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.LDLOC0         # x = -x
            + Opcode.NEGATE
            + Opcode.STLOC0
            + Opcode.JMP        # else:
            + Integer(6).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0         # x += arg
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # finally
            + Opcode.PUSH2          # x *= 2
            + Opcode.MUL
            + Opcode.STLOC0
            + Opcode.ENDFINALLY
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('TryExceptElseFinally.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test_try_except', 10))
        expected_results.append(44)
        invokes.append(runner.call_contract(path, 'test_try_except', -110))
        expected_results.append(-494)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
