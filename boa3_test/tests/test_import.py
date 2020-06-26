from boa3.boa3 import Boa3
from boa3.exception.CompilerError import UnresolvedReference
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest


class TestImport(BoaTest):

    def test_import_typing(self):
        path = '%s/boa3_test/example/import_test/ImportTyping.py' % self.dirname
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

    def test_import_typing_with_alias(self):
        path = '%s/boa3_test/example/import_test/ImportTypingWithAlias.py' % self.dirname
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

    def test_import_user_module(self):
        path = '%s/boa3_test/example/import_test/ImportUserModule.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_import_user_module_with_alias(self):
        path = '%s/boa3_test/example/import_test/ImportUserModuleWithAlias.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_typing_python_library(self):
        path = '%s/boa3_test/example/import_test/ImportPythonLib.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_from_typing_import(self):
        path = '%s/boa3_test/example/import_test/FromImportTyping.py' % self.dirname

        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_from_typing_import_with_alias(self):
        path = '%s/boa3_test/example/import_test/FromImportTypingWithAlias.py' % self.dirname

        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_from_typing_import_not_supported_type(self):
        path = '%s/boa3_test/example/import_test/FromImportTypingNotImplementedType.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_from_import_user_module(self):
        path = '%s/boa3_test/example/import_test/FromImportUserModule.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_from_import_user_module_with_alias(self):
        path = '%s/boa3_test/example/import_test/FromImportUserModuleWithAlias.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)
