from typing import Any, Self

from boa3.internal.neo3.vm import VMState, vmstate
from boa3_test.test_drive.model.network.payloads.testtransaction import TestTransaction
from boa3_test.tests.test_classes import transactionattribute as tx_attribute
from boa3_test.tests.test_classes.signer import Signer
from boa3_test.tests.test_classes.witness import Witness


class Transaction(TestTransaction):
    def __init__(self, script: bytes, signers: list[Signer] = None, witnesses: list[Witness] = None):
        super().__init__(None, script, signers, witnesses)
        self._attributes: list[tx_attribute.TransactionAttribute] = []
        self._state: VMState = VMState.NONE

    def add_attribute(self, tx_attr: tx_attribute.TransactionAttribute):
        if tx_attr not in self._attributes:
            self._attributes.append(tx_attr)

    @property
    def hash(self) -> bytes | None:
        if self._hash is None:
            return None

        return super().hash.to_array()

    @property
    def state(self) -> VMState:
        return self._state

    def to_json(self) -> dict[str, Any]:
        json = super().to_json()

        json.pop('hash')  # don't include hash in this json
        json['state'] = self._state.name

        return json

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        tx: Self = super().from_json(json)

        if 'attributes' in json:
            attributes_json = json['attributes']
            if not isinstance(attributes_json, list):
                attributes_json = [attributes_json]
            tx._attributes = [tx_attribute.TransactionAttribute.from_json(js) for js in attributes_json]

        if 'state' in json and isinstance(json['state'], str):
            tx._state = vmstate.get_vm_state(json['state'])

        return tx

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
