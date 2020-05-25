from abc import ABC
from typing import Optional


class CompilerWarning(ABC):
    def __init__(self, line: int, col: int):
        self.line: int = line
        self.col: int = col

    @property
    def message(self) -> str:
        message = '' if self._warning_message is None else ' - ' + self._warning_message
        return '{0}:{1}{2}'.format(self.line, self.col, message)

    @property
    def _warning_message(self) -> Optional[str]:
        return None
