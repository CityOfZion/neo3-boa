from typing import Any, Self

from boa3_test.test_drive.model.network.payloads.transactionattribute import TransactionAttribute, \
    TransactionAttributeType


class OracleResponse(TransactionAttribute):
    def __init__(self, id_: int, code: str, result: str):
        super().__init__(TransactionAttributeType.ORACLE_RESPONSE)
        self._id = id_
        self._code = code
        self._result = result

    def to_json(self) -> dict[str, Any]:
        import base64
        import json
        json_response = super().to_json()

        json_response['id'] = self._id
        json_response['code'] = self._code
        json_response['result'] = json.loads(base64.b64decode(self._result))

        return json_response

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        oracle_response: OracleResponse = OracleResponse(json['id'], json['code'], json['result'])

        return oracle_response
