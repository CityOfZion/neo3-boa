from typing import Any, Self

from boa3.internal.neo import from_hex_str, utils
from boa3.internal.neo3.core.types import UInt256
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.model.network.payloads.signer import Signer
from boa3_test.test_drive.model.network.payloads.transactionattribute import TransactionAttribute
from boa3_test.test_drive.model.network.payloads.witness import Witness
from boa3_test.test_drive.model.smart_contract.contractcollection import ContractCollection
from boa3_test.test_drive.model.smart_contract.triggertype import TriggerType
from boa3_test.test_drive.testrunner.blockchain.notification import TestRunnerNotification as Notification


class TestTransaction:
    def __init__(self, tx_hash: UInt256 | bytes, script: bytes, signers: list[Signer] = None, witnesses: list[Witness] = None):
        if isinstance(tx_hash, bytes):
            tx_hash = UInt256(tx_hash)

        self._hash: UInt256 = tx_hash
        self._script: bytes = script

        self._signers: list[Signer] = signers if signers is not None else []
        self._witnesses: list[Witness] = witnesses if witnesses is not None else []
        self._attributes: list[TransactionAttribute] = []

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @property
    def hash(self) -> UInt256:
        return self._hash

    def to_json(self) -> dict[str, Any]:
        import base64
        from boa3.internal.neo.vm.type.String import String
        return {
            'hash': str(self._hash),
            'signers': [signer.to_json() for signer in self._signers],
            'witnesses': [witness.to_json() for witness in self._witnesses],
            'attributes': [attr.to_json() for attr in self._attributes if hasattr(attr, 'to_json')],
            'script': String.from_bytes(base64.b64encode(self._script))
        }

    @classmethod
    def from_json(cls, json: dict[str, Any], *args, **kwargs) -> Self:
        import base64

        if 'hash' in json and isinstance(json['hash'], str):
            tx_hash = UInt256(from_hex_str(json['hash']))
        else:
            tx_hash = UInt256.zero()

        script = base64.b64decode(json['script'])
        tx = object.__new__(cls)  # init was causing errors with inherited classes
        tx._hash = tx_hash
        tx._script = script

        tx._attributes = []
        if 'attributes' in json:
            tx._attributes = [TransactionAttribute.from_json(attr) for attr in json['attributes']]
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

        return tx

    def __repr__(self) -> str:
        return str(self._hash)


class TransactionExecution:
    def __init__(self):
        super().__init__()
        self._trigger = TriggerType.All
        self._vm_state = VMState.NONE
        self._gas_consumed: int = 0
        self._exception: str = None
        self._stack = []
        self._notifications: list[Notification] = []

    @property
    def trigger(self) -> TriggerType:
        return self._trigger

    @property
    def vm_state(self) -> VMState:
        return self._vm_state

    @property
    def exception(self) -> str | None:
        return self._exception

    @property
    def gas_consumed(self) -> int:
        return self._gas_consumed

    @property
    def result_stack(self) -> list:
        return self._stack.copy()

    @property
    def notifications(self) -> list[Notification]:
        return self._notifications.copy()

    @classmethod
    def from_json(cls, json: dict[str, Any], contract_collection: ContractCollection = None) -> Self:
        tx_exec = cls()

        tx_exec._trigger = TriggerType[json['trigger']]
        tx_exec._vm_state = VMState[json['vmstate']]
        tx_exec._gas_consumed = int(json['gasconsumed'])
        tx_exec._exception = str(json['exception']) if json['exception'] is not None else None
        tx_exec._stack = [utils.stack_item_from_json(value) for value in json['stack']]
        tx_exec._notifications = [Notification.from_json(notification, contract_collection) for notification in json['notifications']]

        return tx_exec
