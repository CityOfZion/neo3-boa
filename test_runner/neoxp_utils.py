import re
import subprocess
from typing import Tuple

from test_runner.blockchain import Contract


def create_neo_express_instance(neoxp_path: str):
    stdout, stderr = run_neo_express_cli('create', neoxp_path,
                                         '--count', '1',
                                         '--force')


def reset_neo_express_instance(neoxp_path: str):
    stdout, stderr = run_neo_express_cli('reset',
                                         '--input', neoxp_path,
                                         '--force')


def get_last_deployed_contract(neoxp_path: str) -> Contract:
    stdout, stderr = run_neo_express_cli('contract', 'list',
                                         '--input', neoxp_path)
    last_line = stdout.splitlines()[-1]
    begin, contract_name, contract_hash, end = re.split(r'(.*?) \((0x\w+)\)', last_line)
    return Contract(contract_name, contract_hash)


def run_batch(neoxp_path: str, batch_path: str):
    stdout, stderr = run_neo_express_cli('batch',
                                         '--input', neoxp_path,
                                         batch_path)


def run_neo_express_cli(*args: str) -> Tuple[str, str]:
    neoxp_args = ['neoxp']
    neoxp_args.extend(args)
    process = subprocess.Popen(neoxp_args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
    return process.communicate()
