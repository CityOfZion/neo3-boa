import unittest

from boa3.boa3 import Boa3
from boa3.exception.CompilerError import (MismatchedTypes, MissingReturnStatement, NotSupportedOperation,
                                          UnexpectedArgument, UnfilledArgument)
from boa3.model.builtin.interop.interop import Interop
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBuiltinMethod(BoaTest):

    # region len test

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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(3, result)

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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(3, result)

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
            + Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.SIZE
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenString.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(11, result)

    def test_len_of_bytes(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/LenBytes.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(3, result)

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

    # region append test

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
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendMutableSequence.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'append_example')
        self.assertEqual([1, 2, 3, 4], result)

    def test_append_mutable_sequence_with_builtin(self):
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
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendMutableSequenceBuiltinCall.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'append_example')
        self.assertEqual([1, 2, 3, 4], result)

    def test_append_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_append_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/AppendTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region clear test

    def test_clear_tuple(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ClearTuple.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_clear_mutable_sequence(self):
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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'clear_example')
        self.assertEqual([], result)

    def test_clear_mutable_sequence_with_builtin(self):
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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'clear_example')
        self.assertEqual([], result)

    def test_clear_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ClearTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_clear_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ClearTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region reverse test

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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([3, 2, 1], result)

    @unittest.skip("reverse items doesn't work with bytestring")
    def test_reverse_mutable_sequence_with_builtin(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ReverseMutableSequenceBuiltinCall.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x03\x02\x01', result)

    def test_reverse_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ReverseTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_reverse_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ReverseTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region extend test

    def test_extend_tuple(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendTuple.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_extend_sequence(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendSequence.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_extend_mutable_sequence(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendMutableSequence.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_extend_mutable_sequence_with_builtin(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendMutableSequenceBuiltinCall.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_extend_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_extend_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ExtendTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region to_script_hash test

    def test_script_hash_int(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashInt.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(script_hash, result)

    def test_script_hash_int_with_builtin(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashIntBuiltinCall.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(script_hash, result)

    def test_script_hash_str(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashStr.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(script_hash, result)

    def test_script_hash_str_with_builtin(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashStrBuiltinCall.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(script_hash, result)

    def test_script_hash_variable(self):
        script_hash = Integer(123).to_byte_array()
        twenty = Integer(20).to_byte_array()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x00'
            + Opcode.PUSHDATA1      # a = 123
            + Integer(len(script_hash)).to_byte_array(min_length=1)
            + script_hash
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.STLOC0
            + Opcode.PUSHDATA1      # a.to_script_hash()
            + Integer(len(script_hash)).to_byte_array(min_length=1)
            + script_hash
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.JMPIFNOT
            + Integer(36).to_byte_array(min_length=1)
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.str.stack_item
            + Opcode.JMPIF
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.SYSCALL
            + Interop.Base58Decode.interop_method_hash
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.PUSHDATA1
            + Integer(len(twenty)).to_byte_array(min_length=1)
            + twenty
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.JMPGT
            + Integer(8).to_byte_array(min_length=1)
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.DEC
            + Opcode.RIGHT
            + Opcode.JMP
            + Integer(9).to_byte_array(min_length=1)
            + Opcode.PUSH1
            + Opcode.PUSHDATA1
            + Integer(len(twenty)).to_byte_array(min_length=1)
            + twenty
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.SUBSTR
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashVariable.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_script_hash_variable_with_builtin(self):
        script_hash = String('123').to_bytes()
        twenty = Integer(20).to_byte_array()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x00'
            + Opcode.PUSHDATA1      # a = 123
            + Integer(len(script_hash)).to_byte_array(min_length=1)
            + script_hash
            + Opcode.STLOC0
            + Opcode.PUSHDATA1      # a.to_script_hash()
            + Integer(len(script_hash)).to_byte_array(min_length=1)
            + script_hash
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.JMPIFNOT
            + Integer(36).to_byte_array(min_length=1)
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.str.stack_item
            + Opcode.JMPIF
            + Integer(4).to_byte_array(min_length=1)
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.SYSCALL
            + Interop.Base58Decode.interop_method_hash
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.PUSHDATA1
            + Integer(len(twenty)).to_byte_array(min_length=1)
            + twenty
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.JMPGT
            + Integer(8).to_byte_array(min_length=1)
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.DEC
            + Opcode.RIGHT
            + Opcode.JMP
            + Integer(9).to_byte_array(min_length=1)
            + Opcode.PUSH1
            + Opcode.PUSHDATA1
            + Integer(len(twenty)).to_byte_array(min_length=1)
            + twenty
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.SUBSTR
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashVariableBuiltinCall.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_script_hahs_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_script_hash_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_script_hash_mismatched_types(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_script_hash_builtin_mismatched_types(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ScriptHashBuiltinMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    # endregion

    # region to_bytes test

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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'int_to_bytes',
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'int_to_bytes',
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'str_to_bytes',
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

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

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'str_to_bytes',
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

    def test_to_bytes_mismatched_types(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/ToBytesMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    # endregion

    # region print test

    def test_print_int(self):
        value = Integer(42).to_byte_array()
        expected_output = (
            Opcode.PUSHDATA1        # print(123)
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.SYSCALL
            + Interop.Log.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/PrintInt.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_str(self):
        value = String('str').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1        # print('str')
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.SYSCALL
            + Interop.Log.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/PrintStr.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_list(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/PrintList.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_print_many_values(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/PrintManyValues.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_print_missing_outer_function_return(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/PrintIntMissingFunctionReturn.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    # endregion

    # region isinstance test

    def test_isinstance_int_literal(self):
        value = Integer(123).to_byte_array()
        expected_output = (
            Opcode.PUSHDATA1        # isinstance(123, int)
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.ISTYPE
            + Type.int.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceIntLiteral.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_isinstance_int_variable(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0         # isinstance(a, int)
            + Opcode.ISTYPE
            + Type.int.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceIntVariable.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(False, result)

    def test_isinstance_bool_literal(self):
        value = Integer(123).to_byte_array()
        expected_output = (
            Opcode.PUSHDATA1        # isinstance(123, bool)
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.ISTYPE
            + Type.bool.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceBoolLiteral.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(False, result)

    def test_isinstance_bool_variable(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0         # isinstance(a, bool)
            + Opcode.ISTYPE
            + Type.bool.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceBoolVariable.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(False, result)

    def test_isinstance_str_literal(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1        # isinstance('123', str)
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.ISTYPE
            + Type.str.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceStrLiteral.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_isinstance_str_variable(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0         # isinstance(a, str)
            + Opcode.ISTYPE
            + Type.str.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceStrVariable.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(True, result)

    def test_isinstance_list_literal(self):
        expected_output = (
            Opcode.NEWARRAY0        # isinstance([], list)
            + Opcode.ISTYPE
            + Type.list.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceListLiteral.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_isinstance_tuple_literal(self):
        expected_output = (
            Opcode.NEWARRAY0        # isinstance([], tuple)
            + Opcode.ISTYPE
            + Type.tuple.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceTupleLiteral.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_isinstance_tuple_variable(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0         # isinstance(a, tuple)
            + Opcode.ISTYPE
            + Type.tuple.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceTupleVariable.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', [])
        self.assertEqual(True, result)

    def test_isinstance_many_types(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0         # isinstance(a, tuple)
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.list.stack_item
            + Opcode.JMPIF
            + Integer(16).to_byte_array(min_length=1, signed=True)
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.int.stack_item
            + Opcode.JMPIF
            + Integer(11).to_byte_array(min_length=1, signed=True)
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.bool.stack_item
            + Opcode.JMPIF
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.ISTYPE
            + Type.dict.stack_item
            + Opcode.JMP
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.DROP
            + Opcode.PUSH1
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/built_in_methods_test/IsInstanceManyTypes.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', {})
        self.assertEqual(True, result)

    # endregion

    # region exit test

    def test_exit(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/Exit.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'main', False)
        self.assertEqual(123, result)

        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'main', True)

    # end region

    # region max test

    def test_max_int(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/MaxInt.py' % self.dirname
        engine = TestEngine(self.dirname)

        value1 = 10
        value2 = 999
        expected_result = max(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2)
        self.assertEqual(expected_result, result)

    def test_max_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/MaxTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_max_mismatched_types(self):
        path = '%s/boa3_test/test_sc/built_in_methods_test/MaxMismatchedTypes.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    # end region
