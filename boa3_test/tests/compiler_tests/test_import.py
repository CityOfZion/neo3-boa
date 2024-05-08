from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3_test.tests import annotation, boatestcase


class TestImport(boatestcase.BoaTestCase):
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
        output, _ = self.assertCompile('ImportTyping.py')
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
        output, _ = self.assertCompile('ImportTypingWithAlias.py')
        self.assertEqual(expected_output, output)

    def test_import_user_module_compile(self):
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

        output, _ = self.assertCompile('ImportUserModule.py')
        self.assertEqual(expected_output, output)

    async def test_import_user_module_run(self):
        await self.set_up_contract('ImportUserModule.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([], result)

    def test_import_user_module_with_alias_compile(self):
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

        output, _ = self.assertCompile('ImportUserModuleWithAlias.py')
        self.assertEqual(expected_output, output)

    async def test_import_user_module_with_alias(self):
        await self.set_up_contract('ImportUserModuleWithAlias.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([], result)

    def test_import_user_module_with_global_variables_compile(self):
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

        output, _ = self.assertCompile('FromImportWithGlobalVariables.py')
        self.assertEqual(expected_output, output)

    async def test_import_user_module_with_global_variables_run(self):
        await self.set_up_contract('FromImportWithGlobalVariables.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([], result)

    def test_import_variable_compile(self):
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

        output, _ = self.assertCompile('FromImportVariable.py')
        self.assertEqual(expected_output, output)

    async def test_import_variable(self):
        await self.set_up_contract('FromImportVariable.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([], result)

    async def test_variable_from_imported_module(self):
        await self.set_up_contract('variable_import', 'VariableFromImportedModule.py')

        result, _ = await self.call('get_foo', [], return_type=bytes)
        self.assertEqual(b'Foo', result)

        result, _ = await self.call('get_bar', [], return_type=str)
        self.assertEqual('bar', result)

    async def test_variable_access_from_imported_module(self):
        await self.set_up_contract('variable_import', 'VariableAccessFromImportedModule.py')

        result, _ = await self.call('get_foo', [], return_type=bytes)
        self.assertEqual(b'Foo', result)

        result, _ = await self.call('get_bar', [], return_type=str)
        self.assertEqual('bar', result)

    def test_typing_python_library(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'ImportPythonLib.py')

    def test_from_typing_import(self):
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET        # return
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.NEWARRAY0
            + Opcode.STSFLD0
            + Opcode.RET
        )

        output, _ = self.assertCompile('FromImportTyping.py')
        self.assertEqual(expected_output, output)

    def test_from_typing_import_with_alias(self):
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('FromImportTypingWithAlias.py')
        self.assertEqual(expected_output, output)

    def test_from_typing_import_not_supported_type(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'FromImportTypingNotImplementedType.py')

    def test_from_import_all_compile(self):
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

        output, _ = self.assertCompile('FromImportAll.py')
        self.assertEqual(expected_output, output)

    async def test_from_import_all_run(self):
        await self.set_up_contract('FromImportAll.py')

        result, _ = await self.call('call_imported_method', [], return_type=list)
        self.assertEqual([], result)

        result, _ = await self.call('call_imported_variable', [], return_type=list)
        self.assertEqual([], result)

    def test_from_import_user_module_compile(self):
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

        output, _ = self.assertCompile('FromImportUserModule.py')
        self.assertEqual(expected_output, output)

    async def test_from_import_user_module_run(self):
        await self.set_up_contract('FromImportUserModule.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([], result)

    def test_from_import_user_module_with_alias_compile(self):
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

        output, _ = self.assertCompile('FromImportUserModuleWithAlias.py')
        self.assertEqual(expected_output, output)

    async def test_from_import_user_module_with_alias_run(self):
        await self.set_up_contract('FromImportUserModuleWithAlias.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([], result)

    async def test_from_import_user_module_from_root_and_file_directories(self):
        await self.set_up_contract('FromImportUserModuleFromRootAndFileDir.py',
                                   root_folder=self.get_dir_path(self.test_root_dir)
                                   )

        result, _ = await self.call('call_imported_from_root', [], return_type=list)
        self.assertEqual([], result)

        result, _ = await self.call('call_imported_from_file_dir', [], return_type=list)
        self.assertEqual([], result)

    def test_import_non_existent_package(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'ImportNonExistentPackage.py')

    async def test_import_interop_with_alias(self):
        await self.set_up_contract('ImportInteropWithAlias.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)
    def test_import_user_module_recursive_import(self):
        self.assertCompilerLogs(CompilerError.CircularImport, 'ImportUserModuleRecursiveImport.py')

    def test_from_import_user_module_recursive_import(self):
        self.assertCompilerLogs(CompilerError.CircularImport, 'FromImportUserModuleRecursiveImport.py')

    async def test_import_user_module_with_not_imported_symbols(self):
        await self.set_up_contract('ImportUserModuleWithNotImportedSymbols.py')

        Notification = annotation.Notification[list[int]]
        script = self.contract_hash
        result, _ = await self.call('main', [[], script], return_type=list)
        self.assertEqual([], result)

        arg = [1, 2, 3]
        expected_result: list[Notification] = [
            (script, 'notify', [x]) for x in arg
        ]
        result, _ = await self.call('main', [arg, script], return_type=list[Notification])
        self.assertEqual(expected_result, result)

        result, _ = await self.call('main', [arg,  b'\x01' * 20], return_type=list[Notification])
        self.assertEqual([], result)

        # 'with_param' is a public method, so it should be included in the manifest when imported
        result, _ = await self.call('with_param', [arg,  b'\x01' * 20], return_type=list[Notification])
        self.assertEqual([], result)

        # 'without_param' is a public method, but it isn't imported, so it shouldn't be included in the manifest
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('without_param', [arg], return_type=list)

        self.assertRegex(str(context.exception), 'method not found: without_param/1')

    def test_import_user_module_with_not_imported_variables_compile(self):
        expected_output = (
            Opcode.CALL
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.RET
            + Opcode.PUSH10    # module function from import
            + Opcode.RET  # return
            + Opcode.PUSH5    # imported function
            + Opcode.RET  # return
        )

        output, _ = self.assertCompile('ImportUserModuleWithNotImportedVariables.py')
        self.assertEqual(expected_output, output)

    def test_import_user_module_with_not_imported_variables_compile_no_optimization(self):
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

        output, _ = self.assertCompile('ImportUserModuleWithNotImportedVariables.py', optimize=False)
        self.assertEqual(expected_output, output)

    async def test_import_user_module_with_not_imported_variables(self):
        await self.set_up_contract('ImportUserModuleWithNotImportedVariables.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(5, result)

    def test_not_imported_builtin_public(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'NotImportedBuiltinPublic.py')

    def test_not_imported_builtin_from_typing(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'NotImportedBuiltinFromTypingInReturn.py')

        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'NotImportedBuiltinFromTypingInArgs.py')

        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'NotImportedBuiltinFromTypingInSubscript.py')

        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'NotImportedBuiltinFromTypingInVariable.py')

    async def test_incorrect_circular_import(self):
        await self.set_up_contract('incorrect_circular_import', 'IncorrectCircularImportDetection.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(3, result)

    async def test_import_module_with_init(self):
        await self.set_up_contract('ImportModuleWithInit.py')

        result, _ = await self.call('call_imported_method', [], return_type=list)
        self.assertEqual([], result)

        result, _ = await self.call('call_imported_variable', [], return_type=int)
        self.assertEqual(42, result)

    async def test_import_module_without_init(self):
        await self.set_up_contract('ImportModuleWithoutInit.py')

        result, _ = await self.call('call_imported_method', [], return_type=dict)
        self.assertEqual({}, result)

        result, _ = await self.call('call_imported_variable', [], return_type=list)
        self.assertEqual([], result)

    async def test_import_user_class_inner_files(self):
        await self.set_up_contract('ImportUserClassInnerFiles.py')
        contract_2 = await self.compile_and_deploy('class_import', 'ImportUserClass.py')

        from boa3_test.test_sc.import_test.class_import.example import Example
        expected_result = Example(42, '42')

        result, _ = await self.call('build_example_object', [], return_type=list,
                                    target_contract=contract_2)
        self.assertObjectEqual(expected_result, result)

        result, _ = await self.call('build_example_object', [], return_type=str)
        self.assertEqual(expected_result.var_str, result)

    def test_from_import_not_existing_method(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'FromImportNotExistingMethod.py')

    def test_import_not_existing_method(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'ImportNotExistingMethod.py')

    def test_import_boa_invalid_package(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'ImportBoaInvalidPackage.py')
