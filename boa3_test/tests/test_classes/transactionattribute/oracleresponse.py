import base64
import enum
from typing import Any, Self

from boa3.internal.neo.vm.type.String import String
from boa3_test.tests.test_classes.transactionattribute import TransactionAttribute, TransactionAttributeType


class OracleResponseCode(enum.IntEnum):
    # Indicates that the request has been successfully completed.
    Success = 0x00

    # Indicates that the protocol of the request is not supported.
    ProtocolNotSupported = 0x10

    # Indicates that the oracle nodes cannot reach a consensus on the result of the request.
    ConsensusUnreachable = 0x12

    # Indicates that the requested Uri does not exist.
    NotFound = 0x14

    # Indicates that the request was not completed within the specified time.
    Timeout = 0x16

    # Indicates that there is no permission to request the resource.
    Forbidden = 0x18

    # Indicates that the data for the response is too large.
    ResponseTooLarge = 0x1a

    # Indicates that the request failed due to insufficient balance.
    InsufficientFunds = 0x1c

    # Indicates that the request failed due to other errors.
    Error = 0xff


class OracleResponse(TransactionAttribute):
    def __init__(self, request_id: int, code: OracleResponseCode, result: bytes):
        super().__init__(TransactionAttributeType.OracleResponse)
        self._id: int = request_id
        self._response_code: OracleResponseCode = code
        self._result: bytes = result

    def to_json(self) -> dict[str, Any]:
        json = super().to_json()
        json.update({
            'id': self._id,
            'code': self._response_code.value,
            'result': String.from_bytes(base64.b64encode(self._result))
        })
        return json

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        return cls(request_id=json['id'],
                   code=json['code'],
                   result=base64.b64decode(json['result']))

    def __eq__(self, other) -> bool:
        return (isinstance(other, OracleResponse)
                and self._id == other._id
                and self._response_code == other._response_code
                and self._result == other._result)
