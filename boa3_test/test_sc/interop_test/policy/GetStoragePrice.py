from boa3.builtin.compile_time import public
from boa3.builtin.interop.policy import get_storage_price


@public
def main() -> int:
    return get_storage_price()
