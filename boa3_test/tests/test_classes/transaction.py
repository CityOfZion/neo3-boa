from __future__ import annotations

import base64
from typing import Any, Dict, List, Optional

from boa3.neo import from_hex_str
from boa3.neo3.core.types import UInt256
from boa3.neo3.vm import VMState, vmstate
from boa3_test.tests.test_classes import transactionattribute as tx_attribute
from boa3_test.tests.test_classes.signer import Signer
from boa3_test.tests.test_classes.witness import Witness


class Transaction:
    def __init__(self, script: bytes, signers: List[Signer] = None, witnesses: List[Witness] = None):
        self._signers: List[Signer] = signers if signers is not None else []
        self._witnesses: List[Witness] = witnesses if witnesses is not None else []
        self._attributes: List[tx_attribute.TransactionAttribute] = []
        self._script: bytes = script
        self._hash: Optional[UInt256] = None
        self._state: VMState = VMState.NONE

    def add_attribute(self, tx_attr: tx_attribute.TransactionAttribute):
        if tx_attr not in self._attributes:
            self._attributes.append(tx_attr)

    @property
    def hash(self) -> Optional[bytes]:
        if self._hash is None:
            return None
        else:
            return self._hash.to_array()

    @property
    def state(self) -> VMState:
        return self._state

    def to_json(self) -> Dict[str, Any]:
        from boa3.neo.vm.type.String import String
        return {
            'signers': [signer.to_json() for signer in self._signers],
            'witnesses': [witness.to_json() for witness in self._witnesses],
            'attributes': [attr.to_json() for attr in self._attributes],
            'script': String.from_bytes(base64.b64encode(self._script)),
            'state': self._state.name
        }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> Transaction:
        script = base64.b64decode(json['script'])
        tx = cls(script)
        if 'signers' in json:
            signers_json = json['signers']
            if not isinstance(signers_json, list):
                signers_json = [signers_json]
            tx._signers = [Signer.from_json(js) for js in signers_json]

        if 'witnesses' in json:
            witnesses_json = json['witnesses']
            if not isinstance(witnesses_json, list):
                witnesses_json = [witnesses_json]
            tx._witnesses = [Witness.from_json(js) for js in witnesses_json]

        if 'attributes' in json:
            attributes_json = json['attributes']
            if not isinstance(attributes_json, list):
                attributes_json = [attributes_json]
            tx._attributes = [tx_attribute.TransactionAttribute.from_json(js) for js in attributes_json]

        if 'hash' in json and isinstance(json['hash'], str):
            tx._hash = UInt256(from_hex_str(json['hash']))

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
