from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.neo.vm.opcode.Opcode import Opcode
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
        path = self.get_contract_path('ImportUserModule.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_import_user_module_with_alias(self):
        path = self.get_contract_path('ImportUserModuleWithAlias.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_import_user_module_with_global_variables(self):
        path = self.get_contract_path('FromImportWithGlobalVariables.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_import_variable(self):
        path = self.get_contract_path('FromImportVariable.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_typing_python_library(self):
        path = self.get_contract_path('ImportPythonLib.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

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
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_from_import_user_module(self):
        path = self.get_contract_path('FromImportUserModule.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_from_import_user_module_with_alias(self):
        path = self.get_contract_path('FromImportUserModuleWithAlias.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_import_non_existent_package(self):
        path = self.get_contract_path('ImportNonExistantPackage.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_import_interop_with_alias(self):
        path = self.get_contract_path('ImportInteropWithAlias.py')
        self.compile_and_save(path)
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
