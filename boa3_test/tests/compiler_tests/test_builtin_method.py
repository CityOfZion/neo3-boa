import unittest

from boa3.boa3 import Boa3
from boa3.exception import CompilerError
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

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(3, result)

    def test_len_of_no_collection(self):
        path = self.get_contract_path('LenMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_len_too_many_parameters(self):
        path = self.get_contract_path('LenTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_len_too_few_parameters(self):
        path = self.get_contract_path('LenTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region append test

    def test_append_tuple(self):
        path = self.get_contract_path('AppendTuple.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_append_sequence(self):
        path = self.get_contract_path('AppendSequence.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_append_too_few_parameters(self):
        path = self.get_contract_path('AppendTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region clear test

    def test_clear_tuple(self):
        path = self.get_contract_path('ClearTuple.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_clear_too_few_parameters(self):
        path = self.get_contract_path('ClearTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region reverse test

    def test_reverse_tuple(self):
        path = self.get_contract_path('ReverseTuple.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

    def test_reverse_mutable_sequence_with_builtin(self):
        path = self.get_contract_path('ReverseMutableSequenceBuiltinCall.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'\x03\x02\x01', result)

    def test_reverse_too_many_parameters(self):
        path = self.get_contract_path('ReverseTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_reverse_too_few_parameters(self):
        path = self.get_contract_path('ReverseTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region extend test

    def test_extend_tuple(self):
        path = self.get_contract_path('ExtendTuple.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_extend_sequence(self):
        path = self.get_contract_path('ExtendSequence.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_extend_mutable_sequence(self):
        path = self.get_contract_path('ExtendMutableSequence.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_extend_mutable_sequence_with_builtin(self):
        path = self.get_contract_path('ExtendMutableSequenceBuiltinCall.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3, 4, 5, 6], result)

    def test_extend_too_many_parameters(self):
        path = self.get_contract_path('ExtendTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_extend_too_few_parameters(self):
        path = self.get_contract_path('ExtendTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region to_script_hash test

    def test_script_hash_int(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())

        path = self.get_contract_path('ScriptHashInt.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(script_hash, result)

    def test_script_hash_int_with_builtin(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())

        path = self.get_contract_path('ScriptHashIntBuiltinCall.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(script_hash, result)

    def test_script_hash_str(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())

        path = self.get_contract_path('ScriptHashStr.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(script_hash, result)

    def test_script_hash_str_with_builtin(self):
        from boa3.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())

        path = self.get_contract_path('ScriptHashStrBuiltinCall.py')

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

    def test_script_hash_too_many_parameters(self):
        path = self.get_contract_path('ScriptHashTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_script_hash_too_few_parameters(self):
        path = self.get_contract_path('ScriptHashTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_script_hash_mismatched_types(self):
        path = self.get_contract_path('ScriptHashMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_script_hash_builtin_mismatched_types(self):
        path = self.get_contract_path('ScriptHashBuiltinMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region to_bytes test

    def test_int_to_bytes(self):
        path = self.get_contract_path('IntToBytes.py')
        engine = TestEngine()

        value = Integer(123).to_byte_array()
        result = self.run_smart_contract(engine, path, 'int_to_bytes',
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

    def test_int_zero_to_bytes(self):
        path = self.get_contract_path('IntZeroToBytes.py')
        engine = TestEngine()

        value = Integer(0).to_byte_array(min_length=1)
        result = self.run_smart_contract(engine, path, 'int_to_bytes',
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

    def test_int_to_bytes_with_builtin(self):
        path = self.get_contract_path('IntToBytesWithBuiltin.py')
        engine = TestEngine()

        value = Integer(123).to_byte_array()
        result = self.run_smart_contract(engine, path, 'int_to_bytes',
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

    def test_int_to_bytes_as_parameter(self):
        path = self.get_contract_path('IntToBytesAsParameter.py')
        engine = TestEngine()

        self.run_smart_contract(engine, path, 'int_to_bytes', 1111,
                                expected_result_type=bytes)
        from boa3.neo3.vm import VMState
        # return is Void, checking to see if there is no error
        self.assertEqual(engine.vm_state, VMState.HALT)

    def test_str_to_bytes(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1        # '123'.to_bytes()
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region print test

    def test_print_int(self):
        path = self.get_contract_path('PrintInt.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_str(self):
        path = self.get_contract_path('PrintStr.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_bytes(self):
        path = self.get_contract_path('PrintBytes.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_bool(self):
        path = self.get_contract_path('PrintBool.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_list(self):
        path = self.get_contract_path('PrintList.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_print_many_values(self):
        path = self.get_contract_path('PrintManyValues.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_no_args(self):
        path = self.get_contract_path('PrintNoArgs.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_print_missing_outer_function_return(self):
        path = self.get_contract_path('PrintIntMissingFunctionReturn.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

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
        result = self.run_smart_contract(engine, path, 'Main', 42)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', [])
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'some string')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', bytes(20))
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', None)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', {1: 2, 2: 4})
        self.assertEqual(True, result)

    def test_isinstance_uint160(self):
        path = self.get_contract_path('IsInstanceUInt160.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', bytes(20))
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', bytes(30))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 42)
        self.assertEqual(False, result)

    def test_isinstance_uint256(self):
        path = self.get_contract_path('IsInstanceUInt256.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', bytes(10))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'main', bytes(20))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'main', bytes(30))
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'main', bytes(32))
        self.assertEqual(True, result)

    # endregion

    # region exit test

    def test_exit(self):
        path = self.get_contract_path('Exit.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', False)
        self.assertEqual(123, result)

        with self.assertRaisesRegex(TestExecutionException, self.ABORTED_CONTRACT_MSG):
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

    def test_max_int_more_arguments(self):
        path = self.get_contract_path('MaxIntMoreArguments.py')
        engine = TestEngine()

        numbers = 4, 1, 16, 8, 2
        expected_result = max(numbers)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_max_str(self):
        path = self.get_contract_path('MaxStr.py')
        engine = TestEngine()

        value1 = 'foo'
        value2 = 'bar'
        expected_result = max(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2)
        self.assertEqual(expected_result, result)

        result = self.run_smart_contract(engine, path, 'main', value2, value1)
        self.assertEqual(expected_result, result)

        value1 = 'alg'
        value2 = 'al'
        expected_result = max(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2)
        self.assertEqual(expected_result, result)

        value = 'some string'
        expected_result = max(value, value)
        result = self.run_smart_contract(engine, path, 'main', value, value)
        self.assertEqual(expected_result, result)

    def test_max_str_more_arguments(self):
        path = self.get_contract_path('MaxStrMoreArguments.py')
        engine = TestEngine()

        values = 'Lorem', 'ipsum', 'dolor', 'sit', 'amet'
        expected_result = max(values)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_max_bytes(self):
        path = self.get_contract_path('MaxBytes.py')
        engine = TestEngine()

        value1 = b'foo'
        value2 = b'bar'
        expected_result = max(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2, expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        result = self.run_smart_contract(engine, path, 'main', value2, value1, expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        value1 = b'alg'
        value2 = b'al'
        expected_result = max(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2, expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        value = b'some string'
        expected_result = max(value, value)
        result = self.run_smart_contract(engine, path, 'main', value, value, expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_max_bytes_more_arguments(self):
        path = self.get_contract_path('MaxBytesMoreArguments.py')
        engine = TestEngine()

        values = b'Lorem', b'ipsum', b'dolor', b'sit', b'amet'
        expected_result = max(values)
        result = self.run_smart_contract(engine, path, 'main', expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_max_too_few_parameters(self):
        path = self.get_contract_path('MaxTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_max_mismatched_types(self):
        path = self.get_contract_path('MaxMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

    def test_min_int_more_arguments(self):
        path = self.get_contract_path('MinIntMoreArguments.py')
        engine = TestEngine()

        numbers = 2, 8, 1, 4, 16
        expected_result = min(numbers)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_min_str(self):
        path = self.get_contract_path('MinStr.py')
        engine = TestEngine()

        value1 = 'foo'
        value2 = 'bar'
        expected_result = min(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2)
        self.assertEqual(expected_result, result)

        result = self.run_smart_contract(engine, path, 'main', value2, value1)
        self.assertEqual(expected_result, result)

        value1 = 'alg'
        value2 = 'al'
        expected_result = min(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2)
        self.assertEqual(expected_result, result)

        value = 'some string'
        expected_result = min(value, value)
        result = self.run_smart_contract(engine, path, 'main', value, value)
        self.assertEqual(expected_result, result)

    def test_min_str_more_arguments(self):
        path = self.get_contract_path('MinStrMoreArguments.py')
        engine = TestEngine()

        values = 'Lorem', 'ipsum', 'dolor', 'sit', 'amet'
        expected_result = min(values)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_min_bytes(self):
        path = self.get_contract_path('MinBytes.py')
        engine = TestEngine()

        value1 = b'foo'
        value2 = b'bar'
        expected_result = min(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2, expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        result = self.run_smart_contract(engine, path, 'main', value2, value1, expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        value1 = b'alg'
        value2 = b'al'
        expected_result = min(value1, value2)
        result = self.run_smart_contract(engine, path, 'main', value1, value2, expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        value = b'some string'
        expected_result = min(value, value)
        result = self.run_smart_contract(engine, path, 'main', value, value, expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_min_bytes_more_arguments(self):
        path = self.get_contract_path('MinBytesMoreArguments.py')
        engine = TestEngine()

        values = b'Lorem', b'ipsum', b'dolor', b'sit', b'amet'
        expected_result = min(values)
        result = self.run_smart_contract(engine, path, 'main', expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_min_too_few_parameters(self):
        path = self.get_contract_path('MinTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_min_mismatched_types(self):
        path = self.get_contract_path('MinMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_abs_string(self):
        path = self.get_contract_path('AbsMismatchedTypesString.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_abs_too_few_parameters(self):
        path = self.get_contract_path('AbsTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_abs_too_many_parameters(self):
        path = self.get_contract_path('AbsTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    # endregion

    # region sum test

    def test_sum(self):
        path = self.get_contract_path('Sum.py')
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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_sum_too_few_parameters(self):
        path = self.get_contract_path('SumTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_sum_too_many_parameters(self):
        path = self.get_contract_path('SumTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    # endregion

    # region str split test

    def test_str_split(self):
        path = self.get_contract_path('StrSplit.py')
        engine = TestEngine()

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 2
        expected_result = string.split(separator, maxsplit)
        result = self.run_smart_contract(engine, path, 'main', string, separator, maxsplit)
        self.assertEqual(expected_result, result)

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 1
        expected_result = string.split(separator, maxsplit)
        result = self.run_smart_contract(engine, path, 'main', string, separator, maxsplit)
        self.assertEqual(expected_result, result)

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 0
        expected_result = string.split(separator, maxsplit)
        result = self.run_smart_contract(engine, path, 'main', string, separator, maxsplit)
        self.assertEqual(expected_result, result)

        string = 'unit123test123str123split'
        separator = '123'
        maxsplit = 1
        expected_result = string.split(separator, maxsplit)
        result = self.run_smart_contract(engine, path, 'main', string, separator, maxsplit)
        self.assertEqual(expected_result, result)

    def test_str_split_maxsplit_default(self):
        path = self.get_contract_path('StrSplitMaxsplitDefault.py')
        engine = TestEngine()

        string = '1#2#3#4'
        separator = '#'
        expected_result = string.split(separator)
        result = self.run_smart_contract(engine, path, 'main', string, separator)
        self.assertEqual(expected_result, result)

        string = 'unit123test123str123split'
        separator = '123'
        expected_result = string.split(separator)
        result = self.run_smart_contract(engine, path, 'main', string, separator)
        self.assertEqual(expected_result, result)

    def test_str_split_default(self):
        path = self.get_contract_path('StrSplitSeparatorDefault.py')
        engine = TestEngine()

        string = '1 2 3 4'
        expected_result = string.split()
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(expected_result, result)

    # endregion

    # region count test

    def test_count_list_int(self):
        path = self.get_contract_path('CountListInt.py')
        engine = TestEngine()

        list_ = [1, 2, 3, 4, 1, 1, 0]
        expected_result = list_.count(1)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_list_str(self):
        path = self.get_contract_path('CountListStr.py')
        engine = TestEngine()

        list_ = ['unit', 'test', 'unit', 'unit', 'random', 'string']
        expected_result = list_.count('unit')
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_list_bytes(self):
        path = self.get_contract_path('CountListBytes.py')
        engine = TestEngine()

        list_ = [b'unit', b'test', b'unit', b'unit', b'random', b'string']
        expected_result = list_.count(b'unit')
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_list_different_primitive_types(self):
        path = self.get_contract_path('CountListDifferentPrimitiveTypes.py')
        engine = TestEngine()

        list_ = [b'unit', 'test', b'unit', b'unit', 123, 123, True, False]
        expected_result = list_.count(b'unit'), list_.count('test'), list_.count(123)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, tuple(result))

    def test_count_list_different_any_types(self):
        path = self.get_contract_path('CountListAnyType.py')
        engine = TestEngine()

        mixed_list = [[b'unit', b'unit'], [123, 123], [True, False], [True, False], [b'unit', 'test'], 'not list']

        count1 = mixed_list.count([b'unit', 'test'])
        count2 = mixed_list.count([123, 123])
        count3 = mixed_list.count([True, False])
        count4 = mixed_list.count(['random value', 'random value', 'random value'])
        expected_result = [count1, count2, count3, count4]

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_list_only_sequences(self):
        path = self.get_contract_path('CountListOnlySequences.py')
        engine = TestEngine()

        mixed_list = [[b'unit', b'unit'], [123, 123], [True, False], [True, False], [b'unit', 'test']]

        count1 = mixed_list.count([b'unit', 'test'])
        count2 = mixed_list.count([123, 123])
        count3 = mixed_list.count([True, False])
        count4 = mixed_list.count(['random value', 'random value', 'random value'])
        expected_result = [count1, count2, count3, count4]

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_list_empty(self):
        path = self.get_contract_path('CountListEmpty.py')
        engine = TestEngine()

        list_ = []
        expected_result = list_.count(1)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_tuple_int(self):
        path = self.get_contract_path('CountTupleInt.py')
        engine = TestEngine()

        tuple_ = (1, 2, 3, 4, 1, 1, 0)
        expected_result = tuple_.count(1)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_tuple_str(self):
        path = self.get_contract_path('CountTupleStr.py')
        engine = TestEngine()

        tuple_ = ('unit', 'test', 'unit', 'unit', 'random', 'string')
        expected_result = tuple_.count('unit')
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_tuple_bytes(self):
        path = self.get_contract_path('CountTupleBytes.py')
        engine = TestEngine()

        tuple_ = (b'unit', b'test', b'unit', b'unit', b'random', b'string')
        expected_result = tuple_.count(b'unit')
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_tuple_different_types(self):
        path = self.get_contract_path('CountTupleDifferentTypes.py')
        engine = TestEngine()

        tuple_ = (b'unit', 'test', b'unit', b'unit', 123, 123, True, False)
        expected_result = tuple_.count(b'unit'), tuple_.count('test'), tuple_.count(123)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, tuple(result))

    def test_count_tuple_different_non_primitive_types(self):
        path = self.get_contract_path('CountTupleDifferentNonPrimitiveTypes.py')
        engine = TestEngine()

        mixed_list = ([b'unit', 'test'], [b'unit', b'unit'], [123, 123], [True, False], [True, False])

        count1 = mixed_list.count([b'unit', 'test'])
        count2 = mixed_list.count([123, 123])
        count3 = mixed_list.count([True, False])
        expected_result = [count1, count2, count3]

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_tuple_empty(self):
        path = self.get_contract_path('CountTupleEmpty.py')
        engine = TestEngine()

        tuple_ = ()
        expected_result = tuple_.count(1)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_range(self):
        path = self.get_contract_path('CountRange.py')
        engine = TestEngine()

        expected_result = range(10).count(1)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_count_sequence_too_many_parameters(self):
        path = self.get_contract_path('CountSequenceTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_count_sequence_too_few_parameters(self):
        path = self.get_contract_path('CountSequenceTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_count_str(self):
        path = self.get_contract_path('CountStr.py')
        engine = TestEngine()

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = 43
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = 1000
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = -1000
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = -4
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 23
        end = 43
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = -11
        end = 43
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = -1000
        end = 43
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 1000
        end = 43
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 0
        end = 43
        expected_result = str_.count(substr, start, end)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start, end)
        self.assertEqual(expected_result, result)

    def test_count_str_end_default(self):
        path = self.get_contract_path('CountStrEndDefault.py')
        engine = TestEngine()

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 0
        expected_result = str_.count(substr, start)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start)
        self.assertEqual(expected_result, result)

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 4
        expected_result = str_.count(substr, start)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        start = 0
        expected_result = str_.count(substr, start)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        start = 5
        expected_result = str_.count(substr, start)
        result = self.run_smart_contract(engine, path, 'main', str_, substr, start)
        self.assertEqual(expected_result, result)

    def test_count_str_default(self):
        path = self.get_contract_path('CountStrDefault.py')
        engine = TestEngine()

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        expected_result = str_.count(substr)
        result = self.run_smart_contract(engine, path, 'main', str_, substr)
        self.assertEqual(expected_result, result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        expected_result = str_.count(substr)
        result = self.run_smart_contract(engine, path, 'main', str_, substr)
        self.assertEqual(expected_result, result)

    def test_count_str_too_many_parameters(self):
        path = self.get_contract_path('CountStrTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_count_str_too_few_parameters(self):
        path = self.get_contract_path('CountStrTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region super test

    def test_super_with_args(self):
        # TODO: Change when super with args is implemented
        path = self.get_contract_path('SuperWithArgs.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_super_call_method(self):
        path = self.get_contract_path('SuperCallMethod.py')
        engine = TestEngine()

        super_method_expected_result = -20
        arg = 20
        result = self.run_smart_contract(engine, path, 'example_method', arg)
        self.assertEqual(arg, result)

        arg = 30
        result = self.run_smart_contract(engine, path, 'example_method', arg)
        self.assertEqual(arg, result)

        arg = 40
        result = self.run_smart_contract(engine, path, 'example_method', arg)
        self.assertEqual(super_method_expected_result, result)

    # endregion

    # region int test

    # TODO: Int constructor is not accepting more than one method
    @unittest.skip('Int constructor is not accepting more than one method')
    def test_int_str(self):
        path = self.get_contract_path('IntStr.py')
        self.compile_and_save(path)  # it doesn't compile, it isn't implemented yet
        engine = TestEngine()

        value = '0b101'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0B101'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0b101'
        base = 2
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0B101'
        base = 2
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0o123'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0O123'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0o123'
        base = 8
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0O123'
        base = 8
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0x123'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0X123'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0x123'
        base = 16
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '0X123'
        base = 16
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '123'
        base = 16
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = '11'
        base = 11
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = 'abcdef'
        base = 16
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = 'abcdefg'
        base = 16
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'main', value, base)
        with self.assertRaises(ValueError):
            int(value, base)

        value = '0x123'
        base = 8
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'main', value, base)
        with self.assertRaises(ValueError):
            int(value, base)

    # TODO: Int constructor is not accepting more than one method
    @unittest.skip('Int constructor is not accepting more than one method')
    def test_int_bytes(self):
        path = self.get_contract_path('IntBytes.py')
        self.compile_and_save(path)  # it doesn't compile, it isn't implemented yet
        engine = TestEngine()

        value = b'0b101'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0B101'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0b101'
        base = 2
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0B101'
        base = 2
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0o123'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0O123'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0o123'
        base = 8
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0O123'
        base = 8
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0x123'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0X123'
        base = 0
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0x123'
        base = 16
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'0X123'
        base = 16
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'123'
        base = 16
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'11'
        base = 11
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'abcdef'
        base = 16
        result = self.run_smart_contract(engine, path, 'main', value, base)
        self.assertEqual(int(value, base), result)

        value = b'abcdefg'
        base = 16
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'main', value, base)
        with self.assertRaises(ValueError):
            int(value, base)

        value = b'0x123'
        base = 8
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'main', value, base)
        with self.assertRaises(ValueError):
            int(value, base)

    def test_int_int(self):
        path = self.get_contract_path('IntInt.py')
        engine = TestEngine()

        value = 10
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(int(value), result)

        value = -10
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(int(value), result)

    def test_int_int_too_many_parameters(self):
        path = self.get_contract_path('IntIntTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_int_no_parameters(self):
        path = self.get_contract_path('IntNoParameters.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(int(), result)

    # endregion

    # region bool test

    def test_bool(self):
        path = self.get_contract_path('Bool.py')
        engine = TestEngine()

        val = 1
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = 'test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = b'test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = [1, 2, 3]
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = {'1': 2}
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

    def test_bool_bytes(self):
        path = self.get_contract_path('BoolBytes.py')
        engine = TestEngine()

        val = b'123'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = b''
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

    def test_bool_class(self):
        path = self.get_contract_path('BoolClass.py')
        engine = TestEngine()

        # dunder methods are not supported in neo3-boa
        class Example:
            def __init__(self):
                self.test = 123
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(bool(Example()), result)

    def test_bool_dict(self):
        path = self.get_contract_path('BoolDict.py')
        engine = TestEngine()

        val = {}
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = {'a': 123, 'b': 56, 'c': 1}
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

    def test_bool_int(self):
        path = self.get_contract_path('BoolInt.py')
        engine = TestEngine()

        val = -1
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = 0
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = 1
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

    def test_bool_list(self):
        path = self.get_contract_path('BoolList.py')
        engine = TestEngine()

        val = []
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = [1, 2, 3, 4, 5]
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

    def test_bool_range(self):
        path = self.get_contract_path('BoolRange.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'range_0')
        self.assertEqual(bool(range(0)), result)

        result = self.run_smart_contract(engine, path, 'range_not_0')
        self.assertEqual(bool(range(10)), result)

    def test_bool_str(self):
        path = self.get_contract_path('BoolStr.py')
        engine = TestEngine()

        val = 'unit test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

        val = ''
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(bool(val), result)

    # endregion

    # region list test

    def test_list_any(self):
        path = self.get_contract_path('ListAny.py')
        engine = TestEngine()

        val = [1, 2, 3, 4]
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

        val = {'a': 1, 'b': '2', 'c': True, 'd': b'01', '12e12e12e12': 123}
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

        val = 'unit test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(bytes(val, 'utf-8')), result)

        val = b'unit test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

        val = 123
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'main', val)

    def test_list_default(self):
        path = self.get_contract_path('ListDefault.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(list(), result)

    def test_list_sequence(self):
        path = self.get_contract_path('ListSequence.py')
        engine = TestEngine()

        val = [1, 2, 3, 4]
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

        val = (1, 2, 3, 4)
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

        val = range(0, 10)
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

        val = [1, 2, 3, 4]
        result = self.run_smart_contract(engine, path, 'verify_list_unchanged', val)
        new_list = list(val)
        val[0] = val[1]
        self.assertEqual(new_list, result)

    def test_list_sequence_mismatched_return_type(self):
        path = self.get_contract_path('ListSequenceMismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_mapping(self):
        path = self.get_contract_path('ListMapping.py')
        engine = TestEngine()

        val = {'a': 1, 'b': 2, 'c': 3, 'd': 0, '12e12e12e12': 123}
        result = self.run_smart_contract(engine, path, 'main', val)
        # result should be a list of all the keys used in the dictionary, in insertion order
        self.assertEqual(list(val), result)

        val = {'a': 1, 'b': '2', 'c': True, 'd': b'01', '12e12e12e12': 123}
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

        val = {1: 0, 23: 12, -10: 412, 25: '123'}
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

        val = {b'123': 123, b'test': 'test', b'unit': 'unit'}
        result = self.run_smart_contract(engine, path, 'main', val)
        for index, item in enumerate(result):
            if isinstance(item, str):
                result[index] = String(item).to_bytes()
        self.assertEqual(list(val), result)

        val = {'a': 1, 'b': '2', 'c': True, 1: 0, 23: 12, 25: 'value'}
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

    def test_list_mapping_mismatched_return_type(self):
        path = self.get_contract_path('ListMappingMismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_bytes(self):
        path = self.get_contract_path('ListBytes.py')
        engine = TestEngine()

        val = b'unit test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

    def test_list_bytes_mismatched_return_type(self):
        path = self.get_contract_path('ListBytesMismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_str(self):
        path = self.get_contract_path('ListString.py')
        engine = TestEngine()

        val = 'unit test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

    def test_list_str_mismatched_return_type(self):
        path = self.get_contract_path('ListStringMismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_bytes_str(self):
        path = self.get_contract_path('ListBytesString.py')
        engine = TestEngine()

        # If the compiler doesn't have a type hint to know if it's a bytes or str value it will consider it as bytes
        val = 'unit test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(bytes(val, 'utf-8')), result)

        val = b'unit test'
        result = self.run_smart_contract(engine, path, 'main', val)
        self.assertEqual(list(val), result)

    # endregion

    # region str test

    def test_str_bytes_str(self):
        path = self.get_contract_path('StrByteString.py')
        engine = TestEngine()

        value = 'test'
        result = self.run_smart_contract(engine, path, 'str_parameter', value)
        self.assertEqual(str(value), result)

        value = b'test'
        result = self.run_smart_contract(engine, path, 'bytes_parameter', value)
        # since bytes and string is the same thing internally it will return 'test' instead of the "b'test'"
        self.assertEqual('test', result)

        result = self.run_smart_contract(engine, path, 'empty_parameter')
        self.assertEqual(str(), result)

    def test_str_int(self):
        path = self.get_contract_path('StrInt.py')
        engine = TestEngine()

        value = 1234567890
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(str(value), result)

        value = -1234567890
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(str(value), result)

    def test_str_bool(self):
        path = self.get_contract_path('StrBool.py')
        engine = TestEngine()

        value = True
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(str(value), result)

        value = False
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(str(value), result)

    def test_str_too_many_parameters(self):
        path = self.get_contract_path('StrTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    # endregion
