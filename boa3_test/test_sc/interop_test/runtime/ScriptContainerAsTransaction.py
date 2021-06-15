from typing import cast

from boa3.builtin import public
from boa3.builtin.interop.blockchain import Transaction
from boa3.builtin.interop.runtime import script_container


@public
def main() -> Transaction:
    return cast(Transaction, script_container)
