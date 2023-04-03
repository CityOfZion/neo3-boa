from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String


class TestAny(BoaTest):
    default_folder: str = 'test_sc/any_test'

    def test_any_variable_assignments(self):
        two = String('2').to_bytes()
        path = self.get_contract_path('AnyVariableAssignments.py')

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # a = 1
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # a = '2'
            + Integer(len(two)).to_byte_array() + two
            + Opcode.STLOC0
            + Opcode.PUSHT      # a = True
            + Opcode.STLOC0
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_variable_assignment_with_any(self):
        path = self.get_contract_path('VariableAssignmentWithAny.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_any_list(self):
        ok = String('ok').to_bytes()
        path = self.get_contract_path('AnyList.py')

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_any_tuple(self):
        ok = String('ok').to_bytes()
        path = self.get_contract_path('AnyTuple.py')

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_any_operation(self):
        path = self.get_contract_path('OperationWithAny.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_function_any_param(self):
        ok = String('ok').to_bytes()
        some_string = String('some_string').to_bytes()

        expected_output = (
            Opcode.INITSLOT   # Main
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHF          # bool_tuple = True, False
            + Opcode.PUSHT
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0         # SequenceFunction(bool_tuple)
            + Opcode.CALL
            + Integer(45).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHDATA1      # SequenceFunction([True, 1, 'ok'])
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.CALL
            + Integer(35).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHDATA1      # SequenceFunction('some_string')
            + Integer(len(some_string)).to_byte_array()
            + some_string
            + Opcode.CALL
            + Integer(20).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHDATA1      # SequenceFunction((True, 1, 'ok'))
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.CALL
            + Integer(10).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH3          # SequenceFunction([1, 2, 3])
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.CALL
            + Integer(3).to_byte_array(min_length=1, signed=True)
            + Opcode.RET        # return
            + Opcode.INITSLOT   # SequenceFunction
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0         # a = sequence
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('FunctionAnyParam.py')
        output = self.compile(path)
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
            + Opcode.PUSHT
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
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.PUSHF      # bool_tuple = True, False
            + Opcode.PUSHT
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
            + Opcode.RET
        )

        path = self.get_contract_path('AnySequenceAssignments.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_int_sequence_any_assignments(self):
        ok = String('ok').to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1  # any_list = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # int_sequence = any_list
            + Opcode.STLOC1
            + Opcode.RET
        )

        path = self.get_contract_path('IntSequenceAnyAssignment.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_str_sequence_any_assignments(self):
        ok = String('ok').to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1  # any_list = [True, 1, 'ok']
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # str_sequence = any_list
            + Opcode.STLOC1
            + Opcode.RET
        )

        path = self.get_contract_path('StrSequenceAnyAssignment.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_str_sequence_str_assignment(self):
        some_string = String('some_string').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # str_sequence = 'some_string'
            + Integer(len(some_string)).to_byte_array() + some_string
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('StrSequenceStrAssignment.py')
        output = self.compile(path)
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
            + Opcode.PUSHT
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
            + Opcode.PUSHF      # bool_tuple = True, False
            + Opcode.PUSHT
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
            + Opcode.RET
        )

        path = self.get_contract_path('SequenceOfAnySequence.py')
        output = self.compile(path)
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
            + Opcode.RET
        )

        path = self.get_contract_path('SequenceOfIntSequence.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_sequence_of_int_sequence_fail(self):
        ok = String('ok').to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH3      # int_list = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # any_tuple = (True, 1, 'ok')
            + Integer(len(ok)).to_byte_array() + ok
            + Opcode.PUSH1
            + Opcode.PUSHT
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.PUSH8      # int_tuple = 10, 9, 8
            + Opcode.PUSH9
            + Opcode.PUSH10
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.LDLOC2     # a = [int_list, any_tuple, int_tuple]
            + Opcode.LDLOC1
            + Opcode.LDLOC0
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC3
            + Opcode.RET
        )

        path = self.get_contract_path('SequenceOfAnyIntSequence.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)
