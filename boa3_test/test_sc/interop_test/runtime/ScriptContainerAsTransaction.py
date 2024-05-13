from boa3.sc.compiletime import public
from boa3.sc.types import Transaction
from boa3.sc.runtime import script_container


@public
def main() -> Transaction:
    return script_container
