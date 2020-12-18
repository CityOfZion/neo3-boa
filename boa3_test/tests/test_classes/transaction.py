from typing import Any, Dict, List

from boa3.neo.core.types.UInt import UInt160
from boa3_test.tests.test_classes.signer import Signer
from boa3_test.tests.test_classes.witness import Witness


class Transaction:
    def __init__(self, script: UInt160, signers: List[Signer] = None, witnesses: List[Witness] = None):
        self._signers: List[Signer] = signers if signers is not None else []
        self._witnesses: List[Witness] = witnesses if witnesses is not None else []
        self._script: UInt160 = script

    def to_json(self) -> Dict[str, Any]:
        return {
            'signers': [signer.to_json() for signer in self._signers],
            'witnesses': [witness.to_json() for witness in self._witnesses],
            'script': str(self._script)
        }
