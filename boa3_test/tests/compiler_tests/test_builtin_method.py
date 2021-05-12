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

    default_folder: str = 'test_sc/built_in_methods_test'

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
        path = self.get_contract_path('LenTuple.py')

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
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
        path = self.get_contract_path('LenList.py')

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
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
        path = self.get_contract_path('LenString.py')

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(11, result)

    def test_len_of_bytes(self):
        path = self.get_contract_path('LenBytes.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(3, result)

    def test_len_of_no_collection(self):
        path = self.get_contract_path('LenMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_len_too_many_parameters(self):
        path = self.get_contract_path('LenTooManyParameters.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_len_too_few_parameters(self):
        path = self.get_contract_path('LenTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region append test

    def test_append_tuple(self):
        path = self.get_contract_path('AppendTuple.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_append_sequence(self):
        path = self.get_contract_path('AppendSequence.py')
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
        path = self.get_contract_path('AppendMutableSequence.py')

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
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
        path = self.get_contract_path('AppendMutableSequenceBuiltinCall.py')

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'append_example')
        self.assertEqual([1, 2, 3, 4], result)

    def test_append_too_many_parameters(self):
        path = self.get_contract_path('AppendTooManyParameters.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_append_too_few_parameters(self):
        path = self.get_contract_path('AppendTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region clear test

    def test_clear_tuple(self):
        path = self.get_contract_path('ClearTuple.py')
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
        path = self.get_contract_path('ClearMutableSequence.py')

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
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
        path = self.get_contract_path('ClearMutableSequenceBuiltinCall.py')

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'clear_example')
        self.assertEqual([], result)

    def test_clear_too_many_parameters(self):
        path = self.get_contract_path('ClearTooManyParameters.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_clear_too_few_parameters(self):
        path = self.get_contract_path('ClearTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region reverse test

    def test_reverse_tuple(self):
        path = self.get_contract_path('ReverseTuple.py')
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
        path = self.get_contract_path('ReverseMutableSequence.py')

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([3, 2, 1], result)

    @unittest.skip("reverse items doesn't work with bytestring")
    def test_reverse_mutable_sequence_with_builtin(self):
        path = self.get_contract_path('ReverseMutableSequenceBuiltinCall.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x03\x02\x01', result)

    def test_reverse_too_many_parameters(self):
        path = self.get_contract_path('ReverseTooManyParameters.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_reverse_too_few_parameters(self):
        path = self.get_contract_path('ReverseTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region extend test

    def test_extend_tuple(self):
        path = self.get_contract_path('ExtendTuple.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_extend_sequence(self):
        path = self.get_contract_path('ExtendSequence.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_extend_mutable_sequence(self):
        path = self.get_contract_path('ExtendMutableSequence.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_extend_mutable_sequence_with_builtin(self):
        path = self.get_contract_path('ExtendMutableSequenceBuiltinCall.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_extend_too_many_parameters(self):
        path = self.get_contract_path('ExtendTooManyParameters.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_extend_too_few_parameters(self):
        path = self.get_contract_path('ExtendTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    # endregion

    # region to_script_hash test

    def test_script_hash_int(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())

        path = self.get_contract_path('ScriptHashInt.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(script_hash, result)

    def test_script_hash_int_with_builtin(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())

        path = self.get_contract_path('ScriptHashIntBuiltinCall.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(script_hash, result)

    def test_script_hash_str(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())

        path = self.get_contract_path('ScriptHashStr.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(script_hash, result)

    def test_script_hash_str_with_builtin(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())

        path = self.get_contract_path('ScriptHashStrBuiltinCall.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(script_hash, result)

    def test_script_hash_variable(self):
        path = self.get_contract_path('ScriptHashVariable.py')
        engine = TestEngine()
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'Main', 123)

        from boa3.neo import to_script_hash
        from base58 import b58encode
        value = b58encode(Integer(123).to_byte_array())
        if isinstance(value, int):
            value = Integer(value).to_byte_array()

        script_hash = to_script_hash(value)

        result = self.run_smart_contract(engine, path, 'Main', value,
                                         expected_result_type=bytes)
        self.assertEqual(script_hash, result)

    def test_script_hash_variable_with_builtin(self):
        path = self.get_contract_path('ScriptHashVariableBuiltinCall.py')
        from boa3.neo import to_script_hash
        from base58 import b58encode
        engine = TestEngine()

        script_hash = to_script_hash('123')
        result = self.run_smart_contract(engine, path, 'Main', '123',
                                         expected_result_type=bytes)
        self.assertEqual(script_hash, result)

        value = b58encode('123')
        if isinstance(value, int):
            value = Integer(value).to_byte_array()

        script_hash = to_script_hash(value)
        result = self.run_smart_contract(engine, path, 'Main', value,
                                         expected_result_type=bytes)
        self.assertEqual(script_hash, result)

    def test_script_hahs_too_many_parameters(self):
        path = self.get_contract_path('ScriptHashTooManyParameters.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_script_hash_too_few_parameters(self):
        path = self.get_contract_path('ScriptHashTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_script_hash_mismatched_types(self):
        path = self.get_contract_path('ScriptHashMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_script_hash_builtin_mismatched_types(self):
        path = self.get_contract_path('ScriptHashBuiltinMismatchedType.py')
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

        path = self.get_contract_path('IntToBytes.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
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

        path = self.get_contract_path('IntToBytesWithBuiltin.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
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

        path = self.get_contract_path('StrToBytes.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
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

        path = self.get_contract_path('StrToBytesWithBuiltin.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'str_to_bytes',
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

    def test_to_bytes_mismatched_types(self):
        path = self.get_contract_path('ToBytesMismatchedType.py')
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

        path = self.get_contract_path('PrintInt.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
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

        path = self.get_contract_path('PrintStr.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_list(self):
        path = self.get_contract_path('PrintList.py')
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_print_many_values(self):
        path = self.get_contract_path('PrintManyValues.py')
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_print_missing_outer_function_return(self):
        path = self.get_contract_path('PrintIntMissingFunctionReturn.py')
        self.assertCompilerLogs(MissingReturnStatement, path)

    # endregion

    # region isinstance test

    def test_isinstance_int_literal(self):
        path = self.get_contract_path('IsInstanceIntLiteral.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_isinstance_int_variable(self):
        path = self.get_contract_path('IsInstanceIntVariable.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(False, result)

    def test_isinstance_bool_literal(self):
        path = self.get_contract_path('IsInstanceBoolLiteral.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(False, result)

    def test_isinstance_bool_variable(self):
        path = self.get_contract_path('IsInstanceBoolVariable.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(False, result)

    def test_isinstance_str_literal(self):
        path = self.get_contract_path('IsInstanceStrLiteral.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_isinstance_str_variable(self):
        path = self.get_contract_path('IsInstanceStrVariable.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(True, result)

    def test_isinstance_list_literal(self):
        path = self.get_contract_path('IsInstanceListLiteral.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_isinstance_tuple_literal(self):
        path = self.get_contract_path('IsInstanceTupleLiteral.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_isinstance_tuple_variable(self):
        path = self.get_contract_path('IsInstanceTupleVariable.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', [])
        self.assertEqual(True, result)

    def test_isinstance_many_types(self):
        path = self.get_contract_path('IsInstanceManyTypes.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'string')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', {})
        self.assertEqual(True, result)

    def test_isinstance_many_types_with_class(self):
        path = self.get_contract_path('IsInstanceManyTypesWithClass.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 42,
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', [],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'some string',
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', bytes(20),
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', None,
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', {1: 2, 2: 4},
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_isinstance_uint160(self):
        path = self.get_contract_path('IsInstanceUInt160.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', bytes(20),
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', bytes(30),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 42,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

    def test_isinstance_uint256(self):
        path = self.get_contract_path('IsInstanceUInt256.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', bytes(10),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'main', bytes(20),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'main', bytes(30),
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'main', bytes(32),
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_isinstance_class(self):
        path = self.get_contract_path('IsInstanceClass.py')
        self.assertCompilerLogs(NotSupportedOperation, path)

    # endregion

    # region exit test

    def test_exit(self):
        path = self.get_contract_path('Exit.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', False)
        self.assertEqual(123, result)

        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'main', True)

    # endregion

    # region max test

    def test_max_int(self):
        path = self.get_contract_path('MaxInt.py')
        engine = TestEngine()

        value1 = 10
        value2 = 999
        expected_result = max(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2)
        self.assertEqual(expected_result, result)

    def test_max_too_few_parameters(self):
        path = self.get_contract_path('MaxTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_max_mismatched_types(self):
        path = self.get_contract_path('MaxMismatchedTypes.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    # endregion

    # region min test

    def test_min_int(self):
        path = self.get_contract_path('MinInt.py')
        engine = TestEngine()

        val1 = 50
        val2 = 1
        expected_result = min(val1, val2)
        result = self.run_smart_contract(engine, path, 'main', val1, val2)
        self.assertEqual(expected_result, result)

    def test_min_too_few_parameters(self):
        path = self.get_contract_path('MinTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_min_mismatched_types(self):
        path = self.get_contract_path('MinMismatchedTypes.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    # endregion

    # region sqrt test

    def test_sqrt_method(self):
        path = self.get_contract_path('Sqrt.py')
        engine = TestEngine()

        from math import sqrt

        expected_result = int(sqrt(0))
        result = self.run_smart_contract(engine, path, 'main', 0)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(1))
        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(3))
        result = self.run_smart_contract(engine, path, 'main', 3)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(4))
        result = self.run_smart_contract(engine, path, 'main', 4)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(8))
        result = self.run_smart_contract(engine, path, 'main', 8)
        self.assertEqual(expected_result, result)
        expected_result = int(sqrt(10))
        result = self.run_smart_contract(engine, path, 'main', 10)
        self.assertEqual(expected_result, result)

        with self.assertRaises(TestExecutionException):
            result = self.run_smart_contract(engine, path, 'main', -1)

        val = 25
        expected_result = int(sqrt(val))
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(expected_result, result)

    # endregion

    # region abs test

    def test_abs(self):
        path = self.get_contract_path('Abs.py')
        engine = TestEngine()

        val = 10
        expected_result = abs(val)
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(expected_result, result)

        expected_result = abs(-1)
        result = self.run_smart_contract(engine, path, 'main', -1)
        self.assertEqual(expected_result, result)

        expected_result = abs(1)
        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual(expected_result, result)

    def test_abs_bytes(self):
        path = self.get_contract_path('AbsMismatchedTypesBytes.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_abs_string(self):
        path = self.get_contract_path('AbsMismatchedTypesString.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_abs_too_few_parameters(self):
        path = self.get_contract_path('AbsTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_abs_too_many_parameters(self):
        path = self.get_contract_path('AbsTooManyParameters.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    # endregion

    # region sum test

    def test_sum(self):
        path = self.get_contract_path('Sum.py')
        self.compile_and_save(path)
        engine = TestEngine()

        val = [1, 2, 3, 4]
        expected_result = sum(val)
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(expected_result, result)

        val = list(range(10, 20, 2))
        expected_result = sum(val)
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(expected_result, result)

    def test_sum_with_start(self):
        path = self.get_contract_path('SumWithStart.py')
        self.compile_and_save(path)
        engine = TestEngine()

        val = [1, 2, 3, 4]
        expected_result = sum(val, 10)
        result = self.run_smart_contract(engine, path, 'main', val, 10)
        self.assertEqual(expected_result, result)

        val = list(range(10, 20, 2))
        expected_result = sum(val, 20)
        result = self.run_smart_contract(engine, path, 'main', val, 20)
        self.assertEqual(expected_result, result)

    def test_sum_mismatched_type(self):
        path = self.get_contract_path('SumMismatchedTypes.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_sum_too_few_parameters(self):
        path = self.get_contract_path('SumTooFewParameters.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_sum_too_many_parameters(self):
        path = self.get_contract_path('SumTooManyParameters.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    # endregion
