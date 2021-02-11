import unittest

from boa3.boa3 import Boa3
from boa3.exception.CompilerError import InternalError, MismatchedTypes, UnresolvedOperation
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


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
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_bool_values(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = (True, True, False)
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BoolTuple.py')
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_get_value(self):
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

    def test_non_sequence_get_value(self):
        path = self.get_contract_path('MismatchedTypeGetValue.py')
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_tuple_set_value(self):
        path = self.get_contract_path('SetValue.py')
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_non_sequence_set_value(self):
        path = self.get_contract_path('MismatchedTypeSetValue.py')
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_tuple_index_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeTupleIndex.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    @unittest.skip("get values from inner arrays is not working as expected")
    def test_tuple_of_tuple(self):
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

        path = self.get_contract_path('TupleOfTuple.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', ((1, 2), (3, 4)))
        self.assertEqual(1, result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', ())
        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', ((), (1, 2), (3, 4)))

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
        result = self.run_smart_contract(engine, path, 'Main', 'op', (1, 2, 3, 4))
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', 'op', ('a', False))
        self.assertEqual('a', result)

        with self.assertRaises(TestExecutionException, msg=self.VALUE_IS_OUT_OF_RANGE_MSG):
            self.run_smart_contract(engine, path, 'Main', 'op', ())

    def test_tuple_slicing(self):
        path = self.get_contract_path('TupleSlicingLiteralValues.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2], result)

    def test_tuple_slicing_start_larger_than_ending(self):
        path = self.get_contract_path('TupleSlicingStartLargerThanEnding.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_tuple_slicing_with_variables(self):
        path = self.get_contract_path('TupleSlicingVariableValues.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2], result)

    def test_tuple_slicing_negative_start(self):
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
            + Opcode.LDLOC0     # return a[-4:]
            + Opcode.DUP
            + Opcode.SIZE       # slice end
            + Opcode.PUSH4
            + Opcode.NEGATE
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.SWAP       # get slice
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
        path = self.get_contract_path('TupleSlicingNegativeStart.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2, 3, 4, 5], result)

    def test_tuple_slicing_negative_end(self):
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
        path = self.get_contract_path('TupleSlicingNegativeEnd.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1], result)

    def test_tuple_slicing_start_omitted(self):
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

        path = self.get_contract_path('TupleSlicingStartOmitted.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1, 2], result)

    def test_tuple_slicing_omitted(self):
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
        path = self.get_contract_path('TupleSlicingOmitted.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1, 2, 3, 4, 5], result)

    def test_tuple_slicing_end_omitted(self):
        path = self.get_contract_path('TupleSlicingEndOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([2, 3, 4, 5], result)

    def test_tuple_slicing_omitted_stride(self):
        path = self.get_contract_path('TupleSlicingWithStride.py')
        self.assertCompilerLogs(InternalError, path)

    def test_tuple_slicing_omitted_with_stride(self):
        path = self.get_contract_path('TupleSlicingOmittedWithStride.py')
        self.assertCompilerLogs(InternalError, path)
