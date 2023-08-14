__all__ = [
    'get_config_data',
    'get_account_by_name',
    'get_account_by_address',
    'get_account_by_identifier',
    'get_default_account',
    'get_genesis_block',
    'get_account_from_script_hash_or_id',
    'create_neo_express_instance',
    'reset_neo_express_instance',
    'get_deployed_contracts',
    'get_transaction',
    'get_transaction_log',
    'get_latest_block',
    'get_block',
    'run_batch',
    'oracle_response',
    'Account',
    'Block',
    'Contract',
    'NeoExpressConfig',
    'Transaction',
    'TransactionLog'
]

from typing import List, Union

from boa3.internal.neo3.core.types import UInt256
from boa3_test.test_drive.model.wallet import utils as wallet_utils
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.executor import NeoExpressWrapper
from boa3_test.test_drive.neoxp.model.neoxpconfig import NeoExpressConfig
from boa3_test.test_drive.testrunner.blockchain.block import TestRunnerBlock as Block
from boa3_test.test_drive.testrunner.blockchain.contract import TestRunnerContract as Contract
from boa3_test.test_drive.testrunner.blockchain.transaction import TestRunnerTransaction as Transaction
from boa3_test.test_drive.testrunner.blockchain.transactionlog import TestRunnerTransactionLog as TransactionLog


def get_config_data(neoxp_path: str) -> NeoExpressConfig:
    return NeoExpressWrapper.get_config_data(neoxp_path)


def get_account_by_name(neoxp_config: NeoExpressConfig, account_name) -> Account:
    return next((account for account in neoxp_config.accounts if account.name == account_name),
                None)


def get_account_by_address(neoxp_config: NeoExpressConfig, account_address: str) -> Account:
    return next((account for account in neoxp_config.accounts if account.address == account_address),
                None)


def get_account_by_identifier(neoxp_config: NeoExpressConfig, account_identifier: str) -> Account:
    return next((account for account in neoxp_config.accounts if (account.address == account_identifier
                                                                  or account.name == account_identifier)),
                None)


def get_default_account(neoxp_config: NeoExpressConfig) -> Account:
    return neoxp_config.default_account


def get_genesis_block(neoxp_config: NeoExpressConfig) -> Block:
    return neoxp_config.genesis_block


def get_account_from_script_hash_or_id(neoxp_config: NeoExpressConfig, script_hash_or_address: Union[bytes, str]) -> Account:
    if isinstance(script_hash_or_address, bytes):
        script_hash = script_hash_or_address
        address = wallet_utils.address_from_script_hash(script_hash, neoxp_config.version)
        account = get_account_by_address(neoxp_config, address)
    elif isinstance(script_hash_or_address, str):
        account = get_account_by_identifier(neoxp_config, script_hash_or_address)
        script_hash = wallet_utils.address_to_script_hash(script_hash_or_address, neoxp_config.version)
    else:
        raise TypeError(f"Invalid data type {type(script_hash_or_address)}. Expecting str or bytes")

    if not isinstance(account, Account):
        from boa3.internal.neo3.core.types import UInt160
        from boa3_test.test_drive.neoxp.model.neoxpaccount import NeoExpressAccount
        account = NeoExpressAccount(UInt160(script_hash), neoxp_config.version)

    return account


def create_neo_express_instance(neoxp_path: str) -> str:
    return NeoExpressWrapper.create_neo_express_instance(neoxp_path)


def reset_neo_express_instance(neoxp_path: str, check_point_file: str = None) -> str:
    return NeoExpressWrapper.reset_neo_express_instance(neoxp_path, check_point_file)


def get_deployed_contracts(neoxp_path: str, check_point_file: str = None) -> List[Contract]:
    return NeoExpressWrapper.get_deployed_contracts(neoxp_path, check_point_file)


def get_transaction(neoxp_path: str, tx_hash: UInt256, check_point_file: str = None) -> Transaction:
    return NeoExpressWrapper.get_transaction(neoxp_path, tx_hash, check_point_file)


def get_transaction_log(neoxp_path: str, tx_hash: UInt256, check_point_file: str = None, contract_collection=None) -> TransactionLog:
    return NeoExpressWrapper.get_transaction_log(neoxp_path, tx_hash, check_point_file, contract_collection)


def get_latest_block(neoxp_path: str, check_point_file: str = None) -> Block:
    return NeoExpressWrapper.get_latest_block(neoxp_path, check_point_file)


def get_block(neoxp_path: str, block_hash_or_index: Union[UInt256, int] = None,
              check_point_file: str = None) -> Block:
    return NeoExpressWrapper.get_block(neoxp_path, block_hash_or_index, check_point_file)


def run_batch(neoxp_path: str, batch_path: str, reset: bool = False, check_point_file: str = None) -> str:
    return NeoExpressWrapper.run_batch(neoxp_path, batch_path, reset, check_point_file)


def oracle_response(neoxp_path: str, url: str, response_path: str, request_id: int = None,
                    check_point_file: str = None) -> List[UInt256]:
    return NeoExpressWrapper.oracle_response(neoxp_path, url, response_path, request_id, check_point_file)
