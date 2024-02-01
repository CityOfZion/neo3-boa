from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestList(BoaTest):
    default_folder: str = 'test_sc/list_test'

    def test_list_int_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('IntList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_string_values(self):
        byte_input0 = String('1').to_bytes()
        byte_input1 = String('2').to_bytes()
        byte_input2 = String('3').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = ['1', '2', '3']
            + Integer(len(byte_input2)).to_byte_array()  # '3'
            + byte_input2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array()  # '2'
            + byte_input1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array()  # '1'
            + byte_input0
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('StrList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_bool_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHF      # a = [True, True, False]
            + Opcode.PUSHT
            + Opcode.PUSHT
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BoolList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_variable_values(self):
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
            + Opcode.PUSH3      # d = [a, b, c]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.RET        # return
        )

        path = self.get_contract_path('VariableList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_empty_dict(self):
        expected_output = (
            Opcode.NEWMAP      # return [{}]
            + Opcode.PUSH1      # array length
            + Opcode.PACK
            + Opcode.RET
        )

        path = self.get_contract_path('ListWithEmptyTypedDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_non_sequence_get_value(self):
        path = self.get_contract_path('MismatchedTypeGetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_list_get_value(self):
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

    def test_list_get_value_with_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[-1]
            + Opcode.PUSHM1

            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('GetValueNegativeIndex.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3, 4]))
        expected_results.append(4)
        invokes.append(runner.call_contract(path, 'Main', [5, 3, 2]))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', [])
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_list_get_value_with_variable(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK
            + Opcode.LDARG0     # [0, 1, 2, 3, 4, 5][arg]

            + Opcode.DUP        # will check if number is negative
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('GetValueWithVariable.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append(0)
        invokes.append(runner.call_contract(path, 'main', 2))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_type_hint(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # list length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('TypeHintAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_assign_empty_list(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.NEWARRAY0
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('EmptyListAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_set_into_list_slice(self):
        path = self.get_contract_path('SetListIntoListSlice.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_list_set_value(self):
        path = self.get_contract_path('SetValue.py')
        self.assertCompilerNotLogs(CompilerWarning.NameShadowing, path)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3, 4]))
        expected_results.append([1, 2, 3, 4])
        invokes.append(runner.call_contract(path, 'Main', [5, 3, 2]))
        expected_results.append([1, 3, 2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', [])
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_list_set_value_with_negative_index(self):
        path = self.get_contract_path('SetValueNegativeIndex.py')
        self.assertCompilerNotLogs(CompilerWarning.NameShadowing, path)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3, 4]))
        expected_results.append([1, 2, 3, 1])
        invokes.append(runner.call_contract(path, 'Main', [5, 3, 2]))
        expected_results.append([5, 3, 1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', [])
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_non_sequence_set_value(self):
        path = self.get_contract_path('MismatchedTypeSetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_list_index_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeListIndex.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_array_boa2_test1(self):
        path, _ = self.get_deploy_file_paths('ArrayBoa2Test1.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_array_test(self):
        path, _ = self.get_deploy_file_paths('ArrayBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(6)

        invokes.append(runner.call_contract(path, 'main', 2))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', 4))
        expected_results.append(8)

        invokes.append(runner.call_contract(path, 'main', 8))
        expected_results.append(9)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_array_test2(self):
        path, _ = self.get_deploy_file_paths('ArrayBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(b'\xa0')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_array_test3(self):
        path, _ = self.get_deploy_file_paths('ArrayBoa2Test3.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append([1, 2, 3])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_of_list(self):
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

        path = self.get_contract_path('ListOfList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [[1, 2], [3, 4]]))
        expected_results.append(1)

        runner.call_contract(path, 'Main', [])
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

        runner.call_contract(path, 'Main', [[], [1, 2], [3, 4]])
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_boa2_demo1(self):
        path, _ = self.get_deploy_file_paths('Demo1Boa2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'add', 1, 3))
        expected_results.append(7)

        invokes.append(runner.call_contract(path, 'main', 'add', 2, 3))
        expected_results.append(8)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # region TestSlicing

    def test_list_slicing(self):
        path, _ = self.get_deploy_file_paths('ListSlicingLiteralValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_start_larger_than_ending(self):
        path, _ = self.get_deploy_file_paths('ListSlicingStartLargerThanEnding.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_with_variables(self):
        path, _ = self.get_deploy_file_paths('ListSlicingVariableValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_negative_start(self):
        path, _ = self.get_deploy_file_paths('ListSlicingNegativeStart.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_negative_end(self):
        path, _ = self.get_deploy_file_paths('ListSlicingNegativeEnd.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_start_omitted(self):
        path, _ = self.get_deploy_file_paths('ListSlicingStartOmitted.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1, 2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_omitted(self):
        path, _ = self.get_deploy_file_paths('ListSlicingOmitted.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1, 2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_end_omitted(self):
        path, _ = self.get_deploy_file_paths('ListSlicingEndOmitted.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([2, 3, 4, 5])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_positive_index_opcode(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK  # [0, 1, 2, 3, 4, 5]
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.PUSH2  # lower index

            + Opcode.DUP  # checks if lower index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.PUSH3  # upper index

            + Opcode.OVER  # checks if upper index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.SWAP
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.SWAP
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.NEWARRAY0  # starts getting the subarray

        )
        path = self.get_contract_path('ListSlicingLiteralValues.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    def test_list_slicing_negative_lower_index_opcode(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK  # [0, 1, 2, 3, 4, 5]
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.PUSH4
            + Opcode.NEGATE  # lower index

            + Opcode.OVER   # fix negative index
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.DUP  # checks if lower index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.OVER
            + Opcode.SIZE  # upper index

            + Opcode.NEWARRAY0  # starts getting the subarray
        )
        path = self.get_contract_path('ListSlicingNegativeStart.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    def test_list_slicing_negative_upper_index_opcode(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK  # [0, 1, 2, 3, 4, 5]
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.PUSH4
            + Opcode.NEGATE  # upper index

            + Opcode.OVER  # fix negative index
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.DUP  # checks if upper index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.PUSH0  # lower index
            + Opcode.SWAP

            + Opcode.NEWARRAY0  # starts getting the subarray
        )
        path = self.get_contract_path('ListSlicingNegativeEnd.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    def test_list_slicing_variable_index_opcode(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK  # [0, 1, 2, 3, 4, 5]
            + Opcode.LDARG0  # lower index

            + Opcode.DUP     # checks if variable is negative
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)

            + Opcode.OVER  # fix negative index
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.DUP  # checks if lower index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.LDARG1  # upper index

            + Opcode.DUP  # checks if variable is negative
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(6).to_byte_array(min_length=1)

            + Opcode.PUSH2  # fix negative index
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.ADD

            + Opcode.OVER  # checks if upper index is out of bounds on the array
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.SWAP
            + Opcode.DROP
            + Opcode.PUSH0
            + Opcode.SWAP
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.MIN

            + Opcode.NEWARRAY0  # starts getting the subarray
        )
        path = self.get_contract_path('ListSlicingWithVariables.py')
        output = self.compile(path)
        self.assertIn(expected_output, output)

    def test_list_slicing_with_stride(self):
        path, _ = self.get_deploy_file_paths('ListSlicingWithStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[2:5:2]
        invokes.append(runner.call_contract(path, 'literal_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6:5:2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6:-1:2]
        invokes.append(runner.call_contract(path, 'negative_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999:5:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999:5:2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999:999:2]
        invokes.append(runner.call_contract(path, 'really_high_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        x = 2
        y = 4
        expected_result = a[x:y:2]
        invokes.append(runner.call_contract(path, 'with_variables', x, y))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('ListSlicingWithNegativeStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[2:5:-1]
        invokes.append(runner.call_contract(path, 'literal_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6:5:-1]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999:5:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999:5:-1]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[0:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_values'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_omitted_with_stride(self):
        path, _ = self.get_deploy_file_paths('ListSlicingOmittedWithStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[::2]
        invokes.append(runner.call_contract(path, 'omitted_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:5:2]
        invokes.append(runner.call_contract(path, 'omitted_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5, 6]
        expected_result = a[2::2]
        invokes.append(runner.call_contract(path, 'omitted_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6::2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999::2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999::2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_slicing_omitted_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('ListSlicingOmittedWithNegativeStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[::-2]
        invokes.append(runner.call_contract(path, 'omitted_values'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:5:-2]
        invokes.append(runner.call_contract(path, 'omitted_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5, 6]
        expected_result = a[2::-2]
        invokes.append(runner.call_contract(path, 'omitted_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-6::-2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:-1:-2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[-999::-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:-999:-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[999::-2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(expected_result)

        a = [0, 1, 2, 3, 4, 5]
        expected_result = a[:999:-2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region TestAppend

    def test_list_append_int_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.append(4)
            + Opcode.PUSH4
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('AppendIntValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_append_any_value(self):
        four = String('4').to_bytes(min_length=1)

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.append(4)
            + Opcode.PUSHDATA1
            + Integer(len(four)).to_byte_array()
            + four
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('AppendAnyValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3, '4'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_append_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeAppendValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_append_with_builtin(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # list.append(a, 4)
            + Opcode.PUSH4
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('AppendIntWithBuiltin.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_append_with_builtin_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeAppendWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_boa2_list_append_test(self):
        path, _ = self.get_deploy_file_paths('AppendBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append([6, 7])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_append_in_class_variable(self):
        path, _ = self.get_deploy_file_paths('AppendInClassVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append([1, 2, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region TestClear

    def test_list_clear(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x02'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.clear()
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(9).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSHDATA1
            + Integer(0).to_byte_array(min_length=1)
            + Opcode.CONVERT
            + Type.bytearray.stack_item
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CLEARITEMS
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('ClearList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_reverse(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.reverse()
            + Opcode.REVERSEITEMS
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('ReverseList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_boa2_list_reverse_test(self):
        path, _ = self.get_deploy_file_paths('ReverseBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(['blah', 4, 2, 1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region TestExtend

    def test_list_extend_tuple_value(self):
        path, _ = self.get_deploy_file_paths('ExtendTupleValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3, 4, 5, 6])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_extend_any_value(self):
        path, _ = self.get_deploy_file_paths('ExtendAnyValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3, '4', 5, 1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_extend_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeExtendValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_extend_mismatched_iterable_value_type(self):
        path = self.get_contract_path('MismatchedTypeExtendTupleValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_extend_with_builtin(self):
        path, _ = self.get_deploy_file_paths('ExtendWithBuiltin.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3, 4, 5, 6])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_extend_with_builtin_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeExtendWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region TestPop

    def test_list_pop(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop()
            + Opcode.PUSHM1
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = self.get_contract_path('PopList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths('PopList.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = (runner.call_contract(path, 'pop_test'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual([1, 2, 3, 4, 5].pop(), invoke.result)

    def test_list_pop_without_assignment(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop()
            + Opcode.PUSHM1
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = self.get_contract_path('PopListWithoutAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths('PopListWithoutAssignment.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = (runner.call_contract(path, 'pop_test'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        list_ = [1, 2, 3, 4, 5]
        list_.pop()
        self.assertEqual(list_, invoke.result)

    def test_list_pop_literal_argument(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop(2)
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = self.get_contract_path('PopListLiteralArgument.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths('PopListLiteralArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = (runner.call_contract(path, 'pop_test'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual([1, 2, 3, 4, 5].pop(2), invoke.result)

    def test_list_pop_literal_negative_argument(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop(-2)
            + Opcode.PUSH2
            + Opcode.NEGATE
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = self.get_contract_path('PopListLiteralNegativeArgument.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths('PopListLiteralNegativeArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = (runner.call_contract(path, 'pop_test'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual([1, 2, 3, 4, 5].pop(-2), invoke.result)

    def test_list_pop_literal_variable_argument(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x01'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop(arg0)
            + Opcode.LDARG0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = self.get_contract_path('PopListVariableArgument.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths('PopListVariableArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [1, 2, 3, 4, 5]
        index = 0
        invokes.append(runner.call_contract(path, 'pop_test', index))
        expected_results.append(list_.pop(index))

        list_ = [1, 2, 3, 4, 5]
        index = len(list_) - 1
        invokes.append(runner.call_contract(path, 'pop_test', index))
        expected_results.append(list_.pop(index))

        list_ = [1, 2, 3, 4, 5]
        index = -len(list_)
        invokes.append(runner.call_contract(path, 'pop_test', index))
        expected_results.append(list_.pop(index))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        list_ = [1, 2, 3, 4, 5]
        index = 99999
        runner.call_contract(path, 'pop_test', index)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)
        self.assertRaises(IndexError, list_.pop, index)

        list_ = [1, 2, 3, 4, 5]
        index = -99999
        runner.call_contract(path, 'pop_test', index)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)
        self.assertRaises(IndexError, list_.pop, index)

    def test_list_pop_mismatched_type_argument(self):
        path = self.get_contract_path('PopListMismatchedTypeArgument.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_pop_mismatched_type_result(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH5      # a = [1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a.pop(2)
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.OVER
            + Opcode.OVER
            + Opcode.PICKITEM
            + Opcode.REVERSE3
            + Opcode.SWAP
            + Opcode.REMOVE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = self.get_contract_path('PopListMismatchedTypeResult.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'pop_test'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_pop_too_many_arguments(self):
        path = self.get_contract_path('PopListTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_boa2_list_remove_test(self):
        path, _ = self.get_deploy_file_paths('RemoveBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append([16, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region TestInsert

    def test_list_insert_int_value(self):
        path, _ = self.get_deploy_file_paths('InsertIntValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 4, 3])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_insert_any_value(self):
        path, _ = self.get_deploy_file_paths('InsertAnyValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [1, 2, 3]
        pos = 0
        value = '0'
        invokes.append(runner.call_contract(path, 'Main', list_, pos, value))
        list_.insert(pos, value)
        expected_results.append(list_)

        list_ = [1, 2, 3]
        pos = 1
        value = '1'
        invokes.append(runner.call_contract(path, 'Main', list_, pos, value))
        list_.insert(pos, value)
        expected_results.append(list_)

        list_ = [1, 2, 3]
        pos = 3
        value = '4'
        invokes.append(runner.call_contract(path, 'Main', list_, pos, value))
        list_.insert(pos, value)
        expected_results.append(list_)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_insert_int_negative_index(self):
        path, _ = self.get_deploy_file_paths('InsertIntNegativeIndex.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 4, 2, 3])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_insert_int_with_builtin(self):
        path, _ = self.get_deploy_file_paths('InsertIntWithBuiltin.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 4, 3])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region TestRemove

    def test_list_remove_value(self):
        path, _ = self.get_deploy_file_paths('RemoveValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3, 4], 3))
        expected_results.append([1, 2, 4])

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3, 2, 3], 3))
        expected_results.append([1, 2, 2, 3])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', [1, 2, 3, 4], 6)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_list_remove_int_value(self):
        path, _ = self.get_deploy_file_paths('RemoveIntValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([10, 30])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_remove_int_with_builtin(self):
        path, _ = self.get_deploy_file_paths('RemoveIntWithBuiltin.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([10, 20])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region TestCopy

    def test_list_copy(self):
        path, _ = self.get_deploy_file_paths('Copy.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'copy_list', [1, 2, 3, 4], 5))
        expected_results.append([[1, 2, 3, 4],
                                 [1, 2, 3, 4, 5]
                                 ])

        invokes.append(runner.call_contract(path, 'copy_list', ['list', 'unit', 'test'], 'copy'))
        expected_results.append([['list', 'unit', 'test'],
                                 ['list', 'unit', 'test', 'copy']
                                 ])

        invokes.append(runner.call_contract(path, 'copy_list', [True, False], True))
        expected_results.append([[True, False],
                                 [True, False, True]
                                 ])

        invokes.append(runner.call_contract(path, 'attribution', [1, 2, 3, 4], 5))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'attribution', ['list', 'unit', 'test'], 'copy'))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'attribution', [True, False], True))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_int_list_copy(self):
        path, _ = self.get_deploy_file_paths('CopyInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'copy_int_list', [1, 2, 3, 4], 5))
        expected_results.append([[1, 2, 3, 4],
                                 [1, 2, 3, 4, 5]])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_list_copy(self):
        path, _ = self.get_deploy_file_paths('CopyStr.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'copy_str_list', ['list', 'unit', 'test'], 'copy'))
        expected_results.append([['list', 'unit', 'test'],
                                 ['list', 'unit', 'test', 'copy']
                                 ])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_list_copy(self):
        path, _ = self.get_deploy_file_paths('CopyBool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'copy_bool_list', [True, False], True))
        expected_results.append([[True, False],
                                 [True, False, True]
                                 ])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_copy_builtin_call(self):
        path, _ = self.get_deploy_file_paths('CopyListBuiltinCall.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'copy_list', [1, 2, 3, 4], 5))
        expected_results.append([[1, 2, 3, 4],
                                 [1, 2, 3, 4, 5]
                                 ])

        invokes.append(runner.call_contract(path, 'copy_list', ['list', 'unit', 'test'], 'copy'))
        expected_results.append([['list', 'unit', 'test'],
                                 ['list', 'unit', 'test', 'copy']])

        invokes.append(runner.call_contract(path, 'copy_list', [True, False], True))
        expected_results.append([[True, False],
                                 [True, False, True]])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region TestIndex

    def test_list_index(self):
        path, _ = self.get_deploy_file_paths('IndexList.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [1, 2, 3, 4]
        value = 3
        start = 0
        end = 4
        invokes.append(runner.call_contract(path, 'main', list_, value, start, end))
        expected_results.append(list_.index(value, start, end))

        list_ = [1, 2, 3, 4]
        value = 3
        start = 2
        end = 4
        invokes.append(runner.call_contract(path, 'main', list_, value, start, end))
        expected_results.append(list_.index(value, start, end))

        list_ = [1, 2, 3, 4]
        value = 3
        start = 0
        end = -1
        invokes.append(runner.call_contract(path, 'main', list_, value, start, end))
        expected_results.append(list_.index(value, start, end))

        list_ = [1, 2, 3, 4]
        value = 2
        start = 0
        end = 99
        invokes.append(runner.call_contract(path, 'main', list_, value, start, end))
        expected_results.append(list_.index(value, start, end))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        from boa3.internal.model.builtin.builtin import Builtin
        runner.call_contract(path, 'main', [1, 2, 3, 4], 3, 3, 4)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

        runner.call_contract(path, 'main', [1, 2, 3, 4], 3, 4, -1)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

        runner.call_contract(path, 'main', [1, 2, 3, 4], 3, 0, -99)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

    def test_list_index_end_default(self):
        path, _ = self.get_deploy_file_paths('IndexListEndDefault.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [1, 2, 3, 4]
        value = 3
        start = 0
        invokes.append(runner.call_contract(path, 'main', list_, value, start))
        expected_results.append(list_.index(value, start))

        list_ = [1, 2, 3, 4]
        value = 2
        start = -10
        invokes.append(runner.call_contract(path, 'main', list_, value, start))
        expected_results.append(list_.index(value, start))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        from boa3.internal.model.builtin.builtin import Builtin
        runner.call_contract(path, 'main', [1, 2, 3, 4], 2, 99)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

        runner.call_contract(path, 'main', [1, 2, 3, 4], 4, -1)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{Builtin.SequenceIndex.exception_message}$')

    def test_list_index_defaults(self):
        path, _ = self.get_deploy_file_paths('IndexListDefaults.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [1, 2, 3, 4]
        value = 3
        invokes.append(runner.call_contract(path, 'main', list_, value))
        expected_results.append(list_.index(value))

        list_ = [1, 2, 3, 4]
        value = 1
        invokes.append(runner.call_contract(path, 'main', list_, value))
        expected_results.append(list_.index(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_index_int(self):
        path, _ = self.get_deploy_file_paths('IndexListInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [1, 2, 3, 4]
        value = 3
        invokes.append(runner.call_contract(path, 'main', list_, value))
        expected_results.append(list_.index(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_index_str(self):
        path, _ = self.get_deploy_file_paths('IndexListStr.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = ['unit', 'test', 'neo3-boa']
        value = 'test'
        invokes.append(runner.call_contract(path, 'main', list_, value))
        expected_results.append(list_.index(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_index_bool(self):
        path, _ = self.get_deploy_file_paths('IndexListBool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [True, True, False]
        value = False
        invokes.append(runner.call_contract(path, 'main', list_, value))
        expected_results.append(list_.index(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region TestSort

    def test_list_sort(self):
        path = self.get_contract_path('SortList.py')
        self.compile_and_save(path, debug=True)
        path, _ = self.get_deploy_file_paths('SortList.py')

        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        sorted_list = [5, 4, 3, 2, 6, 1]
        sorted_list.sort()
        invokes.append(runner.call_contract(path, 'sort_test'))
        expected_results.append(sorted_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_sort_with_args(self):
        # list.sort arguments must be used as kwargs
        path = self.get_contract_path('SortArgsList.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_list_sort_reverse_true(self):
        path, _ = self.get_deploy_file_paths('SortReverseTrueList.py')

        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        sorted_list = [5, 4, 3, 2, 6, 1]
        sorted_list.sort(reverse=True)
        invokes.append(runner.call_contract(path, 'sort_test'))
        expected_results.append(sorted_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_sort_reverse_false(self):
        path, _ = self.get_deploy_file_paths('SortReverseFalseList.py')

        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        sorted_list = [5, 4, 3, 2, 6, 1]
        sorted_list.sort(reverse=False)
        invokes.append(runner.call_contract(path, 'sort_test'))
        expected_results.append(sorted_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_sort_key(self):
        path = self.get_contract_path('SortKeyList.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_list_any_sort(self):
        path = self.get_contract_path('SortListAny.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_list_of_list_sort(self):
        path = self.get_contract_path('SortListOfList.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    # endregion

    # region TestComprehension

    def test_list_comprehension_str(self):
        path = self.get_contract_path('ListComprehensionStr.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    # endregion

    # region TestDel

    def test_del_list_item(self):
        path = self.get_contract_path('DelItem.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    # endregion
