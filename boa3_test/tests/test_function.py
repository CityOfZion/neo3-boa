from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, TooManyReturns, TypeHintMissing
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestFunction(BoaTest):

    def test_integer_function(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'           # num local variables
            + b'\x01'           # num arguments
            + Opcode.PUSH10     # body
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/function_test/IntegerFunction.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_string_function(self):
        expected_output = (
            Opcode.INITSLOT         # function signature
            + b'\x00'               # num local variables
            + b'\x00'               # num arguments
            + Opcode.PUSHDATA1      # body
            + bytes([len('42')])
            + bytes('42', 'UTF-8')
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/example/function_test/StringFunction.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_bool_function(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'           # num local variables
            + b'\x00'           # num arguments
            + Opcode.PUSH1      # body
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/function_test/BoolFunction.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_none_function(self):
        path = '%s/boa3_test/example/function_test/NoneFunction.py' % self.dirname

        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)

    def test_arg_without_type_hint(self):
        path = '%s/boa3_test/example/function_test/ArgWithoutTypeHintFunction.py' % self.dirname
        self.assertCompilerLogs(TypeHintMissing, path)

    def test_no_return_hint_function_with_empty_return_statement(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'           # num local variables
            + b'\x01'           # num arguments
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/function_test/EmptyReturnFunction.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_no_return_hint_function_without_return_statement(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'           # num local variables
            + b'\x01'           # num arguments
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/function_test/NoReturnFunction.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_return_type_hint_function_with_empty_return(self):
        path = '%s/boa3_test/example/function_test/ExpectingReturnFunction.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_multiple_return_function(self):
        path = '%s/boa3_test/example/function_test/MultipleReturnFunction.py' % self.dirname
        self.assertCompilerLogs(TooManyReturns, path)

    def test_tuple_function(self):
        path = '%s/boa3_test/example/function_test/TupleFunction.py' % self.dirname
        self.assertCompilerLogs(TooManyReturns, path)

    def test_default_return(self):
        twenty = Integer(20).to_byte_array(min_length=1)
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # if arg0
            + Opcode.JMPIFNOT
                + Integer(4).to_byte_array(min_length=1, signed=True)
                + Opcode.PUSH10         # return 10
                + Opcode.RET
            + Opcode.LDARG1         # elif arg1
            + Opcode.JMPIFNOT
            + Integer(8).to_byte_array(min_length=1, signed=True)
                + Opcode.PUSHDATA1      # return 20
                + Integer(len(twenty)).to_byte_array() + twenty
                + Opcode.CONVERT
                + Type.int.stack_item
                + Opcode.RET
            + Opcode.PUSH0          # default return
            + Opcode.RET
        )

        path = '%s/boa3_test/example/function_test/DefaultReturn.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_empty_list_return(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.NEWARRAY0
            + Opcode.RET
        )

        path = '%s/boa3_test/example/function_test/EmptyListReturn.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_return_type(self):
        path = '%s/boa3_test/example/function_test/MismatchedReturnType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_return_type_with_if(self):
        path = '%s/boa3_test/example/function_test/MismatchedReturnTypeWithIf.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_call_void_function_without_args(self):
        called_function_address = Integer(4).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x00'
            + b'\x02'
            + Opcode.CALL           # TestFunction()
            + called_function_address
            + Opcode.PUSH1          # return True
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1          # a = 1
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/example/function_test/CallVoidFunctionWithoutArgs.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_call_function_without_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x01'
            + b'\x02'
            + Opcode.CALL           # a = TestFunction()
            + called_function_address
            + Opcode.STLOC0
            + Opcode.LDLOC0         # return a
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH1          # return 1
            + Opcode.RET
        )

        path = '%s/boa3_test/example/function_test/CallReturnFunctionWithoutArgs.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_call_void_function_with_literal_args(self):
        called_function_address = Integer(4).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH2          # TestAdd(1, 2)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.PUSH1          # return True
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x01'
            + b'\x02'
            + Opcode.LDARG0         # c = a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/example/function_test/CallVoidFunctionWithLiteralArgs.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_call_function_with_literal_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x01'
            + b'\x02'
            + Opcode.PUSH2          # a = TestAdd(1, 2)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.STLOC0
            + Opcode.LDLOC0         # return a
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/example/function_test/CallReturnFunctionWithLiteralArgs.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_call_void_function_with_variable_args(self):
        called_function_address = Integer(4).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH1          # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2          # b = 2
            + Opcode.STLOC1
            + Opcode.LDLOC1         # TestAdd(a, b)
            + Opcode.LDLOC0
            + Opcode.CALL
            + called_function_address
            + Opcode.PUSH1          # return True
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x01'
            + b'\x02'
            + Opcode.LDARG0         # c = a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/example/function_test/CallVoidFunctionWithVariableArgs.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_call_function_with_variable_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x03'
            + b'\x02'
            + Opcode.PUSH1          # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2          # b = 2
            + Opcode.STLOC1
            + Opcode.LDLOC1         # c = TestAdd(a, b)
            + Opcode.LDLOC0
            + Opcode.CALL
            + called_function_address
            + Opcode.STLOC2
            + Opcode.LDLOC2         # return c
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/example/function_test/CallReturnFunctionWithVariableArgs.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_call_function_with_on_return(self):
        called_function_address = Integer(3).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH1          # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2          # b = 2
            + Opcode.STLOC1
            + Opcode.LDLOC1         # return TestAdd(a, b)
            + Opcode.LDLOC0
            + Opcode.CALL
            + called_function_address
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/example/function_test/CallReturnFunctionOnReturn.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_call_function_written_before_caller(self):
        test_add: bytes = String('TestAdd').to_bytes()
        first_call_address = Integer(7).to_byte_array(min_length=1, signed=True)
        second_call_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # if operation == 'TestAdd'
            + Opcode.PUSHDATA1
            + Integer(len(test_add)).to_byte_array(min_length=1)
            + test_add
            + Opcode.EQUAL
            + Opcode.JMPIFNOT
            + first_call_address
                + Opcode.PUSH2          # return TestAdd(a, b)
                + Opcode.PUSH1
                + Opcode.CALL
                + second_call_address
                + Opcode.RET
            + Opcode.PUSH0
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/example/function_test/CallFunctionWrittenBefore.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)
