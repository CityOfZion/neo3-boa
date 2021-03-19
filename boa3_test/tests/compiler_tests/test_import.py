from boa3.boa3 import Boa3
from boa3.exception.CompilerError import UnresolvedReference
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestImport(BoaTest):

    default_folder: str = 'test_sc/import_test'

    def test_import_typing(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.NEWARRAY0
            + Opcode.STLOC0
            + Opcode.RET        # return
        )
        path = self.get_contract_path('ImportTyping.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_import_typing_with_alias(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.NEWARRAY0
            + Opcode.STLOC0
            + Opcode.RET        # return
        )
        path = self.get_contract_path('ImportTypingWithAlias.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_import_user_module(self):
        expected_output = (
            Opcode.CALL
            + Integer(8).to_byte_array(min_length=1, signed=True)
            + Opcode.RET
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0
            + Opcode.STSFLD0
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        path = self.get_contract_path('ImportUserModule.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_import_user_module_with_alias(self):
        expected_output = (
            Opcode.CALL
            + Integer(8).to_byte_array(min_length=1, signed=True)
            + Opcode.RET
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0
            + Opcode.STSFLD0
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        path = self.get_contract_path('ImportUserModuleWithAlias.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_import_user_module_with_global_variables(self):
        expected_output = (
            Opcode.LDSFLD0    # b = a
            + Opcode.RET
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.CALL       # a = UserModule.EmptyList()
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.STSFLD0
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        path = self.get_contract_path('FromImportWithGlobalVariables.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_import_variable(self):
        expected_output = (
            Opcode.LDSFLD0    # b = a
            + Opcode.RET
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0  # imported variable
            + Opcode.STSFLD0
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        path = self.get_contract_path('FromImportVariable.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_typing_python_library(self):
        path = self.get_contract_path('ImportPythonLib.py')
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_from_typing_import(self):
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET        # return
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0
            + Opcode.STSFLD0
            + Opcode.RET
        )

        path = self.get_contract_path('FromImportTyping.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_from_typing_import_with_alias(self):
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('FromImportTypingWithAlias.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_from_typing_import_not_supported_type(self):
        path = self.get_contract_path('FromImportTypingNotImplementedType.py')
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_from_import_user_module(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        path = self.get_contract_path('FromImportUserModule.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_from_import_user_module_with_alias(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET        # return
        )

        path = self.get_contract_path('FromImportUserModuleWithAlias.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_import_non_existent_package(self):
        path = self.get_contract_path('ImportNonExistantPackage.py')
        self.assertCompilerLogs(UnresolvedReference, path)
