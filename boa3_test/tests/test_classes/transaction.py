import base64
from typing import Any, Self

from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.core.types import UInt256
from boa3.internal.neo3.vm import VMState, vmstate
from boa3_test.tests.test_classes import transactionattribute as tx_attribute
from boa3_test.tests.test_classes.signer import Signer
from boa3_test.tests.test_classes.witness import Witness


class Transaction:
    def __init__(self, script: bytes, signers: list[Signer] = None, witnesses: list[Witness] = None):
        self._hash: UInt256 | None = None
        self._script: bytes = script

        self._signers: list[Signer] = signers if signers is not None else []
        self._witnesses: list[Witness] = witnesses if witnesses is not None else []
        self._attributes: list[tx_attribute.TransactionAttribute] = []
        self._state: VMState = VMState.NONE

    def add_attribute(self, tx_attr: tx_attribute.TransactionAttribute):
        if tx_attr not in self._attributes:
            self._attributes.append(tx_attr)

    @property
    def hash(self) -> bytes | None:
        if self._hash is None:
            return None

        return self._hash.to_array()

    @property
    def state(self) -> VMState:
        return self._state

    def to_json(self) -> dict[str, Any]:
        json = {
            'signers': [signer.to_json() for signer in self._signers],
            'witnesses': [witness.to_json() for witness in self._witnesses],
            'attributes': [attr.to_json() for attr in self._attributes if hasattr(attr, 'to_json')],
            'script': String.from_bytes(base64.b64encode(self._script)),
            'state': self._state.name
        }

        return json

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        if 'hash' in json and isinstance(json['hash'], str):
            tx_hash = UInt256.from_string(json['hash'])
        else:
            tx_hash = UInt256.zero()

        script = base64.b64decode(json['script'])
        tx = object.__new__(cls)  # init was causing errors with inherited classes
        tx._hash = tx_hash
        tx._script = script

        tx._attributes = []
        if 'attributes' in json:
            tx._attributes = [tx_attribute.TransactionAttribute.from_json(attr) for attr in json['attributes']]
        else:
            tx._attributes = []

        if 'signers' in json:
            signers_json = json['signers']
            if not isinstance(signers_json, list):
                signers_json = [signers_json]
            tx._signers = [Signer.from_json(js) for js in signers_json]
        else:
            tx._signers = []

        if 'witnesses' in json:
            witnesses_json = json['witnesses']
            if not isinstance(witnesses_json, list):
                witnesses_json = [witnesses_json]
            tx._witnesses = [Witness.from_json(js) for js in witnesses_json]
        else:
            tx._witnesses = []

        if 'state' in json and isinstance(json['state'], str):
            tx._state = vmstate.get_vm_state(json['state'])

        return tx

    def __repr__(self) -> str:
        return str(self._hash)

    def copy(self):
        copied = Transaction(self._script, self._signers, self._witnesses)
        copied._hash = self._hash
        return copied

    def __eq__(self, other) -> bool:
        if not isinstance(other, Transaction):
            return False
        if self._hash == other._hash:
            return True

        return (self._script == other._script
                and self._attributes == self._attributes
                and self._signers == other._signers
                and self._witnesses == other._witnesses)
