from typing import Any, Self

from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.wallet import utils
from boa3_test.test_drive.model.wallet.account import Account


class NeoExpressAccount(Account):
    def __init__(self, script_hash: UInt160,
                 account_version: int = 53,  # default Neo account version
                 name: str = None,
                 label: str = None):

        super().__init__(script_hash, account_version, name=name, label=label)

    @property
    def address(self) -> str | None:
        return utils.address_from_script_hash(self._script_hash.to_array(), self._version)

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        address = json['script-hash']
        label = json['label']
        account = NeoExpressAccount(
            script_hash=UInt160(utils.address_to_script_hash(address)),
            label=label
        )
        return account
