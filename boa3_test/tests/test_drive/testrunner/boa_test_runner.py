__all__ = [
    'BoaTestRunner'
]

import os.path
import threading
from typing import Callable, List, Sequence, Optional, Tuple, Union

from boa3.internal import env
from boa3.internal.neo3.core.types import UInt256
from boa3_test.test_drive.model.smart_contract.contractcollection import ContractCollection
from boa3_test.test_drive.neoxp.model.neoxpconfig import NeoExpressConfig
from boa3_test.test_drive.testrunner.blockchain.block import TestRunnerBlock as Block
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner
from boa3_test.tests.test_drive.neoxp import utils as boa_neoxp_utils
from boa3_test.tests.test_drive.testrunner.boa_neoxp_batch import BoaNeoExpressBatch


class BoaTestRunner(NeoTestRunner):
    _DEFAULT_ACCOUNT = boa_neoxp_utils.get_default_account()

    def __init__(self, neoxp_path: str = None, runner_id: str = None, cleanup_files: bool = True):
        if not isinstance(neoxp_path, str):
            neoxp_path = os.path.join(env.NEO_EXPRESS_INSTANCE_DIRECTORY, 'default.neo-express')

        super().__init__(neoxp_path, runner_id)
        self._batch = BoaNeoExpressBatch(self._neoxp_config)

        self._clear_files_when_destroyed = cleanup_files

    def _set_up_neoxp_config(self) -> NeoExpressConfig:
        default_config = boa_neoxp_utils._NEOXP_CONFIG
        if self._neoxp_abs_path == os.path.abspath(default_config.config_path):
            return default_config
        return super()._set_up_neoxp_config()

    def _set_up_generate_file_names(self, file_name: str):
        from boa3_test.test_drive import utils
        runner_specific_id = utils.create_custom_id(file_name)
        super()._set_up_generate_file_names(runner_specific_id)

    def add_neo(self, script_hash_or_address: Union[bytes, str], amount: int):
        address = boa_neoxp_utils.get_account_from_script_hash_or_id(script_hash_or_address)
        self._batch.transfer_assets(sender=self._DEFAULT_ACCOUNT, receiver=address,
                                    quantity=amount,
                                    asset='NEO')

    def add_gas(self, script_hash_or_address: Union[bytes, str], amount: int):
        address = boa_neoxp_utils.get_account_from_script_hash_or_id(script_hash_or_address)
        gas_decimals = 8
        self._batch.transfer_assets(sender=self._DEFAULT_ACCOUNT, receiver=address,
                                    asset='GAS', decimals=gas_decimals,
                                    quantity=(amount / (10 ** gas_decimals)))

    def _internal_generate_files(self, methods_to_call: List[Tuple[Callable, Sequence]]):
        worker_threads = []

        if len(methods_to_call) > 0:
            last_method, last_method_args = methods_to_call[-1]

            for method, args in methods_to_call[:-1]:
                work_thread = threading.Thread(target=method, args=args)
                worker_threads.append(
                    work_thread
                )
                work_thread.start()

            last_method(*last_method_args)

        for worker in worker_threads:
            worker.join()

    def _get_genesis_block(self) -> Optional[Block]:
        return boa_neoxp_utils.get_genesis_block()

    def _get_block(self, block_hash_or_index) -> Optional[Block]:
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)
        return boa_neoxp_utils.get_block(self._neoxp_abs_path, block_hash_or_index,
                                         check_point_file=check_point_path)

    def _get_tx(self, tx_hash: UInt256):
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)
        return boa_neoxp_utils.get_transaction(self._neoxp_abs_path, tx_hash,
                                               check_point_file=check_point_path)

    def _get_tx_log(self, tx_hash: UInt256, contract_collection: ContractCollection):
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)
        return boa_neoxp_utils.get_transaction_log(self._neoxp_abs_path, tx_hash,
                                                   check_point_file=check_point_path,
                                                   contract_collection=contract_collection)

    def _get_oracle_resp(self, url: str, response_path: str, request_id: int = None) -> List[UInt256]:
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)
        return boa_neoxp_utils.oracle_response(self._neoxp_abs_path, url, response_path, request_id,
                                               check_point_file=check_point_path)

    def __del__(self):
        self.reset()
        if self._clear_files_when_destroyed:
            paths_to_delete = [
                self.get_full_path(self._CHECKPOINT_FILE),
                self.get_full_path(self._BATCH_FILE),
                self.get_full_path(self._INVOKE_FILE)
            ]
            for path in paths_to_delete:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except BaseException as e:
                    print(e)
                    continue
