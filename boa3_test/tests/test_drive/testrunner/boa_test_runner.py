__all__ = [
    'BoaTestRunner'
]

import os.path
import threading
from typing import Callable, List, Sequence, Tuple

from boa3.internal import env
from boa3_test.test_drive.neoxp.model.neoxpconfig import NeoExpressConfig
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner
from boa3_test.tests.test_drive.neoxp import utils as neoxp_utils


class BoaTestRunner(NeoTestRunner):
    _DEFAULT_ACCOUNT = neoxp_utils.get_default_account()

    def __init__(self, neoxp_path: str = None, runner_id: str = None, cleanup_files: bool = True):
        if not isinstance(neoxp_path, str):
            neoxp_path = os.path.join(env.NEO_EXPRESS_INSTANCE_DIRECTORY, 'default.neo-express')

        super().__init__(neoxp_path, runner_id)

        self._clear_files_when_destroyed = cleanup_files

    def _set_up_neoxp_config(self) -> NeoExpressConfig:
        default_config = neoxp_utils._NEOXP_CONFIG
        if self._neoxp_abs_path == os.path.abspath(default_config.config_path):
            return default_config
        return super()._set_up_neoxp_config()

    def _set_up_generate_file_names(self, file_name: str):
        from boa3_test.test_drive import utils
        runner_specific_id = utils.create_custom_id(file_name)
        super()._set_up_generate_file_names(runner_specific_id)

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
