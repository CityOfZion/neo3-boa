from boa3.builtin import public
from boa3.builtin.interop.blockchain import current_height


@public
def Main() -> int:
    return current_height
