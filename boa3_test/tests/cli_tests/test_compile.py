from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

import io
import os
from boa3.cli import main
from boa3.internal import constants, env
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner
from contextlib import redirect_stdout
from unittest.mock import patch


class TestCli(BoaTest):
    default_folder = 'test_cli/smart_contract_folder'

    @patch('sys.argv', ['neo3-boa', '-h'])
    def test_cli_help(self):
        with redirect_stdout(io.StringIO()) as output, self.assertRaises(SystemExit):
            main()
        cli_output = output.getvalue()

        self.assertIn('usage: neo3-boa [-h] [-v] {compile}', cli_output)
        self.assertIn(f'neo3-boa by COZ - version {constants.BOA_VERSION}', cli_output)
        self.assertIn('Write smart contracts for Neo3 in Python', cli_output)

    @patch('sys.argv', ['neo3-boa', '--version'])
    def test_cli_version(self):
        with redirect_stdout(io.StringIO()) as output, self.assertRaises(SystemExit):
            main()
        cli_output = output.getvalue()

        self.assertIn(f'neo3-boa {constants.BOA_VERSION}', cli_output)

    @patch('sys.argv', [
        'neo3-boa',
        'compile',
        constants.PATH_SEPARATOR.join(
            [env.PROJECT_ROOT_DIRECTORY, 'boa3_test', 'test_cli', 'smart_contract_folder', 'smart_contract.py']
        )
    ])
    def test_cli_compile(self):
        sc_name = 'smart_contract.py'
        nef_path, manifest_path = self.get_deploy_file_paths(sc_name)
        debug_info_path = nef_path.replace('nef', 'nefdbgnfo')

        if os.path.isfile(nef_path):
            os.remove(nef_path)
        if os.path.isfile(manifest_path):
            os.remove(manifest_path)
        if os.path.isfile(debug_info_path):
            os.remove(debug_info_path)

        with self.assertLogs() as logs:
            main()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_name.replace("py", "nef")} to ' in log in log for log in logs.output))
        self.assertTrue(os.path.isfile(nef_path))
        self.assertTrue(os.path.isfile(manifest_path))
        self.assertFalse(os.path.isfile(debug_info_path))

    @patch('sys.argv', [
        'neo3-boa',
        'compile',
        '-db',
        constants.PATH_SEPARATOR.join(
            [env.PROJECT_ROOT_DIRECTORY, 'boa3_test', 'test_cli', 'smart_contract_folder', 'smart_contract.py']
        )
    ])
    def test_cli_compile_debug(self):
        sc_name = 'smart_contract.py'
        nef_path, manifest_path = self.get_deploy_file_paths(sc_name)
        debug_info_path = nef_path.replace('nef', 'nefdbgnfo')

        if os.path.isfile(nef_path):
            os.remove(nef_path)
        if os.path.isfile(manifest_path):
            os.remove(manifest_path)
        if os.path.isfile(debug_info_path):
            os.remove(debug_info_path)

        with self.assertLogs() as logs:
            main()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_name.replace("py", "nef")} to ' in log in log for log in logs.output))
        self.assertTrue(os.path.isfile(nef_path))
        self.assertTrue(os.path.isfile(manifest_path))
        self.assertTrue(os.path.isfile(debug_info_path))

    @patch('sys.argv', [
        'neo3-boa',
        'compile',
        '-o', constants.PATH_SEPARATOR.join(
            [env.PROJECT_ROOT_DIRECTORY, 'boa3_test', 'test_cli', 'smart_contract.nef']
        ),
        constants.PATH_SEPARATOR.join(
            [env.PROJECT_ROOT_DIRECTORY, 'boa3_test', 'test_cli', 'smart_contract_folder', 'smart_contract.py']
        )
    ])
    def test_cli_compile_new_output_path(self):
        sc_nef_name = 'smart_contract.nef'
        nef_path = constants.PATH_SEPARATOR.join([env.PROJECT_ROOT_DIRECTORY, 'boa3_test', 'test_cli', sc_nef_name])
        manifest_path = nef_path.replace('nef', 'manifest.json')

        if os.path.isfile(nef_path):
            os.remove(nef_path)
        if os.path.isfile(manifest_path):
            os.remove(manifest_path)

        with self.assertLogs() as logs:
            main()

        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_nef_name} to ' in log in log for log in logs.output))
        self.assertTrue(os.path.isfile(nef_path))
        self.assertTrue(os.path.isfile(manifest_path))

    @patch('sys.argv', [
        'neo3-boa',
        'compile',
        '-e', 'env_changed',
        constants.PATH_SEPARATOR.join(
            [env.PROJECT_ROOT_DIRECTORY, 'boa3_test', 'test_cli', 'smart_contract_folder', 'smart_contract.py']
        )
    ])
    def test_cli_compile_env(self):
        sc_name = 'smart_contract.py'
        path, _ = self.get_deploy_file_paths(sc_name)
        runner = NeoTestRunner(runner_id=self.method_name())

        with self.assertLogs() as logs:
            main()
        self.assertTrue(any(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in log for log in logs.output))
        self.assertTrue(any('Started compiling' in log for log in logs.output))
        self.assertTrue(any(f'Wrote {sc_name.replace("py", "nef")} to ' in log in log for log in logs.output))

        invoke = runner.call_contract(path, 'main')
        expected_result = 'env_changed'
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(invoke.result, expected_result)

    @patch('sys.argv', ['neo3-boa', 'compile', '-h'])
    def test_cli_compile_help(self):
        with redirect_stdout(io.StringIO()) as output, self.assertRaises(SystemExit):
            main()
        cli_output = output.getvalue()

        self.assertIn('neo3-boa compile', cli_output)
        self.assertIn('[-h]', cli_output)
        self.assertIn('[-db]', cli_output)
        self.assertIn('[--project-path PROJECT_PATH]', cli_output)
        self.assertIn('[-e ENV]', cli_output)
        self.assertIn('[-o NEF_OUTPUT]', cli_output)
        self.assertIn('input', cli_output)
