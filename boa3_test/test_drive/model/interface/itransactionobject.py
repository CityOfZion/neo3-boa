import abc

from boa3.internal.neo3.core.types import UInt256


class ITransactionObject(abc.ABC):
    tx_hash_group = 'txhash'

    def __init__(self):
        self._log: str = ''
        self._tx_id: UInt256 = None

    def set_log(self, log: str):
        if not self._log:
            self._log = log

    @property
    def tx_id(self) -> UInt256:
        if not isinstance(self._tx_id, UInt256) and not self._log.isspace():
            self._handle_log()

        return self._tx_id

    def _log_pattern(self) -> str:
        return rf'(?P<{self.tx_hash_group}>0x\w+) submitted$'

    def _match_log(self) -> dict:
        import re
        pattern = self._log_pattern()
        if not pattern.startswith('^'):
            pattern = r'.*?' + pattern
        return re.match(pattern, self._log).groupdict()

    def _set_data_from_match_result(self, match_groups: dict):
        tx_hash = match_groups[self.tx_hash_group]
        self._tx_id = UInt256.from_string(tx_hash)

    def _handle_log(self):
        try:
            match_groups = self._match_log()
            self._set_data_from_match_result(match_groups)
        except:
            pass
