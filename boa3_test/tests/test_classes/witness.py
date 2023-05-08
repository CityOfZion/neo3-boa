from __future__ import annotations

from boa3_test.test_drive.model.network.payloads.witness import Witness as TestWitness

__all__ = ['Witness']


class Witness(TestWitness):
    def __init__(self, invocation_script: bytes, verification_script: bytes):
        super().__init__(invocation_script, verification_script)
