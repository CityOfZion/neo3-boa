from boa3_test.tests.cli_tests.cli_test import BoaCliTest  # needs to be the first import to avoid circular imports

import os.path

from boa3.internal import constants
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner
from boa3_test.tests.cli_tests.utils import neo3_boa_cli, get_path_from_boa3_test


class TestCliCompile(BoaCliTest):

    @neo3_boa_cli('compile', '-h')
    def test_cli_compile_help(self):
        cli_output, _, system_exit = self._assert_cli_raises(SystemExit)

        self.assertEqual(self.EXIT_CODE_SUCCESS, system_exit.exception.code)
        self.assertIn('usage: neo3-boa compile [-h] [-db] [--project-path PROJECT_PATH] [-e ENV] [-o NEF_OUTPUT] input',
                      cli_output)

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'))
    def test_cli_compile(self):
        sc_nef_name = 'Env.nef'
        nef_path = get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', sc_nef_name)
        manifest_path = nef_path.replace('nef', 'manifest.json')
        debug_info_path = nef_path.replace('nef', 'nefdbgnfo')

        if os.path.isfile(nef_path):
            os.remove(nef_path)
        if os.path.isfile(manifest_path):
            os.remove(manifest_path)
        if os.path.isfile(debug_info_path):
            os.remove(debug_info_path)

        logs = self._get_cli_log()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_nef_name} to ' in log in log for log in logs.output))
        self.assertTrue(os.path.isfile(nef_path))
        self.assertTrue(os.path.isfile(manifest_path))
        self.assertFalse(os.path.isfile(debug_info_path))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-db')
    def test_cli_compile_debug(self):
        sc_nef_name = 'Env.nef'
        nef_path = get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', sc_nef_name)
        manifest_path = nef_path.replace('nef', 'manifest.json')
        debug_info_path = nef_path.replace('nef', 'nefdbgnfo')

        if os.path.isfile(nef_path):
            os.remove(nef_path)
        if os.path.isfile(manifest_path):
            os.remove(manifest_path)
        if os.path.isfile(debug_info_path):
            os.remove(debug_info_path)

        logs = self._get_cli_log()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_nef_name} to ' in log in log for log in logs.output))
        self.assertTrue(os.path.isfile(nef_path))
        self.assertTrue(os.path.isfile(manifest_path))
        self.assertTrue(os.path.isfile(debug_info_path))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-o', get_path_from_boa3_test('test_cli', 'smart_contract.nef', get_unique=True))
    def test_cli_compile_new_output_path(self):
        sc_nef_name = 'smart_contract.nef'

        nef_path, manifest_path = self.get_deploy_file_paths(
            get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
            output_name=get_path_from_boa3_test('test_cli', sc_nef_name),
            compile_if_found=False
        )
        sc_nef_name = os.path.basename(nef_path)

        if os.path.isfile(nef_path):
            os.remove(nef_path)
        if os.path.isfile(manifest_path):
            os.remove(manifest_path)

        logs = self._get_cli_log()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_nef_name} to ' in log in log for log in logs.output))
        self.assertTrue(os.path.isfile(nef_path))
        self.assertTrue(os.path.isfile(manifest_path))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-e', 'env_changed',
                  '-o', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.nef', get_unique=True))
    def test_cli_compile_env(self):
        nef_path, _ = self.get_deploy_file_paths(
            get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
            compile_if_found=False
        )
        nef_generated = nef_path.split(constants.PATH_SEPARATOR)[-1]

        logs = self._get_cli_log()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {nef_generated} to ' in log in log for log in logs.output))

        runner = NeoTestRunner(runner_id=self.method_name())

        runner.deploy_contract(nef_path)
        invoke = runner.call_contract(nef_path, 'main')
        expected_result = 'env_changed'
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(invoke.result, expected_result)

    @neo3_boa_cli('compile', 'wrong_file')
    def test_cli_compile_wrong_file(self):
        logs, system_exit = self._assert_cli_raises(SystemExit, get_log=True)

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        self.assertTrue(any('Input file is not .py' in log in log for log in logs.output))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'interop_test', 'storage', 'StoragePutStrKeyStrValue.py'))
    def test_cli_compile_invalid_smart_contract(self):
        logs = self._get_cli_log()
        self.assertTrue(any('Could not compile' in log in log for log in logs.output))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-o', 'wrong_output_path')
    def test_cli_compile_wrong_output_path(self):
        logs, system_exit = self._assert_cli_raises(SystemExit, get_log=True)

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        self.assertTrue(any('Output path file extension is not .nef' in log in log for log in logs.output))
