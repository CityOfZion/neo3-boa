from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, TypeHintMissing, TooManyReturns
from boa3.neo.vm.opcode.Opcode import Opcode
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
