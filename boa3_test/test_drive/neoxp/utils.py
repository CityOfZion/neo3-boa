import re
import subprocess
from typing import Tuple, List, Union

from boa3.internal import env
from boa3_test.test_drive.model.wallet import utils as wallet_utils
from boa3_test.test_drive.model.wallet.account import Account
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


def get_account_identifier_from_script_hash_or_name(script_hash_or_address: Union[bytes, str]) -> str:
    if isinstance(script_hash_or_address, bytes):
        address = wallet_utils.address_from_script_hash(script_hash_or_address, _NEOXP_CONFIG.version)
    elif isinstance(script_hash_or_address, str):
        account = get_account_by_identifier(script_hash_or_address)
        if hasattr(account, 'get_identifier'):
            address = account.get_identifier()
        else:
            address = script_hash_or_address
    else:
        raise TypeError(f"Invalid data type {type(script_hash_or_address)}. Expecting str or bytes")

    return address


def create_neo_express_instance(neoxp_path: str) -> str:
    stdout, stderr = run_neo_express_cli('create', neoxp_path,
                                         '--count', '1',
                                         '--force')
    return stdout


def reset_neo_express_instance(neoxp_path: str) -> str:
    stdout, stderr = run_neo_express_cli('reset',
                                         '--input', neoxp_path,
                                         '--force')
    return stdout


def get_deployed_contracts(neoxp_path: str) -> List[Contract]:
    stdout, stderr = run_neo_express_cli('contract', 'list',
                                         '--input', neoxp_path)
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
    options = ['--input', neoxp_path]
    if reset:
        options.append('--reset')

    stdout, stderr = run_neo_express_cli('batch',
                                         *options,
                                         batch_path)
    return stdout


def run_neo_express_cli(*args: str) -> Tuple[str, str]:
    neoxp_args = ['neoxp']
    neoxp_args.extend(args)
    process = subprocess.Popen(neoxp_args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
    return process.communicate()
