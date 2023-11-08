from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestRange(BoaTest):
    default_folder: str = 'test_sc/range_test'

    RANGE_ERROR_MESSAGE = String('range() arg 3 must not be zero').to_bytes()

    def test_range_given_length(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.PUSH1      # range(arg0)
            + Opcode.PUSH0
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = self.get_contract_path('RangeGivenLen.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'range_example', 5))
        expected_results.append([0, 1, 2, 3, 4])
        invokes.append(runner.call_contract(path, 'range_example', 10))
        expected_results.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        invokes.append(runner.call_contract(path, 'range_example', 0))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_given_start(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH1      # range(arg0, arg1)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = self.get_contract_path('RangeGivenStart.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'range_example', 2, 6))
        expected_results.append([2, 3, 4, 5])
        invokes.append(runner.call_contract(path, 'range_example', -10, 0))
        expected_results.append([-10, -9, -8, -7, -6, -5, -4, -3, -2, -1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_given_step(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG2     # range(arg0, arg1, arg2)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = self.get_contract_path('RangeGivenStep.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'range_example', 2, 10, 3))
        expected_results.append([2, 5, 8])
        invokes.append(runner.call_contract(path, 'range_example', -2, 10, 3))
        expected_results.append([-2, 1, 4, 7])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_parameter_mismatched_type(self):
        path = self.get_contract_path('RangeParameterMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_range_as_sequence(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH1      # range(arg0, arg1)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = self.get_contract_path('RangeExpectedSequence.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'range_example', 2, 6))
        expected_results.append([2, 3, 4, 5])
        invokes.append(runner.call_contract(path, 'range_example', -10, 0))
        expected_results.append([-10, -9, -8, -7, -6, -5, -4, -3, -2, -1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_mismatched_type(self):
        path = self.get_contract_path('RangeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_range_too_few_parameters(self):
        path = self.get_contract_path('RangeTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_range_too_many_parameters(self):
        path = self.get_contract_path('RangeTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_range_get_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('GetValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3, 4]))
        expected_results.append(1)
        invokes.append(runner.call_contract(path, 'Main', [5, 3, 2]))
        expected_results.append(5)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', [])
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_range_set_value(self):
        path = self.get_contract_path('SetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_range_slicing(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingLiteralValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_start_larger_than_ending(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingStartLargerThanEnding.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_with_variables(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingVariableValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_negative_start(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingNegativeStart.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_negative_end(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingNegativeEnd.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_start_omitted(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingStartOmitted.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1, 2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_omitted(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingOmitted.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1, 2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_end_omitted(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingEndOmitted.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_with_stride(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingWithStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = range(6)
        expected_result = a[2:5:2]
        invokes.append(runner.call_contract(path, 'literal_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[2:5:2]
        invokes.append(runner.call_contract(path, 'literal_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-6:5:2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[0:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-6:-1:2]
        invokes.append(runner.call_contract(path, 'negative_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-999:5:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[0:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-999:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[999:5:2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[0:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[999:999:2]
        invokes.append(runner.call_contract(path, 'really_high_values'))
        expected_results.append(list(expected_result))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingWithNegativeStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = range(6)
        expected_result = a[2:5:-1]
        invokes.append(runner.call_contract(path, 'literal_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-6:5:-1]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[0:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-6:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-999:5:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[0:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-999:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[999:5:-1]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[0:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[999:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_values'))
        expected_results.append(list(expected_result))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_omitted_with_stride(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingOmittedWithStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = range(6)
        expected_result = a[::2]
        invokes.append(runner.call_contract(path, 'omitted_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[:5:2]
        invokes.append(runner.call_contract(path, 'omitted_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[2::2]
        invokes.append(runner.call_contract(path, 'omitted_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-6::2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-999::2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[999::2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(list(expected_result))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_slicing_omitted_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('RangeSlicingOmittedWithNegativeStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = range(6)
        expected_result = a[::-2]
        invokes.append(runner.call_contract(path, 'omitted_values'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[:5:-2]
        invokes.append(runner.call_contract(path, 'omitted_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[2::-2]
        invokes.append(runner.call_contract(path, 'omitted_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-6::-2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[:-1:-2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[-999::-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[:-999:-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[999::-2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(list(expected_result))

        a = range(6)
        expected_result = a[:999:-2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(list(expected_result))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_range_test(self):
        path, _ = self.get_deploy_file_paths('RangeBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(list(range(100, 120)))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_range_index(self):
        path = self.get_contract_path('IndexRange.py')
        # TODO: change when index() with only one argument is implemented for range #2kq1y13
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)
