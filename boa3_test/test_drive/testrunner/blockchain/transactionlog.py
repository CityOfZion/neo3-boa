from __future__ import annotations

from typing import List, Dict, Any

from boa3_test.test_drive.model.interface.itransactionobject import ITransactionObject
from boa3_test.test_drive.model.network.payloads.testtransaction import TransactionExecution
from boa3_test.test_drive.model.smart_contract.contractcollection import ContractCollection


class TestRunnerTransactionLog(ITransactionObject):
    def __init__(self):
        super().__init__()
        self._executions: List[TransactionExecution] = []

    @property
    def executions(self) -> List[TransactionExecution]:
        return self._executions.copy()

    @classmethod
    def from_json(cls, json: Dict[str, Any], contract_collection: ContractCollection = None) -> TestRunnerTransactionLog:
        tx_log = cls()

        tx_log._executions = [TransactionExecution.from_json(execution, contract_collection) for execution in json['executions']]

        return tx_log
