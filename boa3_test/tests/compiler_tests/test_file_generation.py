import os
from typing import Dict

from boa3 import constants
from boa3.boa3 import Boa3
from boa3.compiler.compiler import Compiler
from boa3.constants import BYTEORDER, ENCODING
from boa3.exception.NotLoadedException import NotLoadedException
from boa3.model.event import Event
from boa3.model.method import Method
from boa3.neo.contracts.neffile import NefFile
from boa3.neo.vm.type.AbiType import AbiType
from boa3_test.tests.boa_test import BoaTest


class TestFileGeneration(BoaTest):

    default_folder: str = 'test_sc/generation_test'

    def test_generate_files(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        expected_nef_output = path.replace('.py', '.nef')
        expected_manifest_output = path.replace('.py', '.manifest.json')
        expected_debug_info_output = path.replace('.py', '.nefdbgnfo')
        Boa3.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_nef_output))
        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertTrue(os.path.exists(expected_debug_info_output))

    def test_generate_nef_file(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        expected_nef_output = path.replace('.py', '.nef')
        Boa3.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_nef_output))
        with open(expected_nef_output, 'rb') as nef_output:
            magic = nef_output.read(constants.SIZE_OF_INT32)
            compiler_with_version = nef_output.read(64)
            compiler, version = compiler_with_version.rsplit(b'-', maxsplit=1)
            version = version[:32]

            nef_output.read(2)  # reserved
            nef_output.read(1)  # TODO: method tokens
            nef_output.read(2)  # reserved

            script_size = nef_output.read(1)
            script = nef_output.read(int.from_bytes(script_size, BYTEORDER))
            check_sum = nef_output.read(constants.SIZE_OF_INT32)

        self.assertEqual(int.from_bytes(script_size, BYTEORDER), len(script))

        nef = NefFile(script)._nef
        self.assertEqual(compiler.decode(ENCODING), nef.compiler)
        self.assertEqual(check_sum, nef.checksum)
        self.assertEqual(version, nef.version.to_array())

    def test_generate_manifest_file_with_decorator(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        expected_manifest_output = path.replace('.py', '.manifest.json')
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
        expected_manifest_output = path.replace('.py', '.manifest.json')
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(0, len(abi['methods']))

        self.assertIn('events', abi)
        self.assertEqual(0, len(abi['events']))

    def test_generate_manifest_file_with_event(self):
        path = self.get_contract_path('test_sc/event_test', 'EventWithArgument.py')
        expected_manifest_output = path.replace('.py', '.manifest.json')
        compiler = Compiler()
        compiler.compile_and_save(path, path.replace('.py', '.nef'))
        events: Dict[str, Event] = {
            name: method
            for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
            if isinstance(method, Event)
        }

        output, manifest = self.get_output(path)
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

    def test_generate_manifest_file_with_nep5_transfer_event(self):
        path = self.get_contract_path('test_sc/event_test', 'EventNep5Transfer.py')
        expected_manifest_output = path.replace('.py', '.manifest.json')
        compiler = Compiler()
        compiler.compile_and_save(path, path.replace('.py', '.nef'))
        events: Dict[str, Event] = {
            event.name: event
            for event in self.get_compiler_analyser(compiler).symbol_table.values()
            if isinstance(event, Event)
        }

        output, manifest = self.get_output(path)
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

    def test_generate_nefdbgnfo_file(self):
        from boa3.model.type.itype import IType
        path = self.get_contract_path('GenerationWithDecorator.py')

        expected_nef_output = path.replace('.py', '.nefdbgnfo')
        compiler = Compiler()
        compiler.compile_and_save(path, path.replace('.py', '.nef'))
        methods: Dict[str, Method] = {
            name: method
            for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
            if isinstance(method, Method)
        }

        self.assertTrue(os.path.exists(expected_nef_output))
        debug_info = self.get_debug_info(path)
        self.assertNotIn('entrypoint', debug_info)
        self.assertIn('methods', debug_info)
        self.assertGreater(len(debug_info['methods']), 0)

        for debug_method in debug_info['methods']:
            self.assertIn('name', debug_method)
            parsed_name = debug_method['name'].split(',')
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
                self.assertEqual(2, len(var.split(',')))
                param_id, param_type = var.split(',')
                self.assertIn(param_id, actual_method.args)
                self.assertEqual(param_type, actual_method.args[param_id].type.abi_type)

            # validate local variables
            self.assertIn('variables', debug_method)
            self.assertEqual(len(actual_method.locals), len(debug_method['variables']))
            for var in debug_method['variables']:
                self.assertEqual(2, len(var.split(',')))
                var_id, var_type = var.split(',')
                self.assertIn(var_id, actual_method.locals)
                local_type = actual_method.locals[var_id].type
                self.assertEqual(local_type.abi_type if isinstance(local_type, IType) else AbiType.Any, var_type)

    def test_generate_nefdbgnfo_file_with_event(self):
        path = self.get_contract_path('test_sc/event_test', 'EventWithArgument.py')

        expected_nef_output = path.replace('.py', '.nefdbgnfo')
        compiler = Compiler()
        compiler.compile_and_save(path, path.replace('.py', '.nef'))
        events: Dict[str, Event] = {
            name: method
            for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
            if isinstance(method, Event)
        }

        self.assertTrue(os.path.exists(expected_nef_output))
        debug_info = self.get_debug_info(path)
        self.assertNotIn('entrypoint', debug_info)
        self.assertIn('events', debug_info)
        self.assertGreater(len(debug_info['events']), 0)

        for debug_event in debug_info['events']:
            self.assertIn('name', debug_event)
            parsed_name = debug_event['name'].split(',')
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
                self.assertEqual(2, len(var.split(',')))
                param_id, param_type = var.split(',')
                self.assertIn(param_id, actual_event.args)
                self.assertEqual(param_type, actual_event.args[param_id].type.abi_type)

    def test_generate_manifest_file_with_notify_event(self):
        path = self.get_contract_path('test_sc/interop_test/runtime', 'NotifySequence.py')
        expected_manifest_output = path.replace('.py', '.manifest.json')
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
        expected_manifest_output = path.replace('.py', '.manifest.json')
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
        path = self.get_contract_path('GenerationWithoutMainAndPublicMethods.py')
        expected_manifest_output = path.replace('.py', '.manifest.json')
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertNotIn('entryPoint', abi)
        self.assertIn('methods', abi)
        self.assertEqual(0, len(abi['methods']))

        self.assertIn('events', abi)
        self.assertEqual(0, len(abi['events']))

    def test_generate_manifest_file_abi_method_offset(self):
        path = self.get_contract_path('GenerationWithDecorator.py')
        manifest_path = path.replace('.py', '.manifest.json')

        compiler = Compiler()
        compiler.compile_and_save(path, path.replace('.py', '.nef'))
        methods: Dict[str, Method] = {
            name: method
            for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
            if isinstance(method, Method)
        }
        self.assertGreater(len(methods), 0)

        output, manifest = self.get_output(path)
        self.assertTrue(os.path.exists(manifest_path))
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

        compiler = Compiler()
        compiler.compile_and_save(path, path.replace('.py', '.nef'))
        methods: Dict[str, Method] = {
            name: method
            for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
            if isinstance(method, Method)
        }
        self.assertGreater(len(methods), 0)

        debug_info = self.get_debug_info(path)
        self.assertIn('methods', debug_info)
        self.assertGreater(len(debug_info['methods']), 0)

        for debug_method in debug_info['methods']:
            self.assertIn('name', debug_method)
            parsed_name = debug_method['name'].split(',')
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
                self.assertEqual(2, len(var.split(',')))
                param_id, param_type = var.split(',')
                self.assertIn(param_id, actual_method.args)
                self.assertEqual(param_type, actual_method.args[param_id].type.abi_type)

            # validate local variables
            self.assertIn('variables', debug_method)
            self.assertEqual(len(actual_method.locals), len(debug_method['variables']))
            for var in debug_method['variables']:
                self.assertEqual(2, len(var.split(',')))
                var_id, var_type = var.split(',')
                self.assertIn(var_id, actual_method.locals)
                self.assertEqual(actual_method.locals[var_id].type.abi_type, var_type)

    def test_generate_init_method(self):
        path = self.get_contract_path('test_sc/variable_test', 'GlobalAssignmentWithType.py')

        compiler = Compiler()
        compiler.compile_and_save(path, path.replace('.py', '.nef'))
        methods: Dict[str, Method] = {
            name: method
            for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
            if isinstance(method, Method)
        }
        from boa3.constants import INITIALIZE_METHOD_ID
        self.assertGreater(len(methods), 0)
        self.assertIn(INITIALIZE_METHOD_ID, methods)
        init_method = methods[INITIALIZE_METHOD_ID]

        output, manifest = self.get_output(path)
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertGreater(len(abi['methods']), 0)

        abi_init = next(method for method in abi['methods']
                        if 'name' in method and method['name'] == INITIALIZE_METHOD_ID)
        self.assertIsNotNone(abi_init)
        self.assertIn('offset', abi_init)
        self.assertEqual(init_method.start_address, abi_init['offset'])
        self.assertIn('parameters', abi_init)
        self.assertEqual(0, len(abi_init['parameters']))
        self.assertIn('returntype', abi_init)
        self.assertEqual(AbiType.Void, abi_init['returntype'])

        debug_info = self.get_debug_info(path)
        self.assertIn('methods', debug_info)
        self.assertGreater(len(debug_info['methods']), 0)

        debug_method = next((method for method in debug_info['methods']
                             if 'id' in method and method['id'] == str(id(init_method))), None)
        self.assertIsNotNone(debug_method)
        parsed_name = debug_method['name'].split(',')
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

    def test_compiler_error(self):
        path = self.get_contract_path('test_sc/built_in_methods_test', 'ClearTooManyParameters.py')

        with self.assertRaises(NotLoadedException):
            Boa3.compile(path)

        with self.assertRaises(NotLoadedException):
            Boa3.compile_and_save(path)

        with self.assertRaises(NotLoadedException):
            self.compile_and_save(path)

    def test_generation_with_recursive_function(self):
        path = self.get_contract_path('test_sc/function_test', 'RecursiveFunction.py')
        self.compile_and_save(path)

        from boa3_test.tests.test_classes.testengine import TestEngine
        engine = TestEngine()

        expected = self.fact(57)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected, result)

    def fact(self, f: int) -> int:
        if f <= 1:
            return 1
        return f * self.fact(f - 1)
