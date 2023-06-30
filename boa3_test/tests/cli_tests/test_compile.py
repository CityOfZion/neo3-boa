from boa3_test.tests.boa_test import BoaTest, _COMPILER_LOCK as LOCK, _LOGGING_LOCK as LOG_LOCK  # needs to be the first import to avoid circular imports

import io
import os
from boa3.cli import main
from boa3.internal import constants
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.cli_tests.utils import neo3_boa_cli, get_path_from_boa3_test, normalize_separators
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner
from contextlib import redirect_stdout


class TestCliCompile(BoaTest):
    default_folder = 'test_cli'

    EXIT_CODE_SUCCESS = 0
    EXIT_CODE_ERROR = 1
    EXIT_CODE_CLI_SYNTAX_ERROR = 2

    @neo3_boa_cli('compile', '-h')
    def test_cli_compile_help(self):
        with LOCK, LOG_LOCK, redirect_stdout(io.StringIO()) as output, self.assertRaises(SystemExit) as system_exit:
            main()
        cli_output = normalize_separators(output.getvalue())

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

        with LOCK, LOG_LOCK, self.assertLogs() as logs:
            main()

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

        with LOCK, LOG_LOCK, self.assertLogs() as logs:
            main()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_nef_name} to ' in log in log for log in logs.output))
        self.assertTrue(os.path.isfile(nef_path))
        self.assertTrue(os.path.isfile(manifest_path))
        self.assertTrue(os.path.isfile(debug_info_path))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-o', get_path_from_boa3_test('test_cli', 'smart_contract.nef'))
    def test_cli_compile_new_output_path(self):
        sc_nef_name = 'smart_contract.nef'
        nef_path = get_path_from_boa3_test('test_cli', sc_nef_name)
        manifest_path = nef_path.replace('nef', 'manifest.json')

        if os.path.isfile(nef_path):
            os.remove(nef_path)
        if os.path.isfile(manifest_path):
            os.remove(manifest_path)

        with LOCK, LOG_LOCK, self.assertLogs() as logs:
            main()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_nef_name} to ' in log in log for log in logs.output))
        self.assertTrue(os.path.isfile(nef_path))
        self.assertTrue(os.path.isfile(manifest_path))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-e', 'env_changed')
    def test_cli_compile_env(self):
        sc_nef_name = 'Env.nef'

        with LOCK, LOG_LOCK, self.assertLogs() as logs:
            main()
        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_nef_name} to ' in log in log for log in logs.output))

        path = get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', sc_nef_name)
        runner = NeoTestRunner(runner_id=self.method_name())

        runner.deploy_contract(path)
        invoke = runner.call_contract(path, 'main')
        expected_result = 'env_changed'
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(invoke.result, expected_result)

    @neo3_boa_cli('compile', 'wrong_file')
    def test_cli_compile_wrong_file(self):
        with LOCK, LOG_LOCK, self.assertLogs() as logs, self.assertRaises(SystemExit) as system_exit:
            main()

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        self.assertTrue(any('Input file is not .py' in log in log for log in logs.output))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'interop_test', 'storage', 'StoragePutStrKeyStrValue.py'))
    def test_cli_compile_invalid_smart_contract(self):
        with LOCK, LOG_LOCK, self.assertLogs() as logs:
            main()

        self.assertTrue(any('Could not compile' in log in log for log in logs.output))

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-o', 'wrong_output_path')
    def test_cli_compile_wrong_output_path(self):
        with LOCK, LOG_LOCK, self.assertLogs() as logs, self.assertRaises(SystemExit) as system_exit:
            main()

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        self.assertTrue(any('Output path file extension is not .nef' in log in log for log in logs.output))
