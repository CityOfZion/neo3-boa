from boa3_test.tests.cli_tests.cli_test import BoaCliTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3_test.tests.cli_tests.utils import neo3_boa_cli


class TestCli(BoaCliTest):

    @neo3_boa_cli('-h')
    def test_cli_help(self):
        cli_output, _, system_exit = self.get_cli_output(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_SUCCESS, system_exit.exception.code)
        self.assertIn('usage: neo3-boa [-h] [-v] {compile}', cli_output)
        self.assertIn(f'neo3-boa by COZ - version {constants.BOA_VERSION}', cli_output)
        self.assertIn('Write smart contracts for Neo3 in Python', cli_output)

    @neo3_boa_cli('--version')
    def test_cli_version(self):
        cli_output, _, system_exit = self.get_cli_output(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_SUCCESS, system_exit.exception.code)
        self.assertIn(f'neo3-boa {constants.BOA_VERSION}', cli_output)

    @neo3_boa_cli('build')
    def test_cli_wrong_syntax(self):
        _, cli_output, system_exit = self.get_cli_output(get_exit_code=True)

        self.assertEqual(self.EXIT_CODE_CLI_SYNTAX_ERROR, system_exit.exception.code)
        self.assertIn("invalid choice: 'build'", cli_output)
