__all__ = [
    'BoaTestCase',
    'BoaTestEvent',
    'Nep17TransferEvent',
    'AbortException',
    'AssertException',
    'FaultException',
    '_COMPILER_LOCK',
    '_LOGGING_LOCK',
    'USE_UNIQUE_NAME',
]

import abc
import asyncio
import logging
import os
import threading
from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol, TypeVar, Type, Sequence, Self

from boaconstructor import (SmartContractTestCase,
                            AbortException,
                            AssertException,
                            Nep17TransferEvent as _Nep17TransferEvent,
                            PostProcessor,
                            )
from neo3.api import noderpc
from neo3.api.wrappers import GenericContract
from neo3.contracts import manifest
from neo3.core import types, cryptography
from neo3.network.payloads import block, transaction
from neo3.network.payloads.verification import Signer
from neo3.wallet import account

from boa3.internal import env, constants
from boa3.internal.analyser.analyser import Analyser
from boa3.internal.compiler.compiler import Compiler
from boa3.internal.exception.CompilerError import CompilerError
from boa3.internal.exception.CompilerWarning import CompilerWarning
from boa3_test.tests.annotation import JsonObject

# type annotations
T = TypeVar("T")

ContractScript = bytes
CompilerOutput = tuple[ContractScript, JsonObject]


class TestNotification(Protocol):
    @classmethod
    def from_notification(cls, n: noderpc.Notification) -> Self:
        ...


_CONTRACT_LOCK = threading.RLock()
_COMPILER_LOCK = threading.RLock()
_LOGGING_LOCK = threading.Lock()

USE_UNIQUE_NAME = False


class FaultException(Exception):
    pass


@dataclass
class BoaTestEvent:
    contract: types.UInt160
    name: str
    state: tuple

    @classmethod
    def from_notification(cls, n: noderpc.Notification, *state_type: Type) -> Self:
        if not state_type:
            if cls is not BoaTestEvent:
                # for inherited classes
                return cls.from_untyped_notification(n)
            expected_type = tuple
        else:
            expected_type = tuple[state_type]

        state = BoaTestCase._unwrap_stack_item(n.state, expected_type=expected_type)
        return BoaTestEvent(contract=n.contract,
                            name=n.event_name,
                            state=state
                            )

    @classmethod
    @abc.abstractmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        if cls is BoaTestEvent:
            state_type = tuple()
        else:
            state_type = cls.__annotations__.values()
        return cls.from_notification(n, *state_type)


@dataclass
class Nep17TransferEvent(_Nep17TransferEvent):
    @classmethod
    def from_notification(cls, n: noderpc.Notification) -> Self:
        try:
            return super().from_notification(n)
        except ValueError:
            from neo3.api import StackItemType
            stack = n.state.as_list()
            source = stack[0].as_uint160() if stack[0].type != StackItemType.ANY else stack[0].as_none()
            destination = stack[1].as_uint160() if stack[1].type != StackItemType.ANY else stack[1].as_none()
            amount = stack[2].as_int()
            return cls(source, destination, amount)


@dataclass
class Nep11TransferEvent(Nep17TransferEvent):
    token_id: str

    @classmethod
    def from_notification(cls, n: noderpc.Notification) -> Self:
        from neo3.api import StackItemType
        stack = n.state.as_list()
        source = stack[0].as_uint160() if stack[0].type != StackItemType.ANY else stack[0].as_none()
        destination = stack[1].as_uint160() if stack[1].type != StackItemType.ANY else stack[1].as_none()
        amount = stack[2].as_int()
        token_id = stack[3].as_str()
        return cls(source, destination, amount, token_id)


