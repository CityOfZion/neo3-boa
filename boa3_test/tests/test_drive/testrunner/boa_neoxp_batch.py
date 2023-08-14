__all__ = [
    'BoaNeoExpressBatch'
]


from boa3_test.test_drive.neoxp.batch import NeoExpressBatch
from boa3_test.tests.test_drive.neoxp import utils as boa_neoxp_utils


class BoaNeoExpressBatch(NeoExpressBatch):
    def _run_batch(self, neoxp_path: str, batch_file_path: str, reset: bool = False, check_point_file: str = None):
        return boa_neoxp_utils.run_batch(neoxp_path, batch_file_path, reset=reset, check_point_file=check_point_file)
