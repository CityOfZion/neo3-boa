from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes


@public
def example(value: str | int) -> bytes:
    if isinstance(value, str):
        return to_bytes(value)
    else:
        return to_bytes(value)