class BoaTestCase(SmartContractTestCase):
    dirname: str
    test_root_dir: str
    default_folder: str

    genesis: account.Account
    deployed_contracts: dict[str, types.UInt160]
    _contract: GenericContract | None = None
    called_tx: types.UInt256

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
                                   if hasattr(cls, 'default_folder') and len(cls.default_folder) else cls.test_root_dir)

        super(BoaTestCase, cls).setUpClass()

        constants.COMPILER_VERSION = '_unit_tests_'  # to not change test contract script hashes in different versions
        cls.contract_hash = None
        cls.called_tx = None
        cls.deployed_contracts = {}

        cls.setupTestCase()

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
    def setupTestCase(cls):
        cls.genesis = cls.node.wallet.account_get_by_label("committee")

    @classmethod
    async def asyncSetupClass(cls) -> None:
        pass

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
    async def set_up_contract(
            cls,
            *contract_path: str,
            output_name: str = None,
            change_manifest_name: bool = False,
            signing_account: account.Account = None,
            compile_if_found: bool = False,
            **kwargs
    ) -> GenericContract:

        contract_path = cls.get_contract_path(*contract_path)
        cls.contract_hash = await cls.compile_and_deploy(contract_path,
                                                         output_name=output_name,
                                                         change_manifest_name=change_manifest_name,
                                                         signing_account=signing_account,
                                                         compile_if_found=compile_if_found,
                                                         **kwargs
                                                         )

        return cls.contract

    @classmethod
    async def compile_and_deploy(
            cls,
            contract_path: str,
            *extra_args: str,
            output_name: str = None,
            change_manifest_name: bool = False,
            signing_account: account.Account = None,
            compile_if_found: bool = False,
            **kwargs
    ) -> types.UInt160:

        nef_abs_path, _ = cls.get_deploy_file_paths(*(contract_path, *extra_args),
                                                    output_name=output_name,
                                                    change_manifest_name=change_manifest_name,
                                                    compile_if_found=compile_if_found,
                                                    **kwargs
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

        return_type_class = return_type.__origin__ if hasattr(return_type, '__origin__') else return_type
        expected_values = return_type.__args__ if hasattr(return_type, '__args__') else ()

        if return_type_class is tuple:
            internal_return_type = list
        elif return_type is bytearray:
            internal_return_type = bytes
        else:
            internal_return_type = return_type_class

        result, events = await super().call(method,
                                            args,
                                            return_type=internal_return_type,
                                            signing_accounts=signing_accounts,
                                            signers=signers,
                                            target_contract=target_contract,
                                            )

        if isinstance(result, (list, dict)):
            cls.unwrap_inner_values(result, *expected_values, expected_result=return_type_class)
        if return_type_class is tuple:
            result = tuple(result)
        elif return_type_class is bytearray:
            result = bytearray(result)

        return result, events

    @classmethod
    async def deploy(
            cls,
            path_to_nef: str,
            signing_account: account.Account
    ) -> types.UInt160:

        import inspect
        import pathlib

        frame = inspect.stack()[1]
        manifest_path = (pathlib.Path(frame.filename)
                         .parent
                         .joinpath(path_to_nef)
                         .with_suffix("")
                         .with_suffix(".manifest.json")
                         )

        try:
            contract_hash = await super().deploy(
                path_to_nef,
                signing_account
            )
            _manifest = manifest.ContractManifest.from_file(str(manifest_path))
            cls.deployed_contracts[_manifest.name] = contract_hash
            return contract_hash

        except ValueError as e:
            # if the contract is already deployed, returns its script hash instead of raising an error
            if not (e.args and isinstance(e.args[0], str) and 'contract already exists' in e.args[0]):
                raise e

            _manifest = manifest.ContractManifest.from_file(str(manifest_path))
            if _manifest.name not in cls.deployed_contracts:
                raise e

            return cls.deployed_contracts[_manifest.name]

    @classmethod
    async def get_storage(
            cls,
            prefix: Optional[bytes] = None,
            *,
            target_contract: Optional[types.UInt160] = None,
            remove_prefix: bool = False,
            key_post_processor: Optional[PostProcessor] = None,
            values_post_processor: Optional[PostProcessor] = None,
    ) -> dict[bytes, bytes]:
        try:
            return await super().get_storage(
                prefix,
                target_contract=target_contract,
                remove_prefix=remove_prefix,
                key_post_processor=key_post_processor,
                values_post_processor=values_post_processor
            )
        except TypeError:
            return {}

    @classmethod
    def unwrap_inner_values(
            cls,
            value: list | dict,
            *args: type,
            expected_result: Type[T] | None = None
    ):
        if isinstance(value, list):
            if expected_result not in (list, tuple):
                expected_result = list

            list_type = args[0] if len(args) else None
            for index, item in enumerate(value):
                if not isinstance(item, noderpc.StackItem):
                    continue

                if expected_result is tuple:
                    list_type = args[index] if len(args) > index else None
                value[index] = cls._unwrap_stack_item(item, list_type)

        elif isinstance(value, dict):
            if expected_result is not dict:
                expected_result = dict

            dict_key_type = args[0] if len(args) else None
            dict_value_type = args[1] if len(args) > 1 else None
            aux = value.copy()
            value.clear()
            for key, item in aux.items():

                if dict_key_type not in (None, bytes, bytearray) and isinstance(key, bytes):
                    key = noderpc.StackItem(
                        noderpc.StackItemType.BYTE_STRING, key
                    )
                if dict_value_type not in (None, bytes, bytearray) and isinstance(item, bytes):
                    item = noderpc.StackItem(
                        noderpc.StackItemType.BYTE_STRING, item
                    )

                dict_key = key if not isinstance(key, noderpc.StackItem) else cls._unwrap_stack_item(key, dict_key_type)
                dict_item = item if not isinstance(item, noderpc.StackItem) else cls._unwrap_stack_item(item,
                                                                                                        dict_value_type)
                if isinstance(dict_item, list):
                    if dict_item and isinstance(dict_item[0], tuple):
                        dict_item = cls._unwrap_stack_item(
                            noderpc.MapStackItem(noderpc.StackItemType.MAP, dict_item),
                            *args[:2]
                        )
                    else:
                        cls.unwrap_inner_values(dict_item, *args[:2])

                value[dict_key] = dict_item

    @classmethod
    def _unwrap_stack_item(
            cls,
            stack_item: noderpc.StackItem,
            expected_type: type | None = None
    ) -> Any:
        result = None

        if stack_item.type is noderpc.StackItemType.STRUCT:
            stack_item.type = noderpc.StackItemType.ARRAY

        if stack_item.type is noderpc.StackItemType.BYTE_STRING:
            if expected_type is str:
                result = stack_item.as_str()
            elif expected_type is bytes:
                result = stack_item.as_bytes()
            elif expected_type is bytearray:
                result = bytearray(stack_item.as_bytes())
            elif expected_type is types.UInt160:
                result = stack_item.as_uint160()
            elif expected_type is types.UInt256:
                result = stack_item.as_uint256()
            elif expected_type is cryptography.ECPoint:
                result = stack_item.as_public_key()
            else:
                try:
                    result = stack_item.as_str()
                except:
                    result = stack_item.as_bytes()

        elif stack_item.type is noderpc.StackItemType.INTEGER:
            result = stack_item.as_int()

        elif stack_item.type is noderpc.StackItemType.BOOL:
            result = stack_item.as_bool()

        elif stack_item.type is noderpc.StackItemType.BUFFER:
            if expected_type is str:
                result = stack_item.as_str()
            elif expected_type is bytes:
                result = stack_item.as_bytes()
            elif expected_type is bytearray:
                result = bytearray(stack_item.as_bytes())
            elif expected_type is types.UInt160:
                result = stack_item.as_uint160()
            elif expected_type is types.UInt256:
                result = stack_item.as_uint256()
            elif expected_type is cryptography.ECPoint:
                result = stack_item.as_public_key()
            else:
                try:
                    result = stack_item.as_uint160()
                except ValueError:
                    try:
                        result = stack_item.as_uint256()
                    except ValueError:
                        try:
                            result = stack_item.as_public_key()
                        except BaseException:
                            try:
                                result = stack_item.as_str()
                            except BaseException:
                                result = stack_item.as_bytes()

        elif stack_item.type is noderpc.StackItemType.ARRAY:
            result = stack_item.as_list()
            inner_list_type = expected_type.__origin__ if hasattr(expected_type, '__origin__') else expected_type
            inner_list_args = expected_type.__args__ if hasattr(expected_type, '__args__') else ()
            cls.unwrap_inner_values(result, *inner_list_args, expected_result=inner_list_type)

            if inner_list_type is tuple:
                result = tuple(result)

        elif stack_item.type is noderpc.StackItemType.MAP:
            result = stack_item.as_dict()
            inner_dict_type = expected_type.__args__ if hasattr(expected_type, '__args__') else ()
            cls.unwrap_inner_values(result, *inner_dict_type, expected_result=dict)

        if result is None:
            result = stack_item.value
        return result

    def filter_events(
            self,
            events: list[noderpc.Notification],
            *,
            origin: types.UInt160 | list[types.UInt160] = None,
            event_name: str = None,
            notification_type: Type[T] = noderpc.Notification
    ) -> list[T]:

        if issubclass(notification_type, BoaTestEvent):
            convert_event: Callable[[noderpc.Notification], BoaTestEvent] = notification_type.from_untyped_notification
        elif hasattr(notification_type, 'from_notification'):
            convert_event: Callable[[noderpc.Notification], TestNotification] = notification_type.from_notification
        else:
            convert_event: Callable[[noderpc.Notification], noderpc.Notification] = lambda event: event

        if origin is None and event_name is None:
            return [convert_event(notification) for notification in events]

        if origin is None:
            return [convert_event(notification) for notification in events if notification.event_name == event_name]
        elif not isinstance(origin, list):
            origin = [origin]

        if event_name is None:
            return [convert_event(notification) for notification in events
                    if notification.contract in origin
                    ]
        else:
            return [convert_event(notification) for notification in events
                    if notification.event_name == event_name and notification.contract in origin
                    ]

    @classmethod
    async def get_valid_tx(cls) -> types.UInt256 | None:
        """
        Must be called after set_up_contract to ensure a valid response.
        If called before, it may not be able to find a valid tx.
        """
        if cls.called_tx is not None:
            return cls.called_tx

        block_ = None
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host) as rpc_client:
            best_block_hash = await rpc_client.get_best_block_hash()
            best_block = await rpc_client.get_block(best_block_hash)
            if len(best_block.transactions):
                return best_block.transactions[0].hash()

            genesis_balances = await rpc_client.get_nep17_balances(cls.genesis.address)
            for asset in genesis_balances.balances:
                block_ = await rpc_client.get_block(asset.last_updated_block)
                if block_.transactions:
                    break

        if hasattr(block_, 'transactions') and block_.transactions:
            return block_.transactions[0].hash()

    @classmethod
    async def get_last_tx(cls) -> transaction.Transaction:
        if cls.called_tx:
            async with noderpc.NeoRpcClient(cls.node.facade.rpc_host) as rpc_client:
                return await rpc_client.get_transaction(cls.called_tx)

    @classmethod
    async def get_genesis_block(cls) -> block.Block:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host) as rpc_client:
            return await rpc_client.get_block(0)

    @classmethod
    async def get_latest_block(cls) -> block.Block:
        """
        Get the latest block emitted in the local chain
        """
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host) as rpc_client:
            best_block_hash = await rpc_client.get_best_block_hash()
            return await rpc_client.get_block(best_block_hash)

    @classmethod
    async def get_last_block(cls, tx_hash: types.UInt256) -> block.Block:
        """
        Returns the last block before the emission of a transaction if it exists
        """
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host) as rpc_client:
            block_index = await rpc_client.get_transaction_height(tx_hash)
            if block_index > 0:
                block_index -= 1
            return await rpc_client.get_block(block_index)

    @classmethod
    def _check_vmstate(cls, receipt):
        try:
            super()._check_vmstate(receipt)
        except ValueError as e:
            raise FaultException(receipt.exception)
        if hasattr(receipt, 'tx_hash'):
            cls.called_tx = receipt.tx_hash

    def get_all_symbols(
            self,
            compiler: Compiler,
            *,
            symbol_type: Type[T],
            debug_info: bool = False
    ) -> dict[str, T]:

        from boa3.internal.compiler.filegenerator.filegenerator import FileGenerator
        from boa3.internal.model.method import Method

        generator = FileGenerator(compiler.result, compiler._analyser, compiler._entry_smart_contract)
        symbols = {}

        if debug_info and symbol_type is Method:
            iterate_target = generator._methods_with_imports
        else:
            compiler_analyser = self.get_compiler_analyser(compiler)
            iterate_target = compiler_analyser.symbol_table

        for name, symbol in iterate_target.items():
            if isinstance(symbol, symbol_type):
                if isinstance(name, tuple):
                    name = constants.VARIABLE_NAME_SEPARATOR.join(name)

                symbols[name] = symbol
                if hasattr(symbol, 'name') and symbol.name not in symbols:
                    symbols[symbol.name] = symbol

        return symbols

    def assertCompile(
            self,
            contract_path: str,
            *,
            root_folder: str = None,
            fail_fast: bool = False,
            get_manifest: bool = False,
            **kwargs
    ) -> CompilerOutput:

        py_abs_path = self.get_contract_path(contract_path)
        if not get_manifest:
            result_manifest = {}
            result = self.compile(
                py_abs_path,
                root_folder=root_folder,
                fail_fast=fail_fast,
                **kwargs
            )
        else:
            result, result_manifest = self.compile_and_save(
                py_abs_path,
                root_folder=root_folder,
                fail_fast=fail_fast,
                **kwargs
            )

        return result, result_manifest

    def assertCompilerLogs(
            self,
            expected_logged_exception,
            *path: str
    ) -> CompilerOutput | str:
        py_abs_path = self.get_contract_path(*path)
        output, error_msg = self._assert_compiler_logs_error(expected_logged_exception, py_abs_path)

        if not issubclass(expected_logged_exception, CompilerError):
            return self.compile_and_save(py_abs_path)
        else:
            # filter to get only the error message, without location information
            import re

            result = re.search('^\\d+:\\d+ - (?P<msg>.*?)\t\\W+\\<.*?\\>', error_msg)
            try:
                return result.group('msg')
            except BaseException:
                return output, manifest

    def assertCompilerNotLogs(
            self,
            expected_logged_exception,
            path
    ) -> ContractScript:

        output, expected_logged = self._get_compiler_log_data(expected_logged_exception, path)
        if len(expected_logged) > 0:
            raise AssertionError(f'{expected_logged_exception.__name__} was logged: "{expected_logged[0].message}"')
        return output

    def assertObjectEqual(self, first: Any, second: Any, msg: str | None = None):
        default_message = msg if msg is not None else f'{first} != {second}'

        if first == second:
            return self.assertEqual(first, second, default_message)
        elif second == first:
            return self.assertEqual(second, first, default_message)

        first_variables = ([value for key, value in vars(type(first)).items()
                            if not key.endswith('__') and not callable(value)]
                           + list(vars(first).values())
                           )
        if isinstance(second, list):
            second_variables = second
        else:
            second_variables = ([value for key, value in vars(type(second)).items()
                                 if not key.endswith('__') and not callable(value)]
                                + list(vars(second).values())
                                )
        if msg is None:
            default_message = f'{first_variables} != {second_variables}'
        return self.assertEqual(first_variables, second_variables, default_message)

    def assertStartsWith(self, first: Any, second: Any):
        if not (hasattr(first, 'startswith') and first.startswith(second)):
            self.fail(f'{first} != {second}')

    def _assert_compiler_logs_error(
            self,
            expected_logged_exception,
            path
    ) -> tuple[ContractScript, str]:

        output, expected_logged = self._get_compiler_log_data(expected_logged_exception, path)
        if len(expected_logged) < 1:
            raise AssertionError('{0} not logged'.format(expected_logged_exception.__name__))
        return output, expected_logged[0].message

    def _get_compiler_log_data(
            self,
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

    def get_all_compile_log_data(
            self,
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
    def get_deploy_file_paths(
            cls,
            *args: str,
            output_name: str = None,
            compile_if_found: bool = False,
            change_manifest_name: bool = False,
            debug: bool = False,
            **kwargs
    ) -> tuple[str, str]:
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
                                             use_unique_name=False,  # already using unique name
                                             **kwargs
                                             )

            return nef_path, manifest_path

        return contract_path, contract_path

    @staticmethod
    def compile(
            path: str,
            root_folder: str = None,
            fail_fast: bool = False,
            **kwargs
    ) -> ContractScript:
        from boa3.boa3 import Boa3

        with _COMPILER_LOCK:
            result = Boa3.compile(path, root_folder=root_folder, fail_fast=fail_fast,
                                  log_level=logging.getLevelName(logging.INFO),
                                  optimize=kwargs['optimize'] if 'optimize' in kwargs else True
                                  )

        return result

    @classmethod
    def compile_and_save(
            cls,
            path: str,
            root_folder: str = None,
            debug: bool = False,
            log: bool = True,
            output_name: str = None,
            env: str = None,
            **kwargs
    ) -> CompilerOutput:

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
        return self._get_compiler_output(
            path=path,
            root_folder=root_folder,
            deserialize=True
        )

    def get_serialized_output(self, path: str) -> CompilerOutput:
        return self._get_compiler_output(
            path=path,
            deserialize=False
        )

    def _get_compiler_output(self, path: str, deserialize: bool, root_folder: str = None):
        if path.endswith('.nef'):
            nef_output = path
            manifest_output = path.replace('.nef', '.manifest.json')
        else:
            nef_output, manifest_output = self.get_deploy_file_paths_without_compiling(path)

        with _COMPILER_LOCK:
            if not os.path.isfile(nef_output):
                return self.compile_and_save(path, root_folder=root_folder, get_raw_nef=not deserialize)

        from boa3.internal.neo.contracts.neffile import NefFile

        if not os.path.isfile(nef_output):
            output = bytes()
        else:
            with open(nef_output, mode='rb') as nef:
                file = nef.read()
                if deserialize:
                    output = NefFile.deserialize(file).script
                else:
                    output = file

        if not os.path.isfile(manifest_output):
            manifest = {}
        else:
            with open(manifest_output) as manifest_output:
                import json
                manifest = json.loads(manifest_output.read())

        return output, manifest

    def get_compiler_analyser(self, compiler: Compiler) -> Analyser:
        return compiler._analyser
