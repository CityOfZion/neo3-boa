import re
import subprocess
from typing import Tuple, List

from boa3_test.test_drive.testrunner.blockchain.contract import TestRunnerContract as Contract


def create_neo_express_instance(neoxp_path: str):
    stdout, stderr = run_neo_express_cli('create', neoxp_path,
                                         '--count', '1',
                                         '--force')


def reset_neo_express_instance(neoxp_path: str):
    stdout, stderr = run_neo_express_cli('reset',
                                         '--input', neoxp_path,
                                         '--force')


def get_deployed_contracts(neoxp_path: str) -> List[Contract]:
    stdout, stderr = run_neo_express_cli('contract', 'list',
                                         '--input', neoxp_path)
    contracts = []
    for line in stdout.splitlines():
        begin, contract_name, contract_hash, end = re.split(r'(.*?) \((0x\w+)\)', line)
        found_contract = Contract(contract_name, contract_hash)
        contracts.append(found_contract)
    return contracts


def run_batch(neoxp_path: str, batch_path: str, reset: bool = False):
    options = ['--input', neoxp_path]
    if reset:
        options.append('--reset')

    stdout, stderr = run_neo_express_cli('batch',
                                         *options,
                                         batch_path)


def run_neo_express_cli(*args: str) -> Tuple[str, str]:
    neoxp_args = ['neoxp']
    neoxp_args.extend(args)
    process = subprocess.Popen(neoxp_args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
    return process.communicate()
