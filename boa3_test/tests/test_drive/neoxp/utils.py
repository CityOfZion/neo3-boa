__all__ = [
    'get_account_by_name',
    'get_account_by_address',
    'get_account_by_identifier',
    'get_default_account',
    'get_genesis_block',
    'get_account_from_script_hash_or_id',
    'reset_neo_express_instance',
    'get_deployed_contracts',
    'get_transaction',
    'get_transaction_log',
    'get_latest_block',
    'get_block',
    'run_batch',
    'oracle_response'
]


import logging

from filelock import FileLock

from boa3.internal import env
from boa3.internal.neo3.core.types import UInt256
from boa3_test.test_drive.neoxp import utils as neoxp_utils
from boa3_test.test_drive.neoxp.executor import NeoExpressWrapper
from boa3_test.test_drive.neoxp.model.neoxpconfig import NeoExpressConfig
from boa3_test.test_drive.neoxp.utils import (Account,
                                              Block,
                                              Contract,
                                              Transaction,
                                              TransactionLog,
                                              )

_NEOXP_CONFIG = NeoExpressConfig(f'{env.NEO_EXPRESS_INSTANCE_DIRECTORY}/default.neo-express')
_NEOXP_FILE_LOCK = FileLock(f'{env.TEST_RUNNER_DIRECTORY}/test-runner.lock')
logging.getLogger("filelock").setLevel(logging.INFO)


def get_account_by_name(account_name) -> Account:
    return neoxp_utils.get_account_by_name(_NEOXP_CONFIG, account_name)


def get_account_by_address(account_address: str) -> Account:
    return neoxp_utils.get_account_by_address(_NEOXP_CONFIG, account_address)


def get_account_by_identifier(account_identifier: str) -> Account:
    return neoxp_utils.get_account_by_identifier(_NEOXP_CONFIG, account_identifier)


def get_account_from_script_hash_or_id(script_hash_or_address: bytes | str) -> Account:
    return neoxp_utils.get_account_from_script_hash_or_id(_NEOXP_CONFIG, script_hash_or_address)


def get_default_account() -> Account:
    return _NEOXP_CONFIG.default_account


def get_address_version() -> int:
    return _NEOXP_CONFIG.version


def get_magic() -> int:
    return _NEOXP_CONFIG.magic


def get_genesis_block() -> Block:
    return _NEOXP_CONFIG.genesis_block


class _BoaNeoExpressWrapper(NeoExpressWrapper):
    @classmethod
    def _run_cli(cls, *neoxp_args: str):
        with _NEOXP_FILE_LOCK:
            cli_result = super()._run_cli(*neoxp_args)
        return cli_result


def reset_neo_express_instance(neoxp_path: str, check_point_file: str = None) -> str:
    return _BoaNeoExpressWrapper.reset_neo_express_instance(neoxp_path, check_point_file)


def get_deployed_contracts(neoxp_path: str, check_point_file: str = None) -> list[Contract]:
    return _BoaNeoExpressWrapper.get_deployed_contracts(neoxp_path, check_point_file)


def get_transaction(neoxp_path: str, tx_hash: UInt256, check_point_file: str = None) -> Transaction:
    return _BoaNeoExpressWrapper.get_transaction(neoxp_path, tx_hash, check_point_file)


def get_transaction_log(neoxp_path: str, tx_hash: UInt256, check_point_file: str = None, contract_collection=None) -> TransactionLog:
    return _BoaNeoExpressWrapper.get_transaction_log(neoxp_path, tx_hash, check_point_file, contract_collection)


def get_latest_block(neoxp_path: str, check_point_file: str = None) -> Block:
    return _BoaNeoExpressWrapper.get_latest_block(neoxp_path, check_point_file)


def get_block(neoxp_path: str, block_hash_or_index: UInt256 | int = None,
              check_point_file: str = None) -> Block:
    return _BoaNeoExpressWrapper.get_block(neoxp_path, block_hash_or_index, check_point_file)


def run_batch(neoxp_path: str, batch_path: str, reset: bool = False, check_point_file: str = None) -> str:
    return _BoaNeoExpressWrapper.run_batch(neoxp_path, batch_path, reset, check_point_file)


def oracle_response(neoxp_path: str, url: str, response_path: str, request_id: int = None,
                    check_point_file: str = None) -> list[UInt256]:
    return _BoaNeoExpressWrapper.oracle_response(neoxp_path, url, response_path, request_id, check_point_file)
