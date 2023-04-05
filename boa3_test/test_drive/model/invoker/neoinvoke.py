from typing import Any, Dict, Tuple, Union

from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.testrunner import utils


class NeoInvoke:
    def __init__(self, contract_id: Union[str, UInt160], operation: str, *args: Any, invoker: Account = None):
        self._contract_id = str(contract_id)
        self._contract: TestContract = None  # set if available
        self._operation = operation
        self._args = tuple(utils.value_to_parameter(x) for x in args)
        self._invoker: Account = invoker

    @property
    def contract(self):
        return self._contract if self._contract is not None else self._contract_id

    @property
    def contract_id(self) -> str:
        return self._contract_id

    @property
    def operation(self) -> str:
        return self._operation

    @property
    def args(self) -> Tuple[str]:
        import json
        return tuple((json.dumps(arg, separators=(',', ':')) for arg in self._args))

    @property
    def cli_args(self) -> Tuple[str]:
        import json
        return tuple((str(arg) if (isinstance(arg, str) and len(arg.split(' ')) == 1)
                      else json.dumps(arg, separators=(',', ':'))
                      for arg in self._args))

    @property
    def invoker(self) -> Account:
        return self._invoker

    def to_json(self) -> Dict[str, Any]:
        return {
            'contract': self._contract_id,
            'operation': self._operation,
            'args': list(self._args)
        }

    def __repr__(self):
        return f'{self._contract_id}.{self._operation}{self._args}'
