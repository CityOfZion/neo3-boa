from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


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
        output = self.compile(path)
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
        output = self.compile(path)
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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_variable_from_imported_module(self):
        path, _ = self.get_deploy_file_paths('variable_import', 'VariableFromImportedModule.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_foo', expected_result_type=bytes))
        expected_results.append(b'Foo')

        invokes.append(runner.call_contract(path, 'get_bar'))
        expected_results.append('bar')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_variable_access_from_imported_module(self):
        path, _ = self.get_deploy_file_paths('variable_import', 'VariableAccessFromImportedModule.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_foo', expected_result_type=bytes))
        expected_results.append(b'Foo')

        invokes.append(runner.call_contract(path, 'get_bar'))
        expected_results.append('bar')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_from_typing_import_with_alias(self):
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('FromImportTypingWithAlias.py')
        output = self.compile(path)
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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_imported_method'))
        expected_results.append([])

        invokes.append(runner.call_contract(path, 'call_imported_variable'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_from_import_user_module_from_root_and_file_directories(self):
        path = self.get_contract_path('FromImportUserModuleFromRootAndFileDir.py')
        self.compile_and_save(path, root_folder=self.get_dir_path(self.test_root_dir))
        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_imported_from_root'))
        expected_results.append([])

        invokes.append(runner.call_contract(path, 'call_imported_from_file_dir'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_non_existent_package(self):
        path = self.get_contract_path('ImportNonExistentPackage.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_import_interop_with_alias(self):
        path, _ = self.get_deploy_file_paths('ImportInteropWithAlias.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_user_module_recursive_import(self):
        path = self.get_contract_path('ImportUserModuleRecursiveImport.py')
        self.assertCompilerLogs(CompilerError.CircularImport, path)

    def test_from_import_user_module_recursive_import(self):
        path = self.get_contract_path('FromImportUserModuleRecursiveImport.py')
        self.assertCompilerLogs(CompilerError.CircularImport, path)

    def test_import_user_module_with_not_imported_symbols(self):
        path, _ = self.get_deploy_file_paths('ImportUserModuleWithNotImportedSymbols.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        contract = runner.deploy_contract(path)
        runner.update_contracts(export_checkpoint=True)
        script = contract.script_hash

        invokes.append(runner.call_contract(path, 'main', [], script))
        expected_results.append([])

        invokes.append(runner.call_contract(path, 'main', [1, 2, 3], script))
        expected_result = []
        for x in [1, 2, 3]:
            expected_result.append([script,
                                    'notify',
                                    [x]])
        expected_results.append(expected_result)

        invokes.append(runner.call_contract(path, 'main', [1, 2, 3], b'\x01' * 20))
        expected_results.append([])

        # 'with_param' is a public method, so it should be included in the manifest when imported
        invokes.append(runner.call_contract(path, 'with_param', [1, 2, 3], b'\x01' * 20))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # 'without_param' is a public method, but it isn't imported, so it shouldn't be included in the manifest
        runner.call_contract(path, 'without_param', [1, 2, 3])
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.FORMAT_METHOD_DOESNT_EXIST_IN_CONTRACT_MSG_REGEX_PREFIX.format('without_param'))

    def test_import_user_module_with_not_imported_variables(self):
        expected_output = (
            Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.RET
            + Opcode.PUSH10    # module function from import
            + Opcode.RET  # return
            + Opcode.PUSH5    # imported function
            + Opcode.RET  # return
        )
        expected_output_no_optimization = (
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
        output = self.compile(path, optimize=False)
        self.assertEqual(expected_output_no_optimization, output)

        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(5)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_imported_builtin_public(self):
        path = self.get_contract_path('NotImportedBuiltinPublic.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_not_imported_builtin_from_typing(self):
        path = self.get_contract_path('NotImportedBuiltinFromTypingInReturn.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

        path = self.get_contract_path('NotImportedBuiltinFromTypingInArgs.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

        path = self.get_contract_path('NotImportedBuiltinFromTypingInSubscript.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

        path = self.get_contract_path('NotImportedBuiltinFromTypingInVariable.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_incorrect_circular_import(self):
        path, _ = self.get_deploy_file_paths('incorrect_circular_import', 'IncorrectCircularImportDetection.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_module_with_init(self):
        path, _ = self.get_deploy_file_paths('ImportModuleWithInit.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_imported_method'))
        expected_results.append([])

        invokes.append(runner.call_contract(path, 'call_imported_variable'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_module_without_init(self):
        path, _ = self.get_deploy_file_paths('ImportModuleWithoutInit.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_imported_method'))
        expected_results.append({})

        invokes.append(runner.call_contract(path, 'call_imported_variable'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_user_class_inner_files(self):
        inner_path, _ = self.get_deploy_file_paths('class_import', 'ImportUserClass.py')
        path, _ = self.get_deploy_file_paths('ImportUserClassInnerFiles.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(inner_path, 'build_example_object'))
        expected_results.append([42, '42'])

        invokes.append(runner.call_contract(path, 'build_example_object'))
        expected_results.append('42')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_from_import_not_existing_method(self):
        path = self.get_contract_path('FromImportNotExistingMethod.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_import_not_existing_method(self):
        path = self.get_contract_path('ImportNotExistingMethod.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_import_boa_invalid_package(self):
        path = self.get_contract_path('ImportBoaInvalidPackage.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)
