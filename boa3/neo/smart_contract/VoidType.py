__all__ = ['VoidType']


class _Void:
    def __repr__(self) -> str:
        return 'Void'


VoidType = _Void()
