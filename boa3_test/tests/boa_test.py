import logging
import os
import threading
from typing import Any, Dict, Optional, Tuple, Union
from unittest import TestCase

from boa3.internal import constants, env
from boa3.internal.analyser.analyser import Analyser
from boa3.internal.compiler.compiler import Compiler
from boa3.internal.exception.CompilerError import CompilerError
from boa3.internal.model.method import Method

__all__ = [
    'BoaTest',
    '_COMPILER_LOCK',
    '_LOGGING_LOCK',
    'USE_UNIQUE_NAME',
]

_COMPILER_LOCK = threading.RLock()
_LOGGING_LOCK = threading.Lock()

USE_UNIQUE_NAME = False


class BoaTest(TestCase):
    dirname: str = None

    ABORTED_CONTRACT_MSG = 'ABORT is executed'
    ARGUMENT_OUT_OF_RANGE_MSG_PREFIX = 'Specified argument was out of the range of valid values.'
    ASSERT_RESULTED_FALSE_MSG = 'ASSERT is executed with false result.'
    BAD_SCRIPT_EXCEPTION_MSG = "Neo.VM.BadScriptException: Exception of type 'Neo.VM.BadScriptException' was thrown."
    CANT_CALL_SYSCALL_WITH_FLAG_MSG_PREFIX = "Cannot call this SYSCALL with the flag"
    CANT_FIND_METHOD_MSG_PREFIX = "Can't find method"
    CANT_PARSE_VALUE_MSG = "The value could not be parsed."
    CANT_CALL_METHOD_PREFIX = "Cannot Call Method"
    CALLED_CONTRACT_DOES_NOT_EXIST_MSG = 'Called Contract Does Not Exist'
    CONTRACT_NOT_FOUND_MSG_REGEX = 'contract "(.*?)" not found'
    GAS_MUST_BE_POSITIVE_MSG = 'GAS must be positive.'
    GIVEN_KEY_NOT_PRESENT_IN_DICT_MSG_REGEX = "The given key '\\S+' was not present in the dictionary."
    INSUFFICIENT_GAS = 'Insufficient GAS.'
    MAP_KEY_NOT_FOUND_ERROR_MSG = 'Key not found in Map'
    MAX_ITEM_SIZE_EXCEED_MSG_PREFIX = 'MaxItemSize exceed'
    FORMAT_METHOD_DOESNT_EXIST_IN_CONTRACT_MSG_REGEX_PREFIX = r'^Method "{0}" with \d+ parameter\(s\) ' \
                                                              r"doesn't exist in the contract"
    METHOD_DOESNT_EXIST_IN_CONTRACT_MSG_REGEX_PREFIX = FORMAT_METHOD_DOESNT_EXIST_IN_CONTRACT_MSG_REGEX_PREFIX.format(r'\S+')
    NULL_POINTER_MSG = 'Object reference not set to an instance of an object.'
    UNHANDLED_EXCEPTION_MSG_PREFIX = "An unhandled exception was thrown."
    VALUE_CANNOT_BE_NEGATIVE_MSG = 'value can not be negative'
    VALUE_DOES_NOT_FALL_WITHIN_EXPECTED_RANGE_MSG = 'Value does not fall within the expected range.'
    VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX = r'The value( \S*)? is out of range.$'

    default_folder: str = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._use_custom_name = USE_UNIQUE_NAME

    @classmethod
    def setUpClass(cls):
        folders = os.path.abspath(__file__).split(os.sep)
        cls.dirname = '/'.join(folders[:-3])
        cls.test_root_dir = '/'.join(folders[-3:-2])
        cls.default_test_folder = ('{0}/{1}'.format(cls.test_root_dir, cls.default_folder)
                                   if len(cls.default_folder) else cls.test_root_dir)

        super(BoaTest, cls).setUpClass()
        constants.COMPILER_VERSION = '_unit_tests_'  # to not change test contract script hashes in different versions

    def method_name(self) -> str:
        return self._testMethodName if hasattr(self, '_testMethodName') else self.id()

    def get_compiler_analyser(self, compiler: Compiler) -> Analyser:
        return compiler._analyser

    def get_all_imported_methods(self, compiler: Compiler) -> Dict[str, Method]:
        from boa3.internal.compiler.filegenerator.filegenerator import FileGenerator
        generator = FileGenerator(compiler.result, compiler._analyser, compiler._entry_smart_contract)
        return {constants.VARIABLE_NAME_SEPARATOR.join(name): value for name, value in generator._methods_with_imports.items()}

    def assertCompilerLogs(self, expected_logged_exception, path) -> Union[bytes, str]:
        output, error_msg = self._assert_compiler_logs_error(expected_logged_exception, path)
        if not issubclass(expected_logged_exception, CompilerError):
            return output
        else:
            # filter to get only the error message, without location information
            import re

            result = re.search('^\\d+:\\d+ - (?P<msg>.*?)\t\\W+\\<.*?\\>', error_msg)
            try:
                return result.group('msg')
            except BaseException:
                return output

    def assertCompilerNotLogs(self, expected_logged_exception, path):
        output, expected_logged = self._get_compiler_log_data(expected_logged_exception, path)
        if len(expected_logged) > 0:
            raise AssertionError(f'{expected_logged_exception.__name__} was logged: "{expected_logged[0].message}"')
        return output

    def _assert_compiler_logs_error(self, expected_logged_exception, path):
        output, expected_logged = self._get_compiler_log_data(expected_logged_exception, path)
        if len(expected_logged) < 1:
            raise AssertionError('{0} not logged'.format(expected_logged_exception.__name__))
        return output, expected_logged[0].message

    def _get_compiler_log_data(self, expected_logged_exception, path, fail_fast=False):
        output = None

        with _LOGGING_LOCK:
            with self.assertLogs() as log:
                from boa3.internal.exception.NotLoadedException import NotLoadedException
                try:
                    output = self.compile(path, fail_fast=fail_fast)
                except NotLoadedException:
                    # when an compiler error is logged this exception is raised.
                    pass

            expected_logged = [exception for exception in log.records
                               if isinstance(exception.msg, expected_logged_exception)]
        return output, expected_logged

    def get_all_compile_log_data(self, path: str, *,
                                 get_errors: bool = True,
                                 get_warnings: bool = False,
                                 fail_fast: bool = False) -> Tuple[list, list]:
        from boa3.internal.exception.CompilerWarning import CompilerWarning

        instance_logs = []
        if get_errors:
            instance_logs.append(CompilerError)
        if get_warnings:
            instance_logs.append(CompilerWarning)

        errors = []
        warnings = []
        _, expected_logged = self._get_compiler_log_data(*instance_logs, path, fail_fast=fail_fast)

        if not get_errors:
            if not get_warnings:
                return errors, warnings
            warnings = [log.msg for log in expected_logged]
        else:
            if get_warnings:
                for log in expected_logged:
                    if isinstance(log.msg, CompilerError):
                        errors.append(log.msg)
                    elif isinstance(log.msg, CompilerWarning):
                        warnings.append(log.msg)
            else:
                errors = [log.msg for log in expected_logged]

        return errors, warnings

    def assertStartsWith(self, first: Any, second: Any):
        if not (hasattr(first, 'startswith') and first.startswith(second)):
            self.fail(f'{first} != {second}')

    def get_dir_path(self, *args: str) -> str:
        type_error_message = 'get_contract_path() takes {0} positional argument but {1} were given'
        num_args = len(args)
        if num_args == 0:
            raise TypeError(type_error_message.format(2, num_args + 1))
        if num_args > 2:
            raise TypeError(type_error_message.format(3, num_args + 1))

        values = [None, env.PROJECT_ROOT_DIRECTORY]
        for index, value in enumerate(reversed(args)):
            values[index] = value

        dir_folder, root_path = values
        return '{0}/{1}'.format(root_path, dir_folder)

    def get_contract_path(self, *args: str) -> str:
        """
        Usages:
            get_contract_path(contract_name)
            get_contract_path(dir_folder, contract_name)
            get_contract_path(root_path, dir_folder, contract_name)
        """
        type_error_message = 'get_contract_path() takes {0} positional argument but {1} were given'
        num_args = len(args)
        if num_args == 0:
            raise TypeError(type_error_message.format(2, num_args + 1))
        if num_args > 3:
            raise TypeError(type_error_message.format(4, num_args + 1))
        if os.path.isabs(args[0]):
            return args[0]

        values = [None, self.default_test_folder, env.PROJECT_ROOT_DIRECTORY]
        for index, value in enumerate(reversed(args)):
            values[index] = value

        contract_name, dir_folder, root_path = values

        from os import path
        if not path.exists(dir_folder) and root_path is env.PROJECT_ROOT_DIRECTORY:
            path_folder = '{0}/{1}'.format(root_path, dir_folder)
            if not path.exists(path_folder) and not dir_folder.startswith(self.test_root_dir):
                path_folder = '{0}/{1}/{2}'.format(root_path, self.test_root_dir, dir_folder)
                if not path.exists(path_folder):
                    path_folder = '{0}/{1}/{2}'.format(root_path, self.default_test_folder, dir_folder)

            dir_folder = path_folder
        else:
            if path.exists(dir_folder):
                dir_folder = os.path.abspath(dir_folder)
            else:
                dir_folder = '{0}/{1}'.format(root_path, dir_folder)

        if not contract_name.endswith('.py'):
            contract_name = contract_name + '.py'

        path = '{0}/{1}'.format(dir_folder, contract_name)
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        else:
            path = os.path.abspath(path).replace(os.path.sep, constants.PATH_SEPARATOR)
        return path

    def get_deploy_file_paths_without_compiling(self, contract_path: str, output_name: str = None) -> Tuple[str, str]:
        if isinstance(output_name, str):
            output_path, output_file = os.path.split(output_name)
            if len(output_path) == 0:
                file_path = os.path.dirname(contract_path)
                file_name, _ = os.path.splitext(os.path.basename(output_name))
                file_path_without_ext = constants.PATH_SEPARATOR.join((file_path, file_name))
            else:
                file_path_without_ext, _ = os.path.splitext(output_name)
        else:
            file_path_without_ext, _ = os.path.splitext(contract_path)

        if USE_UNIQUE_NAME:
            from boa3_test.test_drive import utils
            file_path_without_ext = utils.create_custom_id(file_path_without_ext, use_time=False)

        return f'{file_path_without_ext}.nef', f'{file_path_without_ext}.manifest.json'

    def get_deploy_file_paths(self, *args: str, output_name: str = None,
                              compile_if_found: bool = False, change_manifest_name: bool = False,
                              debug: bool = False) -> Tuple[str, str]:
        contract_path = self.get_contract_path(*args)
        if isinstance(contract_path, str):
            nef_path, manifest_path = self.get_deploy_file_paths_without_compiling(contract_path, output_name)
            if contract_path.endswith('.py'):
                with _COMPILER_LOCK:
                    if compile_if_found or not (os.path.isfile(nef_path) and os.path.isfile(manifest_path)):
                        # both .nef and .manifest.json are required to execute the smart contract
                        self.compile_and_save(contract_path, output_name=nef_path, log=True,
                                              change_manifest_name=change_manifest_name,
                                              debug=debug,
                                              use_unique_name=False  # already using unique name
                                              )

            return nef_path, manifest_path

        return contract_path, contract_path

    def compile(self, path: str, root_folder: str = None, fail_fast: bool = False, **kwargs) -> bytes:
        from boa3.boa3 import Boa3

        with _COMPILER_LOCK:
            result = Boa3.compile(path, root_folder=root_folder, fail_fast=fail_fast,
                                  log_level=logging.getLevelName(logging.INFO),
                                  optimize=kwargs['optimize'] if 'optimize' in kwargs else True
                                  )

        return result

    def compile_and_save(self, path: str, root_folder: str = None, debug: bool = False, log: bool = True,
                         output_name: str = None, env: str = None, **kwargs) -> Tuple[bytes, Dict[str, Any]]:

        if output_name is not None:
            output_dir, manifest_name = os.path.split(output_name)  # get name
            if len(output_dir) == 0:
                output_dir, _ = os.path.split(path)
                output_name = f'{output_dir}/{manifest_name}'
            manifest_name, _ = os.path.splitext(manifest_name)  # remove extension
        else:
            manifest_name = None

        use_unique_name = kwargs['use_unique_name'] if 'use_unique_name' in kwargs else True
        if not isinstance(output_name, str) or not output_name.endswith('.nef'):
            nef_output, _ = self.get_deploy_file_paths_without_compiling(path)
        elif use_unique_name and USE_UNIQUE_NAME:
            nef_output, _ = self.get_deploy_file_paths_without_compiling(output_name)
        else:
            nef_output = output_name

        if nef_output.endswith('.py'):
            nef_output = nef_output.replace('.py', '.nef')
        manifest_output = nef_output.replace('.nef', '.manifest.json')

        from boa3.boa3 import Boa3
        from boa3.internal.neo.contracts.neffile import NefFile
        with _COMPILER_LOCK:
            Boa3.compile_and_save(path, output_path=nef_output, root_folder=root_folder,
                                  env=env, debug=debug,
                                  show_errors=log,
                                  log_level=logging.getLevelName(logging.INFO),
                                  optimize=kwargs['optimize'] if 'optimize' in kwargs else True
                                  )

        get_raw_nef = kwargs['get_raw_nef'] if 'get_raw_nef' in kwargs else False
        change_manifest_name = kwargs['change_manifest_name'] if 'change_manifest_name' in kwargs else False

        with open(nef_output, mode='rb') as nef:
            file = nef.read()
            if get_raw_nef:
                output = file
            else:
                output = NefFile.deserialize(file).script

        with open(manifest_output) as manifest_file:
            import json
            manifest = json.loads(manifest_file.read())

        if change_manifest_name and manifest_name is not None:
            manifest['name'] = manifest_name
            with _COMPILER_LOCK:
                with open(manifest_output, mode='w') as manifest_file:
                    manifest_file.write(json.dumps(manifest, indent=4))

        return output, manifest

    def get_debug_info(self, path: str) -> Optional[Dict[str, Any]]:
        if path.endswith('.nef'):
            nef_output = path
        else:
            nef_output, _ = self.get_deploy_file_paths_without_compiling(path)
        debug_info_output = nef_output.replace('.nef', '.nefdbgnfo')

        if not os.path.isfile(debug_info_output):
            return None

        from zipfile import ZipFile
        with ZipFile(debug_info_output, 'r') as dbgnfo:
            import json
            debug_info = json.loads(dbgnfo.read(os.path.basename(nef_output.replace('.nef', '.debug.json'))))
        return debug_info

    def get_output(self, path: str, root_folder: str = None) -> Tuple[bytes, Dict[str, Any]]:
        if path.endswith('.nef'):
            nef_output = path
            manifest_output = path.replace('.nef', '.manifest.json')
        else:
            nef_output, manifest_output = self.get_deploy_file_paths_without_compiling(path)

        with _COMPILER_LOCK:
            if not os.path.isfile(nef_output):
                return self.compile_and_save(path, root_folder=root_folder)

        from boa3.internal.neo.contracts.neffile import NefFile

        if not os.path.isfile(nef_output):
            output = bytes()
        else:
            with open(nef_output, mode='rb') as nef:
                file = nef.read()
                output = NefFile.deserialize(file).script

        if not os.path.isfile(manifest_output):
            manifest = {}
        else:
            with open(manifest_output) as manifest_output:
                import json
                manifest = json.loads(manifest_output.read())

        return output, manifest

    def get_bytes_output(self, path: str) -> Tuple[bytes, Dict[str, Any]]:
        nef_output, manifest_output = self.get_deploy_file_paths_without_compiling(path)
        with _COMPILER_LOCK:
            if not os.path.isfile(nef_output):
                return self.compile_and_save(path, get_raw_nef=True)

        if not os.path.isfile(nef_output):
            output = bytes()
        else:
            with open(nef_output, mode='rb') as nef:
                output = nef.read()

        if not os.path.isfile(manifest_output):
            manifest = {}
        else:
            with open(manifest_output) as manifest_output:
                import json
                manifest = json.loads(manifest_output.read())

        return output, manifest
