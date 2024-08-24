from typing import Any

from boa3.sc.compiletime import contract


@contract('0x1234567890123456789012345678901234567890')
def main() -> Any:
    return 'unit test'
