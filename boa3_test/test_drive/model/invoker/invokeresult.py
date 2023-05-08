class _NotExecuted:
    def __repr__(self) -> str:
        return 'Invoke not executed yet'


class _TransactionExecuted:
    def __repr__(self) -> str:
        return 'Invoke was accepted and persisted. Use the transaction id to get the result'


class _Canceled:
    def __repr__(self) -> str:
        return 'Invoke was canceled before being executed'


NOT_EXECUTED = _NotExecuted()
CANCELED = _Canceled()
TRANSACTION_EXECUTED = _TransactionExecuted()
