import abc

from boa3.internal.neo3.core.types import UInt256


class ITransactionObject(abc.ABC):
    def __init__(self):
        self._log: str = ''
        self._tx_id: UInt256 = None

    @property
    def tx_id(self) -> UInt256:
        if not isinstance(self._tx_id, UInt256) and not self._log.isspace():
            try:
                import re
                groups = re.match(r'.*?(?P<txhash>0x\w+) submitted$', self._log).groupdict()
                tx_hash = groups['txhash']
                self._tx_id = UInt256.from_string(tx_hash)
            except:
                pass

        return self._tx_id
