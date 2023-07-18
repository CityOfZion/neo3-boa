from __future__ import annotations

from typing import Dict, Any


class TransactionAttributeType:

    ORACLE_RESPONSE = 'OracleResponse'
    NOT_VALID_BEFORE = 'NotValidBefore'
    HIGH_PRIORITY_ATTRIBUTE = 'HighPriorityAttribute'


class TransactionAttribute:
    def __init__(self, type_: str):
        self._type = type_

    def to_json(self) -> Dict[str, Any]:
        return {
            'type': self._type,
        }

    @staticmethod
    def from_json(json: Dict[str, Any]) -> TransactionAttribute:
        if json['type'] == TransactionAttributeType.ORACLE_RESPONSE:
            from boa3_test.test_drive.model.network.payloads.oracleresponse import OracleResponse
            tx_attr = OracleResponse.from_json(json)
        else:
            tx_attr = TransactionAttribute(json['type'])

        return tx_attr
