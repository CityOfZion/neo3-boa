from boa3_test.tests.boa_test import (BoaTest,  # needs to be the first import to avoid circular imports
                                      _COMPILER_LOCK as LOCK,
                                      _LOGGING_LOCK as LOG_LOCK
                                      )

__all__ = [
    'BoaCliTest',
]

import abc
import io
from contextlib import redirect_stdout, redirect_stderr

from boa3.cli import main
from boa3_test.tests.cli_tests import utils


class BoaCliTest(BoaTest, abc.ABC):
    default_folder = 'test_cli'

    EXIT_CODE_SUCCESS = 0
    EXIT_CODE_ERROR = 1
    EXIT_CODE_CLI_SYNTAX_ERROR = 2

    def setUp(self):
        LOG_LOCK.acquire()
        LOCK.acquire()

    def tearDown(self):
        LOCK.release()
        LOG_LOCK.release()

    def get_cli_log(self, get_exit_code: bool = False):
        if get_exit_code:
            return self._assert_cli_raises(SystemExit, get_log=True)
        return self._run_cli_log()

    def get_cli_output(self, get_exit_code: bool = False):
        if get_exit_code:
            return self._assert_cli_raises(SystemExit, get_log=False)
        return self._run_cli()

    def _assert_cli_raises(self, exception, get_log=False):
        if get_log:
            return self._run_cli_log(exception)
        else:
            return self._run_cli(exception)

    def _run_cli_log(self, expected_exception=None) -> tuple:
        with self.assertLogs() as logs:
            if expected_exception is not None:
                with self.assertRaises(expected_exception) as error:
                    main()
            else:
                main()

        if expected_exception is None:
            return logs
        return logs, error

    def _run_cli(self, expected_exception=None) -> tuple:
        with redirect_stdout(io.StringIO()) as stdout, redirect_stderr(io.StringIO()) as stderr:
            if expected_exception is not None:
                with self.assertRaises(expected_exception) as error:
                    main()
            else:
                main()

        str_stdout = utils.normalize_separators(stdout.getvalue())
        str_stderr = utils.normalize_separators(stderr.getvalue())

        if expected_exception is None:
            return str_stdout, str_stderr
        return str_stdout, str_stderr, error
