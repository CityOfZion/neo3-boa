from boa3.sc.compiletime import public
from boa3.sc.runtime import script_container
from boa3.sc.types import Transaction


@public
def main() -> Transaction:
    return script_container
