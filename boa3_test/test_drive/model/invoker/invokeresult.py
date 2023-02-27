class _NotExecuted:
    def __repr__(self) -> str:
        return 'Invoke not executed yet'


class _Canceled:
    def __repr__(self) -> str:
        return 'Invoke was canceled before being executed'


NOT_EXECUTED = _NotExecuted()
CANCELED = _Canceled()
