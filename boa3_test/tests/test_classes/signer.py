from typing import Any, Dict

from boa3.neo.core.types.UInt import UInt160


class Signer:
    def __init__(self, account: UInt160):
        self._account: UInt160 = account

    @property
    def account(self) -> UInt160:
        return self._account

    def to_json(self) -> Dict[str, Any]:
        return {
            'account': str(self._account)
        }

    def __str__(self) -> str:
        return self._account.__str__()
