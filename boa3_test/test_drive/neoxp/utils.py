import re
import subprocess
from typing import Tuple, List, Union

from boa3.internal import env
from boa3_test.test_drive.model.wallet import utils as wallet_utils
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import neoexpresscommand as neoxp
from boa3_test.test_drive.neoxp.model.neoxpconfig import NeoExpressConfig
from boa3_test.test_drive.testrunner.blockchain.contract import TestRunnerContract as Contract

_NEOXP_CONFIG = NeoExpressConfig(f'{env.NEO_EXPRESS_INSTANCE_DIRECTORY}/default.neo-express')


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


def get_account_from_script_hash_or_name(script_hash_or_address: Union[bytes, str]) -> Account:
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
        from boa3.neo3.core.types import UInt160
        from boa3_test.test_drive.neoxp.model.neoxpaccount import NeoExpressAccount
        account = NeoExpressAccount(UInt160(script_hash), get_address_version())

    return account


def create_neo_express_instance(neoxp_path: str) -> str:
    command = neoxp.create.CreateCommand(config_output=neoxp_path,
                                         node_count=1,
                                         force=True)
    stdout, stderr = run_neo_express_cli(command)
    return stdout


def reset_neo_express_instance(neoxp_path: str) -> str:
    command = neoxp.reset.ResetCommand(neo_express_data_file=neoxp_path,
                                       force=True)
    stdout, stderr = run_neo_express_cli(command)
    return stdout


def get_deployed_contracts(neoxp_path: str) -> List[Contract]:
    command = neoxp.contract.ContractListCommand(neo_express_data_file=neoxp_path)
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


def run_batch(neoxp_path: str, batch_path: str, reset: bool = False) -> str:
    command = neoxp.batch.BatchCommand(batch_path,
                                       neo_express_data_file=neoxp_path,
                                       reset=reset)
    stdout, stderr = run_neo_express_cli(command)
    return stdout


def run_neo_express_cli(command: neoxp.NeoExpressCommand) -> Tuple[str, str]:
    neoxp_args = ['neoxp']
    neoxp_args.extend(command.cli_command().split())

    process = subprocess.Popen(neoxp_args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
    return process.communicate()
