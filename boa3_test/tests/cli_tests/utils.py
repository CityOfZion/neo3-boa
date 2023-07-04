from unittest.mock import patch

from boa3.internal import constants, env


def neo3_boa_cli(*args: str):
    return patch('sys.argv', ['neo3-boa', *args])


def get_path_from_boa3_test(*args: str, get_unique=False) -> str:
    result = constants.PATH_SEPARATOR.join([env.PROJECT_ROOT_DIRECTORY, 'boa3_test', *args])

    if get_unique:
        from boa3_test.tests.boa_test import USE_UNIQUE_NAME

        if USE_UNIQUE_NAME:
            import os.path
            from boa3_test.test_drive import utils

            file_path_without_ext, ext = os.path.splitext(result)
            file_path_without_ext = utils.create_custom_id(file_path_without_ext, use_time=False)
            result = file_path_without_ext + ext
    return result


def normalize_separators(original_string: str) -> str:
    """
    This function will try to normalize all separators (e.g., '\t', '\n', multiple spaces) into a single white space,
    because the stdout sometimes might have different spacing depending on console size.
    """
    return ' '.join(original_string.split())
