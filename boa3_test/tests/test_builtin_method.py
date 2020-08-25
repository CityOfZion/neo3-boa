from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation, UnexpectedArgument, UnfilledArgument
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestVariable(BoaTest):

    # region TestLen

    def test_len_of_tuple(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3      # a = (1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = len(a)
            + Opcode.SIZE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenTuple.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_len_of_list(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = len(a)
            + Opcode.SIZE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenList.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_len_of_str(self):
        input = 'just a test'
        byte_input = String(input).to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.SIZE
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenString.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_len_of_bytes(self):
        byte_input = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.SIZE
            + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenBytes.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_len_of_no_collection(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_len_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_len_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region TestAppend

    def test_append_tuple(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendTuple.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_append_sequence(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendSequence.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_append_mutable_sequence(self):
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
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendMutableSequence.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_append_mutable_sequence_with_builtin(self):
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
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendMutableSequenceBuiltinCall.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_append_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_append_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region TestClear

    def test_clear_tuple(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ClearTuple.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_clear_mutable_sequence(self):
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
        path = '%s/boa3_test/test_sc/built_in_methods_test/ClearMutableSequence.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_clear_mutable_sequence_with_builtin(self):
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
            + Opcode.LDLOC0     # MutableSequence.clear(a)
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
        path = '%s/boa3_test/test_sc/built_in_methods_test/ClearMutableSequenceBuiltinCall.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_clear_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ClearTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_clear_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ClearTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region TestReverse

    def test_reverse_tuple(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ReverseTuple.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_reverse_mutable_sequence(self):
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
        path = '%s/boa3_test/test_sc/built_in_methods_test/ReverseMutableSequence.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_reverse_mutable_sequence_with_builtin(self):
        data = b'\x01\x02\x03'
        expected_output = (
                Opcode.INITSLOT     # function signature
                + b'\x01'
                + b'\x00'
                + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
                + Integer(len(data)).to_byte_array(min_length=1)
                + data
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.STLOC0
                + Opcode.LDLOC0     # MutableSequence.reverse(a)
                + Opcode.REVERSEITEMS
                + Opcode.LDLOC0     # return a
                + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/built_in_methods_test/ReverseMutableSequenceBuiltinCall.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_reverse_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ReverseTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_reverse_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ReverseTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region TestExtend

    def test_extend_tuple(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendTuple.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_extend_sequence(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendSequence.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_extend_mutable_sequence(self):
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
            + Opcode.LDLOC0     # a.extend((4, 5, 6))
            + Opcode.PUSH6      # (4, 5, 6)
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.UNPACK     # a.extend
                + Opcode.JMP
                + Integer(9).to_byte_array(signed=True, min_length=1)
                + Opcode.DUP
                + Opcode.INC
                + Opcode.PICK
                + Opcode.PUSH2
                + Opcode.ROLL
                + Opcode.APPEND
                + Opcode.DEC
                + Opcode.DUP
                + Opcode.JMPIF
                + Integer(-8).to_byte_array(signed=True, min_length=1)
                + Opcode.DROP
                + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendMutableSequence.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_extend_mutable_sequence_with_builtin(self):
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
            + Opcode.LDLOC0     # MutableSequence.extend(a, [4, 5, 6])
            + Opcode.PUSH6      # [4, 5, 6]
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.UNPACK     # a.extend
                + Opcode.JMP
                + Integer(9).to_byte_array(signed=True, min_length=1)
                + Opcode.DUP
                + Opcode.INC
                + Opcode.PICK
                + Opcode.PUSH2
                + Opcode.ROLL
                + Opcode.APPEND
                + Opcode.DEC
                + Opcode.DUP
                + Opcode.JMPIF
                + Integer(-8).to_byte_array(signed=True, min_length=1)
                + Opcode.DROP
                + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendMutableSequenceBuiltinCall.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_extend_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_extend_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region TestToScriptHash

    def test_script_hash_int(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(script_hash)).to_byte_array(min_length=1)
            + script_hash
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashInt.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_script_hash_int_with_builtin(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(script_hash)).to_byte_array(min_length=1)
            + script_hash
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashIntBuiltinCall.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_script_hash_str(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(script_hash)).to_byte_array(min_length=1)
            + script_hash
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashStr.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_script_hash_str_with_builtin(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(script_hash)).to_byte_array(min_length=1)
            + script_hash
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashStrBuiltinCall.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_script_hash_variable(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashVariable.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_script_hash_variable_with_builtin(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashVariableBuiltinCall.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_script_hahs_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_script_hash_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_script_hash_mismatched_types(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashMismatchedType.py' % self.dirname
        # TODO: change to MismatchedTypes when 'to_script_hash' with variables is implemented
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_script_hash_builtin_mismatched_types(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashBuiltinMismatchedType.py' % self.dirname
        # TODO: change to MismatchedTypes when 'to_script_hash' with variables is implemented
        self.assertCompilerLogs(NotSupportedOperation, path)

    # endregion

    # region TestToBytes

    def test_int_to_bytes(self):
        value = Integer(123).to_byte_array()
        expected_output = (
            Opcode.PUSHDATA1        # (123).to_bytes()
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IntToBytes.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_int_to_bytes_with_builtin(self):
        value = Integer(123).to_byte_array()
        expected_output = (
            Opcode.PUSHDATA1        # int.to_bytes(123)
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IntToBytesWithBuiltin.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_str_to_bytes(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1        # '123'.to_bytes()
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/StrToBytes.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_str_to_bytes_with_builtin(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1        # str.to_bytes('123')
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/StrToBytesWithBuiltin.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_to_bytes_mismatched_types(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ToBytesMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    # endregion
