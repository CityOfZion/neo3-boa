import os
import sys

from boa3 import constants
from boa3.boa3 import Boa3
from boa3.neo.smart_contract.neffile import NefFile
from boa3.neo.vm.type.AbiType import AbiType
from boa3_test.tests.boa_test import BoaTest


class TestFileGeneration(BoaTest):

    def test_generate_files(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithDecorator.py' % self.dirname

        expected_nef_output = path.replace('.py', '.nef')
        expected_manifest_output = path.replace('.py', '.manifest.json')
        Boa3.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_nef_output))
        self.assertTrue(os.path.exists(expected_manifest_output))

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

        self.assertEqual(int.from_bytes(script_size, sys.byteorder), len(script))

        nef = NefFile(script)
        blank = b'\x00'.decode('utf-8')
        self.assertEqual(compiler.decode('utf-8').replace(blank, ''), nef.compiler)
        self.assertEqual(hash, nef.script_hash)
        self.assertEqual(int.from_bytes(check_sum, sys.byteorder), nef.check_sum)

        for index, field in enumerate(nef._NefFile__version_info):
            begin = index * constants.SIZE_OF_INT32
            byte_field = version[begin:begin + constants.SIZE_OF_INT32]
            self.assertEqual(int.from_bytes(byte_field, sys.byteorder), field)

    def test_generate_manifest_file_with_decorator(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithDecorator.py' % self.dirname

        expected_manifest_output = path.replace('.py', '.manifest.json')
        Boa3.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        with open(expected_manifest_output, 'r') as manifest_output:
            import json
            manifest = json.loads(manifest_output.read())

        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('entryPoint', abi)
        self.assertIn('name', abi['entryPoint'])
        self.assertEqual(abi['entryPoint']['name'], 'Main')
        self.assertIn('returnType', abi['entryPoint'])
        self.assertEqual(abi['entryPoint']['returnType'], AbiType.Integer)

        self.assertIn('parameters', abi['entryPoint'])
        self.assertEqual(len(abi['entryPoint']['parameters']), 2)

        arg0 = abi['entryPoint']['parameters'][0]
        self.assertIn('name', arg0)
        self.assertEqual(arg0['name'], 'a')
        self.assertIn('type', arg0)
        self.assertEqual(arg0['type'], AbiType.Integer)

        arg1 = abi['entryPoint']['parameters'][1]
        self.assertIn('name', arg1)
        self.assertEqual(arg1['name'], 'b')
        self.assertIn('type', arg1)
        self.assertEqual(arg1['type'], AbiType.Integer)

        self.assertIn('methods', abi)
        self.assertEqual(len(abi['methods']), 1)

        self.assertIn('events', abi)
        self.assertEqual(len(abi['events']), 0)

    def test_generate_manifest_file_without_decorator(self):
        path = '%s/boa3_test/example/generation_test/GenerationWithoutDecorator.py' % self.dirname

        expected_manifest_output = path.replace('.py', '.manifest.json')
        Boa3.compile_and_save(path)

        self.assertTrue(os.path.exists(expected_manifest_output))
        with open(expected_manifest_output, 'r') as manifest_output:
            import json
            manifest = json.loads(manifest_output.read())

        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('entryPoint', abi)
        self.assertEqual(len(abi['entryPoint']), 0)

        self.assertIn('methods', abi)
        self.assertEqual(len(abi['methods']), 0)

        self.assertIn('events', abi)
        self.assertEqual(len(abi['events']), 0)
