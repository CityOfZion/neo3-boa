from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, UnresolvedOperation
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestList(BoaTest):

    def test_list_int_values(self):
        path = '%s/boa3_test/example/list_test/IntList.py' % self.dirname

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
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_string_values(self):
        path = '%s/boa3_test/example/list_test/StrList.py' % self.dirname
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_bool_values(self):
        path = '%s/boa3_test/example/list_test/BoolList.py' % self.dirname

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_variable_values(self):
        path = '%s/boa3_test/example/list_test/VariableList.py' % self.dirname

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
            + Opcode.LDLOC2     # d = [a, b, c]
            + Opcode.LDLOC1
            + Opcode.LDLOC0
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_non_sequence_get_value(self):
        path = '%s/boa3_test/example/list_test/MismatchedTypeGetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_list_get_value(self):
        path = '%s/boa3_test/example/list_test/GetValue.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_type_hint(self):
        path = '%s/boa3_test/example/list_test/TypeHintAssignment.py' % self.dirname

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_set_value(self):
        path = '%s/boa3_test/example/list_test/SetValue.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0] = 1
            + Opcode.PUSH0
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.PUSH1      # return 1
            + Opcode.RET
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_non_sequence_set_value(self):
        path = '%s/boa3_test/example/list_test/MismatchedTypeSetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_list_index_mismatched_type(self):
        path = '%s/boa3_test/example/list_test/MismatchedTypeListIndex.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_list_of_list(self):
        path = '%s/boa3_test/example/list_test/ListOfList.py' % self.dirname

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_nep5_main(self):
        path = '%s/boa3_test/example/list_test/Nep5Main.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG1     # args[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_slicing_omitted(self):
        path = '%s/boa3_test/example/list_test/ListSlicing.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_list_append_int_value(self):
        path = '%s/boa3_test/example/list_test/AppendIntValue.py' % self.dirname

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
            + Opcode.LDLOC0     # a.append(4)
            + Opcode.PUSH4
            + Opcode.APPEND
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_append_any_value(self):
        four = String('4').to_bytes(min_length=1)
        path = '%s/boa3_test/example/list_test/AppendAnyValue.py' % self.dirname

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
            + Opcode.LDLOC0     # a.append(4)
            + Opcode.PUSHDATA1
            + Integer(len(four)).to_byte_array()
            + four
            + Opcode.APPEND
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_append_mismatched_type(self):
        path = '%s/boa3_test/example/list_test/MismatchedTypeAppendValue.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_list_append_with_builtin(self):
        path = '%s/boa3_test/example/list_test/AppendIntWithBuiltin.py' % self.dirname

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
            + Opcode.LDLOC0     # list.append(a, 4)
            + Opcode.PUSH4
            + Opcode.APPEND
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_list_append_with_builtin_mismatched_type(self):
        path = '%s/boa3_test/example/list_test/MismatchedTypesAppendWithBuiltin.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
