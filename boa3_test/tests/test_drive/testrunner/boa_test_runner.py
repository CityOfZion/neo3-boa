__all__ = [
    'BoaTestRunner'
]

import os.path
import threading
from typing import Callable, List, Sequence, Tuple

from boa3.internal import env
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


class BoaTestRunner(NeoTestRunner):

    def __init__(self, neoxp_path: str = None, runner_id: str = None):
        if not isinstance(neoxp_path, str):
            neoxp_path = f'{env.NEO_EXPRESS_INSTANCE_DIRECTORY}{os.path.sep}default.neo-express'

        super().__init__(neoxp_path, runner_id)

        self._clear_files_when_destroyed = True

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
