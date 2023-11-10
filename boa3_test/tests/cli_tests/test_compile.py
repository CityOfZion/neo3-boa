import os.path

from boa3_test.tests.cli_tests.cli_test import BoaCliTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.cli_tests.utils import neo3_boa_cli, get_path_from_boa3_test
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestCliCompile(BoaCliTest):

    @neo3_boa_cli('compile', '-h')
    def test_cli_compile_help(self):
        cli_output, _, system_exit = self.get_cli_output(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_SUCCESS, system_exit.exception.code)
        self.assertIn('usage: neo3-boa compile [-h] [-db] '
                      '[--project-path PROJECT_PATH] [-e ENV] '
                      '[-o NEF_OUTPUT] [--no-failfast] '
                      '[--log-level LOG_LEVEL] '
                      'input',
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

        logs = self.get_cli_log()

        self.assertEqual(3, len(logs.output))
        self.assertTrue(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in logs.output[0])
        self.assertTrue('Started compiling' in logs.output[1])
        self.assertTrue(f'Wrote {sc_nef_name} to ' in logs.output[-1],
                        msg=f'Something went wrong when compiling {sc_nef_name}')
        self.assertTrue(os.path.isfile(nef_path),
                        msg=f'{nef_path} not found')
        self.assertTrue(os.path.isfile(manifest_path),
                        msg=f'{manifest_path} not found')
        self.assertFalse(os.path.isfile(debug_info_path),
                         msg=f'{debug_info_path} exists')

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

        logs = self.get_cli_log()

        self.assertEqual(3, len(logs.output))
        self.assertTrue(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in logs.output[0])
        self.assertTrue('Started compiling' in logs.output[1])
        self.assertTrue(f'Wrote {sc_nef_name} to ' in logs.output[-1],
                        msg=f'Something went wrong when compiling {sc_nef_name}')
        self.assertTrue(os.path.isfile(nef_path),
                        msg=f'{nef_path} not found')
        self.assertTrue(os.path.isfile(manifest_path),
                        msg=f'{manifest_path} not found')
        self.assertTrue(os.path.isfile(debug_info_path),
                        msg=f'{debug_info_path} not found')

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

        logs = self.get_cli_log()

        self.assertEqual(3, len(logs.output))
        self.assertTrue(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in logs.output[0])
        self.assertTrue('Started compiling' in logs.output[1])
        self.assertTrue(f'Wrote {sc_nef_name} to ' in logs.output[-1],
                        msg=f'Something went wrong when compiling {sc_nef_name}')
        self.assertTrue(os.path.isfile(nef_path),
                        msg=f'{nef_path} not found')
        self.assertTrue(os.path.isfile(manifest_path),
                        msg=f'{manifest_path} not found')

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-e', 'env_changed',
                  '-o', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env_cli.nef', get_unique=True))
    def test_cli_compile_env(self):
        nef_path, _ = self.get_deploy_file_paths(
            get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
            output_name='Env_cli.nef',
            compile_if_found=False
        )
        nef_generated = nef_path.split(constants.PATH_SEPARATOR)[-1]

        logs = self.get_cli_log()

        self.assertEqual(3, len(logs.output))
        self.assertTrue(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}' in logs.output[0])
        self.assertTrue('Started compiling' in logs.output[1])
        self.assertTrue(f'Wrote {nef_generated} to ' in logs.output[-1],
                        msg=f'Something went wrong when compiling {nef_generated}')

        runner = BoaTestRunner(runner_id=self.method_name())

        runner.deploy_contract(nef_path)
        invoke = runner.call_contract(nef_path, 'main')
        expected_result = 'env_changed'
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(invoke.result, expected_result)

    @neo3_boa_cli('compile', 'wrong_file')
    def test_cli_compile_wrong_file(self):
        logs, system_exit = self.get_cli_log(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        self.assertTrue('Input file is not .py' in logs.output[-1])

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'interop_test', 'storage', 'StoragePutStrKeyStrValue.py'))
    def test_cli_compile_invalid_smart_contract(self):
        logs, system_exit = self.get_cli_log(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        self.assertTrue('Could not compile' in logs.output[-1])

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'boa_built_in_methods_test', 'Env.py'),
                  '-o', 'wrong_output_path')
    def test_cli_compile_wrong_output_path(self):
        logs, system_exit = self.get_cli_log(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        self.assertTrue('Output path file extension is not .nef' in logs.output[-1])

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'import_test', 'ImportFailInnerNotExistingMethod.py'))
    def test_cli_compile_fail_fast_true(self):
        logs, system_exit = self.get_cli_log(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        errors_logged = [log for log in logs.output if log.startswith('ERROR')]
        # with fail fast, only two errors are logged
        # 1. the actual compiler error
        # 2. the cli error informing that the compilation failed
        self.assertEqual(2, len(errors_logged))
        self.assertIn('Could not compile', errors_logged[-1])

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'import_test', 'ImportFailInnerNotExistingMethod.py'),
                  '--no-failfast')
    def test_cli_compile_fail_fast_false(self):
        logs, system_exit = self.get_cli_log(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        errors_logged = [log for log in logs.output if log.startswith('ERROR')]
        # the given contract has more than one error, so it should log more than 2 errors with fail fast disabled
        self.assertGreater(len(errors_logged), 2)
        self.assertIn('Could not compile', errors_logged[-1])

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'arithmetic_test', 'Addition.py'))
    def test_cli_compile_log_level_default(self):
        file_name = 'Addition'
        logs = self.get_cli_log()

        info_logged = [log for log in logs.output if log.startswith('INFO')]
        # three info logs are logged regardless of the log level
        # 1. neo3-boa and python version info
        # 2. compilation start info
        # 3. cli message when compilation is successful
        self.assertEqual(3, len(info_logged))
        self.assertIn(f'Wrote {file_name}.nef', info_logged[-1])

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'arithmetic_test', 'Addition.py'),
                  '--log-level', 'INFO')
    def test_cli_compile_log_level_info(self):
        file_name = 'Addition'
        logs = self.get_cli_log()

        info_logged = [log for log in logs.output if log.startswith('INFO')]
        # three info logs are logged regardless of the log level
        # 1. neo3-boa and python version info
        # 2. compilation start info
        # 3. cli message when compilation is successful
        self.assertGreater(len(info_logged), 3)
        self.assertIn(f'Wrote {file_name}.nef', info_logged[-1])

    @neo3_boa_cli('compile', get_path_from_boa3_test('test_sc', 'arithmetic_test', 'Addition.py'),
                  '--log-level', 'FOO')
    def test_cli_compile_log_level_invalid(self):
        logs, system_exit = self.get_cli_log(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_ERROR, system_exit.exception.code)
        self.assertEqual(1, len(logs.output))
        self.assertIn("Unknown level: 'FOO'", logs.output[-1])
