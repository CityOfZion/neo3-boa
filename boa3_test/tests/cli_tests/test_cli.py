from boa3_test.tests.boa_test import BoaTest, _COMPILER_LOCK as LOCK, _LOGGING_LOCK as LOG_LOCK  # needs to be the first import to avoid circular imports

import io
from boa3.cli import main
from boa3.internal import constants
from boa3_test.tests.cli_tests.utils import neo3_boa_cli, normalize_separators
from contextlib import redirect_stdout, redirect_stderr


class TestCli(BoaTest):
    default_folder = 'test_cli'

    EXIT_CODE_SUCCESS = 0
    EXIT_CODE_ERROR = 1
    EXIT_CODE_CLI_SYNTAX_ERROR = 2

    @neo3_boa_cli('-h')
    def test_cli_help(self):
        with LOCK, LOG_LOCK, redirect_stdout(io.StringIO()) as output, self.assertRaises(SystemExit) as system_exit:
            main()
        cli_output = normalize_separators(output.getvalue())

        self.assertEqual(self.EXIT_CODE_SUCCESS, system_exit.exception.code)
        self.assertIn('usage: neo3-boa [-h] [-v] {compile}', cli_output)
        self.assertIn(f'neo3-boa by COZ - version {constants.BOA_VERSION}', cli_output)
        self.assertIn('Write smart contracts for Neo3 in Python', cli_output)

    @neo3_boa_cli('--version')
    def test_cli_version(self):
        with LOCK, LOG_LOCK, redirect_stdout(io.StringIO()) as output, self.assertRaises(SystemExit) as system_exit:
            main()
        cli_output = normalize_separators(output.getvalue())

        self.assertEqual(self.EXIT_CODE_SUCCESS, system_exit.exception.code)
        self.assertIn(f'neo3-boa {constants.BOA_VERSION}', cli_output)

    @neo3_boa_cli('build')
    def test_cli_wrong_syntax(self):
        with LOCK, LOG_LOCK, redirect_stderr(io.StringIO()) as output, self.assertRaises(SystemExit) as system_exit:
            main()
        cli_output = normalize_separators(output.getvalue())

        self.assertEqual(self.EXIT_CODE_CLI_SYNTAX_ERROR, system_exit.exception.code)
        self.assertIn("invalid choice: 'build'", cli_output)
