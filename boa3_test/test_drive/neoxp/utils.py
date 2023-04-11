import logging
import os.path
import re
import subprocess
import threading
from typing import Tuple, List, Union

from filelock import FileLock

from boa3.internal import env
from boa3.internal.neo3.core.types import UInt256
from boa3_test.test_drive.model.wallet import utils as wallet_utils
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import neoexpresscommand as neoxp
from boa3_test.test_drive.neoxp.model.neoxpconfig import NeoExpressConfig
from boa3_test.test_drive.testrunner.blockchain.block import TestRunnerBlock as Block
from boa3_test.test_drive.testrunner.blockchain.contract import TestRunnerContract as Contract
from boa3_test.test_drive.testrunner.blockchain.transaction import TestRunnerTransaction as Transaction
from boa3_test.test_drive.testrunner.blockchain.transactionlog import TestRunnerTransactionLog as TransactionLog

_NEOXP_CONFIG = NeoExpressConfig(f'{env.NEO_EXPRESS_INSTANCE_DIRECTORY}/default.neo-express')
_NEOXP_CONFIG_LOCK = threading.Lock()
_NEOXP_FILE_LOCK = FileLock(f'{env.TEST_RUNNER_DIRECTORY}/test-runner.lock')
logging.getLogger("filelock").setLevel(logging.INFO)


def get_account_by_name(account_name) -> Account:
    return next((account for account in _NEOXP_CONFIG.accounts if account.name == account_name),
                None)


def get_account_by_address(account_address: str) -> Account:
    return next((account for account in _NEOXP_CONFIG.accounts if account.address == account_address),
                None)


def get_account_by_identifier(account_identifier: str) -> Account:
    return next((account for account in _NEOXP_CONFIG.accounts if (account.address == account_identifier
                                                                   or account.name == account_identifier)),
                None)


def get_default_account() -> Account:
    return _NEOXP_CONFIG.default_account


def get_address_version() -> int:
    return _NEOXP_CONFIG.version


def get_magic() -> int:
    return _NEOXP_CONFIG.magic


def get_genesis_block() -> Block:
    return _NEOXP_CONFIG.genesis_block


def _set_genesis_block(found_block: Block):
    if _NEOXP_CONFIG.genesis_block is None:  # avoid overwrite
        _NEOXP_CONFIG._genesis_block = found_block


def get_account_from_script_hash_or_id(script_hash_or_address: Union[bytes, str]) -> Account:
    if isinstance(script_hash_or_address, bytes):
        script_hash = script_hash_or_address
        address = wallet_utils.address_from_script_hash(script_hash, get_address_version())
        account = get_account_by_address(address)
    elif isinstance(script_hash_or_address, str):
        account = get_account_by_identifier(script_hash_or_address)
        script_hash = wallet_utils.address_to_script_hash(script_hash_or_address, get_address_version())
    else:
        raise TypeError(f"Invalid data type {type(script_hash_or_address)}. Expecting str or bytes")

    if not isinstance(account, Account):
        from boa3.internal.neo3.core.types import UInt160
        from boa3_test.test_drive.neoxp.model.neoxpaccount import NeoExpressAccount
        account = NeoExpressAccount(UInt160(script_hash), get_address_version())

    return account


def create_neo_express_instance(neoxp_path: str) -> str:
    command = neoxp.create.CreateCommand(config_output=neoxp_path,
                                         node_count=1,
                                         force=True)
    with _NEOXP_CONFIG_LOCK:
        stdout, stderr = run_neo_express_cli(command)

    return stdout


def reset_neo_express_instance(neoxp_path: str, check_point_file: str = None) -> str:
    if isinstance(check_point_file, str) and os.path.isfile(check_point_file):
        command = neoxp.checkpoint.CheckpointRestoreCommand(neo_express_data_file=neoxp_path,
                                                            file_name=check_point_file,
                                                            force=True)
    else:
        command = neoxp.reset.ResetCommand(neo_express_data_file=neoxp_path,
                                           force=True)
    stdout, stderr = run_neo_express_cli(command)
    return stdout


