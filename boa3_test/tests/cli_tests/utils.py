from boa3.internal import constants, env
from unittest.mock import patch


def neo3_boa_cli(*args: str):
    return patch('sys.argv', ['neo3-boa', *args])


def get_path_from_boa3_test(*args: str) -> str:
    return constants.PATH_SEPARATOR.join([env.PROJECT_ROOT_DIRECTORY, 'boa3_test', *args])


def normalize_separators(original_string: str) -> str:
    """
    This function will try to normalize all separators (e.g., '\t', '\n', multiple spaces) into a single white space,
    because the stdout sometimes might have different spacing depending on console size.
    """
    return ' '.join(original_string.split())
