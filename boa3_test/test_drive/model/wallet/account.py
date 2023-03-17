from __future__ import annotations

import abc
from typing import Any, Dict, Optional

from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.wallet import utils


class Account(abc.ABC):
    def __init__(self, script_hash: UInt160,
                 account_version: int,
                 name: str = None,
                 label: str = None):

        if script_hash is not None:
            if isinstance(script_hash, bytes):
                script_hash = UInt160(script_hash)
            elif not isinstance(script_hash, UInt160):
                raise TypeError(f"Invalid data type {type(script_hash)}. Expecting UInt160 or bytes")
        self._script_hash: UInt160 = script_hash
        self._version: int = account_version

        if name is not None and not isinstance(name, str):
            raise TypeError(f"Invalid data type {type(name)}. Expecting str or None")
        self._name: Optional[str] = name

        if label is not None and not isinstance(label, str):
            raise TypeError(f"Invalid data type {type(label)}. Expecting str or None")
        self._label: Optional[str] = label

    @property
    def script_hash(self) -> UInt160:
        return self._script_hash

    @property
    def address(self) -> Optional[str]:
        return utils.address_from_script_hash(self._script_hash.to_array(), self._version)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def label(self) -> Optional[str]:
        return self._label

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json: Dict[str, Any]) -> Account:
        pass

    def get_identifier(self) -> str:
        if isinstance(self._name, str):
            return self._name
        return self.address

    def __str__(self) -> str:
        prefix = f'{self._name}: ' if self._name is not None else ''
        return f'{prefix}{self.address}'

    def __repr__(self) -> str:
        return self.__str__()
