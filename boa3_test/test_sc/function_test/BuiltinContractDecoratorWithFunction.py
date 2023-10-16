from typing import Any

from boa3.builtin.compile_time import contract


@contract('0x1234567890123456789012345678901234567890')
def main() -> Any:
    return 'unit test'
