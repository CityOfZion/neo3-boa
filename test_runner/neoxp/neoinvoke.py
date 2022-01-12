from typing import Any, Dict, Tuple, Union

from boa3.neo3.core.types import UInt160
from test_runner import utils


class NeoInvoke:
    def __init__(self, contract_id: Union[str, UInt160], operation: str, *args: Any):
        self._contract_id = str(contract_id)
        self._operation = operation
        self._args = tuple(utils.value_to_parameter(x) for x in args)
        self._invoker = 'genesis'  # TODO: allow to change to any account

    @property
    def contract(self) -> str:
        return self._contract_id

    @property
    def operation(self) -> str:
        return self._operation

    @property
    def args(self) -> Tuple[str]:
        import json
        return tuple((json.dumps(arg, separators=(',', ':')) for arg in self._args))

    @property
    def invoker(self) -> str:
        return self._invoker

    def to_json(self) -> Dict[str, Any]:
        return {
            'contract': self._contract_id,
            'operation': self._operation,
            'args': list(self._args)
        }
