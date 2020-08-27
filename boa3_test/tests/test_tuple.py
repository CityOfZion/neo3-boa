from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, UnresolvedOperation
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestTuple(BoaTest):

    def test_tuple_int_values(self):
        path = '%s/boa3_test/test_sc/tuple_test/IntTuple.py' % self.dirname

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
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_string_values(self):
        path = '%s/boa3_test/test_sc/tuple_test/StrTuple.py' % self.dirname
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
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_bool_values(self):
        path = '%s/boa3_test/test_sc/tuple_test/BoolTuple.py' % self.dirname

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
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_variable_values(self):
        path = '%s/boa3_test/test_sc/tuple_test/VariableTuple.py' % self.dirname

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
            + Opcode.LDLOC2     # d = (a, b, c)
            + Opcode.LDLOC1
            + Opcode.LDLOC0
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_assign_empty_tuple(self):
        path = '%s/boa3_test/test_sc/tuple_test/EmptyTupleAssignment.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.NEWARRAY0
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_get_value(self):
        path = '%s/boa3_test/test_sc/tuple_test/GetValue.py' % self.dirname

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_non_sequence_get_value(self):
        path = '%s/boa3_test/test_sc/tuple_test/MismatchedTypeGetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_tuple_set_value(self):
        path = '%s/boa3_test/test_sc/tuple_test/SetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_non_sequence_set_value(self):
        path = '%s/boa3_test/test_sc/tuple_test/MismatchedTypeSetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_tuple_index_mismatched_type(self):
        path = '%s/boa3_test/test_sc/tuple_test/MismatchedTypeTupleIndex.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_tuple_of_tuple(self):
        path = '%s/boa3_test/test_sc/tuple_test/TupleOfTuple.py' % self.dirname

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_nep5_main(self):
        path = '%s/boa3_test/test_sc/tuple_test/Nep5Main.py' % self.dirname

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_slicing(self):
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
            + Opcode.LDLOC0     # return a[2:3]
            + Opcode.PUSH2
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PUSH3
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
                + Opcode.PUSH2      # get slice
                + Opcode.PICK
                + Opcode.SIZE
                + Opcode.MIN        # slice end
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
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingLiteralValues.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_slicing_with_variables(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH2      # a1 = 2
            + Opcode.STLOC0
            + Opcode.PUSH3      # a2 = 3
            + Opcode.STLOC1
            + Opcode.PUSH5      # a = [0, 1, 2, 3, 4, 5]
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return a[a1:a2]
            + Opcode.LDLOC0
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.LDLOC1
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
                + Opcode.PUSH2      # get slice
                + Opcode.PICK
                + Opcode.SIZE
                + Opcode.MIN        # slice end
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
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingVariableValues.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
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
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingNegativeStart.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.PUSH4          # slice end
            + Opcode.NEGATE
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
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
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingNegativeEnd.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingStartOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_slicing_end_omitted(self):
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
            + Opcode.LDLOC0     # return a[2:]
            + Opcode.DUP
            + Opcode.SIZE       # slice end
            + Opcode.PUSH2
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
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
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingEndOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_slicing_omitted_stride(self):
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingWithStride.py' % self.dirname
        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)

    def test_tuple_slicing_omitted_with_stride(self):
        path = '%s/boa3_test/test_sc/tuple_test/TupleSlicingOmittedWithStride.py' % self.dirname
        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)
