__all__ = [
    'NeoExpressWrapper',
    '_NEOXP_CONFIG_LOCK'
]

import os.path
import re
import subprocess
import threading
from typing import Tuple, List, Union

from boa3.internal.neo3.core.types import UInt256
from boa3_test.test_drive.neoxp.command import neoexpresscommand as neoxp
from boa3_test.test_drive.neoxp.model.neoxpconfig import NeoExpressConfig
from boa3_test.test_drive.testrunner.blockchain.block import TestRunnerBlock as Block
from boa3_test.test_drive.testrunner.blockchain.contract import TestRunnerContract as Contract
from boa3_test.test_drive.testrunner.blockchain.transaction import TestRunnerTransaction as Transaction
from boa3_test.test_drive.testrunner.blockchain.transactionlog import TestRunnerTransactionLog as TransactionLog

_NEOXP_CONFIG_LOCK = threading.Lock()


class NeoExpressWrapper:
    @classmethod
    def run_neo_express_cli(cls, command: neoxp.NeoExpressCommand) -> Tuple[str, str]:
        neoxp_args = ['neoxp']
        neoxp_args.extend(command.cli_command().split())

        cli_result = cls._run_cli(*neoxp_args)
        return cli_result

    @classmethod
    def _run_cli(cls, *neoxp_args: str):
        process = subprocess.Popen(neoxp_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
        return process.communicate()

    @staticmethod
    def get_config_data(neoxp_path: str) -> NeoExpressConfig:
        return NeoExpressConfig(neoxp_path)

    @classmethod
    def create_neo_express_instance(cls, neoxp_path: str) -> str:
        command = neoxp.create.CreateCommand(config_output=neoxp_path,
                                             node_count=1,
                                             force=True)
        with _NEOXP_CONFIG_LOCK:
            stdout, stderr = cls.run_neo_express_cli(command)

        return stdout

    @classmethod
    def reset_neo_express_instance(cls, neoxp_path: str, check_point_file: str = None) -> str:
        if isinstance(check_point_file, str) and os.path.isfile(check_point_file):
            command = neoxp.checkpoint.CheckpointRestoreCommand(neo_express_data_file=neoxp_path,
                                                                file_name=check_point_file,
                                                                force=True)
        else:
            command = neoxp.reset.ResetCommand(neo_express_data_file=neoxp_path,
                                               force=True)
        stdout, stderr = cls.run_neo_express_cli(command)
        return stdout

    @classmethod
    def get_deployed_contracts(cls, neoxp_path: str, check_point_file: str = None) -> List[Contract]:
        command = neoxp.contract.ContractListCommand(neo_express_data_file=neoxp_path)
        with _NEOXP_CONFIG_LOCK:
            cls.reset_neo_express_instance(neoxp_path, check_point_file)
            stdout, stderr = cls.run_neo_express_cli(command)

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

    @classmethod
    def _get_transaction_raw(cls, neoxp_path: str, tx_hash: UInt256, check_point_file: str = None) -> str:
        command = neoxp.show.ShowTransactionCommand(tx_hash.to_array(), neo_express_data_file=neoxp_path)
        with _NEOXP_CONFIG_LOCK:
            if isinstance(check_point_file, str):
                cls.reset_neo_express_instance(neoxp_path, check_point_file)
            stdout, stderr = cls.run_neo_express_cli(command)

        return stdout

    @classmethod
    def get_transaction(cls, neoxp_path: str, tx_hash: UInt256, check_point_file: str = None) -> Transaction:
        raw_result = cls._get_transaction_raw(neoxp_path, tx_hash, check_point_file)

        tx: Transaction
        try:
            import json
            result_json = json.loads(raw_result)
            tx = Transaction.from_json(result_json['transaction'], neoxp_config=cls.get_config_data(neoxp_path))
        except:
            tx = None

        return tx

    @classmethod
    def get_transaction_log(cls, neoxp_path: str, tx_hash: UInt256, check_point_file: str = None, contract_collection=None) -> TransactionLog:
        raw_result = cls._get_transaction_raw(neoxp_path, tx_hash, check_point_file)

        tx_log: TransactionLog
        try:
            import json
            result_json = json.loads(raw_result)
            tx_log = TransactionLog.from_json(result_json['application-log'], contract_collection)
            tx_log._tx_id = tx_hash
        except:
            tx_log = None

        return tx_log

    @classmethod
    def get_latest_block(cls, neoxp_path: str, check_point_file: str = None) -> Block:
        return cls.get_block(neoxp_path, check_point_file=check_point_file)

    @classmethod
    def get_block(cls, neoxp_path: str, block_hash_or_index: Union[UInt256, int] = None,
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
                cls.reset_neo_express_instance(neoxp_path, check_point_file)
            stdout, stderr = cls.run_neo_express_cli(command)

        block: Block
        try:
            import json
            result_json = json.loads(stdout)
            block = Block.from_json(result_json, neoxp_config=cls.get_config_data(neoxp_path))
        except:
            block = None

        return block

    @classmethod
    def run_batch(cls, neoxp_path: str, batch_path: str, reset: bool = False, check_point_file: str = None) -> str:
        if isinstance(check_point_file, str) and not os.path.isfile(check_point_file):
            check_point_file = None
        command = neoxp.batch.BatchCommand(batch_path,
                                           neo_express_data_file=neoxp_path,
                                           check_point_file=check_point_file,
                                           reset=reset)
        with _NEOXP_CONFIG_LOCK:
            stdout, stderr = cls.run_neo_express_cli(command)

        return stdout

    @classmethod
    def oracle_response(cls, neoxp_path: str, url: str, response_path: str, request_id: int = None,
                        check_point_file: str = None) -> List[UInt256]:
        command = neoxp.oracle.OracleResponseCommand(url, response_path, request_id, neo_express_data_file=neoxp_path)

        with _NEOXP_CONFIG_LOCK:
            if isinstance(check_point_file, str):
                cls.reset_neo_express_instance(neoxp_path, check_point_file)
            stdout, stderr = cls.run_neo_express_cli(command)

        import re
        from boa3.internal.neo import from_hex_str

        oracle_response_submitted = re.findall(r"0x\w{64}", stdout)

        return [UInt256(from_hex_str(tx)) for tx in oracle_response_submitted]
