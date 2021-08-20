from typing import Any

from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160


class ContractManagement:
    @classmethod
    def get_minimum_deployment_fee(cls) -> int:
        pass

    @classmethod
    def get_contract(cls, script_hash: UInt160) -> Contract:
        pass

    @classmethod
    def deploy(cls, nef_file: bytes, manifest: bytes, data: Any = None) -> Contract:
        pass

    @classmethod
    def update(cls, nef_file: bytes, manifest: bytes, data: Any = None):
        pass

    @classmethod
    def destroy(cls):
        pass
