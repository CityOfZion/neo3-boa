import os
import threading
from typing import Any, Dict, Iterable, Optional, Tuple, Type, Union
from unittest import TestCase

from boa3.internal import constants, env
from boa3.internal.analyser.analyser import Analyser
from boa3.internal.compiler.compiler import Compiler
from boa3.internal.exception.CompilerError import CompilerError
from boa3.internal.model.method import Method
from boa3.internal.neo.smart_contract.VoidType import VoidType
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine
from boa3_test.tests.test_classes.transactionattribute import oracleresponse

_COMPILER_LOCK = threading.RLock()
_LOGGING_LOCK = threading.Lock()

USE_UNIQUE_NAME = False


class BoaTest(TestCase):
    dirname: str = None

    ABORTED_CONTRACT_MSG = 'ABORT is executed'
    ARGUMENT_OUT_OF_RANGE_MSG_PREFIX = 'Specified argument was out of the range of valid values.'
    ASSERT_RESULTED_FALSE_MSG = 'ASSERT is executed with false result.'
    CANT_CALL_SYSCALL_WITH_FLAG_MSG_PREFIX = "Cannot call this SYSCALL with the flag"
    CANT_FIND_METHOD_MSG_PREFIX = "Can't find method"
    CANT_PARSE_VALUE_MSG = "The value could not be parsed."
    CALLED_CONTRACT_DOES_NOT_EXIST_MSG = 'Called Contract Does Not Exist'
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
        from boa3.internal.compiler.filegenerator import FileGenerator
        generator = FileGenerator(compiler.result, compiler._analyser, compiler._entry_smart_contract)
        return {constants.VARIABLE_NAME_SEPARATOR.join(name): value for name, value in generator._methods_with_imports.items()}

    def indent_text(self, text: str, no_spaces: int = 4) -> str:
        import re
        return re.sub('\n[ \t]+', '\n' + ' ' * no_spaces, text)

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

    def _get_compiler_log_data(self, expected_logged_exception, path):
        output = None

        with _LOGGING_LOCK:
            with self.assertLogs() as log:
                from boa3.internal.exception.NotLoadedException import NotLoadedException
                try:
                    output = self.compile(path)
                except NotLoadedException:
                    # when an compiler error is logged this exception is raised.
                    pass

        expected_logged = [exception for exception in log.records
                           if isinstance(exception.msg, expected_logged_exception)]
        return output, expected_logged

    def assertIsVoid(self, obj: Any):
        if obj is not VoidType:
            self.fail('{0} is not Void'.format(obj))

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
        return path

    def get_deploy_file_paths_without_compiling(self, contract_path: str) -> Tuple[str, str]:
        file_path_without_ext, _ = os.path.splitext(contract_path)
        if USE_UNIQUE_NAME:
            from boa3_test.test_drive import utils
            file_path_without_ext = utils.create_custom_id(file_path_without_ext, use_time=False)

        return f'{file_path_without_ext}.nef', f'{file_path_without_ext}.manifest.json'

    def get_deploy_file_paths(self, *args: str, compile_if_found: bool = False) -> Tuple[str, str]:
        contract_path = self.get_contract_path(*args)
        if isinstance(contract_path, str):
            nef_path, manifest_path = self.get_deploy_file_paths_without_compiling(contract_path)
            if contract_path.endswith('.py'):
                with _COMPILER_LOCK:
                    if compile_if_found or not (os.path.isfile(nef_path) and os.path.isfile(manifest_path)):
                        # both .nef and .manifest.json are required to execute the smart contract
                        self.compile_and_save(contract_path, output_path=nef_path, log=False)

            return nef_path, manifest_path

        return contract_path, contract_path

    def compile(self, path: str, root_folder: str = None) -> bytes:
        from boa3.boa3 import Boa3

        with _COMPILER_LOCK:
            result = Boa3.compile(path, root_folder=root_folder)

        return result

    def compile_and_save(self, path: str, root_folder: str = None, debug: bool = False, log: bool = True,
                         output_path: str = None, **kwargs) -> Tuple[bytes, Dict[str, Any]]:

        if not isinstance(output_path, str) or not output_path.endswith('.nef'):
            nef_output, _ = self.get_deploy_file_paths_without_compiling(path)
        else:
            nef_output = output_path

        if nef_output.endswith('.py'):
            nef_output = nef_output.replace('.py', '.nef')
        manifest_output = nef_output.replace('.nef', '.manifest.json')

        from boa3.boa3 import Boa3
        from boa3.internal.neo.contracts.neffile import NefFile
        with _COMPILER_LOCK:
            Boa3.compile_and_save(path, output_path=nef_output, root_folder=root_folder,
                                  show_errors=log, debug=debug)

        get_raw_nef = kwargs['get_raw_nef'] if 'get_raw_nef' in kwargs else False
        with open(nef_output, mode='rb') as nef:
            file = nef.read()
            if get_raw_nef:
                output = file
            else:
                output = NefFile.deserialize(file).script

        with open(manifest_output) as manifest_output:
            import json
            manifest = json.loads(manifest_output.read())

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

    def run_smart_contract(self, test_engine: TestEngine, smart_contract_path: Union[str, bytes], method: str,
                           *arguments: Any, reset_engine: bool = False,
                           fake_storage: Dict[Tuple[str, str], Any] = None,
                           signer_accounts: Iterable[bytes] = (),
                           calling_script_hash: Optional[bytes] = None,
                           expected_result_type: Type = None,
                           rollback_on_fault: bool = True) -> Any:

        if isinstance(smart_contract_path, str) and smart_contract_path.endswith('.py'):
            nef_path, manifest_path = self.get_deploy_file_paths_without_compiling(smart_contract_path)

            with _COMPILER_LOCK:
                if not (os.path.isfile(nef_path) and os.path.isfile(manifest_path)):
                    # both .nef and .manifest.json are required to execute the smart contract
                    self.compile_and_save(smart_contract_path, log=False, output_path=nef_path)
            smart_contract_path = nef_path
        elif isinstance(smart_contract_path, bytes):
            from boa3.internal.neo3.core.types import UInt160
            smart_contract_path = UInt160(smart_contract_path)

        self._set_fake_data(test_engine, fake_storage, signer_accounts, calling_script_hash)
        result = test_engine.run(smart_contract_path, method, *arguments,
                                 reset_engine=reset_engine, rollback_on_fault=rollback_on_fault)

        return self._filter_result(test_engine, expected_result_type, result)

    def run_oracle_response(self, test_engine: TestEngine, request_id: int,
                            response_code: oracleresponse.OracleResponseCode,
                            oracle_result: bytes, reset_engine: bool = False,
                            fake_storage: Dict[Tuple[str, str], Any] = None,
                            signer_accounts: Iterable[bytes] = (),
                            expected_result_type: Type = None,
                            rollback_on_fault: bool = True) -> Any:

        self._set_fake_data(test_engine, fake_storage, signer_accounts)
        result = test_engine.run_oracle_response(request_id, response_code, oracle_result,
                                                 reset_engine=reset_engine, rollback_on_fault=rollback_on_fault)

        return self._filter_result(test_engine, expected_result_type, result)

    def _set_fake_data(self, test_engine: TestEngine,
                       fake_storage: Dict[Tuple[str, str], Any],
                       signer_accounts: Iterable[bytes],
                       calling_script_hash: Optional[bytes] = None):

        if isinstance(fake_storage, dict):
            test_engine.set_storage(fake_storage)

        if calling_script_hash is not None and len(calling_script_hash) == constants.SIZE_OF_INT160:
            test_engine.set_calling_script_hash(calling_script_hash)

        from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope
        for account in signer_accounts:
            test_engine.add_signer_account(account, WitnessScope.Global)

    def _filter_result(self, test_engine, expected_result_type, result) -> Any:
        if test_engine.vm_state is not VMState.HALT and test_engine.error is not None:
            raise TestExecutionException(test_engine.error)

        if expected_result_type is not None:
            if expected_result_type is not str and isinstance(result, str):
                result = String(result).to_bytes()

            if expected_result_type is bool:
                if isinstance(result, bytes):
                    result = Integer.from_bytes(result, signed=True)
                if isinstance(result, int) and result in (False, True):
                    result = bool(result)

            if expected_result_type is bytearray and isinstance(result, bytes):
                result = bytearray(result)

        return result
