from typing import Any, Self

from boa3.internal.neo3.core.types import UInt256
from boa3_test.test_drive.model.network.payloads.signer import Signer
from boa3_test.test_drive.model.network.payloads.testtransaction import TestTransaction
from boa3_test.test_drive.model.network.payloads.witness import Witness
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp import utils


class TestRunnerTransaction(TestTransaction):
    def __init__(self, tx_hash: UInt256 | bytes, script: bytes, sender: Account):
        super().__init__(tx_hash, script)
        self._size = 0
        self._version = 0
        self._nonce = 0
        self._sender = sender
        self._system_fee = 0
        self._network_fee = 0
        self._valid_until_block = 0

    @property
    def script(self) -> bytes:
        return self._script

    @property
    def size(self) -> int:
        return self._size

    @property
    def version(self) -> int:
        return self._version

    @property
    def nonce(self) -> int:
        return self._nonce

    @property
    def sender(self) -> Account:
        return self._sender

    @property
    def system_fee(self) -> int:
        return self._system_fee

    @property
    def network_fee(self) -> int:
        return self._network_fee

    @property
    def valid_until_block(self) -> int:
        return self._valid_until_block

    @property
    def signers(self) -> list[Signer]:
        return self._signers.copy()

    @property
    def attributes(self) -> list:
        return self._attributes.copy()

    @property
    def witnesses(self) -> list[Witness]:
        return self._witnesses.copy()

    @classmethod
    def from_json(cls, json: dict[str, Any], *args, **kwargs) -> Self:
        tx: Self = super().from_json(json)

        if 'neoxp_config' in kwargs:
            neoxp_config = kwargs['neoxp_config']
        elif len(args) > 0:
            neoxp_config = args[0]
        else:
            neoxp_config = None

        tx._size = json['size']
        tx._version = json['version']
        tx._nonce = json['nonce']
        sender_account = json['sender']
        tx._sender = (utils.get_account_from_script_hash_or_id(neoxp_config, sender_account)
                      if neoxp_config is not None
                      else sender_account
                      )
        tx._system_fee = int(json['sysfee'])
        tx._network_fee = int(json['netfee'])
        tx._valid_until_block = json['validuntilblock']

        return tx
