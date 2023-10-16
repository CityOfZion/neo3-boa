from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestTuple(BoaTest):
    default_folder: str = 'test_sc/tuple_test'

    def test_tuple_int_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = (1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('IntTuple.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_string_values(self):
        byte_input0 = String('1').to_bytes()
        byte_input1 = String('2').to_bytes()
        byte_input2 = String('3').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = ('1', '2', '3')
            + Integer(len(byte_input2)).to_byte_array()
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array()
            + byte_input0
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('StrTuple.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_bool_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHF      # a = (True, True, False)
            + Opcode.PUSHT
            + Opcode.PUSHT
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BoolTuple.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_variable_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH1      # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2      # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH3      # c = 3
            + Opcode.STLOC2
            + Opcode.PUSH3      # d = (a, b, c)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.RET        # return
        )

        path = self.get_contract_path('VariableTuple.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_assign_empty_tuple(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.NEWARRAY0
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('EmptyTupleAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_get_value(self):
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

    def test_non_sequence_get_value(self):
        path = self.get_contract_path('MismatchedTypeGetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_tuple_set_value(self):
        path = self.get_contract_path('SetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_non_sequence_set_value(self):
        path = self.get_contract_path('MismatchedTypeSetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_tuple_index_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeTupleIndex.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_tuple_of_tuple(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0][0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('TupleOfTuple.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', ((1, 2), (3, 4))))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', ())
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

        runner.call_contract(path, 'Main', ((), (1, 2), (3, 4)))
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_tuple_slicing(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingLiteralValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_start_larger_than_ending(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingStartLargerThanEnding.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_with_variables(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingVariableValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_negative_start(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingNegativeStart.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_negative_end(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingNegativeEnd.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_start_omitted(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingStartOmitted.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1, 2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_omitted(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5      # a = (0, 1, 2, 3, 4, 5)
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:]
            + Opcode.UNPACK
            + Opcode.PACK
            + Opcode.RET        # return
        )
        path = self.get_contract_path('TupleSlicingOmitted.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1, 2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_end_omitted(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingEndOmitted.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_with_stride(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingWithStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[2:5:2]
        invokes.append(runner.call_contract(path, 'literal_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6:5:2]
        invokes.append(runner.call_contract(path, 'negative_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6:-1:2]
        invokes.append(runner.call_contract(path, 'negative_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999:5:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999:5:2]
        invokes.append(runner.call_contract(path, 'really_high_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999:999:2]
        invokes.append(runner.call_contract(path, 'really_high_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingWithNegativeStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[2:5:-1]
        invokes.append(runner.call_contract(path, 'literal_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6:5:-1]
        invokes.append(runner.call_contract(path, 'negative_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999:5:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999:5:-1]
        invokes.append(runner.call_contract(path, 'really_high_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[0:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_omitted_with_stride(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingOmittedWithStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[::2]
        invokes.append(runner.call_contract(path, 'omitted_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:5:2]
        invokes.append(runner.call_contract(path, 'omitted_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[2::2]
        invokes.append(runner.call_contract(path, 'omitted_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6::2]
        invokes.append(runner.call_contract(path, 'negative_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999::2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999::2]
        invokes.append(runner.call_contract(path, 'really_high_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_slicing_omitted_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('TupleSlicingOmittedWithNegativeStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[::-2]
        invokes.append(runner.call_contract(path, 'omitted_values',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:5:-2]
        invokes.append(runner.call_contract(path, 'omitted_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[2::-2]
        invokes.append(runner.call_contract(path, 'omitted_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-6::-2]
        invokes.append(runner.call_contract(path, 'negative_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:-1:-2]
        invokes.append(runner.call_contract(path, 'negative_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[-999::-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:-999:-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[999::-2]
        invokes.append(runner.call_contract(path, 'really_high_start',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        a = (0, 1, 2, 3, 4, 5)
        expected_result = a[:999:-2]
        invokes.append(runner.call_contract(path, 'really_high_end',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_index(self):
        path, _ = self.get_deploy_file_paths('IndexTuple.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_ = (1, 2, 3, 4)
        value = 3
        start = 0
        end = 4
        invokes.append(runner.call_contract(path, 'main', tuple_, value, start, end))
        expected_results.append(tuple_.index(value, start, end))

        tuple_ = (1, 2, 3, 4)
        value = 3
        start = 2
        end = 4
        invokes.append(runner.call_contract(path, 'main', tuple_, value, start, end))
        expected_results.append(tuple_.index(value, start, end))

        tuple_ = (1, 2, 3, 4)
        value = 3
        start = 0
        end = -1
        invokes.append(runner.call_contract(path, 'main', tuple_, value, start, end))
        expected_results.append(tuple_.index(value, start, end))

        tuple_ = (1, 2, 3, 4)
        value = 2
        start = 0
        end = 99
        invokes.append(runner.call_contract(path, 'main', tuple_, value, start, end))
        expected_results.append(tuple_.index(value, start, end))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        from boa3.internal.model.builtin.builtin import Builtin
        runner.call_contract(path, 'main', (1, 2, 3, 4), 3, 3, 4)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

        runner.call_contract(path, 'main', (1, 2, 3, 4), 3, 4, -1)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

        runner.call_contract(path, 'main', (1, 2, 3, 4), 3, 0, -99)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

    def test_tuple_index_end_default(self):
        path, _ = self.get_deploy_file_paths('IndexTupleEndDefault.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_ = (1, 2, 3, 4)
        value = 3
        start = 0
        invokes.append(runner.call_contract(path, 'main', tuple_, value, start))
        expected_results.append(tuple_.index(value, start))

        tuple_ = (1, 2, 3, 4)
        value = 2
        start = -10
        invokes.append(runner.call_contract(path, 'main', tuple_, value, start))
        expected_results.append(tuple_.index(value, start))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        from boa3.internal.model.builtin.builtin import Builtin
        runner.call_contract(path, 'main', (1, 2, 3, 4), 2, 99)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

        runner.call_contract(path, 'main', (1, 2, 3, 4), 4, -1)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

    def test_tuple_index_defaults(self):
        path, _ = self.get_deploy_file_paths('IndexTupleDefaults.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_ = (1, 2, 3, 4)
        value = 3
        invokes.append(runner.call_contract(path, 'main', tuple_, value))
        expected_results.append(tuple_.index(value))

        tuple_ = (1, 2, 3, 4)
        value = 1
        invokes.append(runner.call_contract(path, 'main', tuple_, value))
        expected_results.append(tuple_.index(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
