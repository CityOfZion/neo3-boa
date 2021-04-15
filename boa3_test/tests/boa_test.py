import os
from typing import Any, Dict, Iterable, Optional, Tuple, Type, Union
from unittest import TestCase

from boa3 import env
from boa3.analyser.analyser import Analyser
from boa3.compiler.compiler import Compiler
from boa3.neo.smart_contract.VoidType import VoidType
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3.neo3.vm import VMState
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine
from boa3_test.tests.test_classes.transactionattribute import oracleresponse


class BoaTest(TestCase):
    dirname: str = None

    ASSERT_RESULTED_FALSE_MSG = 'ASSERT is executed with false result.'
    MAP_KEY_NOT_FOUND_ERROR_MSG = 'Key not found in Map'
    VALUE_IS_OUT_OF_RANGE_MSG = 'The value is out of range'
    STORAGE_VALUE_IS_OUT_OF_RANGE_MSG = 'Specified argument was out of the range of valid values.'
    CALLED_CONTRACT_DOES_NOT_EXIST_MSG = 'Called Contract Does Not Exist'
    ABORTED_CONTRACT_MSG = 'ABORT is executed'

    default_folder: str = ''

    @classmethod
    def setUpClass(cls):
        folders = os.path.abspath(__file__).split(os.sep)
        cls.dirname = '/'.join(folders[:-3])
        cls.test_root_dir = '/'.join(folders[-3:-2])
        cls.default_test_folder = ('{0}/{1}'.format(cls.test_root_dir, cls.default_folder)
                                   if len(cls.default_folder) else cls.test_root_dir)

        super(BoaTest, cls).setUpClass()

    def get_compiler_analyser(self, compiler: Compiler) -> Analyser:
        return compiler._analyser

    def indent_text(self, text: str, no_spaces: int = 4) -> str:
        import re
        return re.sub('\n[ \t]+', '\n' + ' ' * no_spaces, text)

    def assertCompilerLogs(self, expected_logged_exception, path):
        output = None
        with self.assertLogs() as log:
            from boa3.exception.NotLoadedException import NotLoadedException
            try:
                from boa3.boa3 import Boa3
                output = Boa3.compile(path)
            except NotLoadedException:
                # when an compiler error is logged this exception is raised.
                pass

        for logger in log.records:
            import logging
            logging.log(level=logger.levelno, msg=logger.msg)

        if len([exception for exception in log.records if isinstance(exception.msg, expected_logged_exception)]) <= 0:
            raise AssertionError('{0} not logged'.format(expected_logged_exception.__name__))
        return output

    def assertIsVoid(self, obj: Any):
        if obj is not VoidType:
            self.fail('{0} is not Void'.format(obj))

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

    def compile_and_save(self, path: str, log: bool = True) -> Tuple[bytes, Dict[str, Any]]:
        nef_output = path.replace('.py', '.nef')
        manifest_output = path.replace('.py', '.manifest.json')

        from boa3.boa3 import Boa3
        from boa3.neo.contracts.neffile import NefFile
        Boa3.compile_and_save(path, show_errors=log)

        with open(nef_output, mode='rb') as nef:
            file = nef.read()
            output = NefFile.deserialize(file).script

        with open(manifest_output) as manifest_output:
            import json
            manifest = json.loads(manifest_output.read())

        return output, manifest

    def get_debug_info(self, path: str) -> Optional[Dict[str, Any]]:
        debug_info_output = path.replace('.py', '.nefdbgnfo')

        if not os.path.isfile(debug_info_output):
            return None

        from zipfile import ZipFile
        with ZipFile(debug_info_output, 'r') as dbgnfo:
            import json
            debug_info = json.loads(dbgnfo.read(os.path.basename(path.replace('.py', '.debug.json'))))
        return debug_info

    def get_output(self, path: str) -> Tuple[bytes, Dict[str, Any]]:
        nef_output = path.replace('.py', '.nef')
        manifest_output = path.replace('.py', '.manifest.json')

        from boa3.neo.contracts.neffile import NefFile

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
        nef_output = path.replace('.py', '.nef')
        manifest_output = path.replace('.py', '.manifest.json')

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
                           expected_result_type: Type = None,
                           rollback_on_fault: bool = True) -> Any:

        if isinstance(smart_contract_path, str) and smart_contract_path.endswith('.py'):
            if not (os.path.isfile(smart_contract_path.replace('.py', '.nef'))
                    and os.path.isfile(smart_contract_path.replace('.py', '.manifest.json'))):
                # both .nef and .manifest.json are required to execute the smart contract
                self.compile_and_save(smart_contract_path, log=False)
            smart_contract_path = smart_contract_path.replace('.py', '.nef')
        elif isinstance(smart_contract_path, bytes):
            from boa3.neo3.core.types import UInt160
            smart_contract_path = UInt160(smart_contract_path)

        self._set_fake_data(test_engine, fake_storage, signer_accounts)
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
                       signer_accounts: Iterable[bytes]):

        if isinstance(fake_storage, dict):
            test_engine.set_storage(fake_storage)

        for account in signer_accounts:
            test_engine.add_signer_account(account)

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