def get_deployed_contracts(neoxp_path: str, check_point_file: str = None) -> List[Contract]:
    command = neoxp.contract.ContractListCommand(neo_express_data_file=neoxp_path)
    with _NEOXP_CONFIG_LOCK:
        reset_neo_express_instance(neoxp_path, check_point_file)
        stdout, stderr = run_neo_express_cli(command)

    contracts = []
    for line in stdout.splitlines():
        try:
            groups = re.match(r'(?P<name>.*?) \((?P<scripthash>0x\w+)\)', line).groupdict()
            contract_name = groups['name']
            contract_hash = groups['scripthash']
            found_contract = Contract(contract_name, contract_hash)
            contracts.append(found_contract)
        except:
            # don't break if some line doesn't match the regex
            continue
    return contracts


def _get_transaction_raw(neoxp_path: str, tx_hash: UInt256, check_point_file: str = None) -> str:
    command = neoxp.show.ShowTransactionCommand(tx_hash.to_array(), neo_express_data_file=neoxp_path)
    with _NEOXP_CONFIG_LOCK:
        if isinstance(check_point_file, str):
            reset_neo_express_instance(neoxp_path, check_point_file)
        stdout, stderr = run_neo_express_cli(command)

    return stdout


def get_transaction(neoxp_path: str, tx_hash: UInt256, check_point_file: str = None) -> Transaction:
    raw_result = _get_transaction_raw(neoxp_path, tx_hash, check_point_file)

    tx: Transaction
    try:
        import json
        result_json = json.loads(raw_result)
        tx = Transaction.from_json(result_json['transaction'])
    except:
        tx = None

    return tx


def get_transaction_log(neoxp_path: str, tx_hash: UInt256, check_point_file: str = None, contract_collection=None) -> TransactionLog:
    raw_result = _get_transaction_raw(neoxp_path, tx_hash, check_point_file)

    tx_log: TransactionLog
    try:
        import json
        result_json = json.loads(raw_result)
        tx_log = TransactionLog.from_json(result_json['application-log'], contract_collection)
        tx_log._tx_id = tx_hash
    except:
        tx_log = None

    return tx_log


def get_latest_block(neoxp_path: str, check_point_file: str = None) -> Block:
    return get_block(neoxp_path, check_point_file=check_point_file)


def get_block(neoxp_path: str, block_hash_or_index: Union[UInt256, int] = None,
              check_point_file: str = None) -> Block:
    if isinstance(block_hash_or_index, (UInt256, int)):
        if isinstance(block_hash_or_index, int):
            if block_hash_or_index < 0:
                block_hash_or_index = 0
        else:
            block_hash_or_index = block_hash_or_index.to_array()

        command = neoxp.show.ShowBlockCommand(block_hash_or_index,
                                              neo_express_data_file=neoxp_path)
    else:
        command = neoxp.show.ShowBlockCommand(neo_express_data_file=neoxp_path)

    with _NEOXP_CONFIG_LOCK:
        if isinstance(check_point_file, str):
            reset_neo_express_instance(neoxp_path, check_point_file)
        stdout, stderr = run_neo_express_cli(command)

    block: Block
    try:
        import json
        result_json = json.loads(stdout)
        block = Block.from_json(result_json)
    except:
        block = None

    return block


def run_batch(neoxp_path: str, batch_path: str, reset: bool = False, check_point_file: str = None) -> str:
    if isinstance(check_point_file, str) and not os.path.isfile(check_point_file):
        check_point_file = None
    command = neoxp.batch.BatchCommand(batch_path,
                                       neo_express_data_file=neoxp_path,
                                       check_point_file=check_point_file,
                                       reset=reset)
    with _NEOXP_CONFIG_LOCK:
        stdout, stderr = run_neo_express_cli(command)

    return stdout


def run_neo_express_cli(command: neoxp.NeoExpressCommand) -> Tuple[str, str]:
    neoxp_args = ['neoxp']
    neoxp_args.extend(command.cli_command().split())

    with _NEOXP_FILE_LOCK:
        process = subprocess.Popen(neoxp_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
        cli_result = process.communicate()
    return cli_result
