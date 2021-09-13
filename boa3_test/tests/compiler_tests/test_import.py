from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.neo.cryptography import hash160
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
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
            + Integer(3).to_byte_array(min_length=1, signed=True)
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported module's function
            + Opcode.RET  # return
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0  # imported module's variable in the init
            + Opcode.STSFLD0
            + Opcode.RET
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
            + Integer(3).to_byte_array(min_length=1, signed=True)
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported module's function
            + Opcode.RET  # return
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0  # imported module's variable in the init
            + Opcode.STSFLD0
            + Opcode.RET
        )

        path = self.get_contract_path('ImportUserModuleWithAlias.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_import_user_module_with_global_variables(self):
        expected_output = (
            Opcode.LDSFLD0  # b = a
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET  # return
            + Opcode.INITSSLOT + b'\x02'
            + Opcode.CALL  # a = UserModule.EmptyList()
            + Integer(-4).to_byte_array(min_length=1, signed=True)
            + Opcode.STSFLD0
            + Opcode.NEWARRAY0     # module variable empty_list from import
            + Opcode.STSFLD1
            + Opcode.RET
        )

        path = self.get_contract_path('FromImportWithGlobalVariables.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_import_variable(self):
        expected_output = (
            Opcode.LDSFLD0  # return empty_list
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET  # return
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0  # imported variable
            + Opcode.STSFLD0
            + Opcode.RET
        )

        path = self.get_contract_path('FromImportVariable.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

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

    def test_from_import_all(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(7).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
            + Opcode.LDSFLD0  # return empty_list
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET  # return
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0     # module variable empty_list from import
            + Opcode.STSFLD0
            + Opcode.RET
        )

        path = self.get_contract_path('FromImportAll.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'call_imported_method')
        self.assertEqual([], result)

        result = self.run_smart_contract(engine, path, 'call_imported_variable')
        self.assertEqual([], result)

    def test_from_import_user_module(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET  # return
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0     # module variable empty_list from import
            + Opcode.STSFLD0
            + Opcode.RET
        )

        path = self.get_contract_path('FromImportUserModule.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_from_import_user_module_with_alias(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
            + Opcode.NEWARRAY0  # imported function
            + Opcode.RET  # return
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0     # module variable empty_list from import
            + Opcode.STSFLD0
            + Opcode.RET
        )

        path = self.get_contract_path('FromImportUserModuleWithAlias.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_import_non_existent_package(self):
        path = self.get_contract_path('ImportNonExistentPackage.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_import_interop_with_alias(self):
        path = self.get_contract_path('ImportInteropWithAlias.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_import_user_module_recursive_import(self):
        path = self.get_contract_path('ImportUserModuleRecursiveImport.py')
        self.assertCompilerLogs(CompilerError.CircularImport, path)

    def test_from_import_user_module_recursive_import(self):
        path = self.get_contract_path('FromImportUserModuleRecursiveImport.py')
        self.assertCompilerLogs(CompilerError.CircularImport, path)

    def test_import_user_module_with_not_imported_symbols(self):
        path = self.get_contract_path('ImportUserModuleWithNotImportedSymbols.py')
        output, manifest = self.compile_and_save(path)
        script = hash160(output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', [], script)
        self.assertEqual([], result)

        result = self.run_smart_contract(engine, path, 'main', [1, 2, 3], script)
        expected_result = []
        for x in [1, 2, 3]:
            expected_result.append([script,
                                    'notify',
                                    [x]])
        self.assertEqual(expected_result, result)

        result = self.run_smart_contract(engine, path, 'main', [1, 2, 3], b'\x01' * 20)
        self.assertEqual([], result)

        # 'with_param' is a public method, so it should be included in the manifest when imported
        result = self.run_smart_contract(engine, path, 'with_param', [1, 2, 3], b'\x01' * 20)
        self.assertEqual([], result)

        # 'without_param' is a public method, but it isn't imported, so it shouldn't be included in the manifest
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'without_param', [1, 2, 3])

    def test_import_user_module_with_not_imported_variables(self):
        expected_output = (
            Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.RET
            + Opcode.LDSFLD1    # module function from import
            + Opcode.RET  # return
            + Opcode.LDSFLD2    # imported function
            + Opcode.RET  # return
            + Opcode.INITSSLOT + b'\x03'
            + Opcode.PUSH15     # module variable a
            + Opcode.STSFLD0
            + Opcode.PUSH10     # module variable a from import
            + Opcode.STSFLD1
            + Opcode.PUSH5      # module variable b from import
            + Opcode.STSFLD2
            + Opcode.RET
        )

        path = self.get_contract_path('ImportUserModuleWithNotImportedVariables.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(5, result)
