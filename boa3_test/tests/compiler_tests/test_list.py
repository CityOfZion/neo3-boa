import unittest

from boa3.boa3 import Boa3
from boa3.exception import CompilerError, CompilerWarning
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


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
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_bool_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = [True, True, False]
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BoolList.py')
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
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
            + Opcode.DUP
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

        path = self.get_contract_path('GetValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3, 4])
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', [5, 3, 2])
        self.assertEqual(5, result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', [])

    def test_list_get_value_with_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[-1]
            + Opcode.PUSHM1
            + Opcode.DUP
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

        path = self.get_contract_path('GetValueNegativeIndex.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3, 4])
        self.assertEqual(4, result)
        result = self.run_smart_contract(engine, path, 'Main', [5, 3, 2])
        self.assertEqual(2, result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', [])

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
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_set_value(self):
        path = self.get_contract_path('SetValue.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3, 4])
        self.assertEqual([1, 2, 3, 4], result)
        result = self.run_smart_contract(engine, path, 'Main', [5, 3, 2])
        self.assertEqual([1, 3, 2], result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', [])

    def test_list_set_value_with_negative_index(self):
        path = self.get_contract_path('SetValueNegativeIndex.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3, 4])
        self.assertEqual([1, 2, 3, 1], result)
        result = self.run_smart_contract(engine, path, 'Main', [5, 3, 2])
        self.assertEqual([5, 3, 1], result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', [])

    def test_non_sequence_set_value(self):
        path = self.get_contract_path('MismatchedTypeSetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_list_index_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeListIndex.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_array_boa2_test1(self):
        path = self.get_contract_path('ArrayBoa2Test1.py')
        Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_boa2_array_test(self):
        path = self.get_contract_path('ArrayBoa2Test.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 0)
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual(6, result)

        result = self.run_smart_contract(engine, path, 'main', 2)
        self.assertEqual(3, result)

        result = self.run_smart_contract(engine, path, 'main', 4)
        self.assertEqual(8, result)

        result = self.run_smart_contract(engine, path, 'main', 8)
        self.assertEqual(9, result)

    def test_boa2_array_test2(self):
        path = self.get_contract_path('ArrayBoa2Test2.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(b'\xa0', result)

    def test_boa2_array_test3(self):
        path = self.get_contract_path('ArrayBoa2Test3.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual([1, 2, 3], result)

    @unittest.skip("get values from inner arrays is not working as expected")
    def test_list_of_list(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0][0]
            + Opcode.PUSH0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.PUSH0
            + Opcode.DUP
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

        path = self.get_contract_path('ListOfList.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', [[1, 2], [3, 4]])
        self.assertEqual(1, result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', [])
        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', [[], [1, 2], [3, 4]])

    def test_nep5_main(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG1     # args[0]
            + Opcode.PUSH0
            + Opcode.DUP
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

        path = self.get_contract_path('Nep5Main.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'op', [1, 2, 3, 4])
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', 'op', ['a', False])
        self.assertEqual('a', result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', 'op', [])

    def test_boa2_demo1(self):
        path = self.get_contract_path('Demo1Boa2.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'add', 1, 3)
        self.assertEqual(7, result)

        result = self.run_smart_contract(engine, path, 'main', 'add', 2, 3)
        self.assertEqual(8, result)

    # region TestSlicing

    def test_list_slicing(self):
        path = self.get_contract_path('ListSlicingLiteralValues.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2], result)

    def test_list_slicing_start_larger_than_ending(self):
        path = self.get_contract_path('ListSlicingStartLargerThanEnding.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_list_slicing_with_variables(self):
        path = self.get_contract_path('ListSlicingVariableValues.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2], result)

    def test_list_slicing_negative_start(self):
        path = self.get_contract_path('ListSlicingNegativeStart.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2, 3, 4, 5], result)

    def test_list_slicing_negative_end(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5      # a = [0, 1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:-4]
            + Opcode.PUSH4
            + Opcode.NEGATE         # slice end
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH0
            + Opcode.SWAP
            + Opcode.NEWARRAY0  # slice
            + Opcode.PUSH2
            + Opcode.PICK       # index
            + Opcode.JMP        # while index < end
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.DUP            # if index >= slice start
            + Opcode.PUSH4
            + Opcode.PICK
            + Opcode.GE
            + Opcode.JMPIFNOT
            + Integer(25).to_byte_array(min_length=1)
            + Opcode.OVER               # slice.append(array[index])
            + Opcode.PUSH5
            + Opcode.PICK
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.INC            # index += 1
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.LT
            + Opcode.JMPIF          # end while index < slice end
            + Integer(-34).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.REVERSE4
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )
        path = self.get_contract_path('ListSlicingNegativeEnd.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1], result)

    def test_list_slicing_start_omitted(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5      # a = [0, 1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:3]
            + Opcode.PUSH3          # slice end
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH0
            + Opcode.SWAP
            + Opcode.NEWARRAY0  # slice
            + Opcode.PUSH2
            + Opcode.PICK       # index
            + Opcode.JMP        # while index < end
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.DUP            # if index >= slice start
            + Opcode.PUSH4
            + Opcode.PICK
            + Opcode.GE
            + Opcode.JMPIFNOT
            + Integer(25).to_byte_array(min_length=1)
            + Opcode.OVER               # slice.append(array[index])
            + Opcode.PUSH5
            + Opcode.PICK
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.INC            # index += 1
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.LT
            + Opcode.JMPIF          # end while index < slice end
            + Integer(-34).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.REVERSE4
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )
        path = self.get_contract_path('ListSlicingStartOmitted.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1, 2], result)

    def test_list_slicing_omitted(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5      # a = [0, 1, 2, 3, 4, 5]
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
        path = self.get_contract_path('ListSlicingOmitted.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1, 2, 3, 4, 5], result)

    def test_list_slicing_end_omitted(self):
        path = self.get_contract_path('ListSlicingEndOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2, 3, 4, 5], result)

    def test_list_slicing_omitted_stride(self):
        path = self.get_contract_path('ListSlicingWithStride.py')
        self.assertCompilerLogs(CompilerError.InternalError, path)

    def test_list_slicing_omitted_with_stride(self):
        path = self.get_contract_path('ListSlicingOmittedWithStride.py')
        self.assertCompilerLogs(CompilerError.InternalError, path)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4], result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, '4'], result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4], result)

    def test_list_append_with_builtin_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeAppendWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_boa2_list_append_test(self):
        path = self.get_contract_path('AppendBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual([6, 7], result)

    # endregion

    # region TestClear

    def test_list_clear(self):
        path = self.get_contract_path('ClearList.py')

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_reverse(self):
        path = self.get_contract_path('ReverseList.py')

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_boa2_list_reverse_test(self):
        path = self.get_contract_path('ReverseBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(['blah', 4, 2, 1], result)

    # endregion

    # region TestExtend

    def test_list_extend_tuple_value(self):
        path = self.get_contract_path('ExtendTupleValue.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_list_extend_any_value(self):
        path = self.get_contract_path('ExtendAnyValue.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, '4', 5, 1], result)

    def test_list_extend_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeExtendValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_extend_mismatched_iterable_value_type(self):
        path = self.get_contract_path('MismatchedTypeExtendTupleValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_extend_with_builtin(self):
        path = self.get_contract_path('ExtendWithBuiltin.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'pop_test')
        self.assertEqual(3, result)

    def test_list_pop_too_many_arguments(self):
        path = self.get_contract_path('PopListTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_boa2_list_remove_test(self):
        path = self.get_contract_path('RemoveBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual([16, 3, 4], result)

    # endregion

    # region TestInsert

    def test_list_insert_int_value(self):
        path = self.get_contract_path('InsertIntValue.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 4, 3], result)

    def test_list_insert_any_value(self):
        path = self.get_contract_path('InsertAnyValue.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, '4', 2, 3], result)

    def test_list_insert_int_negative_index(self):
        path = self.get_contract_path('InsertIntNegativeIndex.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 4, 2, 3], result)

    def test_list_insert_int_with_builtin(self):
        path = self.get_contract_path('InsertIntWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 4, 3], result)

    # endregion

    # region TestRemove

    def test_list_remove_value(self):
        path = self.get_contract_path('RemoveValue.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3, 4], 3)
        self.assertEqual([1, 2, 4], result)

        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3, 2, 3], 3)
        self.assertEqual([1, 2, 2, 3], result)

        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', [1, 2, 3, 4], 6)

    def test_list_remove_int_value(self):
        path = self.get_contract_path('RemoveIntValue.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([10, 30], result)

    def test_list_remove_int_with_builtin(self):
        path = self.get_contract_path('RemoveIntWithBuiltin.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([10, 20], result)

    # endregion
