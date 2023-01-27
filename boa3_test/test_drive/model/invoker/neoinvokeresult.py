from boa3_test.test_drive.model.invoker.neoinvoke import NeoInvoke


class NeoInvokeResult:
    def __init__(self, invoke: NeoInvoke):
        self._invoke: NeoInvoke = invoke
        self._result = NOT_EXECUTED

    @property
    def invoke(self) -> NeoInvoke:
        return self._invoke

    @property
    def result(self):
        if hasattr(self._result, 'copy'):
            return self._result.copy()
        return self._result

    def __repr__(self):
        return f'{self._invoke.__repr__()} -> {self._result.__repr__()}'


class _NotExecuted:
    def __repr__(self) -> str:
        return 'Invoke not executed yet'


class _Canceled:
    def __repr__(self) -> str:
        return 'Invoke was canceled before being executed'


NOT_EXECUTED = _NotExecuted()
CANCELED = _Canceled()
