__all__ = [
    'BoaTestCase',
    'AbortException',
    'FaultException',
    'AssertException',
]

import asyncio
import logging
import os
import threading
from typing import Any, Optional, TypeVar, Type, Sequence

from boaconstructor import SmartContractTestCase, AbortException, AssertException
from neo3.api import noderpc
from neo3.api.wrappers import GenericContract
from neo3.core import types
from neo3.network.payloads.verification import Signer
from neo3.wallet import account

from boa3.internal import env, constants
from boa3.internal.exception.CompilerError import CompilerError
from boa3.internal.exception.CompilerWarning import CompilerWarning
from boa3_test.tests.boa_test import (USE_UNIQUE_NAME,  # move theses to this module when refactoring is done
                                      _COMPILER_LOCK,
                                      _LOGGING_LOCK)

# type annotations
T = TypeVar("T")

JsonToken = int | str | bool | None | list['JsonToken'] | dict[str, 'JsonToken']
JsonObject = dict[str, JsonToken]
ContractScript = bytes
CompilerOutput = tuple[ContractScript, JsonObject]

_CONTRACT_LOCK = threading.RLock()


class FaultException(Exception):
    pass


class BoaTestCase(SmartContractTestCase):
    dirname: str
    test_root_dir: str
    default_folder: str

    genesis: account.Account
    _contract: GenericContract | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._use_custom_name = USE_UNIQUE_NAME

    # TODO: Remove method after unit test refactoring is done
    def method_name(self) -> str:
        return self._testMethodName if hasattr(self, '_testMethodName') else self.id()

    @classmethod
    def setUpClass(cls):
        folders = os.path.abspath(__file__).split(os.sep)
        cls.dirname = constants.PATH_SEPARATOR.join(folders[:-3])
        cls.test_root_dir = constants.PATH_SEPARATOR.join(folders[-3:-2])
        cls.default_test_folder = (constants.PATH_SEPARATOR.join((cls.test_root_dir, cls.default_folder))
                                   if len(cls.default_folder) else cls.test_root_dir)

        super(BoaTestCase, cls).setUpClass()

        constants.COMPILER_VERSION = '_unit_tests_'  # to not change test contract script hashes in different versions
        cls.contract_hash = None

        # Due to a lack of an asyncSetupClass we have to do it manually
        # Use this if you for example want to initialise some blockchain state

        # asyncio.run() works because the `IsolatedAsyncioTestCase` class we inherit from
        # hasn't started its own loop yet
        # asyncio.run(cls.asyncSetupClass())
        try:
            asyncio.run(cls.asyncSetupClass())
        except RuntimeError:
            running_loop = asyncio.get_running_loop()
            asyncio.ensure_future(cls.asyncSetupClass(), loop=running_loop)

    @classmethod
    async def asyncSetupClass(cls) -> None:
        cls.genesis = cls.node.wallet.account_get_by_label("committee")

    def tearDown(self):
        if self.contract_hash is not None:
            self.contract_hash = None

        if self._contract is not None:
            self._contract = None
            print(f"'Exit test method {self._testMethodName if hasattr(self, '_testMethodName') else self.id()}'")
            _CONTRACT_LOCK.release()

        super().tearDown()

    @property
    def contract(self) -> GenericContract | None:
        if self._contract is None and self.contract_hash is not None:
            _CONTRACT_LOCK.acquire()
            print(f"'Enter test method {self._testMethodName if hasattr(self, '_testMethodName') else self.id()}'")
            self._contract = GenericContract(self.contract_hash)

        return self._contract

    @classmethod
    async def set_up_contract(cls,
                              *contract_path: str,
                              output_name: str = None,
                              change_manifest_name: bool = False,
                              signing_account: account.Account = None,
                              compile_if_found: bool = False
                              ) -> GenericContract:

        contract_path = cls.get_contract_path(*contract_path)
        cls.contract_hash = await cls.compile_and_deploy(contract_path,
                                                         output_name=output_name,
                                                         change_manifest_name=change_manifest_name,
                                                         signing_account=signing_account,
                                                         compile_if_found=compile_if_found
                                                         )

        return cls.contract

    @classmethod
    async def compile_and_deploy(cls,
                                 contract_path: str,
                                 *,
                                 output_name: str = None,
                                 change_manifest_name: bool = False,
                                 signing_account: account.Account = None,
                                 compile_if_found: bool = False
                                 ) -> types.UInt160:

        nef_abs_path, _ = cls.get_deploy_file_paths(contract_path,
                                                    output_name=output_name,
                                                    change_manifest_name=change_manifest_name,
                                                    compile_if_found=compile_if_found
                                                    )

        if not signing_account:
            signing_account = cls.genesis

        return await cls.deploy(nef_abs_path, signing_account)

    @classmethod
    async def call(
            cls,
            method: str,
            args: Optional[list] = None,
            *,
            return_type: Type[T],
            signing_accounts: Optional[Sequence[account.Account]] = None,
            signers: Optional[Sequence[Signer]] = None,
            target_contract: Optional[types.UInt160] = None,
    ) -> tuple[T, list[noderpc.Notification]]:

        # dict arguments are being pushed to the stack reversed
        args = args.copy()
        for index, arg in enumerate(args):
            if isinstance(arg, dict):
                args[index] = cls._handle_dict_arg(arg)

        return await super().call(method,
                                  args,
                                  return_type=return_type,
                                  signing_accounts=signing_accounts,
                                  signers=signers,
                                  target_contract=target_contract,
                                  )

    @classmethod
    def _handle_dict_arg(cls, arg: dict) -> dict:
        # don't change the original obj
        aux = {}
        for key, item in reversed(arg.items()):
            if isinstance(item, dict):
                item = cls._handle_dict_arg(item)
            aux[key] = item
        return aux

    def unwrap_inner_values(self, value: list | dict):
        if isinstance(value, list):
            for index, item in enumerate(value):
                if not isinstance(item, noderpc.StackItem):
                    continue

                value[index] = self._unwrap_stack_item(item)

        elif isinstance(value, dict):
            aux = value.copy()
            value.clear()
            for key, item in aux.items():
                dict_key = key if not isinstance(key, noderpc.StackItem) else self._unwrap_stack_item(key)
                dict_item = item if not isinstance(item, noderpc.StackItem) else self._unwrap_stack_item(item)
                if isinstance(dict_item, list):
                    if dict_item and isinstance(dict_item[0], tuple):
                        dict_item = self._unwrap_stack_item(
                            noderpc.MapStackItem(noderpc.StackItemType.MAP, dict_item)
                        )
                    else:
                        self.unwrap_inner_values(dict_item)

                value[dict_key] = dict_item

    def _unwrap_stack_item(self, stack_item: noderpc.StackItem) -> Any:
        result = None

        if stack_item.type is noderpc.StackItemType.BYTE_STRING:
            try:
                result = stack_item.as_str()
            except:
                result = stack_item.as_bytes()

        elif stack_item.type is noderpc.StackItemType.INTEGER:
            result = stack_item.as_int()

        elif stack_item.type is noderpc.StackItemType.BOOL:
            result = stack_item.as_bool()

        elif stack_item.type is noderpc.StackItemType.BUFFER:
            try:
                result = stack_item.as_uint160()
            except ValueError:
                try:
                    result = stack_item.as_uint256()
                except ValueError:
                    try:
                        result = stack_item.as_public_key()
                    except ValueError:
                        result = stack_item.value

        elif stack_item.type is noderpc.StackItemType.ARRAY:
            result = stack_item.as_list()
            self.unwrap_inner_values(result)

        elif stack_item.type is noderpc.StackItemType.MAP:
            result = stack_item.as_dict()
            self.unwrap_inner_values(result)

        if result is None:
            result = stack_item.value
        return result

    @classmethod
    async def get_valid_tx(cls) -> types.UInt256 | None:
        """
        Must be called after set_up_contract to ensure a valid response.
        If called before, it may not be able to find a valid tx.
        """
        block_ = None
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host) as rpc_client:
            genesis_balances = await rpc_client.get_nep17_balances(cls.genesis.address)
            for asset in genesis_balances.balances:
                block_ = await rpc_client.get_block(asset.last_updated_block)
                if block_.transactions:
                    break

        if hasattr(block_, 'transactions') and block_.transactions:
            return block_.transactions[0].hash()

    @classmethod
    def _check_vmstate(cls, receipt):
        try:
            super()._check_vmstate(receipt)
        except ValueError as e:
            raise FaultException(receipt.exception)

    def assertCompile(self,
                      contract_path: str,
                      *,
                      root_folder: str = None,
                      fail_fast: bool = False,
                      **kwargs
                      ) -> CompilerOutput:

        py_abs_path = self.get_contract_path(contract_path)
        result = self.compile(
            py_abs_path,
            root_folder=root_folder,
            fail_fast=fail_fast,
            kwargs=kwargs
        )

        return result, {}

    def assertCompilerLogs(self,
                           expected_logged_exception,
                           path
                           ) -> CompilerOutput | str:

        output, error_msg = self._assert_compiler_logs_error(expected_logged_exception, path)
        manifest = {}
        if not issubclass(expected_logged_exception, CompilerError):
            return output, manifest
        else:
            # filter to get only the error message, without location information
            import re

            result = re.search('^\\d+:\\d+ - (?P<msg>.*?)\t\\W+\\<.*?\\>', error_msg)
            try:
                return result.group('msg')
            except BaseException:
                return output, manifest

    def assertCompilerNotLogs(self,
                              expected_logged_exception,
                              path
                              ) -> ContractScript:

        output, expected_logged = self._get_compiler_log_data(expected_logged_exception, path)
        if len(expected_logged) > 0:
            raise AssertionError(f'{expected_logged_exception.__name__} was logged: "{expected_logged[0].message}"')
        return output

    def assertStartsWith(self, first: Any, second: Any):
        if not (hasattr(first, 'startswith') and first.startswith(second)):
            self.fail(f'{first} != {second}')

    def _assert_compiler_logs_error(self,
                                    expected_logged_exception,
                                    path
                                    ) -> tuple[ContractScript, str]:

        output, expected_logged = self._get_compiler_log_data(expected_logged_exception, path)
        if len(expected_logged) < 1:
            raise AssertionError('{0} not logged'.format(expected_logged_exception.__name__))
        return output, expected_logged[0].message

    def _get_compiler_log_data(self,
                               expected_logged_exception,
                               path,
                               *,
                               fail_fast=False
                               ) -> tuple[ContractScript, list[logging.LogRecord]]:
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

    def get_all_compile_log_data(self,
                                 path: str,
                                 *,
                                 get_errors: bool = True,
                                 get_warnings: bool = False,
                                 fail_fast: bool = False
                                 ) -> tuple[list[CompilerError], list[CompilerWarning]]:

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

    @staticmethod
    def get_dir_path(*args: str) -> str:
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
        return constants.PATH_SEPARATOR.join((root_path, dir_folder))

    @classmethod
    def get_contract_path(cls, *args: str) -> str:
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

        values = [None, cls.default_test_folder, env.PROJECT_ROOT_DIRECTORY]
        for index, value in enumerate(reversed(args)):
            values[index] = value

        contract_name, dir_folder, root_path = values

        from os import path
        if not path.exists(dir_folder) and root_path is env.PROJECT_ROOT_DIRECTORY:
            path_folder = constants.PATH_SEPARATOR.join((root_path, dir_folder))
            if not path.exists(path_folder) and not dir_folder.startswith(cls.test_root_dir):
                path_folder = constants.PATH_SEPARATOR.join((root_path, cls.test_root_dir, dir_folder))
                if not path.exists(path_folder):
                    path_folder = constants.PATH_SEPARATOR.join((root_path, cls.default_test_folder, dir_folder))

            dir_folder = path_folder
        else:
            if path.exists(dir_folder):
                dir_folder = os.path.abspath(dir_folder)
            else:
                dir_folder = constants.PATH_SEPARATOR.join((root_path, dir_folder))

        if not contract_name.endswith('.py'):
            contract_name = contract_name + '.py'

        path = constants.PATH_SEPARATOR.join((dir_folder, contract_name))
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        else:
            path = os.path.abspath(path).replace(os.path.sep, constants.PATH_SEPARATOR)
        return path

    @classmethod
    def get_deploy_file_paths_without_compiling(cls, contract_path: str, output_name: str = None) -> tuple[str, str]:
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

    @classmethod
    def get_deploy_file_paths(cls, *args: str, output_name: str = None,
                              compile_if_found: bool = False, change_manifest_name: bool = False,
                              debug: bool = False) -> tuple[str, str]:
        contract_path = cls.get_contract_path(*args)
        if isinstance(contract_path, str):
            nef_path, manifest_path = cls.get_deploy_file_paths_without_compiling(contract_path, output_name)
            if contract_path.endswith('.py'):
                with _COMPILER_LOCK:
                    if compile_if_found or not (os.path.isfile(nef_path) and os.path.isfile(manifest_path)):
                        # both .nef and .manifest.json are required to execute the smart contract
                        cls.compile_and_save(contract_path, output_name=nef_path, log=True,
                                             change_manifest_name=change_manifest_name,
                                             debug=debug,
                                             use_unique_name=False  # already using unique name
                                             )

            return nef_path, manifest_path

        return contract_path, contract_path

    @staticmethod
    def compile(path: str, root_folder: str = None, fail_fast: bool = False, **kwargs) -> ContractScript:
        from boa3.boa3 import Boa3

        with _COMPILER_LOCK:
            result = Boa3.compile(path, root_folder=root_folder, fail_fast=fail_fast,
                                  log_level=logging.getLevelName(logging.INFO),
                                  optimize=kwargs['optimize'] if 'optimize' in kwargs else True
                                  )

        return result

    @classmethod
    def compile_and_save(cls, path: str, root_folder: str = None, debug: bool = False, log: bool = True,
                         output_name: str = None, env: str = None, **kwargs) -> CompilerOutput:

        if output_name is not None:
            output_dir, manifest_name = os.path.split(output_name)  # get name
            if len(output_dir) == 0:
                output_dir, _ = os.path.split(path)
                output_name = constants.PATH_SEPARATOR.join((output_dir, manifest_name))
            manifest_name, _ = os.path.splitext(manifest_name)  # remove extension
        else:
            manifest_name = None

        use_unique_name = kwargs['use_unique_name'] if 'use_unique_name' in kwargs else True
        if not isinstance(output_name, str) or not output_name.endswith('.nef'):
            nef_output, _ = cls.get_deploy_file_paths_without_compiling(path)
        elif use_unique_name and USE_UNIQUE_NAME:
            nef_output, _ = cls.get_deploy_file_paths_without_compiling(output_name)
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

    def get_debug_info(self, path: str) -> JsonObject | None:
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

    def get_output(self, path: str, root_folder: str = None) -> CompilerOutput:
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

    def get_serialized_output(self, path: str) -> CompilerOutput:
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
