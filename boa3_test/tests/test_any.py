from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestAny(BoaTest):

    def test_any_variable_assignments(self):
        two = String('2').to_bytes()
        path = '%s/boa3_test/test_sc/any_test/AnyVariableAssignments.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # a = 1
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # a = '2'
            + Integer(len(two)).to_byte_array() + two
            + Opcode.STLOC0
            + Opcode.PUSH1      # a = True
            + Opcode.STLOC0
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_variable_assignment_with_any(self):
        path = '%s/boa3_test/test_sc/any_test/VariableAssignmentWithAny.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_any_list(self):
        ok = String('ok').to_bytes()
        path = '%s/boa3_test/test_sc/any_test/AnyList.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_any_tuple(self):
        ok = String('ok').to_bytes()
        path = '%s/boa3_test/test_sc/any_test/AnyTuple.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_any_operation(self):
        path = '%s/boa3_test/test_sc/any_test/OperationWithAny.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_function_any_param(self):
        ok = String('ok').to_bytes()
        some_string = String('some_string').to_bytes()

        expected_output = (
            Opcode.INITSLOT   # Main
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0          # bool_tuple = True, False
            + Opcode.PUSH1
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0         # SequenceFunction(bool_tuple)
            + Opcode.CALL
            + Integer(46).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHDATA1      # SequenceFunction([True, 1, 'ok'])
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.CALL
            + Integer(36).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHDATA1      # SequenceFunction('some_string')
            + Integer(len(some_string)).to_byte_array()
            + some_string
            + Opcode.CALL
            + Integer(21).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHDATA1      # SequenceFunction((True, 1, 'ok'))
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.CALL
            + Integer(11).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH3          # SequenceFunction([1, 2, 3])
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.CALL
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHNULL
            + Opcode.RET        # return
            + Opcode.INITSLOT   # SequenceFunction
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0         # a = sequence
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/any_test/FunctionAnyParam.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_any_sequence_assignments(self):
        ok = String('ok').to_bytes()
        some_string = String('some_string').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x05'
            + b'\x00'
            + Opcode.PUSHDATA1  # any_list = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSH3      # int_list = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.PUSHDATA1  # any_tuple = (True, 1, 'ok')
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.PUSH0      # bool_tuple = True, False
            + Opcode.PUSH1
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.LDLOC0     # a = any_list
            + Opcode.STLOC4
            + Opcode.LDLOC2     # a = any_tuple
            + Opcode.STLOC4
            + Opcode.PUSHDATA1  # a = 'some_string'
            + Integer(len(some_string)).to_byte_array() + some_string
            + Opcode.STLOC4
            + Opcode.LDLOC1     # a = int_list
            + Opcode.STLOC4
            + Opcode.LDLOC3     # a = bool_tuple
            + Opcode.STLOC4
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/any_test/AnySequenceAssignments.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_int_sequence_any_assignments(self):
        path = '%s/boa3_test/test_sc/any_test/IntSequenceAnyAssignment.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_str_sequence_any_assignments(self):
        path = '%s/boa3_test/test_sc/any_test/StrSequenceAnyAssignment.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_str_sequence_str_assignment(self):
        some_string = String('some_string').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # str_sequence = 'some_string'
            + Integer(len(some_string)).to_byte_array() + some_string
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/any_test/StrSequenceStrAssignment.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_sequence_of_any_sequence(self):
        ok = String('ok').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x05'
            + b'\x00'
            + Opcode.PUSHDATA1  # any_list = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSH3      # int_list = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.PUSHDATA1  # any_tuple = (None, 1, 'ok')
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHNULL
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.PUSH0      # bool_tuple = True, False
            + Opcode.PUSH1
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.LDLOC3     # a = [any_list, int_list, any_tuple, bool_tuple]
            + Opcode.LDLOC2
            + Opcode.LDLOC1
            + Opcode.LDLOC0
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.STLOC4
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/any_test/SequenceOfAnySequence.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_sequence_of_int_sequence_success(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH3      # int_list = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSH8      # int_tuple = 10, 9, 8
            + Opcode.PUSH9
            + Opcode.PUSH10
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.LDLOC1     # a = [int_list, int_tuple]
            + Opcode.LDLOC0
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/any_test/SequenceOfIntSequence.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_sequence_of_int_sequence_fail(self):
        path = '%s/boa3_test/test_sc/any_test/SequenceOfAnyIntSequence.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
