import os
from typing import Dict

from boa3 import constants
from boa3.boa3 import Boa3
from boa3.compiler.compiler import Compiler
from boa3.constants import BYTEORDER, ENCODING
from boa3.model.method import Method
from boa3.neo.contracts.neffile import NefFile
from boa3.neo.vm.type.AbiType import AbiType
from boa3_test.tests.boa_test import BoaTest


class TestFileGeneration(BoaTest):

    def test_generate_files(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithDecorator.py' % self.dirname
        expected_nef_output = path.replace('.py', '.nef')
        expected_manifest_output = path.replace('.py', '.manifest.json')
        expected_debug_info_output = path.replace('.py', '.nefdbgnfo')
        Boa3.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_nef_output))
        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertTrue(os.path.exists(expected_debug_info_output))

    def test_generate_nef_file(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithDecorator.py' % self.dirname
        expected_nef_output = path.replace('.py', '.nef')
        Boa3.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_nef_output))
        with open(expected_nef_output, 'rb') as nef_output:
            magic = nef_output.read(constants.SIZE_OF_INT32)
            compiler = nef_output.read(32)
            version = nef_output.read(16)
            hash = nef_output.read(constants.SIZE_OF_INT160)
            check_sum = nef_output.read(constants.SIZE_OF_INT32)
            script_size = nef_output.read(1)
            script = nef_output.read()

        self.assertEqual(int.from_bytes(script_size, BYTEORDER), len(script))

        nef = NefFile(script)._nef
        self.assertEqual(compiler.decode(ENCODING), nef.compiler)
        self.assertEqual(hash, nef.script_hash.to_array())
        self.assertEqual(check_sum, nef.checksum)
        self.assertEqual(version, nef.version.to_array())

    def test_generate_manifest_file_with_decorator(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithDecorator.py' % self.dirname
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
        self.assertIn('returnType', method0)
        self.assertEqual(AbiType.Integer, method0['returnType'])
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
        self.assertIn('returnType', method1)
        self.assertEqual(AbiType.Integer, method1['returnType'])
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
        path = '%s/boa3_test/example/generation_test/GenerationWithoutDecorator.py' % self.dirname
        expected_manifest_output = path.replace('.py', '.manifest.json')
        output, manifest = self.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('methods', abi)
        self.assertEqual(0, len(abi['methods']))

        self.assertIn('events', abi)
        self.assertEqual(0, len(abi['events']))

    def test_generate_nefdbgnfo_file(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithDecorator.py' % self.dirname

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
                self.assertEqual(actual_method.locals[var_id].type.abi_type, var_type)

    def test_generate_without_main(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithoutMain.py' % self.dirname
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
        path = '%s/boa3_test/example/generation_test/GenerationWithoutMainAndPublicMethods.py' % self.dirname
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
        path = '%s/boa3_test/example/generation_test/GenerationWithDecorator.py' % self.dirname
        manifest_path = path.replace('.py', '.manifest.json')

        compiler = Compiler()
        compiler.compile(path)
        methods: Dict[str, Method] = {
            name: method
            for name, method in self.get_compiler_analyser(compiler).symbol_table.items()
            if isinstance(method, Method)
        }
        self.assertGreater(len(methods), 0)

        output, manifest = self.compile_and_save(path)
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

    def test_generate_manifest_file_storage_feature(self):
        path = '%s/boa3_test/example/storage_test/StorageGetBytesKey.py' % self.dirname
        manifest_path = path.replace('.py', '.manifest.json')

        output, manifest = self.compile_and_save(path)
        self.assertTrue(os.path.exists(manifest_path))

        self.assertIn('features', manifest)
        self.assertIn('storage', manifest['features'])
        self.assertEqual(True, manifest['features']['storage'])

    def test_generate_debug_info_with_multiple_flows(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithMultipleFlows.py' % self.dirname

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
