import os
from typing import Dict, Tuple

from boa3_test.tests.boa_test import BoaTest, _COMPILER_LOCK as LOCK  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.compiler.compiler import Compiler
from boa3.internal.exception import CompilerError
from boa3.internal.exception.NotLoadedException import NotLoadedException
from boa3.internal.model.event import Event
from boa3.internal.model.method import Method
from boa3.internal.model.variable import Variable
from boa3.internal.neo.contracts.neffile import NefFile
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.Integer import Integer


class TestFileGeneration(BoaTest):
    default_folder: str = 'test_sc/generation_test'

    def test_generate_files(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        expected_nef_output, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_nef_output))
        self.assertTrue(os.path.exists(expected_manifest_output))

    def test_generate_files_with_debug_info(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        expected_nef_output, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        expected_debug_info_output = expected_nef_output.replace('.nef', '.nefdbgnfo')
        self.compile_and_save(path, debug=True)

        self.assertTrue(os.path.exists(expected_nef_output))
        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertTrue(os.path.exists(expected_debug_info_output))

    def test_generate_nef_file(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        expected_nef_output, _ = self.get_deploy_file_paths_without_compiling(path)
        self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_nef_output))
        with open(expected_nef_output, 'rb') as nef_output:
            magic = nef_output.read(constants.SIZE_OF_INT32)
            compiler = nef_output.read(64)
            compiler = compiler.replace(b'\x00', b'')

            nef_output.read(2)  # reserved

            method_token_count = nef_output.read(1)
            self.assertEqual(Integer.from_bytes(method_token_count), 0)

            nef_output.read(2)  # reserved

            script_size = nef_output.read(1)
            script = nef_output.read(Integer.from_bytes(script_size))
            check_sum = Integer.from_bytes(nef_output.read(constants.SIZE_OF_INT32))

        self.assertEqual(Integer.from_bytes(script_size), len(script))

        nef = NefFile(script)._nef
        self.assertEqual(compiler.decode(constants.ENCODING), nef.compiler)
        self.assertEqual(check_sum, nef.checksum)

    def test_generate_manifest_file_with_decorator(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertNotIn('entrypoint', abi)
        self.assertIn('methods', abi)
        self.assertEqual(2, len(abi['methods']))

        # method Main
        method0 = abi['methods'][0]
        self.assertIn('returntype', method0)
        self.assertEqual(AbiType.Integer, method0['returntype'])
        self.assertIn('parameters', method0)
        self.assertEqual(2, len(method0['parameters']))

        arg0 = method0['parameters'][0]
        self.assertIn('name', arg0)
        self.assertEqual('a', arg0['name'])
        self.assertIn('type', arg0)
        self.assertEqual(AbiType.Integer, arg0['type'])

        arg1 = method0['parameters'][1]
        self.assertIn('name', arg1)
        self.assertEqual('b', arg1['name'])
        self.assertIn('type', arg1)
        self.assertEqual(AbiType.Integer, arg1['type'])

        # method Sub
        method1 = abi['methods'][1]
        self.assertIn('returntype', method1)
        self.assertEqual(AbiType.Integer, method1['returntype'])
        self.assertIn('parameters', method1)
        self.assertEqual(2, len(method1['parameters']))

        arg0 = method1['parameters'][0]
        self.assertIn('name', arg0)
        self.assertEqual('a', arg0['name'])
        self.assertIn('type', arg0)
        self.assertEqual(AbiType.Integer, arg0['type'])

        arg1 = method1['parameters'][1]
        self.assertIn('name', arg1)
        self.assertEqual('b', arg1['name'])
        self.assertIn('type', arg1)
        self.assertEqual(AbiType.Integer, arg1['type'])

        self.assertIn('events', abi)
        self.assertEqual(0, len(abi['events']))

    def test_generate_manifest_file_without_decorator(self):
        path = self.get_contract_path('GenerationWithoutDecorator.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(1, len(abi['methods']))

        self.assertIn('events', abi)
        self.assertEqual(0, len(abi['events']))

    def test_generate_manifest_file_with_event(self):
        path = self.get_contract_path('test_sc/event_test', 'EventWithArgument.py')
        nef_output, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output)

            events: Dict[str, Event] = {
                name: method
                for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
                if isinstance(method, Event)
            }

            output, manifest = self.get_output(nef_output)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(1, len(abi['methods']))

        self.assertIn('events', abi)
        self.assertEqual(1, len(abi['events']))

        for abi_event in abi['events']:
            self.assertIn('name', abi_event)
            self.assertIn(abi_event['name'], events)
            self.assertIn('parameters', abi_event)

            event_args = events[abi_event['name']].args
            for event_param in abi_event['parameters']:
                self.assertIn('name', event_param)
                self.assertIn(event_param['name'], event_args)
                self.assertIn('type', event_param)
                self.assertEqual(event_args[event_param['name']].type.abi_type,
                                 event_param['type'])

    def test_generate_manifest_file_with_imported_event(self):
        path = self.get_contract_path('GenerationWithImportedEvent.py')
        nef_output, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output)

            events: Dict[str, Event] = {}
            for name, method in self.get_compiler_analyser(compiler).symbol_table.items():
                if isinstance(method, Event):
                    events[name] = method
                    if method.name not in events:
                        events[method.name] = method

            output, manifest = self.get_output(nef_output)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('events', abi)
        self.assertEqual(1, len(abi['events']))

        for abi_event in abi['events']:
            self.assertIn('name', abi_event)
            self.assertIn(abi_event['name'], events)
            self.assertIn('parameters', abi_event)
            event_args = events[abi_event['name']].args
            for event_param in abi_event['parameters']:
                self.assertIn('name', event_param)
                self.assertIn(event_param['name'], event_args)
                self.assertIn('type', event_param)
                self.assertEqual(event_args[event_param['name']].type.abi_type,
                                 event_param['type'])

    def test_generate_manifest_file_with_public_name_decorator_kwarg(self):
        path = self.get_contract_path('MetadataMethodName.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(2, len(abi['methods']))

        # method Main named as Add
        method0 = abi['methods'][0]
        self.assertIn('name', method0)
        self.assertEqual('Add', method0['name'])

    def test_generate_manifest_file_with_public_name_decorator_arg(self):
        path = self.get_contract_path('MetadataMethodNameArg.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(2, len(abi['methods']))

        # method Main named as Add
        method0 = abi['methods'][0]
        self.assertIn('name', method0)
        self.assertEqual('Add', method0['name'])

    def test_metadata_abi_method_name_mismatched_type(self):
        path = self.get_contract_path('MetadataMethodNameMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_metadata_abi_method_with_duplicated_name_but_different_args(self):
        path = self.get_contract_path('MetadataMethodDuplicatedNameDifferentArgs.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(3, len(abi['methods']))

        # method Inc named as Add
        method0 = abi['methods'][0]
        self.assertIn('name', method0)
        self.assertEqual('Add', method0['name'])
        self.assertIn('parameters', method0)
        self.assertEqual(1, len(method0['parameters']))

        # method Add also named as Add, but with different arg count
        method1 = abi['methods'][1]
        self.assertIn('name', method1)
        self.assertEqual('Add', method1['name'])
        self.assertIn('parameters', method1)
        self.assertEqual(2, len(method1['parameters']))

    def test_metadata_abi_method_with_duplicated_name_and_args(self):
        path = self.get_contract_path('MetadataMethodDuplicatedNameAndArgs.py')
        self.assertCompilerLogs(CompilerError.DuplicatedManifestIdentifier, path)

    def test_generate_manifest_file_with_public_safe_decorator_kwarg(self):
        path = self.get_contract_path('MetadataMethodSafe.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(2, len(abi['methods']))

        # method Main
        method0 = abi['methods'][0]
        self.assertIn('safe', method0)
        self.assertEqual(True, method0['safe'])

    def test_generate_manifest_file_with_public_safe_decorator_arg(self):
        path = self.get_contract_path('MetadataMethodSafeArg.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(2, len(abi['methods']))

        # method Main named as Add
        method0 = abi['methods'][0]
        self.assertIn('name', method0)
        self.assertEqual('Add', method0['name'])
        self.assertIn('safe', method0)
        self.assertEqual(True, method0['safe'])

    def test_generate_manifest_file_with_unused_event(self):
        path = self.get_contract_path('MetadataUnusedEvent.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(1, len(abi['methods']))

        # notify and uncalled_event shouldn't be added on the abi, because they were not called
        self.assertIn('events', abi)
        self.assertEqual(1, len(abi['events']))

        event = abi['events'][0]
        self.assertIn('name', event)
        self.assertEqual('CalledEvent', event['name'])
        self.assertIn('parameters', event)
        self.assertEqual(3, len(event['parameters']))
        parameters = event['parameters']
        self.assertEqual(('var4', 'Integer'), (parameters[0]['name'], parameters[0]['type']))
        self.assertEqual(('var5', 'String'), (parameters[1]['name'], parameters[1]['type']))
        self.assertEqual(('var6', 'ByteArray'), (parameters[2]['name'], parameters[2]['type']))

    def test_metadata_abi_method_safe_mismatched_type(self):
        path = self.get_contract_path('MetadataMethodSafeMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_generate_nefdbgnfo_file(self):
        from boa3.internal.model.type.itype import IType
        path = self.get_contract_path('GenerationWithDecorator.py')
        nef_output, _ = self.get_deploy_file_paths(path)
        expected_debug_info_output = nef_output.replace('.nef', '.nefdbgnfo')

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output, debug=True)

            methods: Dict[str, Method] = {
                name: method
                for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
                if isinstance(method, Method)
            }

            debug_info = self.get_debug_info(nef_output)

        self.assertTrue(os.path.exists(expected_debug_info_output))
        self.assertIn('entrypoint', debug_info)
        self.assertEqual(path, debug_info['entrypoint'])
        self.assertIn('methods', debug_info)
        self.assertGreater(len(debug_info['methods']), 0)

        for debug_method in debug_info['methods']:
            self.assertIn('name', debug_method)
            parsed_name = debug_method['name'].split(constants.VARIABLE_NAME_SEPARATOR)
            self.assertEqual(2, len(parsed_name))
            self.assertIn(parsed_name[-1], methods)
            actual_method = methods[parsed_name[-1]]

            # validate id
            self.assertIn('id', debug_method)
            self.assertEqual(str(id(actual_method)), debug_method['id'])

            # validate parameters
            self.assertIn('params', debug_method)
            self.assertEqual(len(actual_method.args), len(debug_method['params']))
            for var in debug_method['params']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                param_id, param_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(param_id, actual_method.args)
                self.assertEqual(param_type, actual_method.args[param_id].type.abi_type)

            # validate local variables
            self.assertIn('variables', debug_method)
            self.assertEqual(len(actual_method.locals), len(debug_method['variables']))
            for var in debug_method['variables']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                var_id, var_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(var_id, actual_method.locals)
                local_type = actual_method.locals[var_id].type
                self.assertEqual(local_type.abi_type if isinstance(local_type, IType) else AbiType.Any, var_type)

    def test_generate_nefdbgnfo_file_with_event(self):
        path = self.get_contract_path('test_sc/event_test', 'EventWithArgument.py')
        nef_output, _ = self.get_deploy_file_paths(path)
        expected_debug_info_output = nef_output.replace('.nef', '.nefdbgnfo')

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output, debug=True)

            events: Dict[str, Event] = {
                name: method
                for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
                if isinstance(method, Event)
            }

            debug_info = self.get_debug_info(nef_output)

        self.assertTrue(os.path.exists(expected_debug_info_output))
        self.assertIn('entrypoint', debug_info)
        self.assertEqual(path, debug_info['entrypoint'])
        self.assertIn('events', debug_info)
        self.assertGreater(len(debug_info['events']), 0)

        for debug_event in debug_info['events']:
            self.assertIn('name', debug_event)
            parsed_name = debug_event['name'].split(constants.VARIABLE_NAME_SEPARATOR)
            self.assertEqual(2, len(parsed_name))
            self.assertIn(parsed_name[-1], events)
            actual_event = events[parsed_name[-1]]

            # validate id
            self.assertIn('id', debug_event)
            self.assertEqual(str(id(actual_event)), debug_event['id'])

            # validate parameters
            self.assertIn('params', debug_event)
            self.assertEqual(len(actual_event.args), len(debug_event['params']))
            for var in debug_event['params']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                param_id, param_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(param_id, actual_event.args)
                self.assertEqual(param_type, actual_event.args[param_id].type.abi_type)

    def test_generate_nefdbgnfo_file_with_static_variables(self):
        path = self.get_contract_path('GenerationWithStaticVariables.py')
        nef_output, _ = self.get_deploy_file_paths(path)
        expected_debug_info_output = nef_output.replace('.nef', '.nefdbgnfo')

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output, debug=True)

            variables: Dict[str, Method] = {
                name: method
                for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
                if isinstance(method, Variable)
            }

            debug_info = self.get_debug_info(nef_output)

        self.assertTrue(os.path.exists(expected_debug_info_output))
        self.assertIn('entrypoint', debug_info)
        self.assertEqual(path, debug_info['entrypoint'])
        self.assertIn('static-variables', debug_info)
        self.assertGreater(len(debug_info['static-variables']), 0)

        for static_variable in debug_info['static-variables']:
            # validate parameters
            self.assertEqual(3, len(static_variable.split(constants.VARIABLE_NAME_SEPARATOR)))
            var_id, var_type, var_slot = static_variable.split(constants.VARIABLE_NAME_SEPARATOR)
            if var_id not in variables:
                self.assertIn(var_id, [var_full_id.split(constants.VARIABLE_NAME_SEPARATOR)[-1]
                                       for var_full_id in variables])
                var_inner_id = next((var for var in variables
                                     if var.split(constants.VARIABLE_NAME_SEPARATOR)[-1] == var_id),
                                    var_id)
            else:
                var_inner_id = var_id

            self.assertIn(var_inner_id, variables)
            self.assertEqual(var_type, variables[var_inner_id].type.abi_type)

    def test_generate_nefdbgnfo_file_with_user_module_import(self):
        from boa3.internal.model.type.itype import IType
        path = self.get_contract_path('GenerationWithUserModuleImports.py')
        nef_output, _ = self.get_deploy_file_paths(path)
        expected_debug_output = nef_output.replace('.nef', '.nefdbgnfo')

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output, debug=True)

            methods: Dict[str, Method] = {
                name: method
                for name, method in self.get_all_imported_methods(compiler).items()
                if isinstance(method, Method)
            }

            debug_info = self.get_debug_info(nef_output)

        self.assertTrue(os.path.exists(expected_debug_output))
        self.assertIn('entrypoint', debug_info)
        self.assertEqual(debug_info['entrypoint'], path)
        self.assertIn('methods', debug_info)
        self.assertGreater(len(debug_info['methods']), 0)

        for debug_method in debug_info['methods']:
            self.assertIn('name', debug_method)
            name_without_parsing = debug_method['name']
            parsed_name = name_without_parsing.split(constants.VARIABLE_NAME_SEPARATOR)
            self.assertEqual(2, len(parsed_name))
            self.assertIn(name_without_parsing, methods)
            actual_method = methods[name_without_parsing]

            # validate id
            self.assertIn('id', debug_method)
            self.assertEqual(str(id(actual_method)), debug_method['id'])

            # validate parameters
            self.assertIn('params', debug_method)
            self.assertEqual(len(actual_method.args), len(debug_method['params']))
            for var in debug_method['params']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                param_id, param_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(param_id, actual_method.args)
                self.assertEqual(param_type, actual_method.args[param_id].type.abi_type)

            # validate local variables
            self.assertIn('variables', debug_method)
            self.assertEqual(len(actual_method.locals), len(debug_method['variables']))
            for var in debug_method['variables']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                var_id, var_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(var_id, actual_method.locals)
                local_type = actual_method.locals[var_id].type
                self.assertEqual(local_type.abi_type if isinstance(local_type, IType) else AbiType.Any, var_type)

    def test_generate_nefdbgnfo_file_with_user_module_name_import(self):
        from boa3.internal.model.type.itype import IType
        path = self.get_contract_path('test_sc/import_test', 'ImportModuleWithoutInit.py')
        imported_path = self.get_contract_path('test_sc/import_test/sample_package/package', 'another_module.py')
        nef_output, _ = self.get_deploy_file_paths(path)
        expected_debug_output = nef_output.replace('.nef', '.nefdbgnfo')

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output, debug=True)

            methods: Dict[str, Method] = {
                name: method
                for name, method in self.get_all_imported_methods(compiler).items()
                if isinstance(method, Method)
            }

            debug_info = self.get_debug_info(nef_output)

        self.assertTrue(os.path.exists(expected_debug_output))
        self.assertIn('entrypoint', debug_info)
        self.assertEqual(debug_info['entrypoint'], path)

        self.assertIn('documents', debug_info)
        self.assertGreater(len(debug_info['documents']), 1)
        self.assertIn(imported_path, debug_info['documents'])

        self.assertIn('methods', debug_info)
        self.assertGreater(len(debug_info['methods']), 0)

        for debug_method in debug_info['methods']:
            self.assertIn('name', debug_method)
            name_without_parsing = debug_method['name']
            parsed_name = name_without_parsing.split(constants.VARIABLE_NAME_SEPARATOR)
            self.assertEqual(2, len(parsed_name))
            self.assertIn(name_without_parsing, methods)
            actual_method = methods[name_without_parsing]

            # validate id
            self.assertIn('id', debug_method)
            self.assertEqual(str(id(actual_method)), debug_method['id'])

            # validate parameters
            self.assertIn('params', debug_method)
            self.assertEqual(len(actual_method.args), len(debug_method['params']))
            for var in debug_method['params']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                param_id, param_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(param_id, actual_method.args)
                self.assertEqual(param_type, actual_method.args[param_id].type.abi_type)

            # validate local variables
            self.assertIn('variables', debug_method)
            self.assertEqual(len(actual_method.locals), len(debug_method['variables']))
            for var in debug_method['variables']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                var_id, var_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(var_id, actual_method.locals)
                local_type = actual_method.locals[var_id].type
                self.assertEqual(local_type.abi_type if isinstance(local_type, IType) else AbiType.Any, var_type)

    def test_generate_manifest_file_with_notify_event(self):
        path = self.get_contract_path('test_sc/interop_test/runtime', 'NotifySequence.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('events', abi)
        self.assertGreater(len(abi['events']), 0)

        notify_event = next(abi_event for abi_event in abi['events']
                            if 'name' in abi_event and abi_event['name'] == 'notify')
        self.assertIsNotNone(notify_event, "notify event is not listed in the contract's abi")
        self.assertIn('parameters', notify_event)
        self.assertEqual(1, len(notify_event['parameters']))
        self.assertIn('type', notify_event['parameters'][0])
        self.assertEqual(AbiType.Any, notify_event['parameters'][0]['type'])

    def test_generate_without_main(self):
        path = self.get_contract_path('GenerationWithoutMain.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertNotIn('entryPoint', abi)
        self.assertIn('methods', abi)
        self.assertEqual(2, len(abi['methods']))

        self.assertIn('events', abi)
        self.assertEqual(0, len(abi['events']))

    def test_generate_without_main_and_public_methods(self):
        # since 0.11.2 methods that are not public nor are called are not generated to optimize code
        # this test generates an empty contract, which results in failing compilation
        path = self.get_contract_path('GenerationWithoutMainAndPublicMethods.py')

        with self.assertRaises(NotLoadedException):
            output, manifest = self.compile_and_save(path)

    def test_generate_manifest_file_abi_method_offset(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        nef_output, manifest_path = self.get_deploy_file_paths_without_compiling(path)

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output)

            methods: Dict[str, Method] = {
                name: method
                for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
                if isinstance(method, Method)
            }

            output, manifest = self.get_output(nef_output)

        self.assertTrue(os.path.exists(manifest_path))
        self.assertGreater(len(methods), 0)
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        abi_methods = abi['methods']
        self.assertGreater(len(abi['methods']), 0)

        for method in abi_methods:
            self.assertIn('name', method)
            self.assertIn('offset', method)
            self.assertIn(method['name'], methods)
            self.assertEqual(method['offset'], methods[method['name']].start_address)

    def test_generate_debug_info_with_multiple_flows(self):
        path = self.get_contract_path('GenerationWithMultipleFlows.py')
        nef_output, _ = self.get_deploy_file_paths_without_compiling(path)

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output, debug=True)

            methods: Dict[str, Method] = {
                name: method
                for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
                if isinstance(method, Method)
            }

            debug_info = self.get_debug_info(nef_output)

        self.assertGreater(len(methods), 0)
        self.assertIn('methods', debug_info)
        self.assertGreater(len(debug_info['methods']), 0)

        for debug_method in debug_info['methods']:
            self.assertIn('name', debug_method)
            parsed_name = debug_method['name'].split(constants.VARIABLE_NAME_SEPARATOR)
            self.assertEqual(2, len(parsed_name))
            self.assertIn(parsed_name[-1], methods)
            actual_method = methods[parsed_name[-1]]

            # validate id
            self.assertIn('id', debug_method)
            self.assertEqual(str(id(actual_method)), debug_method['id'])

            # validate parameters
            self.assertIn('params', debug_method)
            self.assertEqual(len(actual_method.args), len(debug_method['params']))
            for var in debug_method['params']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                param_id, param_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(param_id, actual_method.args)
                self.assertEqual(param_type, actual_method.args[param_id].type.abi_type)

            # validate local variables
            self.assertIn('variables', debug_method)
            self.assertEqual(len(actual_method.locals), len(debug_method['variables']))
            for var in debug_method['variables']:
                self.assertEqual(2, len(var.split(constants.VARIABLE_NAME_SEPARATOR)))
                var_id, var_type = var.split(constants.VARIABLE_NAME_SEPARATOR)
                self.assertIn(var_id, actual_method.locals)
                self.assertEqual(actual_method.locals[var_id].type.abi_type, var_type)

    def test_generate_init_method(self):
        path = self.get_contract_path('test_sc/variable_test', 'GlobalAssignmentWithType.py')
        nef_output, _ = self.get_deploy_file_paths_without_compiling(path)

        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output, debug=True)

            methods: Dict[str, Method] = {
                name: method
                for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
                if isinstance(method, Method)
            }

            output, manifest = self.get_output(nef_output)

        self.assertGreater(len(methods), 0)
        self.assertIn(constants.INITIALIZE_METHOD_ID, methods)
        init_method = methods[constants.INITIALIZE_METHOD_ID]

        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertGreater(len(abi['methods']), 0)

        abi_init = next(method for method in abi['methods']
                        if 'name' in method and method['name'] == constants.INITIALIZE_METHOD_ID)
        self.assertIsNotNone(abi_init)
        self.assertIn('offset', abi_init)
        self.assertEqual(init_method.start_address, abi_init['offset'])
        self.assertIn('parameters', abi_init)
        self.assertEqual(0, len(abi_init['parameters']))
        self.assertIn('returntype', abi_init)
        self.assertEqual(AbiType.Void, abi_init['returntype'])

        debug_info = self.get_debug_info(nef_output)
        self.assertIn('methods', debug_info)
        self.assertGreater(len(debug_info['methods']), 0)

        debug_method = next((method for method in debug_info['methods']
                             if 'id' in method and method['id'] == str(id(init_method))), None)
        self.assertIsNotNone(debug_method)
        parsed_name = debug_method['name'].split(constants.VARIABLE_NAME_SEPARATOR)
        self.assertEqual(2, len(parsed_name))
        self.assertIn(parsed_name[-1], methods)

        # validate parameters
        self.assertIn('params', debug_method)
        self.assertEqual(0, len(debug_method['params']))

        # validate local variables
        self.assertIn('variables', debug_method)
        self.assertEqual(0, len(debug_method['variables']))

        # validate sequence points
        self.assertIn('sequence-points', debug_method)
        self.assertEqual(0, len(debug_method['sequence-points']))

    def test_generate_with_user_module_import(self):
        path = self.get_contract_path('GenerationWithUserModuleImports.py')
        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertNotIn('entryPoint', abi)
        self.assertIn('methods', abi)
        self.assertEqual(2, len(abi['methods']))

        self.assertIn('events', abi)
        self.assertEqual(1, len(abi['events']))

    def test_generate_with_user_module_import_with_project_root(self):
        path = self.get_contract_path('project_path', 'GenerationWithUserModuleImportsFromProjectRoot.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

        _, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        output, manifest = self.compile_and_save(path, root_folder=self.get_dir_path(self.default_test_folder))

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertNotIn('entryPoint', abi)
        self.assertIn('methods', abi)
        self.assertEqual(2, len(abi['methods']))

        self.assertIn('events', abi)
        self.assertEqual(1, len(abi['events']))

    def test_compiler_error(self):
        path = self.get_contract_path('test_sc/built_in_methods_test', 'ClearTooManyParameters.py')

        with self.assertRaises(NotLoadedException):
            self.compile(path)

        with self.assertRaises(NotLoadedException):
            from boa3.boa3 import Boa3

            with LOCK:
                Boa3.compile_and_save(path)

        with self.assertRaises(NotLoadedException):
            self.compile_and_save(path)

    def test_generation_with_recursive_function(self):
        path, _ = self.get_deploy_file_paths('test_sc/function_test', 'RecursiveFunction.py')

        from boa3.internal.neo3.vm import VMState
        from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner
        runner = BoaTestRunner(runner_id=self.method_name())

        expected = self.fact(57)
        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.cli_log)
        self.assertEqual(expected, invoke.result)

    def fact(self, f: int) -> int:
        if f <= 1:
            return 1
        return f * self.fact(f - 1)

    def test_generate_manifest_file_with_type_hint_list(self):
        path = self.get_contract_path('test_sc/list_test', 'CopyBool.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        abi_method_main = abi_methods[0]
        self.assertEqual('Array', abi_method_main['returntype'])
        self.assertIn('returngeneric', abi_method_main)
        self.assertIn('type', abi_method_main['returngeneric'])
        self.assertEqual('Array', abi_method_main['returngeneric']['type'])
        self.assertIn('generic', abi_method_main['returngeneric'])
        self.assertIn('type', abi_method_main['returngeneric']['generic'])

        abi_method_main_parameters = abi_method_main['parameters']
        self.assertIn('generic', abi_method_main_parameters[0])
        self.assertIn('type', abi_method_main_parameters[0]['generic'])

    def test_generate_manifest_file_with_type_hint_dict(self):
        path = self.get_contract_path('test_sc/dict_test', 'SetValue.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        abi_method_main = abi_methods[0]
        self.assertEqual('Map', abi_method_main['returntype'])
        self.assertIn('returngenerickey', abi_method_main)
        self.assertIn('type', abi_method_main['returngenerickey'])
        self.assertIn('returngenericitem', abi_method_main)
        self.assertIn('type', abi_method_main['returngenericitem'])

        abi_method_main_parameters = abi_method_main['parameters']
        self.assertIn('generickey', abi_method_main_parameters[0])
        self.assertIn('type', abi_method_main_parameters[0]['generickey'])
        self.assertIn('genericitem', abi_method_main_parameters[0])
        self.assertIn('type', abi_method_main_parameters[0]['genericitem'])

    def test_generate_manifest_file_with_type_hint_union_return(self):
        path = self.get_contract_path('test_sc/union_test', 'UnionReturn.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        abi_method_main = abi_methods[0]
        self.assertEqual('Any', abi_method_main['returntype'])
        self.assertIn('returnunion', abi_method_main)
        self.assertIsInstance(abi_method_main['returnunion'], list)
        for union_type in abi_method_main['returnunion']:
            self.assertIn('type', union_type)

    def test_generate_manifest_file_with_type_hint_union_args(self):
        path = self.get_contract_path('test_sc/union_test', 'UnionIsInstanceValidation.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        abi_method_main = abi_methods[0]
        abi_method_main_parameters = abi_method_main['parameters']
        self.assertIn('union', abi_method_main_parameters[0])
        self.assertIsInstance(abi_method_main_parameters[0]['union'], list)
        for union_type in abi_method_main_parameters[0]['union']:
            self.assertIn('type', union_type)

    def test_generate_manifest_file_with_type_hint_optional(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintOptional.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        abi_method_main = abi_methods[0]
        self.assertEqual('Integer', abi_method_main['returntype'])
        self.assertIn('returnnullable', abi_method_main)

        abi_method_main_parameters = abi_method_main['parameters']
        self.assertIn('nullable', abi_method_main_parameters[0])
        self.assertIn('union', abi_method_main_parameters[0])
        self.assertIsInstance(abi_method_main_parameters[0]['union'], list)
        for union_type in abi_method_main_parameters[0]['union']:
            self.assertIn('type', union_type)

    def test_generate_manifest_file_with_type_hint_storage_context(self):
        path = self.get_contract_path('test_sc/interop_test/storage', 'StorageGetContext.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        abi_method_main = abi_methods[0]
        self.assertEqual('InteropInterface', abi_method_main['returntype'])
        self.assertIn('returnhint', abi_method_main)
        self.assertEqual(abi_method_main['returnhint'], 'StorageContext')

    def test_generate_manifest_file_with_type_hint_iterator(self):
        path = self.get_contract_path('test_sc/interop_test/iterator', 'ImportIterator.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        abi_method_main = abi_methods[0]
        self.assertEqual('InteropInterface', abi_method_main['returntype'])
        self.assertIn('returnhint', abi_method_main)
        self.assertEqual(abi_method_main['returnhint'], 'Iterator')

    def test_generate_manifest_file_with_type_hint_address(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintAddress.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import AddressType
        self.assertIsInstance(method_main.return_type, AddressType)

        abi_method_main = abi_methods[0]
        self.assertEqual(abi_method_main['returntype'], 'String')
        self.assertIn('returnhint', abi_method_main)
        self.assertEqual(abi_method_main['returnhint'], 'Address')

    def test_generate_manifest_file_with_type_hint_str_to_address(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintFromStrToAddress.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import AddressType
        self.assertIsInstance(method_main.return_type, AddressType)

    def test_generate_manifest_file_with_type_hint_blockhash(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintBlockHash.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import BlockHashType
        self.assertIsInstance(method_main.return_type, BlockHashType)

        abi_method_main = abi_methods[0]
        self.assertEqual(abi_method_main['returntype'], 'Hash256')
        self.assertIn('returnhint', abi_method_main)
        self.assertEqual(abi_method_main['returnhint'], 'BlockHash')

    def test_generate_manifest_file_with_type_hint_uint256_to_blockhash(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintFromUInt256ToBlockHash.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import BlockHashType
        self.assertIsInstance(method_main.return_type, BlockHashType)

    def test_generate_manifest_file_with_type_hint_publickey(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintPublicKey.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import PublicKeyType
        self.assertIsInstance(method_main.return_type, PublicKeyType)

        abi_method_main = abi_methods[0]
        self.assertEqual(abi_method_main['returntype'], 'PublicKey')
        # 'PublicKey' already is a abi type, so there is no need to use a 'returnhint'
        self.assertNotIn('returnhint', abi_method_main)

    def test_generate_manifest_file_with_type_hint_ecpoint_to_publickey(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintFromECPointToPublicKey.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)  # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import PublicKeyType
        self.assertIsInstance(method_main.return_type, PublicKeyType)

    def test_generate_manifest_file_with_type_hint_scripthash(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintScriptHash.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import ScriptHashType
        self.assertIsInstance(method_main.return_type, ScriptHashType)

        abi_method_main = abi_methods[0]
        self.assertEqual(abi_method_main['returntype'], 'Hash160')
        self.assertIn('returnhint', abi_method_main)
        self.assertEqual(abi_method_main['returnhint'], 'ScriptHash')

    def test_generate_manifest_file_with_type_hint_uint160_to_scripthash(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintFromUInt160ToScriptHash.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import ScriptHashType
        self.assertIsInstance(method_main.return_type, ScriptHashType)

    def test_generate_manifest_file_with_type_hint_scripthashlittleendian(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintScriptHashLittleEndian.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import ScriptHashLittleEndianType
        self.assertIsInstance(method_main.return_type, ScriptHashLittleEndianType)

        abi_method_main = abi_methods[0]
        self.assertEqual(abi_method_main['returntype'], 'Hash160')
        self.assertIn('returnhint', abi_method_main)
        self.assertEqual(abi_method_main['returnhint'], 'ScriptHashLittleEndian')

    def test_generate_manifest_file_with_type_hint_uint160_to_scripthashlittleendian(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintFromUInt160ToScriptHashLittleEndian.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import ScriptHashLittleEndianType
        self.assertIsInstance(method_main.return_type, ScriptHashLittleEndianType)

    def test_generate_manifest_file_with_type_hint_transactionid(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintTransactionId.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import TransactionIdType
        self.assertIsInstance(method_main.return_type, TransactionIdType)

        abi_method_main = abi_methods[0]
        self.assertEqual(abi_method_main['returntype'], 'Hash256')
        self.assertIn('returnhint', abi_method_main)
        self.assertEqual(abi_method_main['returnhint'], 'TransactionId')

    def test_generate_manifest_file_with_type_hint_uint256_to_transactionid(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintFromUInt256ToTransactionId.py')
        methods, abi_methods = self.verify_parameters_and_return_manifest(path)     # type: dict, list

        method_main: Method = methods[abi_methods[0]['name']]

        from boa3.internal.model.type.neo import TransactionIdType
        self.assertIsInstance(method_main.return_type, TransactionIdType)

    def test_generate_manifest_file_with_type_hint_any(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintAny.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)  # type: dict, list

        abi_method_main = abi_methods[0]
        self.assertEqual(abi_method_main['returntype'], 'Any')
        # verifying if 'returnunion' was not wrongfully added to the manifest
        self.assertNotIn('returnunion', abi_method_main)

    def test_generate_manifest_file_with_type_hint_maps_array_union_hint(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintMapsArraysUnionHint.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)  # type: dict, list

        abi_method_main = abi_methods[0]
        abi_method_main_parameter = abi_method_main['parameters'][0]

        # verifying arg type
        self.assertEqual('Map', abi_method_main_parameter['type'])
        self.assertIn('generickey', abi_method_main_parameter)
        self.assertIn('type', abi_method_main_parameter['generickey'])
        self.assertEqual('String', abi_method_main_parameter['generickey']['type'])
        self.assertIn('genericitem', abi_method_main_parameter)
        self.assertIn('type', abi_method_main_parameter['genericitem'])
        self.assertEqual('Array', abi_method_main_parameter['genericitem']['type'])
        self.assertIn('generic', abi_method_main_parameter['genericitem'])
        self.assertIn('type', abi_method_main_parameter['genericitem']['generic'])

        # verifying return type
        self.assertEqual('Array', abi_method_main['returntype'])
        self.assertIn('returngeneric', abi_method_main)
        self.assertIn('type', abi_method_main['returngeneric'])
        self.assertEqual('Any', abi_method_main['returngeneric']['type'])
        self.assertIn('union', abi_method_main['returngeneric'])
        self.assertEqual(3, len(abi_method_main['returngeneric']['union']))
        self.assertTrue(any(
            union_type['type'] == 'Map' and 'generickey' in union_type and 'genericitem' in union_type
            for union_type in abi_method_main['returngeneric']['union']
        ))

    def test_generate_manifest_file_with_type_hint_list_and_dict_not_from_typing(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestTypeHintListDictNotFromTyping.py')
        _, abi_methods = self.verify_parameters_and_return_manifest(path)  # type: dict, list

        abi_method_main = abi_methods[0]
        abi_method_main_parameter = abi_method_main['parameters'][0]

        # verifying arg type
        self.assertEqual('Map', abi_method_main_parameter['type'])
        self.assertIn('generickey', abi_method_main_parameter)
        self.assertIn('type', abi_method_main_parameter['generickey'])
        self.assertEqual('Any', abi_method_main_parameter['generickey']['type'])
        self.assertIn('genericitem', abi_method_main_parameter)
        self.assertIn('type', abi_method_main_parameter['genericitem'])
        self.assertEqual('Any', abi_method_main_parameter['genericitem']['type'])

        # verifying return type
        self.assertEqual('Array', abi_method_main['returntype'])
        self.assertIn('returngeneric', abi_method_main)
        self.assertIn('type', abi_method_main['returngeneric'])
        self.assertEqual('Any', abi_method_main['returngeneric']['type'])

    def verify_parameters_and_return_manifest(self, path: str) -> Tuple[dict, list]:
        nef_output, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output)

            methods: Dict[str, Event] = {
                name: method
                for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
                if isinstance(method, Method)
            }

            output, manifest = self.get_output(nef_output)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)

        for abi_method in abi['methods']:
            self.assertIn('name', abi_method)
            self.assertIn(abi_method['name'], abi_method['name'])
            self.assertIn('parameters', abi_method)

            method_args = methods[abi_method['name']].args
            for abi_method_param in abi_method['parameters']:
                self.assertIn('name', abi_method_param)
                self.assertIn(abi_method_param['name'], method_args)

            self.assertIn('returntype', abi_method)

        return methods, abi['methods']

    def test_event_runtime_notify_manifest(self):
        path = self.get_contract_path('ManifestEventRuntimeNotify.py')
        nef_output, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output)
            _, manifest = self.get_output(nef_output)

        self.assertTrue(len(manifest['abi']['events']) > 0)
        self.assertEqual('notify', manifest['abi']['events'][0]['name'])

    def test_manifest_optional_union_eventsd(self):
        path = self.get_contract_path('test_sc/generation_test', 'ManifestOptionalUnionEvent.py')
        nef_output, expected_manifest_output = self.get_deploy_file_paths_without_compiling(path)
        compiler = Compiler()
        with LOCK:
            compiler.compile_and_save(path, nef_output)
            _, manifest = self.get_output(nef_output)

        self.assertEqual(manifest['abi']['events'][0]['parameters'][0]['type'], 'String')
        self.assertEqual(manifest['abi']['events'][0]['parameters'][1]['type'], 'Integer')
